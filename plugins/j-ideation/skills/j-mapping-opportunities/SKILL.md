---
name: j-mapping-opportunities
description: Build an evidence-backed Opportunity Solution Tree (06-opportunity-tree.md) that separates customer needs from solutions, cites T1/T2 evidence per opportunity, marks T3/T4-backed ones SPECULATIVE, includes do-nothing and process-change options, and records ruled-out opportunities. Use inside /j-independent-ideation for new-service, market, and feature routes after research, or whenever a request jumps to features before the underlying need is known.
---

# Mapping opportunities

Prefer the installed `pm-product-discovery:opportunity-solution-tree` skill for the method; fall back to
`../j-independent-ideation/templates/opportunity-tree.md`. Either way, apply the rules below.

**Input**: `00-decision-brief.md`, `03-evidence-ledger.jsonl`, `05-lightning-demos.md` (if present). **Output**: `06-opportunity-tree.md`.

## Rules

- One desired outcome per tree (from the brief).
- Opportunity = need, pain, desire, or unserved job. A feature name is a solution; move it down a level.
- Each non-speculative opportunity cites ≥1 T1/T2 evidence ID. T3/T4-only → label SPECULATIVE.
- List the current alternative for each opportunity, including "do nothing".
- Include a "process change / do nothing" branch where it is a real option.
- Record ruled-out opportunities and the evidence or reason.

## Procedure

1. Copy outcome from brief. 2. Cluster ledger items by customer need. 3. Draw the tree (mermaid) and the table.
4. Attach candidate solutions per opportunity without ranking them. 5. Hand off to j-generating-independent-variants.

Failure: no T1/T2 evidence for any opportunity → every branch is SPECULATIVE; say so and recommend RESEARCH-MORE to j-making-the-call.
