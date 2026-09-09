---
name: "Search Routing"
description: "Route queries to the correct online search tool: simple search (searxng/perplexica) vs deep research (wigolo-research / LDR quick/detailed / omniroute). Use when choosing which search MCP/tool to invoke."
disable-model-invocation: true
---

# Search Routing

## Simple Search (fast, single-source)
- `wigolo-search` / `searxng` (`:8081`) — raw ranked, cache-first
- `perplexica-search` — cited single answer
- `omniroute-policy` — combo selection

## Deep Research (multi-source, synthesis)
- `wigolo-research` — multi-query, citations
- `ldr-quick_research` / `ldr-detailed_research` — cited summary

## Routing Rule
1. Cache (`wigolo-cache`) first.
2. Simple → `search` / `searxng` / `perplexica`.
3. Deep / synthesis → `wigolo-research` or `ldr-detailed_research`.
4. Policy/combo → `omniroute`.
