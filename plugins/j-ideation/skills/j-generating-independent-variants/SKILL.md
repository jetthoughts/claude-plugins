---
name: j-generating-independent-variants
description: Generate materially different service, market, feature, channel, experiment, or UX concepts in isolated contexts using eight forced-constraint lenses (or six UX archetypes), then deduplicate and select A lowest-cost, B highest-upside, C contrarian, and optional D do-nothing, written anonymized to 07-concepts/. Use inside /j-independent-ideation after opportunities are mapped, or whenever ideation is converging on one obvious answer.
---

# Generating independent variants

**Input**: `00-decision-brief.md`, `03-evidence-ledger.jsonl`, `06-opportunity-tree.md`, `05-lightning-demos.md` (if any). **Output**: `07-concepts/concept-{A,B,C[,D]}.md`, `07-concepts/concept-map.md`. Template: `../j-independent-ideation/templates/concept.md`.

## Lenses (one isolated agent each; never expose another lens's output)

Business decisions: 1 customer/JTBD-first · 2 productized high-velocity entry offer · 3 premium high-LTV transformation · 4 AI-harness leverage/automation-first · 5 10× cheaper or 10× simpler · 6 must reuse an existing agency asset · 7 opposite-of-obvious / remove complexity · 8 skeptical: do nothing, process change, non-product.

UX decisions: familiar/conservative · efficiency-first · guided/onboarding-first · information-dense · conversion-first · accessibility-first.

## Procedure

1. Spawn one `j-service-designer` (business) or `j-ux-heuristic-evaluator` (ux) agent per lens with brief + ledger + tree only. Each returns up to three candidates in the concept template. Ideators may not score.
2. Wait for all. Only then deduplicate: merge candidates with the same mechanism AND same target job.
3. Select: A lowest-cost/fastest learning · B highest upside/strategic · C differentiated or contrarian · D optional do-nothing/process-only comparator. Reject a set where A, B, C differ only in pricing or naming.
4. Anonymize: strip lens and author; label `concept-A/B/C/D`. Fill `concept-map.md` with lens → label mapping kept OUTSIDE reviewer inputs.
5. Every concept's "Evidence used" cites `E-nnn`; economics are ESTIMATE with formula and range.

Failure: fewer than three materially distinct concepts → report which lenses collapsed and why; do not pad with variants of one idea.
