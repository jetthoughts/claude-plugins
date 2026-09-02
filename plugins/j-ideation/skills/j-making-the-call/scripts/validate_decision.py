#!/usr/bin/env python3
"""Validate an 11-decision-record.md against the decision policy.

Usage: validate_decision.py <11-decision-record.md> [--ledger 03-evidence-ledger.jsonl]
Fixture: docs/independent-ideation/examples/fixture-run/11-decision-record.md
Exit 0 = pass, 1 = policy violation, 2 = usage. Stdlib only, no network.
"""
import json, re, sys
from pathlib import Path

VERDICTS = {"GO", "EXPERIMENT", "RESEARCH-MORE", "PIVOT", "STOP"}
LIKELIHOOD = {"almost-no-chance", "very-unlikely", "unlikely", "roughly-even", "likely", "very-likely", "almost-certain"}
CONFIDENCE = {"low", "moderate", "high"}
EID = re.compile(r"\bE-\d{3,}\b")


def frontmatter(text):
    m = re.match(r"^(?:---|\*\*\*)\s*\n(.*?)\n(?:---|\*\*\*)\s*\n", text, re.S)
    fm = {}
    for line in (m.group(1) if m else "").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def section(text, title):
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else None


def table_rows(body):
    rows = []
    for line in (body or "").splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows[1:] if rows else []  # drop header


def main(path: Path, ledger: Path | None) -> int:
    text = path.read_text()
    fm = frontmatter(text)
    errors = []
    verdict = fm.get("verdict", "")
    if verdict not in VERDICTS:
        errors.append(f"verdict {verdict!r} must be exactly one of {sorted(VERDICTS)}")
    tiers = {}
    if ledger and ledger.exists():
        for line in ledger.read_text().splitlines():
            if line.strip():
                e = json.loads(line); tiers[e["evidence_id"]] = e.get("source_tier")
    for sec in ("Evidence for", "Evidence against"):
        body = section(text, sec)
        ids = EID.findall(body or "")
        if not ids:
            errors.append(f"'## {sec}' must cite at least one evidence ID")
        for i in ids:
            if tiers and i not in tiers:
                errors.append(f"'## {sec}' cites {i} which is not in the ledger")
    council = section(text, "Council distribution") or ""
    if not re.search(r"dissent", council, re.I) or not re.search(r"\d", council):
        errors.append("'## Council distribution' must report numbers and the preserved dissent (or state 'no council convened: <reason>' with dissent = none)")
    for row in table_rows(section(text, "Key uncertainties")):
        if len(row) >= 3 and (row[1].lower() not in LIKELIHOOD or row[2].lower() not in CONFIDENCE):
            errors.append(f"key uncertainty {row[0]!r}: likelihood/confidence must use the allowed words, separately")
    kill = table_rows(section(text, "Pre-mortem and kill criteria"))
    good = [r for r in kill if len(r) >= 6 and all(r[:6]) and re.search(r"\d{4}-\d{2}-\d{2}", r[3])]
    if not good:
        errors.append("kill criteria need >=1 table row with signal, metric, threshold, date (YYYY-MM-DD), owner, action")
    rev = fm.get("reversibility", "")
    approval = fm.get("human_approval", "")
    if rev == "type-1" and approval not in ("required", "approved"):
        errors.append("type-1 decision must set human_approval: required|approved")
    if fm.get("status") in ("approved", "testing") and rev == "type-1" and not fm.get("approved_by"):
        errors.append("type-1 decision in approved/testing status needs approved_by")
    if not (section(text, "Human approval required") or "").strip():
        errors.append("'## Human approval required' must not be empty")
    if verdict == "GO":
        for_ids = EID.findall(section(text, "Evidence for") or "")
        if tiers and not any(tiers.get(i) in ("T1", "T2") for i in for_ids):
            errors.append("GO requires at least one T1/T2 evidence item in 'Evidence for'")
        for row in table_rows(section(text, "Critical assumptions")):
            if len(row) >= 3 and "unresolved" in row[1].lower() and row[2].lower().startswith("y"):
                errors.append(f"GO with unresolved fatal assumption {row[0]!r}")
        if fm.get("status") != "approved" or not fm.get("approved_by"):
            errors.append("GO requires status: approved and approved_by set by the human decider")
    for e in errors: print("ERROR", e)
    print(f"decision: verdict={verdict or '?'} reversibility={rev or '?'} {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); sys.exit(2)
    led = Path(a[a.index("--ledger") + 1]) if "--ledger" in a else None
    sys.exit(main(Path(a[0]), led))
