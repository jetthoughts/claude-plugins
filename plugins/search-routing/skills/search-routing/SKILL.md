---
name: search-routing
description: "Human-invoked reference card for picking a specific search or deep-research tool once the request's shape is known. Not model-invocable by design — the model-invocable router is j-research. Use when a human asks which search tool to call; route actual requests through j-research."
disable-model-invocation: true
---

# Search Routing — human-invoked reference card

**This is not a router and not a second front door.** It carries `disable-model-invocation: true`, so
the model can never select it; a human reads it, or an agent already told to consult it does. Routing
is owned by the `j-research` skill — one front door, one ladder.

## The ladder (owned by `j-research`)

In order:

1. `mcp__searxng__searxng_web_search` — first rung. Free, ~0.8s, raw ranked URLs; read the source yourself.
2. `mcp__tavily__tavily_search` — the single **metered** fallback. Announce it in the answer; never call it silently.
3. Built-in `web_search` / `web_extract` — only when both rungs fail, naming the failed rung.

`wigolo` and `perplexica` are **off-ladder backend/roles**, not rungs:

- `j-perplexica-search` — a cited single answer when a synthesized paragraph beats a link list.
- `wigolo search` / `wigolo fetch` / `wigolo cache` — the local, keyless fetch/search backend and cache; cache-first *inside* wigolo.

## Deep research (off-ladder synthesis, not a rung)

- `j-deep-research` (`mcp__ldr__quick_research` / `detailed_research`) — cited multi-source synthesis via LDR.
- `wigolo research` — multi-query structured brief with citations, local.
- `mcp__omniroute__omniroute_web_search` — always pass `provider`; with no provider it silently bills `brave-search`.

## What this card used to say

It read "1. Cache (`wigolo-cache`) first. 2. Simple → search/searxng/perplexica/tavily. 3. Deep →
wigolo-research or ldr." That put non-rung tools ahead of searxng and made wigolo a ladder step,
which contradicts the policy the estate approved:

> searxng first; tavily as the announced metered fallback; wigolo is not a ladder rung (it is a
> fetch/search backend); a metered tool is never used silently.
