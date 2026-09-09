"""Offline fixture tests: python3 -m unittest discover -s plugin/tests -v."""

import base64
import contextlib
import datetime as dt
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "harness.py"
SPEC = importlib.util.spec_from_file_location("harness", SCRIPT)
harness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(harness)


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "project"
        self.root.mkdir()
        self.bundle = self.base / "bundle"
        self.plan = self.base / "plan.json"

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, content):
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def stage(self, changes=None, rationale="Improve project guidance"):
        if changes is None:
            changes = [{"path": "CLAUDE.md", "operation": "managed_block",
                        "value": "Run the documented tests before proposing a change."}]
        self.plan.write_text(json.dumps({"schema_version": 1, "rationale": rationale,
                                         "changes": changes}), encoding="utf-8")
        return harness.stage(self.root, self.plan, self.bundle)

    def manifest(self):
        return json.loads((self.bundle / "manifest.json").read_text())

    def save_manifest(self, value, redigest=False):
        if redigest:
            value["digest"] = harness.candidate_digest(value)
        (self.bundle / "manifest.json").write_bytes(harness.canonical(value))

    def json_change(self, value):
        return {"path": ".claude/settings.json", "operation": "json_merge", "value": value}

    def create_change(self, path=".claude/skills/check/SKILL.md"):
        body = "# Check\n\nReview tests.\n"
        if "/references/" in path:
            value = body
        elif path.endswith("/SKILL.md"):
            value = (f'---\nname: {Path(path).parent.name}\ndescription: "Review tests."\n'
                     f"disable-model-invocation: true\n---\n{body}")
        else:
            value = (f'---\nname: {Path(path).stem}\ndescription: "Review tests."\n'
                     f"tools: Read, Glob, Grep\n---\n{body}")
        return {"path": path, "operation": "create", "value": value}

    def receipt(self):
        return json.loads((self.bundle / "receipt.json").read_text())

    def test_recursive_merge_preserves_unrelated_keys_and_replaces_array(self):
        original = {"nested": {"keep": 1, "replace": [1]}, "unrelated": True}
        merged = harness.recursive_merge(original, {"nested": {"replace": [2]}})
        self.assertEqual(merged, {"nested": {"keep": 1, "replace": [2]}, "unrelated": True})
        self.assertEqual(original["nested"]["replace"], [1])

    def test_settings_preserve_existing_provider_permissions_and_hooks(self):
        original = {"model": "unchanged", "env": {"ANTHROPIC_BASE_URL": "SECRET_URL"},
                    "hooks": {"SessionStart": [{"command": "DO_NOT_RUN"}]},
                    "permissions": {"allow": ["Read"], "deny": ["Bash(rm:*)"]},
                    "enabledPlugins": {"claude-code-setup@official": True}}
        self.write(".claude/settings.json", json.dumps(original))
        result = self.stage([self.json_change({
            "permissions": {"deny": ["Bash(rm:*)", "Read(.env)"]},
            "enabledPlugins": {"harness-setup@local": True},
        })])
        harness.apply(self.bundle, result["digest"])
        actual = json.loads((self.root / ".claude/settings.json").read_text())
        self.assertEqual(actual["env"], original["env"])
        self.assertEqual(actual["model"], original["model"])
        self.assertEqual(actual["hooks"], original["hooks"])
        self.assertEqual(actual["permissions"]["allow"], ["Read"])
        self.assertEqual(actual["enabledPlugins"]["claude-code-setup@official"], True)

    def test_managed_block_idempotent_and_preserves_outside_bytes(self):
        before = b"outside\r\n" + harness.BEGIN.encode() + b"\r\nold\r\n" + harness.END.encode() + b"\r\ntrailer"
        after = harness.managed_block(before, "new\n")
        self.assertTrue(after.startswith(b"outside\r\n"))
        self.assertTrue(after.endswith(b"\r\ntrailer"))
        self.assertEqual(after, harness.managed_block(after, "new"))

    def test_managed_block_append_preserves_original_prefix(self):
        self.assertTrue(harness.managed_block(b"no trailing newline", "owned").startswith(b"no trailing newline\n"))

    def test_broken_repeated_inline_reversed_markers_rejected(self):
        for before in (
            harness.BEGIN, harness.END,
            harness.BEGIN + "\n" + harness.END + "\n" + harness.BEGIN + "\n" + harness.END,
            harness.END + "\n" + harness.BEGIN,
            "prefix " + harness.BEGIN + "\n" + harness.END,
            harness.BEGIN + " inline\n" + harness.END,
        ):
            with self.subTest(before=before), self.assertRaises(harness.HarnessError):
                harness.managed_block(before.encode(), "new")

    def test_managed_value_cannot_inject_marker(self):
        with self.assertRaises(harness.HarnessError):
            harness.managed_block(b"", harness.BEGIN)

    def test_stage_check_apply_rollback_all_operations(self):
        original = b'{"permissions":{"deny":["Read(.env)"]},"extra":{"keep":true}}\n'
        settings = self.write(".claude/settings.json", original)
        settings.chmod(0o640)
        claude = self.write("CLAUDE.md", b"Human-owned notes.\r\n")
        before = claude.read_bytes()
        result = self.stage([
            self.json_change({"enabledPlugins": {"harness-setup@local": True}}),
            {"path": "CLAUDE.md", "operation": "managed_block", "value": "Owned instructions."},
            self.create_change(),
            self.create_change(".claude/skills/check/references/testing.md"),
            self.create_change(".claude/agents/reviewer.md"),
        ])
        self.assertEqual(settings.read_bytes(), original)
        self.assertEqual(claude.read_bytes(), before)
        self.assertEqual(harness.check(self.bundle, self.root)["status"], "ready")
        self.assertIn("--- a/CLAUDE.md", harness.diff(self.bundle))
        self.assertIn("--- /dev/null", harness.diff(self.bundle))
        self.assertEqual(harness.apply(self.bundle, result["digest"])["status"], "applied")
        self.assertEqual(stat.S_IMODE(settings.stat().st_mode), 0o640)
        self.assertEqual((self.bundle / "backups/0000.bin").read_bytes(), original)
        self.assertEqual(harness.rollback(self.bundle, result["digest"])["status"], "rolled_back")
        self.assertEqual(settings.read_bytes(), original)
        self.assertEqual(claude.read_bytes(), before)
        self.assertFalse((self.root / ".claude/skills/check/SKILL.md").exists())
        self.assertFalse((self.root / ".claude/skills/check/references/testing.md").exists())
        self.assertFalse((self.root / ".claude/agents/reviewer.md").exists())

    def test_wrong_digest_never_writes(self):
        self.stage()
        with self.assertRaises(harness.HarnessError):
            harness.apply(self.bundle, "0" * 64)
        self.assertFalse((self.root / "CLAUDE.md").exists())
        self.assertFalse((self.bundle / "receipt.json").exists())

    def test_stale_bundle_blocks_check_apply_but_diff_remains_reviewable(self):
        self.stage()
        manifest = self.manifest()
        created = harness.now() - dt.timedelta(days=2)
        manifest["created_at"] = harness.stamp(created)
        manifest["expires_at"] = harness.stamp(created + dt.timedelta(hours=24))
        self.save_manifest(manifest, redigest=True)
        for fn in (lambda: harness.check(self.bundle),
                   lambda: harness.apply(self.bundle, manifest["digest"])):
            with self.assertRaisesRegex(harness.HarnessError, "expired"):
                fn()
        self.assertIn("harness-setup:begin", harness.diff(self.bundle))

    def test_rollback_allowed_after_expiry_without_rewriting_digest(self):
        clock = harness.now()
        with mock.patch.object(harness, "now", return_value=clock):
            result = self.stage()
            harness.apply(self.bundle, result["digest"])
        with mock.patch.object(harness, "now", return_value=clock + dt.timedelta(days=3)):
            self.assertEqual(harness.rollback(self.bundle, result["digest"])["status"], "rolled_back")

    def test_future_timestamp_rejected(self):
        self.stage()
        manifest = self.manifest()
        created = harness.now() + dt.timedelta(hours=1)
        manifest["created_at"] = harness.stamp(created)
        manifest["expires_at"] = harness.stamp(created + dt.timedelta(hours=24))
        self.save_manifest(manifest, redigest=True)
        with self.assertRaisesRegex(harness.HarnessError, "future"):
            harness.check(self.bundle)

    def test_live_drift_blocks_all_writes(self):
        self.write("CLAUDE.md", "before")
        result = self.stage([self.create_change(), {"path": "CLAUDE.md", "operation": "managed_block", "value": "owned"}])
        self.write("CLAUDE.md", "external edit")
        with self.assertRaisesRegex(harness.HarnessError, "drift"):
            harness.apply(self.bundle, result["digest"])
        self.assertFalse((self.root / ".claude").exists())

    def test_file_mode_drift_blocks_apply(self):
        path = self.write("CLAUDE.md", "before")
        path.chmod(0o644)
        self.stage()
        path.chmod(0o600)
        with self.assertRaisesRegex(harness.HarnessError, "drift"):
            harness.check(self.bundle)

    def test_manifest_digest_binds_rationale_and_bytes(self):
        self.stage()
        manifest = self.manifest()
        manifest["rationale"] = "tampered"
        self.save_manifest(manifest)
        with self.assertRaisesRegex(harness.HarnessError, "digest"):
            harness.check(self.bundle)

    def test_rehashed_arbitrary_postimage_still_fails_operation_validation(self):
        self.stage()
        manifest = self.manifest()
        data = b"unapproved replacement"
        manifest["changes"][0]["postimage"]["content_b64"] = base64.b64encode(data).decode()
        manifest["changes"][0]["postimage"]["sha256"] = harness.sha(data)
        self.save_manifest(manifest, redigest=True)
        with self.assertRaisesRegex(harness.HarnessError, "postimage"):
            harness.check(self.bundle)

    def test_bad_image_hash_rejected_even_with_new_manifest_digest(self):
        self.stage()
        manifest = self.manifest()
        manifest["changes"][0]["postimage"]["sha256"] = "0" * 64
        self.save_manifest(manifest, redigest=True)
        with self.assertRaisesRegex(harness.HarnessError, "hash"):
            harness.check(self.bundle)

    def test_unknown_manifest_field_rejected(self):
        self.stage()
        manifest = self.manifest()
        manifest["run"] = "do-not-execute"
        self.save_manifest(manifest, redigest=True)
        with self.assertRaises(harness.HarnessError):
            harness.check(self.bundle)

    def test_project_binding_rejected(self):
        self.stage()
        other = self.base / "other"
        other.mkdir()
        with self.assertRaisesRegex(harness.HarnessError, "different project"):
            harness.check(self.bundle, other)

    def test_invalid_paths_and_operations(self):
        for path, operation in (
            ("../CLAUDE.md", "managed_block"), ("/CLAUDE.md", "managed_block"),
            ("./CLAUDE.md", "managed_block"), ("x/../CLAUDE.md", "managed_block"),
            (".claude//settings.json", "json_merge"), (r".claude\settings.json", "json_merge"),
            (".mcp.json", "json_merge"), (".claude/settings.local.json", "json_merge"),
            ("~/.claude/settings.json", "json_merge"), (".claude/hooks/start.sh", "create"),
            (".claude/skills/check/scripts/run.py", "create"), ("AGENTS.md", "managed_block"),
            ("CLAUDE.md", "delete"), ("CLAUDE.md", "unknown"),
        ):
            with self.subTest(path=path, operation=operation):
                with self.assertRaises(harness.HarnessError):
                    self.stage([{"path": path, "operation": operation, "value": "x"}])
                self.assertFalse(self.bundle.exists())

    def test_duplicate_paths_rejected(self):
        change = self.create_change()
        with self.assertRaisesRegex(harness.HarnessError, "duplicate"):
            self.stage([change, change])

    def test_create_existing_file_rejected_even_identical(self):
        change = self.create_change()
        self.write(change["path"], change["value"])
        with self.assertRaisesRegex(harness.HarnessError, "existing"):
            self.stage([change])

    def test_created_carriers_reject_all_unapproved_native_frontmatter(self):
        for path in (".claude/skills/check/SKILL.md", ".claude/agents/check.md"):
            for field in (
                'model: opus', 'permissionMode: bypassPermissions',
                'hooks: {"PreToolUse":[{"command":"DO_NOT_RUN"}]}',
                'mcpServers: {"server":{"command":"DO_NOT_RUN"}}',
                'allowed-tools: Bash', 'memory: project', 'skills: other',
                'unknown: true', 'name: duplicate',
            ):
                change = self.create_change(path)
                change["value"] = change["value"].replace("\n---\n", f"\n{field}\n---\n", 1)
                with self.subTest(path=path, field=field), self.assertRaises(harness.HarnessError):
                    self.stage([change])
                self.assertFalse(self.bundle.exists())

    def test_created_carriers_reject_malformed_yaml_subset(self):
        for path in (".claude/skills/check/SKILL.md", ".claude/agents/check.md"):
            valid = self.create_change(path)
            for value in (
                "No frontmatter\n", "\ufeff" + valid["value"],
                valid["value"].replace("name: check", "name: different"),
                valid["value"].replace("name: check", " name: check"),
                valid["value"].replace('description: "Review tests."', "description: unquoted"),
                valid["value"].replace('description: "Review tests."', "description: 'single quoted'"),
                valid["value"].replace('description: "Review tests."', "description: |\n  multiline"),
                valid["value"].replace('description: "Review tests."', "description: &alias value"),
                valid["value"].replace('description: "Review tests."', "description: *alias"),
                valid["value"].replace('description: "Review tests."', 'description: ""'),
                valid["value"].replace('description: "Review tests."', 'description: "one\\ntwo"'),
                valid["value"].replace("\n---\n", "\n...\n"),
                valid["value"].replace("\n", "\r\n"),
            ):
                with self.subTest(path=path, value=value), self.assertRaises(harness.HarnessError):
                    self.stage([{**valid, "value": value}])
                self.assertFalse(self.bundle.exists())

    def test_created_skills_must_be_explicitly_invoked(self):
        valid = self.create_change()
        for value in (
            valid["value"].replace("disable-model-invocation: true\n", ""),
            valid["value"].replace("disable-model-invocation: true", "disable-model-invocation: false"),
            valid["value"].replace("disable-model-invocation: true", 'disable-model-invocation: "true"'),
        ):
            with self.subTest(value=value), self.assertRaises(harness.HarnessError):
                self.stage([{**valid, "value": value}])

    def test_created_agents_require_read_only_tool_subset(self):
        valid = self.create_change(".claude/agents/check.md")
        for tools in ("Bash", "Read, Write", "Read, Edit", "Agent", "Read, Read", "",
                      "Read,", "[Read, Grep]", "*alias", "mcp__server__tool"):
            value = valid["value"].replace("tools: Read, Glob, Grep", "tools: " + tools)
            with self.subTest(tools=tools), self.assertRaises(harness.HarnessError):
                self.stage([{**valid, "value": value}])

    def test_valid_created_skill_hint_agent_tools_and_plain_reference(self):
        skill = self.create_change()
        skill["value"] = skill["value"].replace("\n---\n", '\nargument-hint: "[target]"\n---\n', 1)
        agent = self.create_change(".claude/agents/check.md")
        agent["value"] = agent["value"].replace("Read, Glob, Grep", "Read,WebSearch,WebFetch")
        reference = self.create_change(".claude/skills/check/references/testing.md")
        result = self.stage([skill, agent, reference])
        harness.check(self.bundle)
        harness.apply(self.bundle, result["digest"])
        self.assertEqual((self.root / skill["path"]).read_text(), skill["value"])
        harness.rollback(self.bundle, result["digest"])

    def test_rehashed_unsafe_carrier_fails_bundle_revalidation(self):
        self.stage([self.create_change(".claude/agents/check.md")])
        manifest = self.manifest()
        change = manifest["changes"][0]
        change["value"] = change["value"].replace("\n---\n", "\npermissionMode: bypassPermissions\n---\n", 1)
        data = change["value"].encode()
        change["postimage"]["content_b64"] = base64.b64encode(data).decode()
        change["postimage"]["sha256"] = harness.sha(data)
        self.save_manifest(manifest, redigest=True)
        with self.assertRaises(harness.HarnessError):
            harness.check(self.bundle)
        with self.assertRaises(harness.HarnessError):
            harness.apply(self.bundle, manifest["digest"])
        self.assertFalse((self.root / change["path"]).exists())

    def test_preexisting_hardlinked_claude_target_rejected(self):
        target = self.write("CLAUDE.md", "shared instructions")
        alias = self.base / "shared.md"
        os.link(target, alias)
        with self.assertRaisesRegex(harness.HarnessError, "hardlinked"):
            self.stage()
        self.assertEqual(target.stat().st_ino, alias.stat().st_ino)
        self.assertFalse(self.bundle.exists())

    def test_preexisting_hardlinked_settings_target_rejected(self):
        target = self.write(".claude/settings.json", "{}")
        alias = self.base / "shared-settings.json"
        os.link(target, alias)
        with self.assertRaisesRegex(harness.HarnessError, "hardlinked"):
            self.stage([self.json_change({"enabledPlugins": {"local@manual": True}})])
        self.assertEqual(target.stat().st_ino, alias.stat().st_ino)
        self.assertFalse(self.bundle.exists())

    def test_hardlink_created_after_stage_blocks_check_and_apply(self):
        target = self.write("CLAUDE.md", "original")
        result = self.stage()
        alias = self.base / "late-link.md"
        os.link(target, alias)
        with self.assertRaisesRegex(harness.HarnessError, "hardlinked"):
            harness.check(self.bundle)
        with self.assertRaisesRegex(harness.HarnessError, "hardlinked"):
            harness.apply(self.bundle, result["digest"])
        self.assertEqual(target.stat().st_ino, alias.stat().st_ino)
        self.assertEqual(target.read_text(), "original")
        self.assertFalse((self.bundle / "receipt.json").exists())

    def test_hardlink_created_after_apply_blocks_rollback(self):
        self.write("CLAUDE.md", "original")
        result = self.stage()
        harness.apply(self.bundle, result["digest"])
        target = self.root / "CLAUDE.md"
        alias = self.base / "late-link.md"
        os.link(target, alias)
        with self.assertRaisesRegex(harness.HarnessError, "hardlinked"):
            harness.rollback(self.bundle, result["digest"])
        self.assertEqual(target.stat().st_ino, alias.stat().st_ino)
        self.assertEqual(self.receipt()["state"], "applied")

    def test_hardlinked_newly_created_target_is_not_deleted_by_rollback(self):
        change = self.create_change()
        result = self.stage([change])
        harness.apply(self.bundle, result["digest"])
        target = self.root / change["path"]
        alias = self.base / "late-skill.md"
        os.link(target, alias)
        with self.assertRaisesRegex(harness.HarnessError, "hardlinked"):
            harness.rollback(self.bundle, result["digest"])
        self.assertTrue(target.exists())
        self.assertEqual(target.stat().st_ino, alias.stat().st_ino)

    def test_no_changes_and_empty_rationale_fail(self):
        for changes, rationale in (([], "why"), (None, ""), (None, "   ")):
            with self.subTest(changes=changes, rationale=rationale):
                with self.assertRaises(harness.HarnessError):
                    self.stage(changes, rationale)

    def test_blank_malformed_duplicate_and_nonfinite_json_fail(self):
        for raw in ("", "  ", "{", "[]", '{"schema_version":1,"schema_version":1}',
                    '{"x":NaN}', '{"x":Infinity}'):
            self.plan.write_text(raw)
            with self.subTest(raw=raw), self.assertRaises(harness.HarnessError):
                harness.stage(self.root, self.plan, self.bundle)

    def test_malformed_existing_settings_fail(self):
        for raw in ("", "[]", "{", '{"permissions":null}'):
            self.write(".claude/settings.json", raw)
            with self.subTest(raw=raw), self.assertRaises(harness.HarnessError):
                self.stage([self.json_change({"permissions": {"ask": ["Bash(*)"]}})])

    def test_unsafe_settings_rejected(self):
        patches = (
            {"permissions": {"defaultMode": "bypassPermissions"}},
            {"permissions": {"defaultMode": "acceptEdits"}},
            {"permissions": {"allow": ["Bash(*)"]}},
            {"allowManagedPermissionRulesOnly": False},
            {"hooks": {"SessionStart": []}}, {"env": {"ANTHROPIC_BASE_URL": "elsewhere"}},
            {"model": "other"}, {"enablePlugins": {"x": True}}, {},
            {"enabledPlugins": {"https://example.invalid": True}},
            {"enabledPlugins": {"valid": "true"}},
            {"enabledPlugins": {"valid": 1}},
            {"permissions": {"ask": [""]}}, {"permissions": {"deny": ["\n"]}},
            {"permissions": {"ask": [1]}}, {"permissions": {"deny": "Bash(*)"}},
            {"permissions": {"ask": ["x" * 513]}},
        )
        for patch in patches:
            with self.subTest(patch=patch), self.assertRaises(harness.HarnessError):
                self.stage([self.json_change(patch)])

    def test_permission_replacement_must_keep_existing_rules(self):
        self.write(".claude/settings.json", '{"permissions":{"deny":["Read(.env)"]}}')
        for rules in ([], ["Bash(*)"]):
            with self.subTest(rules=rules), self.assertRaisesRegex(harness.HarnessError, "retain"):
                self.stage([self.json_change({"permissions": {"deny": rules}})])

    def test_project_symlink_and_ancestor_symlink_rejected(self):
        alias = self.base / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        for project in (alias, alias / "child"):
            (self.root / "child").mkdir(exist_ok=True)
            with self.subTest(project=project), self.assertRaises(harness.HarnessError):
                harness.scan(project)

    def test_target_and_target_ancestor_symlinks_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        target = self.root / ".claude"
        target.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            self.stage([self.create_change()])
        (self.root / "CLAUDE.md").symlink_to(outside / "missing")
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            self.stage()

    def test_input_symlink_rejected(self):
        target = self.base / "real-plan.json"
        target.write_text("{}")
        self.plan.symlink_to(target)
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            harness.stage(self.root, self.plan, self.bundle)

    def test_bundle_symlink_and_ancestor_symlink_rejected(self):
        result = self.stage()
        alias = self.base / "alias-bundle"
        alias.symlink_to(self.bundle, target_is_directory=True)
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            harness.apply(alias, result["digest"])
        outer = self.base / "alias-base"
        outer.symlink_to(self.base, target_is_directory=True)
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            harness.check(outer / "bundle")

    def test_manifest_and_receipt_symlinks_rejected(self):
        result = self.stage()
        target = self.base / "receipt"
        target.write_text("{}")
        (self.bundle / "receipt.json").symlink_to(target)
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            harness.apply(self.bundle, result["digest"])
        other = self.base / "other-bundle"
        other.mkdir()
        (other / "manifest.json").symlink_to(self.bundle / "manifest.json")
        with self.assertRaisesRegex(harness.HarnessError, "symlink"):
            harness.check(other)

    def test_target_symlink_created_after_stage_blocks_apply(self):
        result = self.stage()
        outside = self.base / "outside.md"
        outside.write_text("unchanged")
        (self.root / "CLAUDE.md").symlink_to(outside)
        with self.assertRaises(harness.HarnessError):
            harness.apply(self.bundle, result["digest"])
        self.assertEqual(outside.read_text(), "unchanged")

    def test_bundle_inside_project_or_existing_bundle_rejected(self):
        self.stage()
        for path in (self.root / "proposal", self.bundle):
            with self.subTest(path=path), self.assertRaises(harness.HarnessError):
                harness.stage(self.root, self.plan, path)

    def test_rollback_refuses_drift_and_wrong_approval(self):
        result = self.stage()
        harness.apply(self.bundle, result["digest"])
        with self.assertRaises(harness.HarnessError):
            harness.rollback(self.bundle, "0" * 64)
        self.write("CLAUDE.md", "human changed after apply")
        with self.assertRaisesRegex(harness.HarnessError, "drift"):
            harness.rollback(self.bundle, result["digest"])
        self.assertEqual((self.root / "CLAUDE.md").read_text(), "human changed after apply")

    def test_rollback_requires_receipt_and_checks_receipt_digest(self):
        result = self.stage()
        with self.assertRaisesRegex(harness.HarnessError, "receipt"):
            harness.rollback(self.bundle, result["digest"])
        harness.apply(self.bundle, result["digest"])
        receipt = self.receipt()
        receipt["digest"] = "0" * 64
        (self.bundle / "receipt.json").write_text(json.dumps(receipt))
        with self.assertRaisesRegex(harness.HarnessError, "receipt"):
            harness.rollback(self.bundle, result["digest"])

    def test_backup_tamper_blocks_rollback(self):
        self.write("CLAUDE.md", "original")
        result = self.stage()
        harness.apply(self.bundle, result["digest"])
        (self.bundle / "backups/0000.bin").write_text("tampered")
        with self.assertRaisesRegex(harness.HarnessError, "backup"):
            harness.rollback(self.bundle, result["digest"])

    def test_replay_apply_and_check_after_apply_refused(self):
        result = self.stage()
        harness.apply(self.bundle, result["digest"])
        with self.assertRaises(harness.HarnessError):
            harness.apply(self.bundle, result["digest"])
        with self.assertRaises(harness.HarnessError):
            harness.check(self.bundle)
        harness.rollback(self.bundle, result["digest"])
        with self.assertRaises(harness.HarnessError):
            harness.apply(self.bundle, result["digest"])

    def test_apply_failure_compensates_completed_writes(self):
        self.write("CLAUDE.md", "original")
        result = self.stage([
            {"path": "CLAUDE.md", "operation": "managed_block", "value": "owned"},
            self.create_change(),
        ])
        real_write = harness.atomic_write

        def fail_second(path, data, mode=0o600):
            if Path(path).name == "SKILL.md":
                raise OSError("simulated failure")
            return real_write(path, data, mode)

        with mock.patch.object(harness, "atomic_write", side_effect=fail_second):
            with self.assertRaisesRegex(harness.HarnessError, "reverted"):
                harness.apply(self.bundle, result["digest"])
        self.assertEqual((self.root / "CLAUDE.md").read_text(), "original")
        self.assertEqual(self.receipt()["state"], "apply_reverted")
        self.assertEqual(self.receipt()["pending"], [])

    def test_partial_compensation_is_recorded_and_can_be_rolled_back(self):
        self.write("CLAUDE.md", "original")
        result = self.stage([
            {"path": "CLAUDE.md", "operation": "managed_block", "value": "owned"},
            self.create_change(),
        ])
        real_write = harness.atomic_write

        def fail_create_and_restore(path, data, mode=0o600):
            if Path(path).name == "SKILL.md" or (Path(path).name == "CLAUDE.md" and data == b"original"):
                raise OSError("simulated failure")
            return real_write(path, data, mode)

        with mock.patch.object(harness, "atomic_write", side_effect=fail_create_and_restore):
            with self.assertRaisesRegex(harness.HarnessError, "partial"):
                harness.apply(self.bundle, result["digest"])
        self.assertEqual(self.receipt()["state"], "apply_failed")
        self.assertEqual(self.receipt()["pending"], ["CLAUDE.md"])
        harness.rollback(self.bundle, result["digest"])
        self.assertEqual((self.root / "CLAUDE.md").read_text(), "original")

    def test_partial_rollback_can_resume_without_touching_reverted_files(self):
        result = self.stage([
            {"path": "CLAUDE.md", "operation": "managed_block", "value": "owned"},
            self.create_change(),
        ])
        harness.apply(self.bundle, result["digest"])
        real_restore = harness.restore

        def fail_one(root, change):
            if change["path"] == "CLAUDE.md":
                raise OSError("simulated failure")
            return real_restore(root, change)

        with mock.patch.object(harness, "restore", side_effect=fail_one):
            with self.assertRaisesRegex(harness.HarnessError, "incomplete"):
                harness.rollback(self.bundle, result["digest"])
        self.assertEqual(self.receipt()["state"], "rollback_failed")
        self.assertEqual(self.receipt()["pending"], ["CLAUDE.md"])
        self.assertFalse((self.root / ".claude/skills/check/SKILL.md").exists())
        harness.rollback(self.bundle, result["digest"])
        self.assertFalse((self.root / "CLAUDE.md").exists())

    def test_cooperating_writer_lock_is_exclusive(self):
        result = self.stage()
        with harness.writer_lock(self.root):
            with self.assertRaisesRegex(harness.HarnessError, "writer"):
                harness.apply(self.bundle, result["digest"])
        self.assertFalse((self.root / "CLAUDE.md").exists())

    def test_writer_lock_resolves_os_temporary_base_symlink(self):
        real_temp = self.base / "real-temp"
        real_temp.mkdir()
        temp_alias = self.base / "temp-alias"
        temp_alias.symlink_to(real_temp, target_is_directory=True)
        result = self.stage()
        with mock.patch.object(tempfile, "gettempdir", return_value=str(temp_alias)):
            self.assertEqual(harness.apply(self.bundle, result["digest"])["status"], "applied")

    def test_non_regular_input_is_rejected_without_reading_fifo(self):
        os.mkfifo(self.plan)
        with self.assertRaisesRegex(harness.HarnessError, "regular"):
            harness.stage(self.root, self.plan, self.bundle)

    def test_bundle_private_and_no_unapproved_baselines(self):
        self.write(".env", "UNRELATED_SECRET")
        self.write("CLAUDE.md", "approved")
        self.stage()
        raw = (self.bundle / "manifest.json").read_bytes()
        self.assertNotIn(b"UNRELATED_SECRET", raw)
        self.assertEqual(stat.S_IMODE(self.bundle.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE((self.bundle / "manifest.json").stat().st_mode), 0o600)

    def test_diff_preserves_missing_newline_evidence(self):
        self.write("CLAUDE.md", "before")
        self.stage()
        self.assertIn("\\ No newline at end of file", harness.diff(self.bundle))

    def test_scan_redacts_credentials_urls_env_args_hooks_and_transcripts(self):
        secrets = ["TOKEN_VALUE_8971", "https://private.example/?key=77",
                   "HOOK_EXECUTION_693", "ARG_SECRET_441", "TRANSCRIPT_SECRET_118"]
        self.write(".claude/settings.json", json.dumps({
            "env": {"ANTHROPIC_AUTH_TOKEN": secrets[0], "ANTHROPIC_BASE_URL": secrets[1]},
            "apiKeyHelper": secrets[2], "hooks": {"SessionStart": [{"command": secrets[2]}]},
            "permissions": {"allow": [secrets[3]], "ask": ["Bash(*)"]},
            "enabledPlugins": {"claude-code-setup@official": True,
                               "claude-md-management@official": True,
                               secrets[1]: True},
            secrets[1]: secrets[0],
        }))
        self.write(".mcp.json", json.dumps({"mcpServers": {"private": {
            "url": secrets[1], "env": {"TOKEN": secrets[0]}, "args": [secrets[3]]}}}))
        self.write("CLAUDE.md", secrets[0])
        self.write("package.json", secrets[0])
        home = self.base / "fake-home"
        config = home / ".claude"
        config.mkdir(parents=True)
        (config / ".credentials.json").write_text(secrets[0])
        (config / "settings.json").write_text(json.dumps({"env": {"TOKEN": secrets[0]}}))
        (config / "sessions").mkdir()
        (config / "sessions/transcript.jsonl").write_text(secrets[4])
        with mock.patch.object(Path, "home", return_value=home), mock.patch.dict(
                os.environ, {"ANTHROPIC_AUTH_TOKEN": secrets[0], "CLAUDE_CONFIG_DIR": str(config)}):
            report = harness.scan(self.root, include_user=True)
        raw = json.dumps(report)
        for secret in secrets:
            self.assertNotIn(secret, raw)
        self.assertNotIn(str(config), raw)
        self.assertNotIn(".credentials.json", raw)
        self.assertNotIn("transcript.jsonl", raw)
        self.assertIn("ANTHROPIC_AUTH_TOKEN", report["runtime"]["route_environment_names_present"])
        self.assertIn("claude-code-setup@official", raw)
        self.assertIn("claude-md-management@official", raw)
        self.assertFalse(report["scope"]["commands_executed"])

    def test_scan_configuration_presence_never_means_connection(self):
        self.write(".mcp.json", '{"mcpServers":{"server":{"command":"DO_NOT_RUN"}}}')
        report = harness.scan(self.root)
        mcp = next(item for item in report["configuration"] if item["kind"] == "mcp")
        self.assertEqual(mcp["status"], "present")
        self.assertEqual(mcp["summary"]["server_count"], 1)
        self.assertEqual(mcp["summary"]["connection"], "unverified")
        self.assertEqual(report["runtime"]["shell_aliases_wrappers"], "unverified")
        self.assertEqual(report["scope"]["runtime_readiness"], "unverified")
        self.assertEqual(report["scope"]["global_managed_state"], "incomplete")

    def test_scan_depth_vendor_exclusion_and_ancestor_instructions(self):
        (self.base / "AGENTS.md").write_text("ancestor-content-not-reported")
        self.write("package.json", "{}")
        self.write("packages/app/pyproject.toml", "[project]")
        self.write("packages/app/deep/go.mod", "module hidden")
        self.write("node_modules/other/package.json", "{}")
        self.write(".git/package.json", "{}")
        report = harness.scan(self.root, max_depth=2)
        paths = [item["path"] for item in report["stack_manifests"]]
        self.assertEqual(paths, ["package.json", "packages/app/pyproject.toml"])
        ancestor = next(item for item in report["instructions"]
                        if item["path"] == str(self.base / "AGENTS.md"))
        self.assertEqual(ancestor["status"], "present")
        self.assertNotIn("ancestor-content-not-reported", json.dumps(report))

    def test_scan_skill_agent_plugin_metadata_not_contents(self):
        self.write(".claude/skills/check/SKILL.md", "DO_NOT_OUTPUT_SKILL_CONTENT")
        self.write(".claude/skills/check/references/testing.md", "DO_NOT_OUTPUT_REFERENCE")
        self.write(".claude/agents/review.md", "DO_NOT_OUTPUT_AGENT_CONTENT")
        self.write(".claude-plugin/plugin.json", '{"name":"harness-setup","version":"1.0.0","secret":"NO"}')
        report = harness.scan(self.root)
        self.assertEqual(len(report["skills"]), 2)
        self.assertEqual(len(report["agents"]), 1)
        self.assertEqual(report["plugin_metadata"][0]["summary"], {"name": "harness-setup", "version": "1.0.0"})
        self.assertNotIn("DO_NOT_OUTPUT", json.dumps(report))

    def test_scan_reports_malformed_symlink_unreadable_and_oversize(self):
        self.write(".claude/settings.json", "{")
        self.write("package.json", b"x" * (harness.MAX_FILE + 1))
        (self.root / ".mcp.json").symlink_to(self.base / "missing")
        report = harness.scan(self.root)
        configurations = {item["path"]: item for item in report["configuration"]}
        self.assertEqual(configurations[".claude/settings.json"]["status"], "malformed")
        self.assertEqual(configurations[".mcp.json"]["status"], "symlink")
        self.assertEqual(report["stack_manifests"][0]["status"], "too_large")
        with mock.patch.object(harness, "bounded_read", side_effect=PermissionError()):
            item = harness.metadata(self.root / ".claude/settings.json", "settings", "settings")
        self.assertEqual(item["status"], "unreadable")

    def test_scan_does_not_read_home_without_include_user(self):
        with mock.patch.object(Path, "home", side_effect=AssertionError("home access forbidden")):
            report = harness.scan(self.root)
        self.assertFalse(report["user"]["included"])
        self.assertEqual(report["user"]["configuration"], [])

    def test_scan_known_user_skills_agents_and_project_rules(self):
        home = self.base / "fake-home"
        skill = home / ".claude/skills/existing/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("PRIVATE_SKILL_CONTENT")
        agent = home / ".claude/agents/review.md"
        agent.parent.mkdir()
        agent.write_text("PRIVATE_AGENT_CONTENT")
        self.write(".claude/CLAUDE.md", "PRIVATE_INSTRUCTION")
        self.write(".claude/rules/testing.md", "PRIVATE_RULE")
        with mock.patch.object(Path, "home", return_value=home), mock.patch.dict(
                os.environ, {"CLAUDE_CONFIG_DIR": ""}):
            report = harness.scan(self.root, include_user=True)
        self.assertIn("~/.claude/skills/existing/SKILL.md", [item["path"] for item in report["skills"]])
        self.assertIn("~/.claude/agents/review.md", [item["path"] for item in report["agents"]])
        self.assertIn(".claude/CLAUDE.md", [item["path"] for item in report["instructions"]])
        self.assertIn(".claude/rules/testing.md", [item["path"] for item in report["instructions"]])
        self.assertNotIn("PRIVATE_", json.dumps(report))

    def test_scan_deterministic_and_read_only(self):
        self.write("package.json", "{}")
        before = sorted(str(path) for path in self.root.rglob("*"))
        first = harness.scan(self.root)
        second = harness.scan(self.root)
        self.assertEqual(first, second)
        self.assertEqual(before, sorted(str(path) for path in self.root.rglob("*")))

    def test_scan_output_only_explicit_artifact_and_no_overwrite(self):
        output = self.base / "report.json"
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(harness.main(["scan", "--project", str(self.root), "--output", str(output)]), 0)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(sorted(self.root.iterdir()), [])
        self.assertEqual(json.loads(output.read_text())["schema_version"], 1)
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(harness.main(["scan", "--project", str(self.root), "--output", str(output)]), 2)

    def test_cli_json_success_error_and_exact_diff(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(harness.main(["scan", "--project", str(self.root)]), 0)
        self.assertEqual(json.loads(out.getvalue())["project"], str(self.root))
        result = self.stage()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(harness.main(["diff", "--bundle", str(self.bundle)]), 0)
        self.assertEqual(out.getvalue(), harness.diff(self.bundle))
        with contextlib.redirect_stderr(err):
            self.assertEqual(harness.main(["apply", "--bundle", str(self.bundle), "--approve", "wrong"]), 2)
        self.assertEqual(json.loads(err.getvalue())["status"], "error")
        self.assertEqual(harness.check(self.bundle)["digest"], result["digest"])

    def test_cli_errors_do_not_echo_untrusted_json(self):
        secret = "SECRET_THAT_MUST_NOT_APPEAR"
        self.plan.write_text('{"bad": ' + secret)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            status = harness.main(["stage", "--project", str(self.root),
                                   "--plan", str(self.plan), "--out", str(self.bundle)])
        self.assertEqual(status, 2)
        self.assertNotIn(secret, err.getvalue())


if __name__ == "__main__":
    unittest.main()
