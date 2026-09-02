#!/usr/bin/env python3
"""Validate an Independent Ideation evidence ledger and the claims that cite it.

Usage: validate_evidence.py <workspace_dir>
Fixture: docs/independent-ideation/examples/fixture-run
Exit 0 = pass (warnings allowed), 1 = errors, 2 = usage. No network, stdlib only.
"""
import json, re, sys
from pathlib import Path

CLAIM_TYPES = {"FACT", "INFERENCE", "ASSUMPTION", "ESTIMATE", "CONTRADICTION", "UNKNOWN"}
TIERS = {"T1", "T2", "T3", "T4"}
LIKELIHOOD = {"almost-no-chance", "very-unlikely", "unlikely", "roughly-even", "likely", "very-likely", "almost-certain"}
CONFIDENCE = {"low", "moderate", "high"}
EID = re.compile(r"\bE-\d{3,}\b")
MD_WITH_CLAIMS = ["00-decision-brief.md", "06-opportunity-tree.md", "08-assumption-map.md", "11-decision-record.md"]


def main(ws: Path) -> int:
    errors, warns = [], []
    ledger_path = ws / "03-evidence-ledger.jsonl"
    if not ledger_path.exists():
        print(f"ERROR missing {ledger_path}"); return 1
    ledger, ids = [], set()
    for n, line in enumerate(ledger_path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError as ex:
            errors.append(f"ledger line {n}: invalid JSON ({ex})"); continue
        eid = e.get("evidence_id", "")
        if not EID.fullmatch(eid or ""):
            errors.append(f"ledger line {n}: bad evidence_id {eid!r}")
        if eid in ids:
            errors.append(f"ledger line {n}: duplicate {eid}")
        ids.add(eid)
        if e.get("claim_type") not in CLAIM_TYPES:
            errors.append(f"{eid}: claim_type must be one of {sorted(CLAIM_TYPES)}")
        if e.get("source_tier") not in TIERS:
            errors.append(f"{eid}: source_tier must be one of {sorted(TIERS)}")
        if e.get("claim_type") == "FACT" and not e.get("source_url_or_path"):
            errors.append(f"{eid}: FACT without source_url_or_path")
        ledger.append(e)

    # contradiction register
    reg = ws / "04-contradiction-register.md"
    if not reg.exists():
        errors.append("missing 04-contradiction-register.md (must exist even if empty)")
    else:
        rows = [l for l in reg.read_text().splitlines() if re.match(r"\|\s*C-\d+", l)]
        contradictions = len(rows) + sum(1 for e in ledger if e.get("claim_type") == "CONTRADICTION")
        if len(ledger) > 15 and contradictions == 0:
            warns.append(f"{len(ledger)} sources but no contradiction recorded — research may be too narrow")

    # claims in markdown must cite evidence; likelihood/confidence must be separate
    md_files = [ws / f for f in MD_WITH_CLAIMS] + sorted((ws / "07-concepts").glob("*.md"))
    cited = set()
    for f in md_files:
        if not f.exists():
            continue
        for n, line in enumerate(f.read_text().splitlines(), 1):
            cited.update(EID.findall(line))
            if re.search(r"(^|[\s\-*|])FACT\b", line) and not EID.search(line):
                errors.append(f"{f.name}:{n}: FACT without evidence ID")
            m = re.search(r"likelihood\s*[:=]\s*`?([\w.-]+)", line, re.I)
            if m and m.group(1).lower() not in LIKELIHOOD:
                errors.append(f"{f.name}:{n}: likelihood {m.group(1)!r} not in allowed set")
            m = re.search(r"confidence\s*[:=]\s*`?([\w.-]+)", line, re.I)
            if m and m.group(1).lower() not in CONFIDENCE:
                errors.append(f"{f.name}:{n}: confidence {m.group(1)!r} must be low|moderate|high, not a number")
        if f.name == "11-decision-record.md":
            for sec in ("Evidence for", "Evidence against"):
                body = section(f.read_text(), sec)
                if body is not None and not EID.search(body):
                    errors.append(f"11-decision-record.md: '## {sec}' cites no evidence ID")
        if f.parent.name == "07-concepts" and f.name != "concept-map.md":
            body = section(f.read_text(), "Evidence used")
            if body is not None and not EID.search(body):
                errors.append(f"{f.name}: '## Evidence used' cites no evidence ID")
    for d in sorted(cited - ids):
        errors.append(f"dangling reference {d}: not in ledger")

    # T3/T4-only conclusions
    tiers_by_target = {}
    for e in ledger:
        for t in e.get("supports", []):
            tiers_by_target.setdefault(t, set()).add(e.get("source_tier"))
    for t, tiers in sorted(tiers_by_target.items()):
        if tiers and tiers <= {"T3", "T4"}:
            warns.append(f"T3/T4-only support for {t!r} — cannot claim high confidence")

    for w in warns: print("WARN ", w)
    for e in errors: print("ERROR", e)
    print(f"evidence: {len(ledger)} items, {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


def section(text: str, title: str):
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(2)
    sys.exit(main(Path(sys.argv[1])))
