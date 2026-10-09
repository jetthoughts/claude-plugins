#!/usr/bin/env python3
"""Test preflight_skills helper.

Run with:
  python3 plugins/hermes-bos/skills/bos-intake/scripts/test_preflight_skills.py
Exit 0 on PASS, 1 on FAIL. No third-party deps.

This file follows the project's house rule 1 (test first) for the
bos-intake preflight hook (composite-experiment card t_ca1713f3).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import preflight_skills  # noqa: E402


class PreflightSkillTests(unittest.TestCase):
    """Capture both metric branches (Pass metric 1 in card t_ca1713f3)."""

    def test_namespaced_form_unresolved(self) -> None:
        """`hermes-bos/skills/bos-intake` must be reported as unknown when
        the resolver cannot reach the plugins root.

        Reproduces the worker-side baseline from card t_ca1713f3: a profile
        without the `skills:` block has `external_dirs = []`, no project
        root is in scope (worker cwd is its own profile home, not the
        claude-plugins checkout), so the namespaced form resolves to
        nothing. The preflight helper must surface that, not invent a path.
        """
        import unittest.mock
        import os
        from agent import skill_utils as su

        # The tmp config has no `skills:` block — same shape as the
        # pre-fix soul-curator / growth-operator configs.
        cfg = Path(self._write_no_skills_config(self.tmp_config_path))
        cwd_state = os.getcwd()
        try:
            os.chdir("/tmp")  # no project root, no skills walks
            with unittest.mock.patch.object(su, "get_config_path", create=True, new=lambda: cfg):
                su._EXTERNAL_DIRS_CACHE.clear() if hasattr(su, "_EXTERNAL_DIRS_CACHE") else None
                su._RAW_CONFIG_CACHE.clear() if hasattr(su, "_RAW_CONFIG_CACHE") else None
                bad = preflight_skills.missing(["hermes-bos/skills/bos-intake"])
        finally:
            os.chdir(cwd_state)
        self.assertIn(
            "hermes-bos/skills/bos-intake",
            bad,
            f"namespaced identifier must be missing when external_dirs is empty and cwd has no project root (got {bad!r})",
        )

    def setUp(self) -> None:
        import tempfile
        self.tmp_config_path = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False).name

    def tearDown(self) -> None:
        try:
            os.unlink(self.tmp_config_path)
        except OSError:
            pass

    @staticmethod
    def _write_no_skills_config(path: str) -> str:
        Path(path).write_text(
            "plane:\n  command: uvx\n  args: ['plane-mcp-server','stdio']\n"
            "  env:\n    PLANE_API_KEY: x\n    PLANE_WORKSPACE_SLUG: jetthoughts\n"
            "enabled: true\n"
            "_config_version: 50\n"
            "kanban:\n  auto_decompose: false\n  failure_limit: 3\n"
            "approvals:\n  deny: ['rm *']\n"
        )
        return path

    def test_message_matches_runtime_wording(self) -> None:
        """The rejection message must use the same `Unknown skill(s): ...` line
        runtime skill_commands.format_missing_skills emits, so a worker that
        eventually runs sees the same surface."""
        msg = preflight_skills.format_rejection(["hermes-bos/skills/bos-intake"])
        self.assertIn(
            "Unknown skill(s): hermes-bos/skills/bos-intake",
            msg,
            f"rejection message must mirror the runtime wording; got {msg!r}",
        )

    def test_no_skills_returns_empty(self) -> None:
        """An empty skill list is a no-op (no missing)."""
        self.assertEqual(preflight_skills.missing([], env=os.environ.copy()), [])

    def test_bos_intake_skill_md_carries_preflight_clause(self) -> None:
        """Backstop guard: bos-intake/SKILL.md must carry the step 5a
        procedure clause verbatim. This is the rubric Check 5 replay guard
        for INC-2026100902: if a future edit removes or silently rewrites
        the procedure, this test fails and the durable backstop is broken.

        Required phrases (each must appear somewhere in the file):

        - "Skills preflight (REQUIRED GATE)" — the step heading.
        - "non-optional" — the duration clause.
        - "preflight_skills.py <id1>" — the helper command shape.
        - "Unknown skill(s): <id>" — the worker-mirrored rejection line.
        - "t_bacc26a7" — the incident lineage pointer (linking back to the
          original failure that this guard prevents from recurring).
        """
        skill_md = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text()
        required = [
            "Skills preflight (REQUIRED GATE)",
            "non-optional",
            "preflight_skills.py <id1>",
            "Unknown skill(s): <id>",
            "t_bacc26a7",
        ]
        missing = [r for r in required if r not in skill_md]
        self.assertEqual(
            missing,
            [],
            (
                "bos-intake/SKILL.md procedure clause is missing the required "
                f"phrases: {missing}. The required-gate wording is the durable "
                "backstop for INC-2026100902 (t_bacc26a7 namespaced-skill "
                "resolution). Restore the clauses; do not reword silently."
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
