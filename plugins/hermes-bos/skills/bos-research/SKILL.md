---
name: bos-research
description: Build a sourced claim-evidence matrix per research ladder.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-research Skill

Produce a claim-evidence matrix in `knowledge/research/` for a bounded
research question: every material claim paired with its sources, a source
quality tier, a confidence level, and contradictions recorded side by side.
Web facts are gathered on the local-first research ladder; the matrix is an
internal draft artifact — nothing outward-facing, no external contact, no
commits (the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Research directory: decided per result by the vault's placement table
  `/Users/pftg/dev/pkm/Research-Notes/research-output-placement.md` (global → `evidence/research/`,
  project → `Research-Notes/` with `Belongs to:`, Hermes's own operation → `business-os/`).
  Name the row you used in the result. Legacy default: `/Users/pftg/dev/pkm/business-os/knowledge/research/`
  (supporting sources live in `knowledge/sources/`, claims in `knowledge/claims/`)
- Researcher seat scope: `READ`/`DRAFT` in `knowledge/**` per the authority
  matrix; running seats above that ceiling keep the file internal-only.

## Use when

Use when a work item, decision record, or owner question needs verified
external facts before judgment. Not for code/repo questions (those use
code-search tooling), not for casual single-fact lookups, and not as a
substitute for the owner's decision — the matrix informs, it does not decide.

## Inputs

- Research question, bounded and falsifiable
- Requesting work item or decision ID (for linkage), if one exists
- Deadline or depth hint, if the requester gave one (never invent one)

## Procedure

1. Read with `read_file`: the Business OS root `AGENTS.md`, the requesting
   artifact, and `constitution/risk-policy.md` (secrets never in files —
   reference env var names only).
2. Gather facts strictly on the ladder, in order. **The ladder is owned by the `j-research` skill**
   (this repo, the front door). `~/.infra/.okf/references/research-routing.md` still carries the
   superseded 2026-09-24 "no cost gate" text and must be re-synced; until it is, `j-research` is
   authoritative. The list below must match it, and `j-research` wins on any disagreement:
   1. `mcp__searxng__searxng_web_search` — first rung for any web fact;
      `mcp__searxng__web_url_read` to read a public page as markdown.
   2. `mcp__tavily__tavily_search` — the single metered fallback, only when
      rung 1 is thin or answer-shaped results are needed; say in the matrix
      that rung 2 was used. A metered rung is never used silently.
   3. `web_search` / `web_extract` — built-in fallback only when both rungs
      failed; name which rung failed and why in the matrix.
   Perplexica, wigolo and LDR are off-ladder roles, not rungs.
3. Tier each source: `primary` (official docs, standards, filings),
   `secondary` (reputable press, analyst reports), `tertiary` (blogs,
   forums, anecdotes), `unverified` (single unattributed claim). Prefer
   primary for any claim that drives a decision.
4. Build the matrix: one row per claim. A claim is atomic and falsifiable.
   Assign confidence `high` (2+ independent primary sources, no
   contradiction), `medium` (one primary or several secondary, minor
   disagreement), or `low` (tertiary/unverified only, or active dispute).
   Every claim without a source is marked `unsupported` — never dropped.
5. Record contradictions explicitly: both positions, their sources and
   tiers, and what evidence would resolve the dispute. Lower confidence to
   `low` while a material contradiction stands; never resolve by choosing
   the more convenient source.
6. Write the matrix with `patch` at
   `knowledge/research/<YYYY-MM-DD>-<slug>.md` (slug from the question) in
   the format below. Link it from the requesting artifact's `evidence`
   field with `patch`.

Matrix format:

```markdown
---
title: <research question>
type: claim-evidence-matrix
date: <YYYY-MM-DD>
author: <running seat>
status: <draft|reviewed>
requesting: <WI-/DEC- id or "owner-direct">
ladder_used: <searxng | searxng+tavily | searxng+tavily+builtin — with reason>
---

# <title>

## Claims

| claim | sources | source_tier | confidence | contradictions |
|---|---|---|---|---|
| <atomic, falsifiable> | <paths or URLs> | <primary/secondary/tertiary/unverified> | <high/medium/low/unsupported> | <conflict id or none> |

## Contradictions

- C<NN>: <position A (source)> vs <position B (source)>; resolution evidence: <what would settle it>

## Gaps
<facts that could not be sourced at any tier — research stops here>

## Bottom line
<3-5 sentences: what the evidence supports, at what confidence, what remains open>
```

## Output

Return the matrix path, the claim count by confidence, the contradiction
list, the ladder rungs used (and why rung 2/3 were touched, if they were),
the gaps, and the bottom line.

## Failure modes

- Do not skip the ladder order or use a metered tool silently — rung 2 use
  is announced in the matrix.
- Do not present `low`/`unsupported` claims at `high` confidence because
  they appear in multiple tertiary copies of the same origin.
- Do not resolve a contradiction by picking the answer that flatters the
  request; leave it open and lower confidence.
- Do not let the matrix become the decision — it informs the owner or the
  `bos-decision-record` flow, which own the choice.
- Do not write secrets, key material, or personal data into the matrix —
  env var names only.
- If both searxng and tavily fail and the built-in fallback cannot reach the
  source either, record the claim as `unsupported` with the failed rungs
  named — do not guess the fact.

## Verification

- Every claim row has a source column entry or the `unsupported` mark; zero
  unsourced factual assertions elsewhere in the file.
- File exists at `knowledge/research/<YYYY-MM-DD>-<slug>.md` and `read_file`
  returns it; it is linked from the requesting artifact's `evidence`.
- Source tiers and confidence levels use only the vocabularies above.
- **Novelty gate (Paul, 2026-09-24):** a `## New findings` section lists at least 3
  findings that appear in neither the card's brief nor the prior research it cites, each
  marked NEW with its source. If there are fewer than 3, the result is FAIL ("a check, not
  research") and is re-run with a sharper question. Restating the brief's candidates or options
  does not count.
- Contradictions section lists both positions with sources for every
  conflict flagged in the matrix; ladder_used matches the rungs actually
  invoked.
