import copy
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import conversations
import library
import offline
import test_server


def turn(question="hello", answer="answer"):
    return {
        "question": question,
        "answer": answer,
        "lang": "en",
        "mode": "chat",
        "sources": [],
        "warning": None,
        "context_omitted": 0,
    }


class ConversationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "db.sqlite3"
        self.db = offline.connect(self.path)
        conversations.initialize(self.db)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_persistence_revision_and_recoverable_archive(self):
        chat = conversations.append(self.db, None, None, turn("first"))
        self.db.close()
        self.db = offline.connect(self.path)
        self.assertEqual(
            conversations.get(self.db, chat["id"])["turns"][0]["question"], "first"
        )
        chat = conversations.append(
            self.db, chat["id"], chat["revision"], turn("follow-up")
        )
        with self.assertRaisesRegex(ValueError, "conversation_changed"):
            conversations.append(self.db, chat["id"], 1, turn("stale"))
        chat = conversations.update(
            self.db, chat["id"], chat["revision"], archived=True
        )
        with self.assertRaisesRegex(ValueError, "conversation_archived"):
            conversations.append(self.db, chat["id"], chat["revision"], turn())
        chat = conversations.update(
            self.db, chat["id"], chat["revision"], archived=False
        )
        self.assertEqual(len(chat["turns"]), 2)

    def test_backup_versions_merge_and_atomic_validation(self):
        library.add_documents(self.db, [{"name": "a.md", "text": "safe"}])
        legacy = library.snapshot(self.db)
        original = conversations.append(self.db, None, None, turn())
        backup = conversations.snapshot(self.db)
        changed = conversations.append(
            self.db, original["id"], original["revision"], turn("later")
        )
        self.assertEqual(
            conversations.restore(self.db, legacy)["conversations_added"], 0
        )
        self.assertEqual(
            conversations.restore(self.db, backup)["conversations_added"], 0
        )
        self.assertEqual(
            conversations.get(self.db, changed["id"])["turns"], changed["turns"]
        )
        other = offline.connect(Path(self.tmp.name) / "other.db")
        conversations.initialize(other)
        try:
            bad = copy.deepcopy(backup)
            bad["conversations"][0]["turns"][0]["sources"] = [{"id": "x"}]
            with self.assertRaises(ValueError):
                conversations.restore(other, bad)
            self.assertEqual(library.snapshot(other)["documents"], [])
            self.assertEqual(
                conversations.restore(other, backup),
                {"added": 1, "conversations_added": 1},
            )
        finally:
            other.close()

    def test_context_keeps_whole_recent_exchanges(self):
        turns = [turn(str(i), "x" * 2000) for i in range(8)]
        prompt, omitted = conversations.prompt("follow up", turns, "ru")
        self.assertGreater(omitted, 0)
        self.assertLessEqual(len(prompt.encode()), 10000)
        self.assertIn("Russian", prompt)
        data = json.loads(prompt.split("\n", 1)[1].rsplit("\nAnswer:", 1)[0])
        self.assertEqual(data["conversation"][-1]["user"], "7")
        self.assertEqual(len(data["conversation"]) + omitted, 8)
        with self.assertRaisesRegex(ValueError, "context_limit"):
            conversations.prompt("大" * 4000, [], "zh")

    def test_limit_rollback(self):
        with patch.object(conversations, "MAX_HISTORY", 10):
            with self.assertRaisesRegex(ValueError, "history_limit"):
                conversations.append(self.db, None, None, turn())
        self.assertEqual(conversations.listing(self.db), [])


class ChatAPIOnlyTests(unittest.TestCase):
    setUpClass = classmethod(test_server.ServerTests.setUpClass.__func__)
    tearDownClass = classmethod(test_server.ServerTests.tearDownClass.__func__)
    request = test_server.ServerTests.request

    def chat_request(self, **kwargs):
        data = {
            "question": "Help me plan",
            "lang": "en",
            "mode": "chat",
            "request_id": "a" * 32,
        }
        data.update(kwargs)
        return self.request("/api/chat", data)

    def test_general_chat_without_documents_and_followup(self):
        self.server.engine, self.server.model = "synthetic-engine", "synthetic-model"
        try:
            with patch.object(
                offline, "generate", return_value="A useful plan"
            ) as generate:
                result = json.loads(self.chat_request()[1])["conversation"]
                follow = json.loads(
                    self.chat_request(
                        id=result["id"],
                        revision=result["revision"],
                        question="Only 20 minutes daily",
                    )[1]
                )["conversation"]
                self.assertEqual(len(follow["turns"]), 2)
                self.assertIn("A useful plan", generate.call_args.args[2])
                self.assertIn("Only 20 minutes daily", generate.call_args.args[2])
            status, raw, _ = self.chat_request(
                id=result["id"], revision=result["revision"]
            )
            self.assertEqual(status, 400)
            self.assertEqual(json.loads(raw)["error"], "conversation_changed")
        finally:
            self.server.engine = self.server.model = None

    def test_failed_generation_does_not_save_partial_turn(self):
        self.server.engine, self.server.model = "synthetic-engine", "synthetic-model"
        before = json.loads(self.request("/api/state")[1])["conversations"]
        try:
            with patch.object(
                offline, "generate", side_effect=ValueError("engine failed")
            ):
                self.assertEqual(json.loads(self.chat_request()[1])["error"], "engine")
            self.assertEqual(
                json.loads(self.request("/api/state")[1])["conversations"], before
            )
        finally:
            self.server.engine = self.server.model = None

    def test_sources_no_match_never_generates(self):
        self.server.engine, self.server.model = "synthetic-engine", "synthetic-model"
        try:
            with patch.object(offline, "generate") as generate:
                result = json.loads(
                    self.chat_request(mode="sources", query="absent_unique_search")[1]
                )
                self.assertEqual(result["error"], "no_sources")
                generate.assert_not_called()
        finally:
            self.server.engine = self.server.model = None

    def test_cancel_and_busy_isolation(self):
        started = threading.Event()
        response = []

        def generate(*args, cancel_event=None):
            started.set()
            self.assertTrue(cancel_event.wait(4))
            raise ValueError("cancelled")

        self.server.engine, self.server.model = "synthetic-engine", "synthetic-model"
        try:
            with patch.object(offline, "generate", side_effect=generate):
                worker = threading.Thread(
                    target=lambda: response.append(self.chat_request())
                )
                worker.start()
                self.assertTrue(started.wait(2))
                self.assertEqual(
                    json.loads(self.chat_request(request_id="b" * 32)[1])["error"],
                    "busy",
                )
                self.request("/api/chat/cancel", {"request_id": "b" * 32})
                self.assertFalse(self.server.cancel_event.is_set())
                self.request("/api/chat/cancel", {"request_id": "a" * 32})
                worker.join(4)
                self.assertFalse(worker.is_alive())
                self.assertEqual(json.loads(response[0][1])["error"], "cancelled")
        finally:
            self.server.engine = self.server.model = None

    def test_assets_cannot_expose_files(self):
        for path in (
            "/assets/../../server.py",
            "/assets/../app.js",
            "/assets/icons/LICENSE",
        ):
            self.assertEqual(self.request(path, method="GET")[0], 404)
        self.assertEqual(self.request("/assets/brand.png", method="GET")[0], 200)
