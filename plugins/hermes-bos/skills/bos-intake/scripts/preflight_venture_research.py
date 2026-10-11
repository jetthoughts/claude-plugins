#!/usr/bin/env python3
"""Preflight: validate that a venture-research kanban card carries the three
mandatory fields before it lands in `ready`.

Why: without a forcing party + date + pain fit, venture research burns
runway. The owner's standing rule (rock 5.1; preference memory
`viking://user/default/memories/preferences/Paul/venture_operating_rules.md`):
"Every opportunity must have a named forcing party and a specific date. No
forcing party = no research." The companion rule (chequebook = sufferer) is
captured here as `pain_fit`. The gate refuses the card with a single-line
rejection the orchestrator can paste back to the operator.

Usage:

    from preflight_venture_research import check, format_rejection

    missing = check(card_body)
    if missing:
        raise ValueError(format_rejection(missing))

Cards without `venture_research: true` are NOT gated — they pass through.
The marker is opt-in to keep non-venture work unaffected; the orchestrator
sets it on any card the operator or upstream skill identifies as
venture-shaped (opportunity one-pager, experiment brief, outreach draft for
a new venture, weekly-opportunity-scan leaf, etc.).
"""
from __future__ import annotations

import re
import sys
from typing import Dict, List, Optional


REQUIRED_FIELDS = ("forcing_party", "forcing_date", "pain_fit")
REJECTION_PREFIX = "venture research preflight: missing field(s) "

_FRONTMATTER_RE = re.compile(r"^---\s*\n(?P<body>.*?)\n---\s*\n?", re.DOTALL)


def parse_frontmatter(card_text: str) -> Dict[str, object]:
    """Minimal YAML-ish frontmatter parser — quotes, booleans, and bare scalars.

    We deliberately do not depend on PyYAML. The venture-research card bodies
    only carry a handful of small fields, so a tiny parser is enough; if a card
    ever needs richer YAML, the orchestrator should ship a full parser as a
    helper, not extend this one.
    """
    match = _FRONTMATTER_RE.match(card_text)
    if not match:
        return {}
    body = match.group("body")
    out: Dict[str, object] = {}
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.lower() in ("true", "false"):
            out[key] = value.lower() == "true"
        elif value.startswith('"') and value.endswith('"'):
            out[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            out[key] = value[1:-1]
        else:
            out[key] = value
    return out


def _body_field(card_text: str, label: str) -> Optional[str]:
    """Find a `Label: value` line in the body (post-frontmatter)."""
    match = _FRONTMATTER_RE.match(card_text)
    body = card_text[match.end():] if match else card_text
    pattern = re.compile(rf"(?im)^[\-\s]*{re.escape(label)}\s*:\s*(.+)$")
    found = pattern.search(body)
    if found:
        v = found.group(1).strip().strip('"').strip("'")
        return v or None
    return None


def _is_present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return False  # bool counts as "not a string" for required fields
    if isinstance(value, str) and not value.strip():
        return False
    return True


def check(card_text: str) -> List[str]:
    """Return the list of required fields that are missing or empty.

    Empty list = card passes. Non-empty list = card must be fixed before
    `kanban_create`. The gate is opt-in: cards without `venture_research:
    true` always return `[]`.
    """
    frontmatter = parse_frontmatter(card_text)
    if not frontmatter.get("venture_research"):
        return []
    missing: List[str] = []
    for field in REQUIRED_FIELDS:
        value = frontmatter.get(field)
        if not _is_present(value):
            body_value = _body_field(card_text, field.replace("_", " ").title())
            if _is_present(body_value):
                continue
            missing.append(field)
    return missing


def format_rejection(missing_fields: List[str]) -> str:
    """Single-line rejection the orchestrator can paste back to the operator."""
    if not missing_fields:
        return ""
    return REJECTION_PREFIX + ", ".join(missing_fields)


if __name__ == "__main__":  # pragma: no cover — manual smoke probe
    argv = sys.argv[1]
    if argv == "--self-test":
        # Minimal smoke: every required field missing → all three names in output.
        body = "---\nventure_research: true\n---\n"
        miss = check(body)
        assert set(miss) == set(REQUIRED_FIELDS), f"unexpected missing: {miss}"
        print(format_rejection(miss))
        sys.exit(0)
    text = sys.stdin.read() if not sys.stdin.isatty() else argv
    miss = check(text)
    if miss:
        print(format_rejection(miss))
        sys.exit(2)
    print("OK: venture research preflight passed")
    sys.exit(0)