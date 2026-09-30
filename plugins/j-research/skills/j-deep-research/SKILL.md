---
name: j-deep-research
description: Deep, multi-source, cited web research using LDR (Local Deep Research) — a distinct tool from plain web search, not a further escalation step of it. Use when the user asks to research a topic thoroughly, wants a deep dive, a cited multi-source summary, a research report, competitor or market evidence, background on a company, product, technology or trend, wants several sources compared or contradictions surfaced, or says one quick search was too thin. Not for searching the local codebase, fetching one known URL, or a single-fact lookup — those are plain search (see j-research router), not this skill.
---

# Deep research with LDR

Plain web search answers one fact or returns ranked pages in seconds. **This skill is for a different job: reconciling several sources into one cited answer**, which needs an agentic loop, not a single query. Reach for it when a plain search was too thin, or the question needs comparison/synthesis up front.

## When to use LDR vs other tools

For detailed routing across all available search tools (Exa, Tavily, You.com, Perplexica, Wigolo, Brave, OmniRoute), use the `j-research` router skill. This skill focuses on LDR specifically.

**Use LDR when:**
- The work must stay local (no API keys, no external services)
- The question is well within a 4B model's synthesis ability
- You need specialist academic/biomedical sources (openalex, pubmed, stackexchange)
- Budget 200-500s per query is acceptable
- You are running in a lane with no API-keyed cloud tools (Tavily/You.com not available)

**Use other tools when:**
- You need speed (<10s): Exa, Tavily, Brave, OmniRoute — all metered, so name the call in the answer
- You need stronger synthesis: OmniRoute with premium models, You.com
- You need semantic search with high recall: Exa
- You need comprehensive crawling: Tavily
- You need academic + forum sources: Perplexica
- You need local-first with caching: Wigolo

**The ladder — one ladder, owned by `j-research` (not by this skill):** `searxng` first → `tavily` as the single metered fallback, announced in the answer → built-in `web_search`/`web_extract` only when both fail, naming the failed rung. `wigolo` and `perplexica` are off-ladder roles (a fetch/search backend and a cited-synthesis helper), not rungs. LDR is this skill's deep-synthesis engine, not a rung either — reach it as a deliberate escalation for the synthesis job, not as something you fall through to. There is no second ladder and no "pick the ladder that matches the tools available": if a tool named here is not callable in this session, say so and stop rather than substituting silently.

### `mcp__ldr__quick_research` (default)
- **Use for:** Most deep research queries
- **Cost:** Free, runs on local LM Studio
- **Speed:** 150-500s (depends on model: qwen3-coder-30b ~145s, gemma-4-e4b ~200-500s)
- **Parameters:** `query` (required), optional `search_engine`, `strategy`
- **Default strategy:** `langgraph-agent`, falls back to `source-based` if local model loses the thread

### `mcp__ldr__detailed_research`
- **Use for:** Decision-grade depth, complex synthesis
- **Cost:** Free, runs on local LM Studio
- **Speed:** Slower than quick_research
- **Parameters:** Same as quick_research
- **Warning:** Never chain without telling the user the expected wait

### `ldr.search` (one-shot, no synthesis)
- **Use for:** Specialist source pulls when you'll read/synthesize yourself
- **Cost:** Free, runs on local LM Studio
- **Speed:** Seconds, not minutes
- **Parameters:** `query`, `engine` (required)
- **Engines:** `searxng`, `arxiv`, `openalex`, `wikipedia`, `pubmed`, `stackexchange`, `semantic_scholar` (run `list_search_engines` for full set)

## Specialist engines (use with ldr.search only)

| Engine | Best for | Notes |
|---|---|---|
| `openalex` | Academic/ML papers | Citations, DOI, OA link. Also indexes arXiv. |
| `pubmed` | Biomedical literature | Study type filtering (RCT > meta-analysis > protocol) |
| `stackexchange` | Code errors, how-to | Accepted answer, score, date vs version in use |
| `arxiv` | Preprint papers | HTTP 406 errors; use openalex instead |
| `wikipedia` | General knowledge | Can be throttled (429); fallback to searxng |
| `semantic_scholar` | Academic papers | Returns 429 without API key |

**Critical:** Do NOT pass `search_engine` to `quick_research`/`detailed_research`. The academic engines return metadata/abstracts that the 4B model cannot synthesize from. Pull specialist sources with `ldr.search` and read them yourself.

## Budget and timing

- One `quick_research` per sub-question, at most three per user request unless decision-grade depth is requested
- Report elapsed time with the result
- Check `lms ps` before quoting a budget to the user (model availability affects speed)
- For any claim that will survive in the output, open the top URL (browseros-neo or wigolo fetch) and read enough to quote it. A synthesized summary of a source is not the same as the source.

## Evidence discipline

- Cite returned URLs next to the claims they support; never invent citations
- Tier honestly: T1 primary, T2 practitioner/buyer, T3 vendor or model output, T4 prior
- If searxng returns nothing useful, say so and try one narrower query, then stop

## LDR failure modes

- **First call after reboot:** ~60s to initialize (heavy imports); warm start ~10s
- **"no loaded chat model":** Should no longer happen — launcher selects model via `mcp/lmstudio-model` (prefers resident, JIT-loads gemma-4-e4b ~10s when idle)
- **`ldr.search` returns `status: success` with 0 results:** Treat as failure, not absence. LDR swallows upstream HTTP errors.
- **Specific engine failures (2026-09-24):** arxiv (HTTP 406), wikipedia (429 throttled), semantic_scholar (429 without key). Use `openalex` for the academic case; for a general web read, go back to the ladder (`searxng`, then `tavily` announced).
- **`ldr (CONNECTION_CLOSED)` at session start:** Launcher exiting when LM Studio couldn't load model. Fixed 2026-09-24; now starts anyway. Research call failing with LM Studio error means run `~/.infra/bin/start`.
- **Tool missing in session:** `/mcp` to reconnect, or `~/.infra/bin/setup-mcp` to re-register
- **Health check:** `bin/bench-research --ldr-only` in `~/.infra` runs two fixed searches plus one `quick_research` (~5 min; per-case timeouts FAIL slow runs instead of hanging)

## Performance measurements (2026-09-24 on gemma-4-e4b)

- `quick_research` with defaults (`langgraph-agent`, searxng) answered known-answer questions correctly (RAGAS metrics, SQLite fixes): ~150-180s each
- Same question with `search_engine: "openalex"` + `source-based` answered "cannot answer" — academic engines return metadata/abstracts that 4B cannot synthesize
- `ldr.search` on `openalex`, `pubmed`, `stackexchange` returned rich, on-topic results in seconds
- Before 2026-09-24 launcher fix, `search_engine` argument was silently ignored (environment override); results measured before then all came from searxng
