# Changelog — j-research

## 0.2.0 — 2026-09-11

- `j-research` added: front-door dispatcher over every research tool now installed (wigolo,
  j-perplexica-search, j-deep-research, Council/deliberate, Research/research-deep, RivalSearchMCP,
  NotebookLM, Perplexity-via-browser). Picks simple/discussion/other-options and hands off; does no
  searching itself. Not wired into `skill-rules.json` deliberately — that file stays reserved for
  hard-to-guess routes, and "research" is exactly the kind of common word ambient description-matching
  already handles.

## 0.1.0 — 2026-09-02

- `j-perplexica-search` moved here from `~/.infra/skills/perplexica-search` (prefix added).
- `j-deep-research` added: how and when to call the `ldr` MCP (Local Deep Research) and the
  `searxng` MCP, with latencies measured on 2026-09-02.
