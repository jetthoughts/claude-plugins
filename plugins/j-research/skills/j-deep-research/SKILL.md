---
name: j-deep-research
description: Deep, multi-source, cited web research using LDR (Local Deep Research) — a distinct tool from plain web search, not a further escalation step of it. Use when the user asks to research a topic thoroughly, wants a deep dive, a cited multi-source summary, a research report, competitor or market evidence, background on a company, product, technology or trend, wants several sources compared or contradictions surfaced, or says one quick search was too thin. Not for searching the local codebase, fetching one known URL, or a single-fact lookup — those are plain search (wigolo, searxng, perplexica; see `j-perplexica-search`), not this skill.
---

# Deep research — the LDR tool

Plain web search (wigolo, searxng, perplexica, omniroute) answers one fact or
returns ranked pages in under a second to ~60 s. **This skill is for a
different job: reconciling several sources into one cited answer**, which
needs an agentic loop, not a single query. Reach for it when a plain search
was too thin, or the question needs comparison/synthesis up front — don't
treat it as step 4 of a search ladder.

Two engines can drive that loop; pick one:

| Engine | Tool | Cost | Use when |
|---|---|---|---|
| **LDR** (default) | `mcp__ldr__quick_research` / `detailed_research` | free, runs on this machine's LM Studio residency. 145 s on `qwen3-coder-30b`; 200–500 s on the 4B `google/gemma-4-e4b` — check `lms ps` before quoting a budget | the work must stay local, or the question is well within a 4B's synthesis ability (see measurements below) |
| **OmniRoute** | `omniroute_web_search` (evidence) + `omniroute_route_request` `role: "analysis"` (synthesis) | varies by combo; check `omniroute_check_quota` first | LDR's local model loses the thread (long/technical/academic synthesis) and a stronger routed model is worth the cost |

`ldr.search` is the one-shot half of the same tool — a specialist pull with no
LLM synthesis, seconds not minutes. Requires `engine` (`searxng`, `arxiv`,
`openalex`, `wikipedia`, `pubmed`, `stackexchange`, `semantic_scholar`, …;
`list_search_engines` for the full set). `quick_research`/`detailed_research`
take `query` plus optional `search_engine` and `strategy` (`list_strategies`;
default `langgraph-agent`, fallback `source-based` when the local model loses
the agent loop) — but see below: don't pass `search_engine` to these two.

## Route and lens by context

Pick the row for the question, pull sources with the named tool, then judge them through the
lens. The lens is how you read the sources; the engine choice is which sources you get.

| Context | Pull sources with | Lens (what makes a source count) |
|---|---|---|
| General or current facts | `searxng_web_search`, or `ldr.search` `engine: "searxng"` | recency, primary source over aggregator |
| Academic / ML papers | `ldr.search` `engine: "openalex"` (citations, DOI, OA link); `semantic_scholar` as second | peer-reviewed venue, citation count, year; paper beats blog summary |
| Biomedical | `ldr.search` `engine: "pubmed"` | study type (RCT, meta-analysis > protocol, narrative review) |
| Code errors, how-to | `ldr.search` `engine: "stackexchange"` | accepted answer, score, date vs the version in use |
| A library or tool's API | Context7 / DeepWiki, not LDR | matches the installed version |
| Vendor, market, competitor | `searxng` + `mcp__perplexica__search` | vendor pages are T3; look for an independent buyer or practitioner source |
| Cited synthesis of one sub-question | `ldr.quick_research` with defaults | then run a second query phrased as the opposite claim and read both |

Measured 2026-09-24 on `google/gemma-4-e4b`, known-answer questions:

- `quick_research` with defaults (`langgraph-agent`, searxng) answered both correctly: RAGAS
  metrics and the SQLite "database is locked" fixes, ~150–180 s each.
- The same question with `search_engine: "openalex"` + `source-based` answered "cannot answer":
  the academic engines return metadata and abstracts, which the 4B cannot synthesise from. So do
  not pass `search_engine` to `quick_research`. Pull specialist sources with `ldr.search` and
  read them yourself.
- `ldr.search` on `openalex`, `pubmed` and `stackexchange` returned rich, on-topic results in
  seconds.
- Before the 2026-09-24 launcher fix, the `search_engine` argument was silently ignored, because
  `LDR_SEARCH_TOOL` in the environment overrode it. Results measured before then all came from
  searxng.

## Budget

- One `quick_research` per sub-question, at most three per user request unless the user asked
  for decision-grade depth. Report the elapsed time with the result.
- Never chain `detailed_research` runs without telling the user the expected wait.
- Read the returned sources; the summary is model output and may compress a source badly.

## Evidence discipline

- Cite the returned URLs next to the claims they support; never invent a citation.
- Tier honestly: T1 primary, T2 practitioner/buyer, T3 vendor or model output, T4 prior.
- If SearXNG returns nothing useful, say so and try one narrower query, then stop.

## When it fails

- `searxng`: "All connection attempts failed" or an empty result set → Vane is down; run
  `~/.infra/bin/start` and check `curl 'http://127.0.0.1:8081/search?q=hello&format=json'`.
- `ldr`: first call after a reboot can take ~60 s to initialise (heavy imports); a warm start
  is ~10 s. "no loaded chat model" should no longer happen — the `mcp/ldr-mcp` launcher
  selects the model itself via `mcp/lmstudio-model` (prefers a resident model, JIT-loads
  `google/gemma-4-e4b` ~10 s when LM Studio is idle). The 4B is slow at research: budget
  200–500 s per `quick_research`, and check `lms ps` before quoting a budget to the user.
- `ldr.search` returns `status: success` with 0 results → treat as a failure, not absence. LDR
  swallows upstream HTTP errors. On 2026-09-24 `arxiv` returned HTTP 406 and `wikipedia` 429
  (throttled), and `semantic_scholar` returned 429 at times without a key. Use `openalex`, which
  also indexes arXiv, or searxng. `github` needs an API key; use `gh search` instead.
- `ldr (CONNECTION_CLOSED)` at session start was the launcher exiting when LM Studio could not
  load a model. It now starts anyway (fixed 2026-09-24). A research call that fails with an
  LM Studio error means run `~/.infra/bin/start`.
- Tool missing in the session → `/mcp` to reconnect, or `~/.infra/bin/setup-mcp` to re-register.
- Health check: `bin/bench-research --ldr-only` in `~/.infra` runs two fixed searches plus
  one `quick_research` through the real launcher (~5 min; per-case timeouts FAIL a slow run
  instead of hanging).
