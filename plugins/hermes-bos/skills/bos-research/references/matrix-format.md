# Matrix format (§9) — full schema

Every research output is written to
`knowledge/research/<YYYY-MM-DD>-<slug>.md` in this exact structure.

## Filename convention

- `<YYYY-MM-DD>-<slug>.md`
- Slug from the question, hyphenated, ≤60 chars
- Example: `2026-10-06-upwork-lead-generation-automation-v3.md`

## Frontmatter

```yaml
---
title: <research question>
type: claim-evidence-matrix
date: <YYYY-MM-DD>
author: researcher
status: draft
mode: <deep-research | quick-lookup>
requesting: <WI-/DEC- id or "owner-direct">
channels_used: <list of channels invoked>
ladder_used: <searxng | searxng+tavily | searxng+tavily+builtin — with reason>
---
```

`ladder_used` MUST match the actual rungs invoked. If a metered tool
was used, name it here AND in the prose answer.

## Required sections

1. **Research question** — the original question, verbatim
2. **Decomposition** — D1–D5 output (claims, evidence surface, must/nice, tier expectation, mode)
3. **Clarification** (deep only) — questions asked, or "No clarification needed"
4. **Channel routing log** — table of which tool was used for which claim and result
5. **Claims** — the main table (one row per atomic claim)
6. **Contradictions** — both positions with sources for every conflict
7. **Gaps** — facts that could not be sourced at any tier (do NOT guess)
8. **Red-team notes** — results of §7 adversarial pass
9. **Bottom line** — 3–5 sentences: what the evidence supports, at what confidence, what remains open
10. **New findings** — ≥3 NEW findings (or marked as quick lookup); FAIL if missing
11. **Source ledger** — every source used, full citation
12. **Checked, not used** — sources checked and rejected with reason
13. **Verification log** (deep only) — gathering tool, verification tool, result per claim

## Claim-row schema

```
| # | claim | sources | tier | confidence | verification | contradictions |
|---|---|---|---|---|---|---|
| 1 | <atomic, falsifiable> | <URLs, dates> | primary/secondary/tertiary/unverified | high/medium/low/unsupported | confirmed/contradicted/qualified/unverified | C<NN> or none |
```

### Source tier vocabulary (only these four)

- **primary** — official docs, standards, filings, primary research
- **secondary** — reputable press, analyst reports, peer review
- **tertiary** — blogs, forums, anecdote
- **unverified** — single unattributed claim

### Confidence vocabulary (only these four)

- **high** — 2+ independent primary sources, no active contradiction
- **medium** — 1 primary or several secondary, minor disagreement
- **low** — tertiary or unverified only, or active material contradiction
- **unsupported** — no source found at any tier; never dropped, never guessed

## Source ledger schema

```
| source | title | publisher | URL | retrieved | relevance |
|---|---|---|---|---|---|
| S1 | ... | ... | ... | YYYY-MM-DD | ... |
```

## Contradiction table schema

```
- C<NN>: <position A (source, tier)> vs <position B (source, tier)>;
  resolution evidence: <what would settle it>
```

## Verification log schema

```
| claim | gathering_tool | verification_tool | result |
|---|---|---|---|
| ... | ... | ... | confirmed/contradicted/qualified |
```

## Output filename (re-stated)

`knowledge/research/<YYYY-MM-DD>-<slug>.md` — researcher seat scope
is READ/DRAFT in `knowledge/**`; seats above that ceiling keep the
file internal-only.

## Verification checklist (run before returning the result)

- [ ] Every claim row has a source column entry or `unsupported`
- [ ] Source tiers use only the vocabulary: primary / secondary / tertiary / unverified
- [ ] Confidence levels use only: high / medium / low / unsupported
- [ ] Ladder rungs actually invoked match `ladder_used` in the header
- [ ] All metered tool use announced in `ladder_used` and in the answer
- [ ] Contradiction table has both positions with sources for every conflict
- [ ] New findings ≥ 3 (deep research mode) or marked as quick lookup
- [ ] Verification log completed for deep research mode
- [ ] Red-team notes completed for deep research mode
- [ ] File written to `knowledge/research/<YYYY-MM-DD>-<slug>.md`
- [ ] File path returned with claim count, contradiction list, gaps, bottom line
