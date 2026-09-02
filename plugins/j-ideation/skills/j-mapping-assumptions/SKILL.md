---
name: j-mapping-assumptions
description: Turn each concept into falsifiable assumptions across desirability, usability, viability, feasibility, distribution, trust, legal, and strategic fit; score impact, uncertainty, immediacy, and evidence strength; compute priority; and flag leap-of-faith, shared, desk-resolvable, experiment-requiring, and fatal assumptions in 08-assumption-map.md. Use inside /j-independent-ideation before the council and before experiment design, or whenever someone asks "what has to be true".
---

# Mapping assumptions

Optional method aids: `pm-product-discovery:identify-assumptions-new` / `:prioritize-assumptions`. Contract below is mandatory regardless.

**Input**: `07-concepts/concept-*.md`, `03-evidence-ledger.jsonl`, `00-decision-brief.md`. **Output**: `08-assumption-map.md` (template in `../j-independent-ideation/templates/`).

## Procedure

1. For each concept and each category (desirability · usability · viability · feasibility · distribution/GTM · trust/brand · legal/privacy/ethics · strategic fit/delivery repeatability) write assumptions as "[Specific condition] must be true for [concept] to achieve [outcome]". Skip a category only with an explicit "none material" note.
2. Score each: failure impact 1–5, uncertainty 1–5, immediacy 1–5, current evidence strength 0–1 (cite `E-nnn`; T4-only ⇒ ≤0.2).
3. Priority = (impact × uncertainty × immediacy) × (1 − evidence). Sort descending.
4. Tag: leap-of-faith (top priority per concept) · shared across concepts · resolvable by desk research · requires user behavior/live experiment · fatal (failure kills the concept outright).
5. Hand the top assumptions to j-designing-experiments; hand fatal + shared ones to j-convening-the-council's brief.

Failure: a concept with no assumption above priority 20 and evidence ≤0.3 everywhere is under-specified; return it to j-generating-independent-variants.
