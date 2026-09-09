"""Independent adversarial regressions, promoted into the permanent test suite.

All mutations use disposable fixtures outside the source tree.
No Claude model calls, remote actions, or generated hook commands are executed.
"""
import base64
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/harness.py"
spec = importlib.util.spec_from_file_location("audited_harness", SCRIPT)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class IndependentAudit(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="harness-independent-review-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.project = self.base / "project with spaces"
        self.project.mkdir()
        self.bundle = self.base / "review bundle"
        self.plan = self.base / "review plan.json"

    def stage(self, changes=None):
        self.plan.write_text(json.dumps({
            "schema_version": 1,
            "rationale": "Independent disposable audit fixture",
            "changes": changes or [
                {"path": "CLAUDE.md", "operation": "managed_block", "value": "Reviewed instructions"}
            ],
        }))
        return h.stage(self.project, self.plan, self.bundle)

    def receipt(self):
        return json.loads((self.bundle / "receipt.json").read_text())

    def test_reject_hook_carrier_in_created_agent(self):
        candidate = (
            "---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
            "tools: Read\nhooks:\n  PreToolUse:\n    - matcher: Read\n"
            "      hooks:\n        - type: command\n"
            "          command: \"printf DO_NOT_EXECUTE_AUDIT_CANARY\"\n"
            "---\nRead-only prose does not neutralize frontmatter.\n"
        )
        with self.assertRaises(h.HarnessError):
            self.stage([{"path": ".claude/agents/audit-only.md", "operation": "create", "value": candidate}])

    def test_reject_model_and_permission_override_in_created_agent(self):
        candidate = (
            "---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
            "model: opus\npermissionMode: bypassPermissions\ntools: Read\n---\nFixture.\n"
        )
        with self.assertRaises(h.HarnessError):
            self.stage([{"path": ".claude/agents/audit-only.md", "operation": "create", "value": candidate}])

    def test_reject_hook_carrier_in_created_skill(self):
        candidate = (
            "---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
            "disable-model-invocation: true\n"
            "hooks:\n  PreToolUse:\n    - matcher: Read\n"
            "      hooks:\n        - type: command\n"
            "          command: \"printf DO_NOT_EXECUTE_AUDIT_CANARY\"\n"
            "---\nFixture.\n"
        )
        with self.assertRaises(h.HarnessError):
            self.stage([{"path": ".claude/skills/audit-only/SKILL.md",
                         "operation": "create", "value": candidate}])
        self.assertFalse(self.bundle.exists())
        self.assertFalse((self.project / ".claude").exists())

    def test_safe_created_skill_agent_and_reference_roundtrip(self):
        skill = ("---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
                 "disable-model-invocation: true\nargument-hint: \"[fixture]\"\n"
                 "---\nReview supplied evidence.\n")
        agent = ("---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
                 "tools: Read, Glob, Grep\n---\nReview supplied evidence.\n")
        changes = [
            {"path": ".claude/skills/audit-only/SKILL.md", "operation": "create", "value": skill},
            {"path": ".claude/agents/audit-only.md", "operation": "create", "value": agent},
            {"path": ".claude/skills/audit-only/references/checks.md",
             "operation": "create", "value": "# Checks\n\nPlain evidence, no runtime invocation.\n"},
        ]
        result = self.stage(changes)
        h.check(self.bundle, self.project)
        h.apply(self.bundle, result["digest"], self.project)
        for change in changes:
            self.assertEqual((self.project / change["path"]).read_text(), change["value"])
        h.rollback(self.bundle, result["digest"], self.project)
        for change in changes:
            self.assertFalse((self.project / change["path"]).exists())

    def test_rehashed_hook_carrier_rejected_by_check_and_apply(self):
        skill = ("---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
                 "disable-model-invocation: true\n---\nReview supplied evidence.\n")
        self.stage([{"path": ".claude/skills/audit-only/SKILL.md",
                     "operation": "create", "value": skill}])
        manifest_path = self.bundle / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        change = manifest["changes"][0]
        change["value"] = skill.replace("\n---\n", "\nhooks: {}\n---\n")
        data = change["value"].encode("utf-8")
        change["postimage"]["content_b64"] = base64.b64encode(data).decode("ascii")
        change["postimage"]["sha256"] = h.sha(data)
        manifest["digest"] = h.candidate_digest(manifest)
        manifest_path.write_bytes(h.canonical(manifest))
        for operation in (
            lambda: h.check(self.bundle, self.project),
            lambda: h.apply(self.bundle, manifest["digest"], self.project),
        ):
            with self.assertRaisesRegex(h.HarnessError, "frontmatter"):
                operation()
        self.assertFalse((self.project / ".claude").exists())
        self.assertFalse((self.bundle / "receipt.json").exists())

    def test_each_forbidden_field_and_yaml_key_variant_rejected(self):
        template = ("---\nname: audit-only\ndescription: \"Fixture, never invoked\"\n"
                    "tools: Read\n{extra}\n---\nReview supplied evidence.\n")
        for extra in (
            "hooks: {}", "model: opus", "permissionMode: bypassPermissions",
            "mcpServers: {}", '"hooks": {}', 'ho\\u006fks: {}',
            "<<: *inherited", "description: \"duplicate\"",
        ):
            with self.subTest(extra=extra):
                with self.assertRaisesRegex(h.HarnessError, "frontmatter"):
                    self.stage([{"path": ".claude/agents/audit-only.md",
                                 "operation": "create", "value": template.format(extra=extra)}])
                self.assertFalse(self.bundle.exists())
                self.assertFalse((self.project / ".claude").exists())

    def test_reject_preexisting_shared_hardlink(self):
        canonical = self.base / "shared-canonical.md"
        canonical.write_text("Shared owner-maintained instructions\n")
        (self.project / "CLAUDE.md").hardlink_to(canonical)
        with self.assertRaises(h.HarnessError):
            self.stage()

    def test_reject_hardlink_added_after_stage(self):
        target = self.project / "CLAUDE.md"
        target.write_text("Owner baseline\n")
        result = self.stage()
        (self.base / "alias-created-after-review.md").hardlink_to(target)
        with self.assertRaises(h.HarnessError):
            h.apply(self.bundle, result["digest"], self.project)

    def test_rollback_rejects_hardlink_added_after_apply(self):
        target = self.project / "CLAUDE.md"
        target.write_text("Owner baseline\n")
        result = self.stage()
        h.apply(self.bundle, result["digest"], self.project)
        canonical = self.base / "shared-after-apply.md"
        canonical.hardlink_to(target)
        applied = target.read_bytes()
        with self.assertRaises(h.HarnessError):
            h.rollback(self.bundle, result["digest"], self.project)
        self.assertEqual(target.read_bytes(), applied)
        self.assertEqual(target.stat().st_ino, canonical.stat().st_ino)

    def test_invalid_second_plan_change_leaves_no_partial_stage_or_project_edits(self):
        target = self.project / "CLAUDE.md"
        target.write_bytes(b"Owner bytes\r\n")
        with self.assertRaises(h.HarnessError):
            self.stage([
                {"path": "CLAUDE.md", "operation": "managed_block", "value": "Candidate"},
                {"path": ".claude/settings.local.json", "operation": "json_merge",
                 "value": {"model": "invalid"}},
            ])
        self.assertEqual(target.read_bytes(), b"Owner bytes\r\n")
        self.assertFalse(self.bundle.exists())
        self.assertFalse((self.project / ".claude").exists())

    def test_receipt_failure_after_first_applied_file_is_compensated(self):
        target = self.project / "CLAUDE.md"
        target.write_bytes(b"Owner bytes\r\n")
        result = self.stage([
            {"path": "CLAUDE.md", "operation": "managed_block", "value": "Candidate"},
            {"path": ".claude/agents/reviewer.md", "operation": "create",
             "value": "---\nname: reviewer\ndescription: \"Review\"\ntools: Read\n---\nReview."},
        ])
        original = h.write_receipt
        calls = 0
        def fail_once(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated disk write failure")
            return original(*args, **kwargs)
        with patch.object(h, "write_receipt", side_effect=fail_once):
            with self.assertRaises(h.HarnessError):
                h.apply(self.bundle, result["digest"], self.project)
        self.assertEqual(target.read_bytes(), b"Owner bytes\r\n")
        self.assertFalse((self.project / ".claude/agents/reviewer.md").exists())
        self.assertEqual(self.receipt()["state"], "apply_reverted")
        self.assertEqual(self.receipt()["pending"], [])

    def test_rollback_receipt_failure_resumes_remaining_paths(self):
        result = self.stage([
            {"path": "CLAUDE.md", "operation": "managed_block", "value": "Candidate"},
            {"path": ".claude/agents/reviewer.md", "operation": "create",
             "value": "---\nname: reviewer\ndescription: \"Review\"\ntools: Read\n---\nReview."},
        ])
        h.apply(self.bundle, result["digest"], self.project)
        original = h.write_receipt
        calls = 0
        def fail_once(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated disk write failure")
            return original(*args, **kwargs)
        with patch.object(h, "write_receipt", side_effect=fail_once):
            with self.assertRaises(h.HarnessError):
                h.rollback(self.bundle, result["digest"], self.project)
        self.assertEqual(self.receipt()["state"], "rollback_failed")
        self.assertEqual(self.receipt()["pending"], ["CLAUDE.md"])
        h.rollback(self.bundle, result["digest"], self.project)
        self.assertFalse((self.project / "CLAUDE.md").exists())
        self.assertFalse((self.project / ".claude/agents/reviewer.md").exists())

    def test_exact_expiry_boundary_is_stale_without_manifest_rewrite(self):
        fixed = h.now()
        with patch.object(h, "now", return_value=fixed):
            result = self.stage()
        with patch.object(h, "now", return_value=fixed + dt.timedelta(hours=24)):
            with self.assertRaisesRegex(h.HarnessError, "expired"):
                h.apply(self.bundle, result["digest"], self.project)
        self.assertFalse((self.project / "CLAUDE.md").exists())

    def test_recomputed_valid_candidate_rejects_old_approval_digest(self):
        result = self.stage()
        manifest_path = self.bundle / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        change = manifest["changes"][0]
        change["value"] = "Different candidate content"
        change["postimage"] = h.postimage(change["path"], change["operation"],
                                         change["value"], change["baseline"])
        manifest["digest"] = h.candidate_digest(manifest)
        manifest_path.write_bytes(h.canonical(manifest))
        with self.assertRaisesRegex(h.HarnessError, "approval"):
            h.apply(self.bundle, result["digest"], self.project)
        self.assertFalse((self.project / "CLAUDE.md").exists())

    def test_deeply_nested_credential_values_are_not_in_scan_or_errors(self):
        token = "sk-audit-FIXTURE-only-9742491"
        target = self.project / ".claude/settings.json"
        target.parent.mkdir()
        target.write_text(json.dumps({
            "env": {"ANTHROPIC_AUTH_TOKEN": token},
            "hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": token}]}]},
            "permissions": {"allow": [f"Bash(curl -H '{token}')"]},
            "extraKnownMarketplaces": {"fixture": {"source": {"url": f"https://u:{token}@example.invalid"}}},
        }))
        (self.project / ".mcp.json").write_text(json.dumps({
            "mcpServers": {"private": {"env": {"TOKEN": token}, "headers": {"Authorization": token}}}
        }))
        self.assertNotIn(token, json.dumps(h.scan(self.project)))
        self.plan.write_text('{"schema_version": 1, "rationale": "' + token + '", invalid')
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "stage", "--project", str(self.project),
             "--plan", str(self.plan), "--out", str(self.bundle)],
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(token, result.stdout + result.stderr)

    def test_documented_cli_flow_works_with_absolute_paths_containing_spaces(self):
        def run(*args):
            return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                                  text=True, capture_output=True, cwd=self.base)
        self.plan.write_bytes((ROOT / "examples/plan.json").read_bytes())
        for command in ("scan", "stage", "check", "diff", "apply", "rollback"):
            self.assertEqual(run(command, "--help").returncode, 0)
        scan = run("scan", "--project", self.project)
        self.assertEqual(scan.returncode, 0)
        staged = run("stage", "--project", self.project, "--plan", self.plan, "--out", self.bundle)
        self.assertEqual(staged.returncode, 0, staged.stderr)
        digest = json.loads(staged.stdout)["digest"]
        checked = run("check", "--bundle", self.bundle, "--project", self.project)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        compared = run("diff", "--bundle", self.bundle)
        self.assertEqual(compared.returncode, 0, compared.stderr)
        self.assertIn("+++ b/CLAUDE.md", compared.stdout)
        applied = run("apply", "--bundle", self.bundle, "--project", self.project, "--approve", digest)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        rolled_back = run("rollback", "--bundle", self.bundle, "--project", self.project, "--approve", digest)
        self.assertEqual(rolled_back.returncode, 0, rolled_back.stderr)
        self.assertFalse((self.project / "CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
