"""Loopback-only UI server. Every API call requires a per-process capability token."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import sqlite3
import threading
from urllib.parse import urlsplit

import library
import offline

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
            db.execute("SELECT 1")
        db.close()
        self.token = secrets.token_urlsafe(32)
        self.engine, self.model = engine, model
        self.inference = threading.Lock()
        super().__init__(address, Handler)
        self.origin = "http://127.0.0.1:" + str(self.server_port)


class Handler(BaseHTTPRequestHandler):
    server_version = "NemukhinaOffline/0.2"

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
        except (OSError, offline.subprocess.TimeoutExpired):
            self.send(503, {"error": "engine"})

    def dispatch(self, db, data):
        path = urlsplit(self.path).path
        if path == "/api/state":
            rows = db.execute(
                "SELECT id,name,size FROM documents ORDER BY name,id"
            ).fetchall()
            return {
                "documents": [dict(zip(("id", "name", "size"), row)) for row in rows],
                "model": bool(self.server.engine and self.server.model),
                "version": "0.2.0",
            }
        if path == "/api/demo":
            return {
                "added": offline.import_files(
                    db, sorted((ROOT / "examples").glob("*.md"))
                )
            }
        if path == "/api/import":
            return {"added": library.add_documents(db, data.get("documents"))}
        if path == "/api/backup":
            return library.snapshot(db)
        if path == "/api/restore":
            return {"added": library.restore(db, data.get("backup"))}
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


ERROR_CODES = {
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
