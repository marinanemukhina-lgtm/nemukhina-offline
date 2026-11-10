import http.client
import json
from pathlib import Path
import socket
import tempfile
import threading
import unittest
from unittest.mock import patch

import library
import offline
from server import LocalServer


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "db.sqlite3"
        self.db = offline.connect(self.path)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_backup_merge_roundtrip_and_tamper(self):
        library.add_documents(self.db, [{"name": "中文.md", "text": "分数\r\n1/2"}])
        backup = library.snapshot(self.db)
        self.assertEqual(library.restore(self.db, backup), 0)
        library.add_documents(self.db, [{"name": "другой.txt", "text": "Другой"}])
        self.assertEqual(library.restore(self.db, backup), 0)
        self.assertEqual(len(library.snapshot(self.db)["documents"]), 2)
        backup["documents"][0]["text"] = "tampered"
        with self.assertRaisesRegex(ValueError, "checksum"):
            library.restore(self.db, backup)
        self.assertEqual(len(library.snapshot(self.db)["documents"]), 2)

    def test_restore_rejects_missing_hash_and_version(self):
        for backup in [
            {"format": library.FORMAT, "version": True, "documents": []},
            {
                "format": library.FORMAT,
                "version": 1,
                "documents": [{"name": "a.txt", "text": "x"}],
            },
        ]:
            with self.assertRaises(ValueError):
                library.restore(self.db, backup)

    def test_document_validation_atomic(self):
        for item in [
            {"name": "../x.md", "text": "x"},
            {"name": "a.txt", "text": "\ud800"},
            {"name": "a.txt", "text": "\x00"},
            {"name": "a.txt", "text": "x" * (offline.MAX_FILE + 1)},
        ]:
            with self.assertRaises(ValueError):
                library.add_documents(
                    self.db, [{"name": "good.txt", "text": "safe"}, item]
                )
            self.assertEqual(library.snapshot(self.db)["documents"], [])

    def test_concurrent_imports_preserve_both(self):
        errors = []

        def write(n):
            db = offline.connect(self.path)
            try:
                library.add_documents(db, [{"name": str(n) + ".txt", "text": str(n)}])
            except Exception as e:
                errors.append(e)
            finally:
                db.close()

        threads = [threading.Thread(target=write, args=(n,)) for n in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        self.assertEqual(len(library.snapshot(self.db)["documents"]), 8)


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.server = LocalServer(("127.0.0.1", 0), Path(cls.tmp.name) / "test.db")
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()
        cls.tmp.cleanup()

    def request(self, path, data=None, headers=None, method="POST", raw=None):
        conn = http.client.HTTPConnection(
            "127.0.0.1", self.server.server_port, timeout=5
        )
        h = {"Content-Type": "application/json", "X-Local-Token": self.server.token}
        h.update(headers or {})
        conn.request(
            method,
            path,
            body=raw if raw is not None else json.dumps(data or {}),
            headers=h,
        )
        r = conn.getresponse()
        body = r.read()
        status = r.status
        response_headers = dict(r.getheaders())
        conn.close()
        return status, body, response_headers

    def test_local_assets_and_no_path_traversal(self):
        status, body, headers = self.request("/", method="GET")
        self.assertEqual(status, 200)
        self.assertIn(self.server.token.encode(), body)
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        for path in (
            "/../offline.py",
            "/data/library.sqlite3",
            "/.git/config",
            "/api/backup",
        ):
            self.assertEqual(self.request(path, method="GET")[0], 404)

    def test_cross_origin_and_token_required(self):
        for headers in (
            {"Origin": "https://evil.example"},
            {"Host": "evil.example"},
            {"X-Local-Token": "wrong"},
            {"X-Local-Token": ""},
        ):
            self.assertEqual(self.request("/api/backup", headers=headers)[0], 403)

    def test_input_shapes_and_size(self):
        for raw in ("[]", "null", '{"x":NaN}', "{"):
            code = self.request("/api/import", raw=raw)[0]
            self.assertEqual(code, 400)
        self.assertEqual(
            self.request("/api/state", headers={"Content-Type": "text/plain"})[0], 415
        )
        self.assertEqual(
            self.request(
                "/api/import", headers={"Content-Length": str(9 * 1024 * 1024)}
            )[0],
            413,
        )

    def test_end_to_end_import_search_backup_delete_restore(self):
        self.assertEqual(
            self.request(
                "/api/import",
                {
                    "documents": [
                        {
                            "name": "workflow.md",
                            "text": "Точный источник: <script>alert(1)</script>",
                        }
                    ]
                },
            )[0],
            200,
        )
        result = json.loads(self.request("/api/search", {"query": "Точный"})[1])
        self.assertEqual(result["sources"][0]["line"], 1)
        ident = result["sources"][0]["id"]
        backup = json.loads(self.request("/api/backup")[1])
        self.assertEqual(self.request("/api/delete", {"id": ident})[0], 200)
        self.assertEqual(
            json.loads(self.request("/api/search", {"query": "Точный"})[1])["sources"],
            [],
        )
        self.assertEqual(self.request("/api/restore", {"backup": backup})[0], 200)
        self.assertEqual(
            json.loads(self.request("/api/document", {"id": ident})[1])["document"][
                "name"
            ],
            "workflow.md",
        )

    def test_no_model_and_no_evidence(self):
        self.request("/api/demo")
        self.assertEqual(
            json.loads(self.request("/api/ask", {"query": "unfindablexyz"})[1])[
                "answer"
            ],
            None,
        )
        self.assertEqual(
            json.loads(self.request("/api/ask", {"query": "fraction"})[1])["error"],
            "no_model",
        )

    def test_model_api_reports_missing_citations(self):
        self.request("/api/demo")
        self.server.engine, self.server.model = "synthetic-engine", "synthetic-model"
        try:
            with patch.object(offline, "generate", return_value="1/2 equals 0.5."):
                result = json.loads(
                    self.request(
                        "/api/ask",
                        {"query": "fraction", "lang": "en", "mode": "school"},
                    )[1]
                )
                self.assertEqual(result["warning"], "missing_citations")
                self.assertEqual(len(result["sources"]), 1)
            self.server.inference.acquire()
            try:
                self.assertEqual(
                    json.loads(self.request("/api/ask", {"query": "fraction"})[1])[
                        "error"
                    ],
                    "busy",
                )
            finally:
                self.server.inference.release()
        finally:
            self.server.engine, self.server.model = None, None

    def test_no_outbound_connections(self):
        # Local HTTP transport is allowed; any attempted remote connect fails the test.
        original = socket.socket.connect

        def guarded(sock, address):
            if not isinstance(address, tuple) or address[0] != "127.0.0.1":
                raise AssertionError("Outbound network attempted")
            return original(sock, address)

        with patch.object(socket.socket, "connect", guarded):
            self.assertEqual(self.request("/api/demo")[0], 200)
            self.assertEqual(self.request("/api/search", {"query": "1/2"})[0], 200)

    def test_bind_rejects_public_interface(self):
        with self.assertRaises(ValueError):
            LocalServer(("0.0.0.0", 0), ":memory:")


if __name__ == "__main__":
    unittest.main()
