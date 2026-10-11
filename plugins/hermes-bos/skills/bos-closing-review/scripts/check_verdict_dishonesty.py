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

VERDICT_RE = re.compile(r"^\s*\*+(?:verdict\s*:?\s*)?\*?\s*pass(?:\s*\((?:\d+/\d+|[^)]*)\))?\s*\.?\s*\*+",
                       re.IGNORECASE | re.MULTILINE)
ROW_RE = re.compile(r"^\|(.+)\|\s*$")
STATUS_RE = re.compile(r"(?i)\b(?:gap|partial-pass|fail-uncertain|hedge|open-behind-hardstop|open-behind-block)\b")
# Prose-narrative gap markers: a verdict PASS headline plus any of these phrases
# in the verdict file's prose body indicates the closure is a substitution,
# not an honest closure. Recipes that produced this defect: 0 (PASS-with-gap).
NARRATIVE_RE = re.compile(
    r"(?i)\b(?:"
    r"remains\s+open(?:\s+behind)?|"
    r"metric\s+(?:remains\s+)?(?:open|unmet)|"
    r"contract\s+(?:text\s+)?(?:is\s+|does\s+not\s+|doesn'?t\s+|does\s+not\s+)?(?:satisfy|satisfies|close(?:s)?|meet(?:s)?)|"
    r"open-behind-(?:hardstop|hard-stop|block)|"
    r"path\s*\(?b\)?.*(?:blocked|hardstop|hard-stop)|"
    r"do(?:es)?\s+not\s+(?:close|satisfy|meet)\s+(?:the\s+)?runtime|"
    r"runtime-?enforcement\s+metric"
    r")\b"
)


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


def narrative_gaps(text):
    """Return (line_no, phrase) for each prose line containing a
    substitution-pattern phrase. This catches the recipe-0 PASS-with-gap
    defect where the table cells are all 'PASS' but the prose narrative
    says the original metric remains open / contract is not runtime.
    """
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        # Skip table lines (already covered by gap_rows) and verdict
        # headline lines (the PASS announcement itself).
        if ROW_RE.match(line):
            continue
        m = NARRATIVE_RE.search(line)
        if m:
            out.append((i, m.group(0)))
    return out


def has_override(text):
    """Return True if the file contains an explicit OVERRIDE comment of the
    form `OVERRIDE: verdict-with-gap approved by <role> at <iso>` AND the
    override is a real approval line (not a documentation reference inside
    backticks/code). Heuristic: real approvals appear on their own line at
    the start of a sentence, not nested in ` ` code spans. Documentation
    matches will contain `<role>` and `<iso>` literal placeholder text.
    """
    for m in re.finditer(
        r"^\s*OVERRIDE\s*:\s*verdict-with-gap\s+approved\s+by\s+(\S+)\s+at\s+(\S+)",
        text, re.IGNORECASE | re.MULTILINE,
    ):
        role, when = m.group(1), m.group(2)
        # Real approvals use a real role + ISO timestamp, not placeholder
        # text like `<role>` / `<iso>`. Reject literal angle-bracket placeholders.
        if role.startswith("<") or role.endswith(">") or role == "<role>":
            return False
        if when.startswith("<") or when.endswith(">") or when == "<iso>":
            return False
        return True
    return False


def main():
    if len(sys.argv) != 2:
        print("usage: check_verdict_dishonesty.py <file|->", file=sys.stderr)
        return 2
    label, text = read_input(sys.argv[1])
    if not VERDICT_RE.search(text):
        print(f"PASS: {label} — no PASS verdict headline, nothing to gate")
        return 0
    rows = gap_rows(text)
    narr = narrative_gaps(text)
    if not rows and not narr:
        print(f"PASS: {label} — verdict PASS, all rows clean")
        return 0
    if has_override(text):
        print(f"PASS: {label} — verdict PASS with {len(rows)} row-gap(s) "
              f"+ {len(narr)} narrative-gap(s); OVERRIDE comment present, "
              f"approved by role")
        return 0
    total = len(rows) + len(narr)
    parts = []
    if rows:
        parts.append(f"{len(rows)} row(s) report a gap")
    if narr:
        parts.append(f"{len(narr)} prose line(s) carry substitution-pattern "
                     f"phrases")
    print(f"FAIL: {label} — verdict PASS but {' / '.join(parts)}; "
          f"PASS-not-permitted")
    for lineno, crit, status in rows:
        print(f"  - {label}:{lineno} [{crit or '?'}] status={status} — "
              f"PASS-with-gap is INCONCLUSIVE per recipe 0 + closing-review "
              f"rubric step 3")
    for lineno, phrase in narr:
        print(f"  - {label}:{lineno} phrase={phrase!r} — "
              f"PASS-with-prose-gap is INCONCLUSIVE per recipe 0 "
              f"(PASS-on-open-metric is the recurring defect)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
