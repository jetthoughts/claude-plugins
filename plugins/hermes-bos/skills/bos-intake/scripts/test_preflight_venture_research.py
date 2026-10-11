#!/usr/bin/env python3
"""Test preflight_venture_research helper (Rock 5.1 — venture research cards).

Run with:
  python3.11 plugins/hermes-bos/skills/bos-intake/scripts/test_preflight_venture_research.py
Exit 0 on PASS, 1 on FAIL. No third-party deps.

This file follows house rule 1 (test first) for the bos-intake venture-research
preflight hook (kanban t_41ee06a4; rock 5.1 — Research ventures only with a
forcing party and a date; Paul preference memory
`viking://user/default/memories/preferences/Paul/venture_operating_rules.md`).

The contract: any card with `venture_research: true` in its frontmatter MUST
also carry `forcing_party`, `forcing_date`, and `pain_fit`. The orchestrator
runs `preflight_venture_research.check(card)` before `kanban_create` and the
gate refuses the card with a one-line error if any field is missing or empty.

Field sources accepted (in order, first non-empty wins):
  - card frontmatter (parsed by `parse_frontmatter`)
  - card body lines (`Forcing party:`, `Date:`, `Pain fit:`) — convenience for
    operators who paste prose instead of YAML

`pain_fit` is the buyer-pain fit per JT rule #2 (sufferer = chequebook holder);
the gate enforces presence + non-empty string, not a rubric score.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import preflight_venture_research as pvr  # noqa: E402


VALID_FRONTMATTER = """---
venture_research: true
forcing_party: EU AI Act enforcement (auditor)
forcing_date: 2026-08-02
pain_fit: "Audit fees payable by the audited entity, not the auditor"
---
# Test
"""

VALID_BODY = """# Card body
Forcing party: EU AI Act enforcement (auditor)
Date: 2026-08-02
Pain fit: Audit fees payable by the audited entity, not the auditor
"""

MISSING_FIELD_BODY = """---
venture_research: true
forcing_party: EU AI Act enforcement (auditor)
pain_fit: Audit fees payable by the audited entity
---
"""

NON_VENTURE_BODY = """---
venture_research: false
---
"""


class PreflightVentureResearchTests(unittest.TestCase):
    def test_parse_frontmatter_basic(self) -> None:
        fm = pvr.parse_frontmatter(VALID_FRONTMATTER)
        self.assertEqual(fm.get("venture_research"), True)
        self.assertEqual(fm.get("forcing_party"), "EU AI Act enforcement (auditor)")
        self.assertEqual(fm.get("forcing_date"), "2026-08-02")
        self.assertEqual(fm.get("pain_fit"), "Audit fees payable by the audited entity, not the auditor")

    def test_check_passes_full_frontmatter(self) -> None:
        """Happy path: all three fields present in frontmatter."""
        missing = pvr.check(VALID_FRONTMATTER)
        self.assertEqual(missing, [], f"expected no missing fields, got {missing}")

    def test_check_passes_body_lines(self) -> None:
        """Operator pastes prose; the gate reads body lines."""
        missing = pvr.check(VALID_BODY)
        self.assertEqual(missing, [], f"expected body lines to satisfy gate, got {missing}")

    def test_check_fails_when_field_missing(self) -> None:
        """RED → GREEN: missing `forcing_date` must be reported."""
        missing = pvr.check(MISSING_FIELD_BODY)
        self.assertIn("forcing_date", missing, f"expected forcing_date in missing, got {missing}")

    def test_check_skips_non_venture_cards(self) -> None:
        """Cards without `venture_research: true` are not gated."""
        missing = pvr.check(NON_VENTURE_BODY)
        self.assertEqual(missing, [])

    def test_check_fails_when_venture_marker_present_but_all_fields_missing(self) -> None:
        body = "---\nventure_research: true\n---\n"
        missing = pvr.check(body)
        self.assertEqual(
            set(missing),
            {"forcing_party", "forcing_date", "pain_fit"},
            f"expected all three fields reported, got {missing}",
        )

    def test_format_rejection_uses_canonical_line(self) -> None:
        """Rejection wording must mirror a single line the orchestrator can paste
        back to the operator without parsing prose."""
        msg = pvr.format_rejection(["forcing_party", "pain_fit"])
        self.assertIn("forcing_party", msg)
        self.assertIn("pain_fit", msg)
        # one-liner for chat-paste
        self.assertNotIn("\n", msg.rstrip("\n"))

    def test_check_treats_empty_string_as_missing(self) -> None:
        body = "---\nventure_research: true\nforcing_party: ''\nforcing_date: 2026-08-02\npain_fit: ok\n---\n"
        missing = pvr.check(body)
        self.assertIn("forcing_party", missing, f"empty string must count as missing, got {missing}")

    def test_bos_intake_skill_md_carries_venture_research_preflight_clause(self) -> None:
        """Backstop guard: bos-intake/SKILL.md must carry the step 5b
        procedure clause verbatim. This is the rubric Check 5 replay guard
        for kanban t_41ee06a4 / rock 5.1: if a future edit removes or
        silently rewrites the procedure, this test fails and the durable
        backstop is broken.

        Required phrases (each must appear somewhere in the file):

        - "Venture research preflight (REQUIRED GATE)" — the step heading.
        - "non-optional" — the duration clause.
        - "preflight_venture_research.py" — the helper command shape.
        - "venture research preflight: missing field(s)" — the rejection line.
        - "t_41ee06a4" — the kanban card lineage pointer.
        """
        skill_md = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text()
        required = [
            "Venture research preflight (REQUIRED GATE)",
            "non-optional",
            "preflight_venture_research.py",
            "venture research preflight: missing field(s)",
            "t_41ee06a4",
        ]
        missing = [r for r in required if r not in skill_md]
        self.assertEqual(
            missing,
            [],
            (
                "bos-intake/SKILL.md procedure clause is missing the required "
                f"phrases: {missing}. The required-gate wording is the durable "
                "backstop for rock 5.1 / kanban t_41ee06a4. Restore the clauses; "
                "do not reword silently."
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)