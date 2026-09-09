"""Static contract checks, deliberately not a substitute for native runtime loading."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def flat_header(path):
    text = path.read_text()
    assert text.startswith("---\n"), path
    header, body = text[4:].split("\n---\n", 1)
    return dict(line.split(":", 1) for line in header.splitlines()), body


class PluginContractTests(unittest.TestCase):
    def test_manifest(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "harness-setup")
        self.assertEqual(manifest["version"], "0.1.0")

    def test_no_global_hooks_or_mcp_installation(self):
        self.assertFalse((ROOT / "hooks/hooks.json").exists())
        self.assertFalse((ROOT / ".mcp.json").exists())
        self.assertFalse((ROOT / "settings.json").exists())

    def test_skills_claude_specific_frontmatter(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            header, _ = flat_header(path)
            self.assertEqual(set(header), {"name", "description",
                                          "disable-model-invocation", "argument-hint"})
            self.assertEqual(header["name"].strip(), path.parent.name)
            self.assertEqual(header["disable-model-invocation"].strip(),
                             "true" if path.parent.name == "setup" else "false")
            self.assertIsInstance(json.loads(header["description"].strip()), str)

    def test_skill_hubs_small(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            self.assertLess(len(path.read_text()), 5000)

    def test_markdown_relative_links_resolve(self):
        for path in (ROOT / "skills").rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if not target.startswith(("https:", "http:", "#")):
                    self.assertTrue((path.parent / target).is_file(), (path, target))

    def test_readonly_agent_tool_allowlists(self):
        expected = {
            "context-auditor": "Read, Glob, Grep",
            "control-reviewer": "Read, Glob, Grep",
            "skill-creator": "Read, Glob, Grep",
            "public-researcher": "WebSearch, WebFetch",
        }
        for name, tools in expected.items():
            text = (ROOT / f"agents/{name}.md").read_text()
            self.assertIn(f"tools: {tools}\n", text)
            self.assertNotIn("permissionMode: bypassPermissions", text)

    def test_no_ignored_plugin_agent_fields(self):
        for path in (ROOT / "agents").glob("*.md"):
            header = path.read_text().split("\n---\n", 1)[0]
            for field in ("hooks", "mcpServers", "permissionMode"):
                self.assertNotIn(f"\n{field}:", header)

    def test_repository_marketplace_points_to_plugin(self):
        repository = ROOT.parents[1]
        marketplace = repository / ".claude-plugin/marketplace.json"
        if not marketplace.is_file():
            self.skipTest("Marketplace integration requires the full repository checkout")
        data = json.loads(marketplace.read_text())
        entries = [entry for entry in data["plugins"] if entry["name"] == "harness-setup"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(data["name"], "jetthoughts")
        self.assertEqual(entries[0]["source"], "./plugins/harness-setup")
        self.assertEqual((repository / entries[0]["source"]).resolve(), ROOT.resolve())

    def test_no_model_pin_or_plugin_dependency(self):
        data = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertNotIn("dependencies", data)
        for path in (ROOT / "agents").glob("*.md"):
            header = path.read_text().split("\n---\n", 1)[0]
            self.assertNotIn("\nmodel:", header)
            self.assertNotIn("\npermissionMode:", header)


if __name__ == "__main__":
    unittest.main()
