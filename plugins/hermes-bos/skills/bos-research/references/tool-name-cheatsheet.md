# Tool name cheatsheet — invokable MCP tool names

The `hermes mcp list` output shows server status. The actual tool name
to call via `tool_call` is different. This file is the canonical map.

Verified 2026-10-06 by `tool_search` and `tool_call` invocations.

## Web search (rung 1 + rung 2 + off-ladder)

| Server | Invokable name | Params | Cost | Notes |
|---|---|---|---|---|
| searxng | `mcp__searxng__searxng_web_search` | `query` | free | rung 1 |
| searxng | `mcp__searxng__searxng_instance_info` | none | free | health check |
| brave-search | `mcp__brave_search__brave_web_search` | `query`, `count`, `offset` | metered | needs valid API key |
| brave-search | `mcp__brave_search__brave_local_search` | `query` | metered | local results only |
| tavily | **NOT invokable** in this session | — | — | enabled in `mcp list` but `tool_call` rejects name |
| omniroute | `mcp__omniroute__omniroute_web_search` | `query` | metered | multi-provider failover (Serper, Brave, Perplexity, Exa, Tavily) |
| omniroute | `mcp__omniroute__omniroute_web_fetch` | `url` | metered | multi-provider fetch (Firecrawl, Jina Reader, Tavily) |
| lightpanda | `mcp__lightpanda__search` | `query` | free (Brave if key, else DDG) | headless browser search |
| you-research | **NOT invokable** in this session | — | — | enabled but name not in tool_search results |
| agent-reach | **NOT invokable** in this session | — | — | enabled but name not in tool_search results |
| exa | `mcp__exa__web_search_exa` | `query`, `numResults`, **`objective`** (required) | metered | objective schema is enforced |
| parallel | `mcp__parallel__web_search` | **`objective`** (required), **`search_queries`** (array of strings) | metered | schema requires both |
| perplexica | `mcp__perplexica__search` | `query`, `sources` (array of `web`/`academic`/`discussions`), `chat_model` | free | server was unreachable in this session |

## Local research

| Server | Invokable name | Notes |
|---|---|---|
| openviking | `viking_search` | semantic corpus search; primary for "own corpus" channel |
| openviking | `viking_read` | `uri` + `level` (`abstract`/`overview`/`full`) |
| openviking | `viking_remember` | submit content; OpenViking decides extraction |
| openviking | `viking_browse` | tree/list/stat of viking:// paths |
| qmd | `mcp__qmd__status`, `mcp__qmd__query`, `mcp__qmd__multi_get` | index empty (0 docs) — not yet usable |
| cognee | `mcp__cognee__recall`, `mcp__cognee__search_tools`, `mcp__cognee__remember` | knowledge graph; this run returned empty |
| ldr | `mcp__ldr__quick_research` | deep multi-source synthesis; **timeout 300s** in this session |
| ldr | `mcp__ldr__detailed_research` | decision-grade; 5-15 min |
| ldr | `mcp__ldr__search` | one-shot, no synthesis; requires `engine` param |
| ldr | `mcp__ldr__list_search_engines` | enumerate engines |
| ldr | `mcp__ldr__list_strategies` | enumerate strategies |
| ldr | `mcp__ldr__generate_report` | 10-30 min full report |
| semble | `mcp__semble__search` | repo code search |
| semble | `mcp__semble__find_related` | related code |
| deepwiki | `mcp__deepwiki__*` | AI-powered codebase Q&A (now enabled) |
| context7 | `mcp__context7__*` | library docs (now enabled) |
| notebooklm | **NOT invokable** in this session | enabled but name not in tool_search results |
| paperclip | **NOT invokable** in this session | enabled but name not in tool_search results |

## Browser

| Server | Invokable name | Notes |
|---|---|---|
| browseros-neo | **NOT invokable** | disabled (`:9010` connection refused) |
| ego-browser | shell binary `/Users/pftg/.local/bin/ego-browser nodejs` | use shell, not `mcp__*` |
| browser | `mcp__browser_exec` (note: separate browser from ego-browser) | uses lightpanda; per-turn fresh workspace |
| browser | `browser_vault_list`, `browser_vault_fill`, `browser_vault_save_login`, `browser_vault_unlock`, `browser_vault_enter_code` | password manager via vault |
| lightpanda | `mcp__lightpanda__goto`, `mcp__lightpanda__html`, `mcp__lightpanda__extract`, `mcp__lightpanda__markdown`, `mcp__lightpanda__click`, `mcp__lightpanda__fill`, ... (33 tools total) | headless Chromium |

## Brand-rule

**Never write `mcp__tavily__tavily_search` from `mcp list` output.** Run `tool_search` to find the invokable name. `mcp list` shows server status, not call signature.

## Gap tracking

- `tavily`, `you-research`, `agent-reach`, `notebooklm`, `paperclip` — all "enabled" in `mcp list` but `tool_call` to canonical names returns "not a known tool name." Probably a Hermes-side tool registry gap, not a server-side gap. Filed in INC-2026100607 (closed; the cheatsheet is the workaround).
