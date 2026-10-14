# Channel routing — full reference

Run all relevant channels for each claim. Do NOT default to "web
search" for every claim — academic, Chinese, social, and real-time
claims need different tools.

## Channel → Tool routing table (canonical)

| Channel | First tool | Fallback | Cost | Notes |
|---|---|---|---|---|
| General web (general facts, news) | `searxng` | `tavily` | Free / paid | Rung 1 + rung 2 together |
| Academic, biomedical, code errors | `ldr` with `engine: openalex \| pubmed \| stackexchange` | `searxng` | Free | |
| Cited synthesis paragraph | `perplexica` | `tavily` | Free / paid | Off-ladder role |
| Cached, explainable scoring | `wigolo` | `searxng` | Free | Off-ladder role |
| Semantic / neural recall | `exa` | `searxng` | Paid | |
| Real-time / current events | `you-research` | `searxng` with `time_range` | Paid | |
| Independent index (non-Google/Bing) | `brave-search` | `searxng` | Paid | |
| Reddit, Twitter, YouTube, GitHub, LinkedIn | `tavily` with `include_domains` | `agent-reach` (skill) | Free | Prefer tavily for cost/speed |
| Chinese-language sources | Kimi via `ego-browser` (logged-in session) | `searxng` | Free | Consumer lane |
| Primary documentation, libraries | `context7` or `deepwiki` | `searxng` | Free | |
| Our own corpus (notes, prior research) | `openviking` search, `qmd` query | — | Free | |
| Repo code and structure | `semble` | `openviking` | Free | |
| Deep multi-source synthesis | `ldr quick_research` | `perplexica` | Free | Off-ladder synthesis role |

## The research ladder (rung order for general web)

1. `mcp__searxng__searxng_web_search` — free, ~0.8s, raw ranked URLs
2. A second MCP service in the same `tool_call` batch, by question shape: `tavily`, `exa`, `brave-search`, `you-research`, `parallel`, `perplexica`, `ldr`, `wigolo`
3. Built-in `web_search` / `web_extract` — only when both above fail; name what failed

Name every service that returned results in the matrix header (`ladder_used: searxng+tavily`).

## Off-ladder roles (NOT rungs)

| Role | Tool | Use when |
|---|---|---|
| Cited synthesis paragraph | `perplexica` | Need a paragraph with citations, not a link list |
| Cached, explainable scoring | `wigolo` | Have a URL and want cached/explainable data |
| Deep multi-source synthesis | `ldr quick_research` | Need 150–500s of multi-source synthesis, not a single search |

These are backend roles, not rungs. They don't replace the ladder; they supplement it.

## Platform-aware routing (Reddit, Twitter, YouTube, etc.)

When the topic names a platform (Upwork jobs, Reddit threads, GitHub issues):

1. `searxng` with `site:` filter first (rung 1)
2. `tavily` with `include_domains` (rung 2)
3. `agent-reach` (off-ladder) only for login-walled content the indexes can't reach

**Sub-rule:** never run `agent-reach` before the ladder has had its turn.

## Consumer research lanes

When the owner asks for a specific consumer service by name (Qwen / Kimi / Perplexity / DeepSeek):

1. Read the verdict file: `~/dev/claude-plugins/plugins/j-research/skills/j-research/references/consumer-lanes.md`
2. Pick the lane the verdict recommends (skip / API / session)
3. Use `ego-browser` for session lanes; direct API for API lanes
4. Log the chat URL per lane run (e.g., `https://chat.qwen.ai/c/<uuid>`) as proof of use

`consumer-lanes.md` is the authoritative reference for which lane to pick, how to start, and how to detect completion.
