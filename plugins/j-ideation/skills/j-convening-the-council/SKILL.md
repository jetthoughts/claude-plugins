---
name: j-convening-the-council
description: Delphi-style, three-round, anonymized review of concepts by five role-based evaluators (customer advocate, commercial analyst, operator, technical reviewer, cold-eyes skeptic; eight UX roles for ux decisions) with evidence-cited scores, no negotiation, median aggregation, degeneracy flags, and preserved dissent, written to 09-council/. Use inside /j-independent-ideation after assumptions are mapped, or when a decision needs independent structured critique instead of a vote or a debate.
---

# Convening the council

Decision-support, never a voting machine. Not the global `Council` skill (that one debates and negotiates; this one forbids it).

**Input**: `00-decision-brief.md`, `03-evidence-ledger.jsonl`, `04-contradiction-register.md`, anonymized `07-concepts/concept-*.md` (NOT `concept-map.md`), `08-assumption-map.md`. **Outputs**: `09-council/brief.md`, `round-1/<role>.md`, `anonymized-rationales.md`, `round-3/<role>.md`, `consensus-report.md`, `consensus-summary.json`.
Aggregator: `scripts/aggregate_council.py 09-council`. Review format: `../j-independent-ideation/templates/council-review.md`.

## Panel

Business/service/feature: `j-customer-advocate`, `j-commercial-analyst`, `j-growth-strategist` (operator lens), `j-technical-feasibility-reviewer`, `j-cold-eyes-reviewer`.
UX: `j-ux-heuristic-evaluator`, `j-accessibility-auditor`, `j-information-architecture-reviewer`, `j-ux-heuristic-evaluator` (task-flow focus), `j-conversion-analyst`, `j-technical-feasibility-reviewer` (design-system focus), `j-cold-eyes-reviewer` (privacy/dark-pattern focus), `j-cold-eyes-reviewer` (user-researcher focus).

Use distinct model families when configured (e.g. Agent `model` parameter, LM Studio/Freebuff2API-backed reviewers via a council MCP). If all reviewers share one provider, write `MODEL FAMILY DIVERSITY LIMITED` in `brief.md`. Never send identical prompts without the role focus. Reviewers never author or edit concepts.

## Rubric (0–5 each; `downside_risk` reverse-scored in aggregation)

customer_value · evidence_strength · revenue_potential · reachability · strategic_fit · delivery_repeatability · feasibility · downside_risk. Every score cites ≥1 `E-nnn` or it is excluded.

## Rounds

1. **Independent scoring**: each reviewer gets only the inputs above and the rubric. Returns scores plus best evidence, strongest counterargument, fatal flaw, required experiment.
2. **Anonymized exchange**: run the aggregator; write `anonymized-rationales.md` listing score distributions and ONLY factual and assumption-level disagreements. No identities, no request to compromise.
3. **Independent re-score**: each reviewer sees `anonymized-rationales.md`; may change a score only with `changed_from_round_1` filled. Originals stay in `round-1/`.

## Aggregation and report

Run the aggregator after round 3. Discard evidence-free or refusing reviews; flag degenerate ones (identical vectors, copied rationale, <half the rubric). Report median, min, max, spread, valid count; trimmed mean only with ≥5 valid reviews. `consensus-report.md` states: what the council agrees on · what it disagrees on · whether the cause is evidence, assumptions, objectives, estimates, or preferences · the smallest empirical test per important disagreement. Do not manufacture convergence.

Failure: <3 valid round-1 reviews → report and stop; j-making-the-call must treat the council as absent.
