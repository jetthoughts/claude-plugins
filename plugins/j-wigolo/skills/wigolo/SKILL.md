---
name: wigolo
description: |
  Local-first fetch/search backend for agents — search, fetch, crawl, cache, extract, diff, watch, research, agent, find-similar. Use when a request needs one of those tools directly (check the cache, read a URL, crawl docs, pull a table) or when searxng and tavily both come back thin. Not the research router; j-research is the front door and wigolo is not a ladder rung.
license: AGPL-3.0-only
metadata:
  author: KnockOutEZ
  version: 0.1.43-beta.2
  homepage: https://github.com/KnockOutEZ/wigolo
  repository: https://github.com/KnockOutEZ/wigolo
---

# Wigolo — web intelligence backend

Wigolo is this estate's **default fetch/search backend**: local-first, ML-reranked results, multi-query search, hybrid semantic discovery, structured extraction, persistent knowledge cache — zero API keys, zero cloud round-trips.

**Wigolo is not the research router and not a rung on the research ladder.** Routing — which shape a research request needs and which rung answers it — belongs to the `j-research` skill. The ladder is `searxng` first, `tavily` as the announced metered fallback, built-in `web_search`/`web_extract` only when both fail. Wigolo answers *how* to fetch, crawl or search a source once something has pointed at it, and it is the sensible local, keyless backend when `searxng` and `tavily` both come back thin.

## Upstream / provenance

This skill is a **fork of vendored upstream** [`KnockOutEZ/wigolo`](https://github.com/KnockOutEZ/wigolo) at `0.1.43-beta.2` (AGPL-3.0-only). Upstream ships an 11-skill pack; this repo restructured it into one skill plus per-tool references, without changing tool semantics. See [references/UPSTREAM.md](references/UPSTREAM.md) for the fork point, what was repackaged, and the sync step for a future upstream revision.

## Tool Selection

| Need | Tool | When |
|------|------|------|
| Find information | `search` | No specific URL, need to discover |
| Get a page | `fetch` | Have a URL, want clean markdown |
| Get a whole site | `crawl` | Need multiple pages from a domain |
| Check what's cached | `cache` | Before searching — cached content is free and instant |
| Get structured data | `extract` | Need tables, JSON-LD, definitions from a page |
| Find related content | `find_similar` | Have one good page, want more like it |
| Deep research | `research` | Need comprehensive multi-source analysis |
| Gather data | `agent` | Need data from multiple sources with a schema |
| Compare two versions | `diff` | See what changed between two pages or a page and its cached copy |
| Monitor for changes | `watch` | Track a page over time; notify on change |

## Wigolo's internal tool order

This is the order to use *inside* wigolo once it has been selected for the job — it is not the research ladder, and it does not route web facts.

1. **cache** — always check first. Instant, free.
2. **search** — don't have a URL yet. Use multi-query arrays for breadth.
3. **fetch** — have a URL. Get clean markdown.
4. **crawl** — need a whole site section (docs, API reference).
5. **extract** — need structured data (tables, key-value, JSON-LD).
6. **find_similar** — have one good source, want to discover related content.
7. **research** — need comprehensive analysis with citations.
8. **agent** — need autonomous multi-source data gathering.
9. **diff** — compare two page versions (or a page vs its cached copy).
10. **watch** — monitor a page for changes over time.

## Search backend

Default `WIGOLO_SEARCH=core` — direct engines + RRF + ML rerank. Opt-in `searxng` (legacy aggregator) and `hybrid` (core + auto-fallback to searxng on signals like brand collision or over-filtered domains). Response carries `fallback_signal` when hybrid fires.

## Key Rules

1. **Cache first** — see [rules/cache-first.md](rules/cache-first.md)
2. **Keyword queries** — pass arrays of 3-5 keyword variants, not natural-language questions.
3. **Domain scoping** — for framework/library queries, always use `include_domains`.
4. **Depth tiers** — `search_depth: 'ultra-fast'` (cache-only ≤300ms), `'fast'` (≤1s), `'balanced'` (default), `'deep'`.
5. **Phrase queries** — `exact_match: true` for quoted-phrase search.
6. **Synthesis** — see [rules/synthesis.md](rules/synthesis.md)

## When NOT to use wigolo

- **Local file operations** — reading, editing, or searching files on disk is not a web task.
- **Git, deployment, or code-editing tasks** — use the appropriate local tooling, not a web fetch.
- **Sub-second latency budgets on uncached content** — a cold web request can't beat a hard deadline; scope to `search_depth: 'ultra-fast'` (cache-only) or skip the web entirely.
- **As a substitute for the research ladder** — a web fact still goes `searxng` → `tavily` (announced). Pick wigolo because it is the right backend for the job, not because it is local.

## Per-Tool References

- Searching → [references/search.md](references/search.md)
- Fetching → [references/fetch.md](references/fetch.md)
- Crawling → [references/crawl.md](references/crawl.md)
- Cache → [references/cache.md](references/cache.md)
- Extracting → [references/extract.md](references/extract.md)
- Finding similar → [references/find-similar.md](references/find-similar.md)
- Research → [references/research.md](references/research.md)
- Agent → [references/agent.md](references/agent.md)
- Diff → [references/diff.md](references/diff.md)
- Watch → [references/watch.md](references/watch.md)
