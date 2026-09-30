# bos-research-incident — variant tool chains by profile

Deliberate diversity chains for the swarm, not the general research ladder.

#### Default variant table (researcher profile — adjust per profile)

| Variant | Posture | Tool chain | Why this chain is different |
|---|---|---|---|
| **A — Discovery (broad recall)** | Wide-net semantic + structured | `exa.web_search_exa` (numResults=15, semantic) → top 5 URLs via `web_extract` → `perplexica.search` (sources: web) | Semantic recall beats keyword; misses nothing obvious |
| **B — Freshness (recency-first)** | Time-bounded, primary sources | `searxng.searxng_web_search` (time_range=week) → `you-research` (standard effort, async poll) → `searxng.searxng_web_search` (time_range=month, topic=news) | Two time-bounded rungs catch what an undated search misses |
| **C — Novelty (alternative + emerging)** | Query expansion + platform/forum sweep | `exa.web_search_exa` (numResults=20, query expansion) → `ldr.search` (openalex, for academic/technical) → `perplexica.search` (sources: discussions) | Brings academic and forum signal that A and B miss |

## Reference variants — by profile (verified against actual mcp_servers)

The researcher profile enables: `searxng`, `perplexica`, `ldr`, `you-research`, `browseros-neo`, `exa`. It does **not** enable: `brave`, `tavily`, `omniroute`, `agent-reach`. The variant tables below use only the tools actually wired in `mcp_servers`, with Tavily/agent-reach as additions when the user enables them.

### researcher (default — already enabled)

| Variant | Tool chain |
|---|---|
| A — Discovery | `exa.web_search_exa` (numResults=15) → top 5 via `web_extract` → `perplexica.search` (sources: web) |
| B — Freshness | `searxng.searxng_web_search` (time_range=week) → `you-research` (standard effort) → `searxng.searxng_web_search` (time_range=month, topic=news) |
| C — Novelty | `exa.web_search_exa` (numResults=20, query expansion) → `ldr.search` (openalex) → `perplexica.search` (sources: discussions) |

### researcher + Tavily (if `mcp_servers.tavily.enabled: true` is set)

| Variant | Tool chain |
|---|---|
| A — Discovery | `tavily_search` (search_depth: advanced, time_range: month) → `exa.web_search_exa` → top 5 via `web_extract` |
| B — Freshness | `searxng.searxng_web_search` (time_range: week) → `tavily_search` (time_range: week, search_depth: advanced) → `you-research` |
| C — Novelty | `tavily_search` (with `include_domains` for the named platform) → `exa.web_search_exa` → `perplexica.search` (sources: discussions) |

Tavily is the announced metered fallback in the freshness and platform lanes because `include_domains` handles Reddit/Twitter/YouTube/GitHub/LinkedIn without a login gate — `searxng` with a `site:` filter still comes first (see `references/platform-ladders.md`). It also has a 2-credit cost per `advanced` search — budget rounds.

### default / kanban-orchestrator (read-only, no Tavily)

| Variant | Tool chain |
|---|---|
| A — Discovery | `searxng.searxng_web_search` → `web_extract` |
| B — Freshness | `searxng.searxng_web_search` (time_range=week) → `you-research` |
| C — Novelty | `searxng.searxng_web_search` with `include_domains` for the platform → `perplexica.search` (sources: discussions) |

## How to enable Tavily on the researcher profile

Tavily is not currently in `mcp_servers` for the researcher profile. To enable it:

```yaml
mcp_servers:
  tavily:
    type: stdio
    command: /Users/pftg/.infra/mcp/tavily-mcp    # or the path from `hermes mcp list`
    args: []
    enabled: true
```

`TAVILY_API_KEY` must be in `~/.hermes/.env`. Free tier: 1,000 searches/month; `advanced` search uses 2 credits each. Test before relying on it: `mcp__tavily__tavily_search` with `query: "test"`, `max_results: 1`, then check the response shape.
