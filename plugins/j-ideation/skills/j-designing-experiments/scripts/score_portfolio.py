#!/usr/bin/env python3
"""Score an experiment portfolio: Experiment Priority, evidence-capped RICE, ranges.

Usage: score_portfolio.py <cards.json | 10-experiment-portfolio.md>
A .md input contributes every ```json block (list of cards or one card).
Writes <input>.scores.json next to the input.
Fixture: docs/independent-ideation/examples/fixture-run/10-experiment-portfolio.md
Exit 0 = ok, 1 = invalid cards, 2 = usage. Stdlib only.

Priority = (EIG × decision_importance) / ((cost+1)(duration+1)(effort+1))
RICE     = (reach × impact × confidence) / effort, confidence capped by evidence_basis.
"""
import json, re, sys
from pathlib import Path

CEILING = {"model-consensus": 0.30, "anecdote": 0.40, "customer-signals": 0.60,
           "prototype": 0.75, "behavioral": 0.85, "paid": 1.00}
REQUIRED = ["experiment_id", "hypothesis", "falsification_condition", "method", "primary_metric",
            "success_threshold", "failure_threshold", "inconclusive_rule", "duration_days",
            "budget_eur", "effort_person_days", "owner", "next_if_pass", "next_if_fail", "next_if_inconclusive",
            "expected_information_gain", "decision_importance", "evidence_basis"]


def rng(v):
    if isinstance(v, (list, tuple)) and len(v) == 2:
        return float(v[0]), float(v[1])
    return float(v), float(v)


def load(p: Path):
    text = p.read_text()
    blocks = re.findall(r"```json\s*(.*?)```", text, re.S) if p.suffix == ".md" else [text]
    cards = []
    for b in blocks:
        d = json.loads(b)
        cards.extend(d if isinstance(d, list) else [d])
    return cards


def score(c):
    eig, di = rng(c["expected_information_gain"]), rng(c["decision_importance"])
    cost, dur, eff = rng(c["budget_eur"]), rng(c["duration_days"]), rng(c["effort_person_days"])
    lo = eig[0] * di[0] / ((cost[1] + 1) * (dur[1] + 1) * (eff[1] + 1))
    hi = eig[1] * di[1] / ((cost[0] + 1) * (dur[0] + 1) * (eff[0] + 1))
    out = {"experiment_id": c["experiment_id"], "priority": [round(lo, 5), round(hi, 5)],
           "priority_mid": round((lo + hi) / 2, 5), "evidence_basis": c["evidence_basis"],
           "requires_human_approval": bool(c.get("requires_human_approval")), "notes": []}
    if all(k in c for k in ("reach", "impact", "confidence")):
        cap = CEILING[c["evidence_basis"]]
        conf = rng(c["confidence"])
        if conf[1] > cap:
            out["notes"].append(f"confidence {conf} capped at {cap} ({c['evidence_basis']})")
            conf = (min(conf[0], cap), min(conf[1], cap))
        r, i = rng(c["reach"]), rng(c["impact"])
        out["rice"] = [round(r[0] * i[0] * conf[0] / max(eff[1], 0.01), 3), round(r[1] * i[1] * conf[1] / max(eff[0], 0.01), 3)]
        out["rice_group"] = c.get("outcome_group") or c.get("decision_id") or "ungrouped"
    return out


def main(p: Path) -> int:
    cards = load(p)
    errors = []
    for c in cards:
        for k in REQUIRED:
            if k not in c or c[k] in ("", None, []):
                errors.append(f"{c.get('experiment_id', '?')}: missing {k}")
        if c.get("evidence_basis") not in CEILING:
            errors.append(f"{c.get('experiment_id', '?')}: evidence_basis must be one of {sorted(CEILING)}")
    if errors:
        for e in errors: print("ERROR", e)
        return 1
    rows = sorted((score(c) for c in cards), key=lambda r: -r["priority_mid"])
    groups = {}
    for r in rows:
        if "rice" in r:
            groups.setdefault(r["rice_group"], []).append(r["experiment_id"])
    for r in rows:
        if "rice" in r and len(groups[r["rice_group"]]) < 2:
            r["notes"].append("RICE shown without a same-outcome comparator")
    print(f"{'experiment':<14} {'priority lo-hi':<22} {'RICE lo-hi':<18} approval  notes")
    for r in rows:
        rice = f"{r['rice'][0]}-{r['rice'][1]}" if "rice" in r else "-"
        print(f"{r['experiment_id']:<14} {r['priority'][0]}-{r['priority'][1]:<12} {rice:<18} {'HUMAN' if r['requires_human_approval'] else 'auto':<9} {'; '.join(r['notes'])}")
    out = p.with_suffix(p.suffix + ".scores.json")
    out.write_text(json.dumps({"ranked": rows, "run_now": rows[0]["experiment_id"], "contingency": rows[1]["experiment_id"] if len(rows) > 1 else None}, indent=2))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(2)
    sys.exit(main(Path(sys.argv[1])))
