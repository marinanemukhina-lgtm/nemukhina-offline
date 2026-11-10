import contextlib
import io
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import offline


class OfflineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db = offline.connect(self.root / "library.sqlite3")

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def source(self, name, content):
        path = self.root / name
        path.write_bytes(content)
        return path

    def test_multilingual_and_no_network(self):
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            offline.import_files(self.db, list(Path("examples").glob("*.md")))
            for query in ("ДРОБЬ", "fraction", "分数"):
                results = offline.search(self.db, query)
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["line"], 2)
                self.assertIn("1/2", results[0]["quote"])

    def test_duplicate_content(self):
        files = [self.source(n, b"same") for n in ("a.txt", "b.md")]
        self.assertEqual(offline.import_files(self.db, files), 1)

    def test_invalid_batch_keeps_data(self):
        a = self.source("a.txt", b"good")
        b = self.source("b.txt", b"\xff")
        with self.assertRaises(ValueError):
            offline.import_files(self.db, [a, b])
        self.assertEqual(
            self.db.execute("SELECT count(*) FROM documents").fetchone()[0], 0
        )

    def test_limit_rolls_back(self):
        with patch.object(offline, "MAX_TOTAL", 2):
            with self.assertRaises(ValueError):
                offline.import_files(self.db, [self.source("a.md", b"123")])
        self.assertEqual(
            self.db.execute("SELECT count(*) FROM documents").fetchone()[0], 0
        )

    def test_long_line_and_hash(self):
        text = "x" * 2000 + " needle"
        offline.import_files(self.db, [self.source("a.txt", text.encode())])
        result = offline.search(self.db, "needle")[0]
        self.assertEqual(result["quote"], text)
        self.assertEqual(
            result["id"], offline.hashlib.sha256(text.encode()).hexdigest()
        )

    def test_no_match_does_not_generate(self):
        with patch.object(
            offline, "generate", side_effect=AssertionError("must not run")
        ):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    offline.main(
                        [
                            "--db",
                            str(self.root / "empty.db"),
                            "ask",
                            "missing",
                            "--engine",
                            "/absent",
                            "--model",
                            "/absent.gguf",
                        ]
                    ),
                    0,
                )

    def test_prompt_modes_and_languages(self):
        for lang in offline.TEXT:
            for mode in ("school", "university", "general"):
                prompt = offline.prompt_for("why", [], lang, mode)
                self.assertIn(offline.TEXT[lang]["language"], prompt)
                self.assertIn("untrusted data", prompt)

    def test_citation_syntax_is_not_entailment(self):
        self.assertEqual(
            offline.citation_warning("No reference", 2), "missing_citations"
        )
        self.assertEqual(offline.citation_warning("Claim [3]", 2), "invalid_citations")
        self.assertEqual(offline.citation_warning("Claim [0]", 2), "invalid_citations")
        self.assertIsNone(offline.citation_warning("Unverified claim [1]", 2))

    def test_missing_model(self):
        with self.assertRaises(ValueError):
            offline.generate("/absent", "/absent.gguf", "hello")

    @unittest.skipIf(
        os.name == "nt", "POSIX fixture; model adapter is covered separately"
    )
    def test_engine_contract_not_real_inference(self):
        engine = self.source("engine", b'#!/bin/sh\nprintf "synthetic engine output"\n')
        engine.chmod(0o700)
        model = self.source("test.gguf", b"not a model")
        self.assertEqual(
            offline.generate(engine, model, "hello"), "synthetic engine output"
        )

    def test_query_limits_and_terminal(self):
        for query in ("", "a " * 25, "x" * 1001):
            with self.assertRaises(ValueError):
                offline.search(self.db, query)
        self.assertNotIn("\x1b", offline.terminal_safe("\x1b[31mhello"))

    def test_file_limits(self):
        for name, data in [
            ("a.pdf", b"x"),
            ("a.txt", b"\x00"),
            ("b.txt", b"x" * (offline.MAX_FILE + 1)),
        ]:
            with self.assertRaises(ValueError):
                offline.import_files(self.db, [self.source(name, data)])


if __name__ == "__main__":
    unittest.main()
