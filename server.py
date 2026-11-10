"""Loopback-only UI server. Every API call requires a per-process capability token."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import sqlite3
import threading
import os
import mimetypes
import re
import time
from urllib.parse import urlsplit

import library
import offline
import conversations
import model_setup

ROOT = Path(__file__).resolve().parent
MAX_REQUEST = 8 * 1024 * 1024
MAX_BACKUP = 320 * 1024 * 1024


class LocalServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, db_path, engine=None, model=None):
        if address[0] != "127.0.0.1":
            raise ValueError("Only 127.0.0.1 is supported")
        self.db_path = Path(db_path)
        with offline.connect(self.db_path) as db:
            conversations.initialize(db)
            saved = dict(db.execute("SELECT key,value FROM settings"))
        db.close()
        self.token = secrets.token_urlsafe(32)
        self.engine, self.model = engine or saved.get("engine"), model or saved.get(
            "model"
        )
        self.inference = threading.Lock()
        self.active_request = None
        self.cancel_event = threading.Event()
        self.model_check = None
        super().__init__(address, Handler)
        self.origin = "http://127.0.0.1:" + str(self.server_port)


class Handler(BaseHTTPRequestHandler):
    server_version = "NemukhinaOffline/0.3.1"

    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def log_message(self, *args):
        pass  # No request, question, source or token logs.

    def send(self, status, body, content_type="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
        )
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def allowed(self, api=False):
        expected = (
            self.server.origin.removeprefix("http://")
            if hasattr(str, "removeprefix")
            else self.server.origin[7:]
        )
        if self.headers.get("Host") != expected:
            self.send(403, {"error": "host"})
            return False
        origin = self.headers.get("Origin")
        if origin is not None and origin != self.server.origin:
            self.send(403, {"error": "origin"})
            return False
        if api and not secrets.compare_digest(
            self.headers.get("X-Local-Token", "").encode("utf-8"),
            self.server.token.encode("utf-8"),
        ):
            self.send(403, {"error": "session"})
            return False
        return True

    def do_GET(self):
        if not self.allowed():
            return
        files = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
            "/style.css": ("style.css", "text/css; charset=utf-8"),
        }
        path = urlsplit(self.path).path
        if path.startswith("/assets/"):
            asset = (ROOT / "web" / path.lstrip("/")).resolve()
            if (
                (ROOT / "web" / "assets").resolve() in asset.parents
                and asset.is_file()
                and asset.suffix in (".svg", ".png", ".ttf")
            ):
                self.send(
                    200,
                    asset.read_bytes(),
                    mimetypes.guess_type(str(asset))[0] or "application/octet-stream",
                )
            else:
                self.send(404, {"error": "not_found"})
            return
        if path not in files:
            self.send(404, {"error": "not_found"})
            return
        filename, mime = files[path]
        data = (ROOT / "web" / filename).read_bytes()
        if path == "/":
            data = data.replace(b"__LOCAL_TOKEN__", self.server.token.encode())
        self.send(200, data, mime)

    def do_POST(self):
        if not self.allowed(api=True):
            return
        try:
            if (
                self.headers.get("Transfer-Encoding")
                or self.headers.get_content_type() != "application/json"
            ):
                self.send(415, {"error": "json_required"})
                return
            size = int(self.headers.get("Content-Length", "0"))
            limit = (
                MAX_BACKUP
                if urlsplit(self.path).path == "/api/restore"
                else MAX_REQUEST
            )
            if not 0 < size <= limit:
                self.send(413, {"error": "request_size"})
                return
            data = json.loads(self.rfile.read(size).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("request_format")
            db = offline.connect(self.server.db_path)
            try:
                result = self.dispatch(db, data)
            finally:
                db.close()
            self.send(200, result)
        except (ValueError, UnicodeError, TypeError, KeyError, RecursionError) as error:
            code = str(error) if str(error) in ERROR_CODES else "invalid_request"
            self.send(400, {"error": code})
        except sqlite3.Error:
            self.send(503, {"error": "storage"})
        except offline.subprocess.TimeoutExpired:
            self.send(503, {"error": "engine_timeout"})
        except OSError:
            self.send(503, {"error": "engine"})

    def dispatch(self, db, data):
        path = urlsplit(self.path).path
        if path == "/api/state":
            rows = db.execute(
                "SELECT id,name,size FROM documents ORDER BY name,id"
            ).fetchall()
            return {
                "documents": [dict(zip(("id", "name", "size"), row)) for row in rows],
                "model": bool(
                    self.server.engine
                    and self.server.model
                    and Path(self.server.engine).is_file()
                    and Path(self.server.model).is_file()
                ),
                "model_name": (
                    Path(self.server.model).name if self.server.model else None
                ),
                "conversations": conversations.listing(db),
                "model_check": self.current_model_check(),
                "version": "0.3.1",
            }
        if path == "/api/model/options":
            return dict(model_setup.discover(ROOT), configuration={
                "engine": self.server.engine or "", "model": self.server.model or ""
            })
        if path == "/api/model":
            if not self.server.inference.acquire(blocking=False):
                raise ValueError("busy")
            try:
                engine, model = model_setup.validate(data.get("engine"), data.get("model"))
                with db:
                    db.executemany(
                        "INSERT OR REPLACE INTO settings VALUES (?,?)",
                        [("engine", str(engine)), ("model", str(model))],
                    )
                self.server.engine, self.server.model = str(engine), str(model)
                self.server.model_check = None
                return {"ok": True, "model_name": Path(model).name}
            finally:
                self.server.inference.release()
        if path == "/api/model/check":
            request_id = data.get("request_id")
            if not isinstance(request_id, str) or not re.fullmatch(r"[a-f0-9]{32}", request_id):
                raise ValueError("invalid_request")
            if not self.server.engine or not self.server.model:
                raise ValueError("no_model")
            if not self.server.inference.acquire(blocking=False):
                raise ValueError("busy")
            self.server.cancel_event.clear()
            self.server.active_request = request_id
            self.server.model_check = None
            try:
                model_setup.validate(self.server.engine, self.server.model)
                identity = model_setup.fingerprint(self.server.engine, self.server.model)
                if identity is None:
                    raise ValueError("model_changed")
                started = time.monotonic()
                try:
                    answer = offline.generate(
                        self.server.engine, self.server.model,
                        "Calculate 2 + 2. Reply with only the number, without any explanation.",
                        cancel_event=self.server.cancel_event, max_tokens=64, timeout=60,
                    )
                except ValueError as error:
                    if str(error) == "cancelled":
                        raise
                    raise ValueError("engine") from None
                if self.server.cancel_event.is_set():
                    raise ValueError("cancelled")
                if identity != model_setup.fingerprint(self.server.engine, self.server.model):
                    raise ValueError("model_changed")
                result = {
                    "status": "passed" if re.fullmatch(r"\s*4[.!。]?\s*", answer) else "unexpected",
                    "answer": answer[:2000],
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                    "model_name": Path(self.server.model).name,
                }
                self.server.model_check = (identity, result)
                return result
            finally:
                self.server.active_request = None
                self.server.inference.release()
        if path == "/api/conversation":
            ident = data.get("id")
            if not isinstance(ident, str):
                raise ValueError("invalid_request")
            return {"conversation": conversations.get(db, ident)}
        if path == "/api/conversation/update":
            if not isinstance(data.get("id"), str):
                raise ValueError("invalid_request")
            return {
                "conversation": conversations.update(
                    db,
                    data["id"],
                    data.get("revision"),
                    data.get("title"),
                    data.get("archived"),
                )
            }
        if path == "/api/chat/cancel":
            if (
                data.get("request_id") == self.server.active_request
                and self.server.active_request is not None
            ):
                self.server.cancel_event.set()
            return {"ok": True}
        if path == "/api/chat":
            question, lang, mode = (
                data.get("question"),
                data.get("lang", "ru"),
                data.get("mode", "chat"),
            )
            ident, revision, request_id = (
                data.get("id"),
                data.get("revision"),
                data.get("request_id"),
            )
            if (
                not isinstance(question, str)
                or not question.strip()
                or len(question) > 4000
                or lang not in offline.TEXT
                or mode not in ("chat", "sources")
                or not isinstance(request_id, str)
                or not re.fullmatch(r"[a-f0-9]{32}", request_id)
                or (ident is not None and not isinstance(ident, str))
            ):
                raise ValueError("invalid_request")
            if not self.server.engine or not self.server.model:
                raise ValueError("no_model")
            if not self.server.inference.acquire(blocking=False):
                raise ValueError("busy")
            self.server.cancel_event.clear()
            self.server.active_request = request_id
            try:
                current = conversations.get(db, ident) if ident else {"turns": []}
                if ident:
                    conversations.check_revision(current, revision)
                    if current["archived"]:
                        raise ValueError("conversation_archived")
                if len(current["turns"]) >= conversations.MAX_TURNS:
                    raise ValueError("turn_limit")
                sources = None
                if mode == "sources":
                    if not isinstance(data.get("query"), str):
                        raise ValueError("query")
                    sources = offline.search(db, data["query"])
                    if not sources:
                        raise ValueError("no_sources")
                prompt, omitted = conversations.prompt(
                    question.strip(), current["turns"], lang, sources
                )
                try:
                    answer = offline.generate(
                        self.server.engine,
                        self.server.model,
                        prompt,
                        cancel_event=self.server.cancel_event,
                    )
                except ValueError as error:
                    if str(error) == "cancelled":
                        raise
                    raise ValueError("engine") from None
                if self.server.cancel_event.is_set():
                    raise ValueError("cancelled")
                if len(answer) > 32000:
                    raise ValueError("answer_limit")
                turn = {
                    "question": question.strip(),
                    "answer": answer,
                    "lang": lang,
                    "mode": mode,
                    "sources": sources or [],
                    "warning": (
                        offline.citation_warning(answer, len(sources))
                        if sources
                        else None
                    ),
                    "context_omitted": omitted,
                }
                return {"conversation": conversations.append(db, ident, revision, turn)}
            finally:
                self.server.active_request = None
                self.server.inference.release()
        if path == "/api/demo":
            return {
                "added": offline.import_files(
                    db, sorted((ROOT / "examples").glob("*.md"))
                )
            }
        if path == "/api/import":
            return {"added": library.add_documents(db, data.get("documents"))}
        if path == "/api/backup":
            return conversations.snapshot(db)
        if path == "/api/restore":
            return conversations.restore(db, data.get("backup"))
        if path in ("/api/document", "/api/delete"):
            ident = data.get("id")
            if not isinstance(ident, str) or len(ident) != 64:
                raise ValueError("invalid_request")
            if path == "/api/delete":
                with db:
                    db.execute("DELETE FROM documents WHERE id=?", (ident,))
                return {"ok": True}
            row = db.execute(
                "SELECT id,name,text FROM documents WHERE id=?", (ident,)
            ).fetchone()
            return {"document": dict(zip(("id", "name", "text"), row)) if row else None}
        if path in ("/api/search", "/api/ask"):
            query = data.get("query")
            if not isinstance(query, str):
                raise ValueError("query")
            sources = offline.search(db, query)
            if path == "/api/search" or not sources:
                return {"sources": sources, "answer": None}
            if not self.server.engine or not self.server.model:
                raise ValueError("no_model")
            lang, mode = data.get("lang", "ru"), data.get("mode", "general")
            question = data.get("question") or query
            if (
                lang not in offline.TEXT
                or mode not in ("general", "school", "university")
                or not isinstance(question, str)
                or len(question) > 2000
            ):
                raise ValueError("invalid_request")
            if not self.server.inference.acquire(blocking=False):
                raise ValueError("busy")
            try:
                answer = offline.generate(
                    self.server.engine,
                    self.server.model,
                    offline.prompt_for(question, sources, lang, mode),
                )
            finally:
                self.server.inference.release()
            return {
                "sources": sources,
                "answer": answer,
                "warning": offline.citation_warning(answer, len(sources)),
            }
        raise ValueError("not_found")

    def current_model_check(self):
        saved = self.server.model_check
        if saved and saved[0] == model_setup.fingerprint(self.server.engine, self.server.model):
            return saved[1]
        return None


ERROR_CODES = {
    "conversation_missing",
    "conversation_changed",
    "conversation_archived",
    "history_limit",
    "turn_limit",
    "context_limit",
    "engine_path",
    "model_path",
    "model_changed",
    "no_sources",
    "cancelled",
    "answer_limit",
    "engine",
    "document_format",
    "file_name",
    "file_encoding",
    "file_size",
    "checksum",
    "document_count",
    "library_limit",
    "backup_format",
    "request_format",
    "query",
    "no_model",
    "invalid_request",
    "busy",
    "not_found",
}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Nemukhina Offline · local browser app"
    )
    parser.add_argument("--db", default="data/library.sqlite3")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--engine")
    parser.add_argument("--model")
    args = parser.parse_args(argv)
    if bool(args.engine) != bool(args.model):
        parser.error("--engine and --model must be provided together")
    if args.engine and (
        not Path(args.engine).is_file() or not Path(args.model).is_file()
    ):
        parser.error("Engine and model must be existing local files")
    with LocalServer(
        ("127.0.0.1", args.port), args.db, args.engine, args.model
    ) as server:
        print("Nemukhina Offline → " + server.origin, flush=True)
        print("Ctrl+C to stop. Library: " + str(server.db_path.resolve()), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
