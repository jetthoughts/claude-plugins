---
name: j-deep-research
description: Deep, multi-source web research that runs entirely on this machine with no API keys. Use when the user asks to research a topic thoroughly, wants a deep dive, a cited multi-source summary, a research report, competitor or market evidence, background on a company, product, technology or trend, wants several sources compared or contradictions surfaced, or says one quick search was too thin. Not for searching the local codebase, fetching one known URL, or a single-fact lookup (use j-perplexica-search).
---

# Deep research with the local stack

Everything runs on this machine. No API key. Order of escalation, cheapest first:

| Step | Tool | Cost (measured 2026-09-02) | Use when |
|---|---|---|---|
| 1 | `mcp__perplexica__search` (see `j-perplexica-search`) | ~10–60 s, one cited answer | a focused question with one answer |
| 2 | `mcp__searxng__searxng_web_search` | 0.8 s, raw ranked results | you need URLs/snippets to read yourself, or to check step 1 |
| 3 | `mcp__ldr__search` with `engine: "searxng"` | ~1 s + ~10 s server start | the same as step 2 through LDR, useful before a research run |
| 4 | `mcp__ldr__quick_research` | 145 s on `qwen3-coder-30b` (3 iterations) | a cited multi-source summary for one sub-question |
| 5 | `mcp__ldr__detailed_research` / `generate_report` | minutes to tens of minutes | a decision-grade report; agree the budget with the user first |

Arguments that matter: `ldr.search` requires `engine` (`searxng`, `arxiv`, `wikipedia`, `pubmed`,
`github`, `semantic_scholar`; `list_search_engines` for the full set). `quick_research` and
`detailed_research` take `query` plus optional `search_engine` and `strategy`
(`list_strategies`; default `langgraph-agent`, fallback `source-based` when the local model
loses the agent loop).

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
  is ~10 s. "no loaded chat model" → load one in LM Studio (`qwen3-coder-30b-a3b-instruct-mlx`
  is the tested model); the launcher picks any loaded non-vision LLM.
- Tool missing in the session → `/mcp` to reconnect, or `~/.infra/bin/setup-mcp` to re-register.
