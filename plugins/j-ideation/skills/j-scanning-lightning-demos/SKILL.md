---
name: j-scanning-lightning-demos
description: Harvest transferable mechanisms from existing products and services before ideation by running five isolated research roles (direct competitor, adjacent industry, distant industry, failed example, consumer-grade) that each return three big ideas in a fixed YAML shape, saved to 05-lightning-demos.md. Use inside /j-independent-ideation for new-service and ux routes, or whenever a team is anchored on its first idea and needs comparables.
---

# Scanning lightning demos

Method reference: the global `lightning-demos` skill (facilitation). This skill adds isolation and the evidence contract.

**Input**: `00-decision-brief.md`, `03-evidence-ledger.jsonl`. **Output**: `05-lightning-demos.md` (template in `../j-independent-ideation/templates/`).

## Procedure

1. Spawn five `j-research-lead` agents in parallel, each with ONE role and no access to the others' output:
   direct-competitor · adjacent-industry · distant-industry · failed-or-negatively-reviewed · consumer-grade/low-friction.
2. Each agent returns exactly three demos in the `demo_id/source/sector/mechanism/user_problem_solved/why_it_works/evidence_id/transferable_to_us/cost_or_complexity_to_adapt/risks_when_transferred` shape. Every demo cites an `E-nnn`; add the source to the ledger first.
3. Merge only after all five return. Check: ≥30% of demos outside the target industry; ≥1 failure pattern with "what to avoid".
4. Extract mechanism, job, incentive, interaction, or delivery model. Reject entries that copy visual styling or a feature list.
5. Save `05-lightning-demos.md`.

## Failure behaviour

A role returns fewer than three sourced demos → record UNKNOWN for that role; do not fill from another role's output.
