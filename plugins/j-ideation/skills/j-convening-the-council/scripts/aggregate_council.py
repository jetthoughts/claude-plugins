#!/usr/bin/env python3
"""Aggregate Delphi council reviews without manufacturing convergence.

Usage: aggregate_council.py <09-council dir>
Reads round-1/*.md and round-3/*.md; each file carries one ```json block (see
templates/council-review.md). Writes <dir>/consensus-summary.json.
Fixture: docs/independent-ideation/examples/fixture-run/09-council
Exit 0 = ok, 1 = no valid round-1 reviews or malformed input, 2 = usage. Stdlib only.
"""
import json, re, statistics, sys
from pathlib import Path

REVERSED = {"downside_risk"}
CRITERIA = ["customer_value", "evidence_strength", "revenue_potential", "reachability",
            "strategic_fit", "delivery_repeatability", "feasibility", "downside_risk"]
JSON_BLOCK = re.compile(r"```json\s*(.*?)```", re.S)


def load_reviews(d: Path):
    out = []
    for f in sorted(d.glob("*.md")) + sorted(d.glob("*.json")):
        text = f.read_text()
        m = JSON_BLOCK.search(text) if f.suffix == ".md" else None
        try:
            r = json.loads(m.group(1) if m else text)
        except (json.JSONDecodeError, AttributeError):
            print(f"WARN  {f}: no parseable JSON block — discarded"); continue
        r["_file"] = f.name
        out.append(r)
    return out


def clean(r):
    """Drop evidence-free scores. Return (valid_scores, flags)."""
    flags, valid = [], {}
    scores = r.get("scores") or {}
    if not scores:
        return {}, ["refused or empty review"]
    for concept, crit in scores.items():
        for c, v in (crit or {}).items():
            if not isinstance(v, dict) or not v.get("evidence"):
                flags.append(f"{concept}.{c}: score without evidence — excluded"); continue
            s = v.get("score")
            if not isinstance(s, (int, float)) or not 0 <= s <= 5:
                flags.append(f"{concept}.{c}: score {s!r} out of 0-5 — excluded"); continue
            valid.setdefault(concept, {})[c] = float(s)
    if not valid:
        flags.append("evidence-free review — discarded")
    vectors = [tuple(sorted(v.items())) for v in valid.values()]
    if len(vectors) > 1 and len(set(vectors)) == 1:
        flags.append("degenerate: identical scores for every concept")
    covered = {c for v in valid.values() for c in v}
    if valid and len(covered & set(CRITERIA)) < len(CRITERIA) / 2:
        flags.append("degenerate: addresses fewer than half the rubric")
    return valid, flags


def rationale(r):
    return " ".join(str(r.get(k, "")) for k in ("best_evidence", "strongest_counterargument", "fatal_flaw")).strip().lower()


def aggregate(reviews):
    per_concept = {}
    totals = {}
    for r in reviews:
        for concept, crit in r["_valid"].items():
            for c, s in crit.items():
                per_concept.setdefault(concept, {}).setdefault(c, []).append(s)
            adj = [5 - s if c in REVERSED else s for c, s in crit.items()]
            totals.setdefault(concept, []).append((r.get("reviewer_role", r["_file"]), sum(adj), r.get("fatal_flaw", ""), r.get("strongest_counterargument", "")))
    summary = {}
    for concept, crits in per_concept.items():
        cs = {}
        for c, vals in crits.items():
            row = {"median": statistics.median(vals), "min": min(vals), "max": max(vals),
                   "spread": max(vals) - min(vals), "n_valid": len(vals)}
            if len(vals) >= 5:
                t = sorted(vals)[1:-1]
                row["trimmed_mean"] = round(sum(t) / len(t), 2)
            cs[c] = row
        tot = totals[concept]
        med = statistics.median(v for _, v, _, _ in tot)
        role, val, flaw, counter = max(tot, key=lambda x: abs(x[1] - med))
        summary[concept] = {"criteria": cs, "total_median": med,
                            "total_min": min(v for _, v, _, _ in tot), "total_max": max(v for _, v, _, _ in tot),
                            "n_valid_reviewers": len(tot),
                            "strongest_dissent": {"reviewer": role, "total": val, "fatal_flaw": flaw, "counterargument": counter}}
    return summary


def main(d: Path) -> int:
    out = {"rounds": {}, "flags": {}, "round3_changes": []}
    r1 = {}
    for rnd in ("round-1", "round-3"):
        rd = d / rnd
        if not rd.exists():
            continue
        reviews, seen = [], {}
        for r in load_reviews(rd):
            r["_valid"], flags = clean(r)
            key = rationale(r)
            if key and key in seen:
                flags.append(f"degenerate: rationale copied from {seen[key]}")
            seen.setdefault(key, r["_file"])
            if flags:
                out["flags"][f"{rnd}/{r['_file']}"] = flags
            if r["_valid"]:
                reviews.append(r)
        out["rounds"][rnd] = {"n_valid_reviews": len(reviews), "concepts": aggregate(reviews)}
        if rnd == "round-1":
            r1 = {r.get("reviewer_role"): r for r in reviews}
        else:
            for r in reviews:
                base = r1.get(r.get("reviewer_role"))
                if not base:
                    continue
                for concept, crit in r["_valid"].items():
                    for c, s in crit.items():
                        b = base["_valid"].get(concept, {}).get(c)
                        if b is not None and b != s:
                            ch = {"reviewer": r.get("reviewer_role"), "concept": concept, "criterion": c, "from": b, "to": s,
                                  "explained": bool(str(r.get("changed_from_round_1", "")).strip())}
                            if not ch["explained"]:
                                out["flags"].setdefault(f"round-3/{r['_file']}", []).append(f"{concept}.{c} changed without explanation")
                            out["round3_changes"].append(ch)
    if not out["rounds"].get("round-1", {}).get("n_valid_reviews"):
        print("ERROR no valid round-1 reviews"); return 1
    (d / "consensus-summary.json").write_text(json.dumps(out, indent=2))
    for rnd, data in out["rounds"].items():
        print(f"== {rnd}: {data['n_valid_reviews']} valid reviews")
        for concept, s in data["concepts"].items():
            dis = s["strongest_dissent"]
            print(f"  {concept}: median {s['total_median']} range {s['total_min']}-{s['total_max']} n={s['n_valid_reviewers']} | dissent {dis['reviewer']} ({dis['total']}): {dis['fatal_flaw'] or dis['counterargument']}")
    for f, fl in out["flags"].items():
        for x in fl: print(f"FLAG  {f}: {x}")
    print(f"wrote {d / 'consensus-summary.json'}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(2)
    sys.exit(main(Path(sys.argv[1])))
