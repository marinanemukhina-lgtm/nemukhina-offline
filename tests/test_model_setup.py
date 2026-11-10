import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import model_setup
import offline
import server as server_module
import test_server


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def file(self, path, data=b"GGUF synthetic"):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        p.chmod(0o700)
        return p

    def test_discovery_only_application_folders(self):
        engine = self.file("runtime/release/llama-completion.exe")
        model = self.file("models/model.gguf")
        self.file("Downloads/private.gguf")
        self.file("models/deeper/than/allowed/hidden.gguf")
        self.file("runtime/not-a-program.txt")
        result = model_setup.discover(self.root)
        self.assertEqual([x["path"] for x in result["engines"]], [str(engine)])
        self.assertEqual([x["path"] for x in result["models"]], [str(model)])

    def test_discovery_does_not_follow_symlinks(self):
        outside = self.root / "private"
        outside.mkdir()
        self.file("private/private.gguf")
        (self.root / "models").mkdir()
        try:
            (self.root / "models/link").symlink_to(outside, target_is_directory=True)
            (self.root / "models/leak.gguf").symlink_to(outside / "private.gguf")
        except OSError:
            self.skipTest("Creating symlinks is unavailable")
        self.assertEqual(model_setup.discover(self.root)["models"], [])

    def test_discovery_has_result_limit_and_validates_before_use(self):
        for n in range(40):
            self.file("models/%02d.gguf" % n)
        self.assertEqual(len(model_setup.discover(self.root)["models"]), 32)
        engine = self.file("runtime/llama-completion")
        invalid = self.file("models/invalid.gguf", b"HTML")
        with self.assertRaisesRegex(ValueError, "model_path"):
            model_setup.validate(str(engine), str(invalid))
        with self.assertRaisesRegex(ValueError, "engine_path"):
            model_setup.validate(str(invalid), str(invalid))


class ModelCheckTests(unittest.TestCase):
    setUpClass = classmethod(test_server.ServerTests.setUpClass.__func__)
    tearDownClass = classmethod(test_server.ServerTests.tearDownClass.__func__)
    request = test_server.ServerTests.request

    def setUp(self):
        self.files = tempfile.TemporaryDirectory()
        self.addCleanup(self.files.cleanup)
        self.root = Path(self.files.name)
        self.engine = self.root / ("llama-completion.exe" if os.name == "nt" else "llama-completion")
        self.engine.write_bytes(b"synthetic, not executable machine code")
        self.engine.chmod(0o700)
        self.model = self.root / "synthetic.gguf"
        self.model.write_bytes(b"GGUF synthetic model header")
        self.server.engine, self.server.model = str(self.engine), str(self.model)
        self.server.model_check = None

    def tearDown(self):
        self.server.engine = self.server.model = self.server.model_check = None

    def check(self, request_id="c" * 32):
        status, raw, _ = self.request("/api/model/check", {"request_id": request_id})
        return status, json.loads(raw)

    def test_success_is_not_a_conversation_and_expires_after_file_change(self):
        before = json.loads(self.request("/api/state")[1])["conversations"]
        with patch.object(offline, "generate", return_value="4") as generate:
            status, result = self.check()
        self.assertEqual(status, 200)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(generate.call_args.kwargs["max_tokens"], 64)
        self.assertEqual(generate.call_args.kwargs["timeout"], 60)
        state = json.loads(self.request("/api/state")[1])
        self.assertEqual(state["conversations"], before)
        self.assertEqual(state["model_check"]["answer"], "4")
        self.model.write_bytes(b"GGUF changed model content, different size")
        self.assertIsNone(json.loads(self.request("/api/state")[1])["model_check"])

    def test_unexpected_answer_is_explicit_not_a_pass(self):
        with patch.object(offline, "generate", return_value="5"):
            status, result = self.check()
        self.assertEqual(status, 200)
        self.assertEqual(result["status"], "unexpected")
        self.assertEqual(result["answer"], "5")

    def test_failure_and_timeout_release_engine_without_success(self):
        for error, code in ((ValueError("failed"), "engine"),
                            (offline.subprocess.TimeoutExpired("synthetic", 60), "engine_timeout")):
            with self.subTest(error=code):
                with patch.object(offline, "generate", side_effect=error):
                    _, result = self.check()
                self.assertEqual(result["error"], code)
                self.assertIsNone(self.server.model_check)
                self.assertTrue(self.server.inference.acquire(blocking=False))
                self.server.inference.release()

    def test_probe_detects_model_replaced_during_generation(self):
        def replace_model(*args, **kwargs):
            self.model.write_bytes(b"GGUF replaced")
            return "4"
        with patch.object(offline, "generate", side_effect=replace_model):
            _, result = self.check()
        self.assertEqual(result["error"], "model_changed")
        self.assertIsNone(self.server.model_check)

    def test_cancellation_is_scoped_and_configuration_cannot_change_mid_check(self):
        started, response = threading.Event(), []
        def generate(*args, cancel_event=None, **kwargs):
            started.set()
            self.assertTrue(cancel_event.wait(3))
            raise ValueError("cancelled")
        with patch.object(offline, "generate", side_effect=generate):
            worker = threading.Thread(target=lambda: response.append(self.check()))
            worker.start()
            try:
                self.assertTrue(started.wait(2))
                self.assertEqual(self.check("d" * 32)[1]["error"], "busy")
                blocked = json.loads(self.request("/api/model", {
                    "engine": str(self.engine), "model": str(self.model)})[1])
                self.assertEqual(blocked["error"], "busy")
                self.request("/api/chat/cancel", {"request_id": "d" * 32})
                self.assertFalse(self.server.cancel_event.is_set())
                self.request("/api/chat/cancel", {"request_id": "c" * 32})
                worker.join(4)
                self.assertFalse(worker.is_alive())
            finally:
                self.server.cancel_event.set()
                worker.join(4)
        self.assertEqual(response[0][1]["error"], "cancelled")
        self.assertIsNone(self.server.model_check)

    def test_new_endpoints_require_session_and_well_formed_id(self):
        for path in ("/api/model/options", "/api/model/check"):
            self.assertEqual(self.request(path, headers={"X-Local-Token": ""})[0], 403)
        with patch.object(offline, "generate") as generate:
            self.assertEqual(self.check("invalid")[1]["error"], "invalid_request")
            generate.assert_not_called()

    def test_options_preserve_explicit_configuration_without_scanning_it(self):
        with patch.object(server_module, "ROOT", self.root):
            result = json.loads(self.request("/api/model/options")[1])
        self.assertEqual(result["engines"], [])
        self.assertEqual(result["models"], [])
        self.assertEqual(result["configuration"]["model"], str(self.model))

    def test_reconnecting_clears_previous_check(self):
        with patch.object(offline, "generate", return_value="4"):
            self.check()
        self.assertIsNotNone(self.server.model_check)
        status, _, _ = self.request("/api/model", {
            "engine": str(self.engine), "model": str(self.model)})
        self.assertEqual(status, 200)
        self.assertIsNone(self.server.model_check)
