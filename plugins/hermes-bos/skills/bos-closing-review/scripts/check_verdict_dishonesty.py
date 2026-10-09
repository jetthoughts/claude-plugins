#!/usr/bin/env python3
"""bos-closing-review verdict-dishonesty verifier.

Reads a verdict file (or '-' for stdin); exits 0 (clean) or 1
(PASS-with-gap dishonesty) with per-row diagnostics on stdout.

Trigger: a line `**Verdict: PASS**` (anchored to start of line) AND a
Markdown table row whose `status` column contains one of {gap,
partial-pass, fail-uncertain, hedge}.
"""
import re
import sys
from pathlib import Path

VERDICT_RE = re.compile(r"^\s*\*\*\s*verdict\s*:\s*pass\s*\*\*",
                       re.IGNORECASE | re.MULTILINE)
ROW_RE = re.compile(r"^\|(.+)\|\s*$")
STATUS_RE = re.compile(r"(?i)\b(?:gap|partial-pass|fail-uncertain|hedge)\b")


def read_input(target):
    if target == "-":
        return "<stdin>", sys.stdin.read()
    p = Path(target)
    if not p.exists():
        print(f"ERROR: file not found: {target}", file=sys.stderr)
        sys.exit(2)
    return str(p), p.read_text()


def gap_rows(text):
    """Return (line_no, criterion_id, status) for each table row whose
    status cell contains a gap marker. status column is detected from
    the first table header that has it; falls back to column 1.
    """
    out, col = [], None
    for i, line in enumerate(text.splitlines(), start=1):
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if col is None:
            lowered = [c.lower() for c in cells]
            if "status" in lowered:
                col = lowered.index("status")
            else:
                col = 1
        if col >= len(cells):
            continue
        sm = STATUS_RE.search(cells[col])
        if sm:
            out.append((i, cells[0], sm.group(0).lower()))
    return out


def main():
    if len(sys.argv) != 2:
        print("usage: check_verdict_dishonesty.py <file|->", file=sys.stderr)
        return 2
    label, text = read_input(sys.argv[1])
    if not VERDICT_RE.search(text):
        print(f"PASS: {label} — no PASS verdict headline, nothing to gate")
        return 0
    rows = gap_rows(text)
    if not rows:
        print(f"PASS: {label} — verdict PASS, all rows clean")
        return 0
    print(f"FAIL: {label} — verdict PASS but {len(rows)} row(s) report "
          f"a gap; PASS-not-permitted")
    for lineno, crit, status in rows:
        print(f"  - {label}:{lineno} [{crit or '?'}] status={status} — "
              f"PASS-with-gap is INCONCLUSIVE per recipe 0 + closing-review "
              f"rubric step 3")
    return 1


if __name__ == "__main__":
    sys.exit(main())
