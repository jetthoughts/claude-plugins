---
name: j-market
description: "Find out what is true about a market before deciding anything in it — size it, name the segments, find who already sells this, and read what buyers actually say. Use whenever the question is how big is this, who is it for, who else does it, is anyone paying for it, what do people say about it, is this worth pursuing, or should we enter this space at all. Runs disjoint evidence lanes and returns a ledger with sources you can open, never an estimate presented as a finding. Not for deciding what to do with the answer — that is `deliberate`; not for pricing or packaging — that is `j-offer`."
---

# j-market

The entry point for *what is true out there*. It exists because market questions get answered from the model's priors — a plausible TAM, a plausible segment, a competitor list from memory — and a number invented in one sentence is indistinguishable from one that was measured.

**The rule: no figure without a source someone can open.** An estimate is allowed, labelled `ESTIMATE`, with the arithmetic shown. An estimate wearing the clothes of a finding is the failure this skill prevents.

## Run it

**1 — Name the decision this feeds.** A market question with no decision behind it produces a report nobody reads. Write one line: *what will be decided, by whom, and what a good answer must contain.* If nothing is being decided, stop and say so.

**2 — Pick the lanes the question actually needs.** Two or three, not all six. They are disjoint by construction, which is the only independence that is arithmetic rather than hope.

| The question turns on | Type this |
|---|---|
| How big, and how many are reachable | `pm-market-research:market-sizing` — then `startup-business-analyst:market-sizing-analysis` if the number carries a funding or hiring decision |
| Who the buyers are, and how they differ | `pm-market-research:market-segments` · `:user-personas` · `:user-segmentation` |
| What they are trying to get done | `pm-market-research:customer-journey-map` · `customer-interviews` when real humans are reachable |
| Who already sells this | `competitor-intel` · `startup-business-analyst:competitive-landscape` · `exec-teardown` for verbatim positioning rather than impressions (vault-scoped agent) |
| What people are saying right now | `pulse:cs-pulse` — Reddit, HN and web in parallel, cross-platform patterns |
| A claim that must survive triangulation | `deep-research:cs-deep-research` — refuses to state a claim carried by fewer than three independent sources |
| What we already know | `qmd query "<need>" -c pkm`, and the project's NotebookLM notebook for Drive corpora that are not indexed |

**Start with the last row.** This vault has answered many market questions already; re-deriving one costs a day and produces a second version to reconcile. Cite the prior finding, and re-run only the lane whose question has moved.

**3 — Return rows, not prose.**

| Claim | Source (openable URL or path) | Date | Quote or figure | FACT / ESTIMATE / ASSUMPTION | What this does NOT prove |
|---|---|---|---|---|---|

**Also return what you looked for and did not find, with the denominator.** *Searched 40 postings, 0 mentioned it* is a finding. Silence is not — a clean result usually means nothing was measured.

**4 — Have someone else open the citations.** Not the lane that produced them. `cold-reviewer` sees the ledger and never the reasoning that built it; that separation is the mechanism, not the prompt. A review returning "looks good" has failed.

**5 — Hand off.** Say which of these the answer now supports, and stop:

- a decision → `deliberate` (it will reuse this ledger; say so rather than re-gathering)
- pricing, packaging or a first offer → `j-offer`
- a message to put in public → `j-publish`
- nothing yet, because the ledger has a hole → name the hole and the lane that would fill it

## Failure modes

| Symptom | What it means | Do |
|---|---|---|
| A TAM with no arithmetic | it came from the model | show the multiplication or label it `ESTIMATE` |
| Competitor list with no URLs | recalled, not looked up | re-run with fetches |
| Every lane agrees | the lanes shared a corpus | add a genuinely different one and say so |
| Segments that match the product's features | the answer was shaped by the offer | re-run from the buyer's job, not the product |
| A finding that repeats something in the vault | the resume step was skipped | cite the original; do not create a second copy |
