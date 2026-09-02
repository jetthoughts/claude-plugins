"""Tests for normalize.py. Run: python3 -m unittest discover -s tests -v"""
import json
import shutil
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import normalize  # noqa: E402


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vault = self.tmp / "vault"
        self.vault.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def inbox(self, source):
        d = self.vault / "research" / "_inbox" / source
        d.mkdir(parents=True, exist_ok=True)
        return d

    def run_cli(self, argv):
        buf = StringIO()
        with patch("sys.stdout", buf):
            code = normalize.main(["--vault", str(self.vault)] + argv)
        return code, buf.getvalue()


class TestMarkdownIngest(BaseCase):
    def test_happy_path_creates_note_and_moves_input(self):
        src = self.inbox("local")
        (src / "notes.md").write_text(
            "---\ntitle: My Finding\nurl: https://example.com/a\n---\n"
            "# My Finding\n\nSome researched content with a [link](https://example.com/a).\n",
            encoding="utf-8",
        )

        code, out = self.run_cli(["ingest"])

        self.assertEqual(code, 0)
        self.assertIn("ok\t", out)
        notes = list(self.vault.glob("research-local-*.md"))
        self.assertEqual(len(notes), 1)
        text = notes[0].read_text(encoding="utf-8")
        self.assertIn("type: Research", text)
        self.assertIn("source: local", text)
        self.assertIn("citations_preserved: true", text)
        self.assertIn("content_hash:", text)
        self.assertIn("# My Finding", text)
        # input moved to _done
        self.assertFalse((src / "notes.md").exists())
        self.assertTrue((self.vault / "research" / "_inbox" / "_done" / "local" / "notes.md").exists())

    def test_dry_run_does_not_write_or_move(self):
        src = self.inbox("local")
        (src / "notes.md").write_text("# Title\n\nbody text\n", encoding="utf-8")

        code, out = self.run_cli(["ingest", "--dry-run"])

        self.assertEqual(code, 0)
        self.assertIn("ok\t", out)
        self.assertEqual(list(self.vault.glob("research-local-*.md")), [])
        self.assertTrue((src / "notes.md").exists())


class TestDedupe(BaseCase):
    def test_second_ingest_of_same_content_skips(self):
        src = self.inbox("local")
        (src / "a.md").write_text("# Same Thing\n\nidentical body\n", encoding="utf-8")
        code1, out1 = self.run_cli(["ingest"])
        self.assertEqual(code1, 0)
        self.assertIn("ok\t", out1)

        # Re-drop an identical-content file (different name/source_id) and ingest again.
        src2 = self.inbox("local")
        (src2 / "b.md").write_text("# Same Thing\n\nidentical body\n", encoding="utf-8")
        code2, out2 = self.run_cli(["ingest"])

        self.assertEqual(code2, 0)
        self.assertIn("skip\t", out2)
        self.assertEqual(len(list(self.vault.glob("research-local-*.md"))), 1)


class TestQuarantine(BaseCase):
    def test_empty_file_is_quarantined_and_exits_nonzero(self):
        src = self.inbox("local")
        (src / "empty.md").write_text("---\ntitle: Empty\n---\n\n", encoding="utf-8")

        code, out = self.run_cli(["ingest"])

        self.assertEqual(code, 1)
        self.assertIn("quarantine\t", out)
        self.assertTrue((self.vault / "research" / "quarantine" / "empty.md").exists())
        self.assertTrue((self.vault / "research" / "quarantine" / "empty.md.reason.txt").exists())
        self.assertFalse((src / "empty.md").exists())


class TestClaudeExport(BaseCase):
    def test_conversations_json_splits_into_one_note_per_conversation(self):
        src = self.inbox("claude")
        payload = [
            {
                "name": "First Chat",
                "created_at": "2026-01-05T10:00:00Z",
                "chat_messages": [
                    {"sender": "human", "text": "What is KISS?"},
                    {"sender": "assistant", "text": "Keep it simple, see https://en.wikipedia.org/wiki/KISS_principle"},
                ],
            },
            {
                "name": "Second Chat",
                "created_at": "2026-01-06T10:00:00Z",
                "chat_messages": [
                    {"sender": "human", "text": "Another question"},
                    {"sender": "assistant", "text": "Another answer, no links here"},
                ],
            },
        ]
        (src / "conversations.json").write_text(json.dumps(payload), encoding="utf-8")

        code, out = self.run_cli(["ingest"])

        self.assertEqual(code, 0)
        notes = sorted(self.vault.glob("research-claude-*.md"))
        self.assertEqual(len(notes), 2)
        first = (self.vault / "research-claude-first-chat.md").read_text(encoding="utf-8")
        self.assertIn("citations_preserved: true", first)
        second = (self.vault / "research-claude-second-chat.md").read_text(encoding="utf-8")
        self.assertIn("citations_preserved: false", second)
        self.assertTrue(
            (self.vault / "research" / "_inbox" / "_done" / "claude" / "conversations.json").exists()
        )


class TestPublish(BaseCase):
    def test_publish_from_stdin_writes_note(self):
        buf = StringIO()
        with patch("sys.stdout", buf), patch("sys.stdin", StringIO("Published body with a source https://example.com\n")):
            code = normalize.main(
                [
                    "--vault",
                    str(self.vault),
                    "publish",
                    "--source",
                    "local",
                    "--title",
                    "Agent Published Result",
                    "--url",
                    "https://example.com",
                    "--tags",
                    "ldr,research",
                ]
            )

        self.assertEqual(code, 0)
        self.assertIn("ok\t", buf.getvalue())
        notes = list(self.vault.glob("research-local-agent-published-result.md"))
        self.assertEqual(len(notes), 1)
        text = notes[0].read_text(encoding="utf-8")
        self.assertIn("tags: [ldr, research]", text)
        self.assertIn("url: https://example.com", text)

    def test_publish_empty_stdin_quarantines_and_exits_nonzero(self):
        buf = StringIO()
        with patch("sys.stdout", buf), patch("sys.stdin", StringIO("   \n")):
            code = normalize.main(
                ["--vault", str(self.vault), "publish", "--source", "local", "--title", "Empty"]
            )

        self.assertEqual(code, 1)
        self.assertIn("quarantine\t", buf.getvalue())
        self.assertTrue(list((self.vault / "research" / "quarantine").glob("*.reason.txt")))


if __name__ == "__main__":
    unittest.main()
