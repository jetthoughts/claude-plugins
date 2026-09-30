# Community signal — definitions and per-tool limits

Use when the request asks for mentions, sentiment, health score, or engagement trend for a tool, company, product, or topic.

## What "community signal" means here

| Signal | Operational meaning | Unit |
|---|---|---|
| Mentions / volume trend | How often the topic appears across chosen platforms, and whether that count is rising or falling over a time bucket | raw count per bucket (day/week/month), trend direction |
| Sentiment cue | The prevailing polarity in representative community discussion — not a numeric score | direction cue (positive / negative / mixed / neutral) + 1–3 representative quotes |
| Health (of a tool/product/repo) | Signs of upkeep and usage liveliness: release cadence, open-vs-closed issue shape, PR activity where extractable, platform presence where exposed | dates, counts, shape where extractable |
| Engagement trend | Shape of audience interaction over time where the platform exposes it | comment counts, view/like shapes where exposed, trend direction |

## Per-tool limits

| Signal | Best source here | What it gives | What it does NOT give |
|---|---|---|---|
| Mentions / volume trend | `agent-reach` (Reddit, X, YouTube, GitHub, LinkedIn) + `wigolo search` with `time_range` | raw counts over a time bucket, thread text | a normalized cross-platform index, a deduplicated mention count across platforms |
| Sentiment cue | `j-perplexica-search` (sources: discussions) + manual read of representative threads | polarity direction + representative quotes | a numeric sentiment score, a representative probability, a controlled sample |
| Health (release cadence / issue velocity / upkeep) | `agent-reach` GitHub backend + `wigolo fetch` on repo/releases page | release dates, open/closed issue shape where extractable | a maintainer health score, bus-factor, SLA, forensics on closed-source |
| Engagement trend | platform-native structure via `agent-reach` (YouTube view/like shape, Reddit comment counts over time) where exposed | shape of engagement over time where the platform exposes it | a normalized engagement metric across platforms, a like/view per-follower rate |

## Rules

- Every signal row cites which lane produced it. A sentence like "sentiment: positive" with no source lane is a fabrication.
- Where a platform does not expose a metric, say "not exposed by this platform" rather than estimating.
- Sentiment is a cue, not a measurement. Label it as such.
- Health and engagement rows name the specific extractable facts (dates, counts, shapes), not a synthesized "score", unless the user asked for a defined score and you can compute it from extractable facts.
