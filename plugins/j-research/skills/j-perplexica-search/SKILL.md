---
name: j-perplexica-search
description: Quick, cited answer from local private web search. Use when the user wants a fast lookup with sources, asks what is current or recent about a topic, wants a company, person, product or paper checked, mentions Perplexica, Vane, local or private search, or needs one well-sourced answer across web, academic, or discussion sources. Not for the local codebase, fetching a known URL, or a thorough multi-source investigation (use j-deep-research).
---

# Perplexica Search

Use `mcp__perplexica__search` to search through the locally hosted Vane service.

## Search workflow

1. Turn the request into one focused, self-contained query. For company research, combine official identity, team, client reviews, location, and likely aliases in that single query.
2. Select at least one source:
   - `web` for general or current information.
   - `academic` for papers and scholarly material.
   - `discussions` returns forum/community perspectives, useful for sentiment cues and lived-use complaints. It is not a sentiment score, a health metric, or an engagement trend — for those, pair it with a count/trend source (agent-reach backend, wigolo search with a time_range, or a platform's own structure) and treat any "sentiment" claim as a cue, not a measurement.
   - Combine source types when the request spans them.
3. Select an optimization mode:
   - `speed` for a quick lookup.
   - `balanced` for the normal default.
   - `quality` for a thorough answer or when accuracy matters more than latency.
4. Call `mcp__perplexica__search` with `stream: false`. Keep the configured chat and embedding model defaults unless the user explicitly asks to override them.
5. Answer from the returned material and cite the returned source URLs near the claims they support.
6. If coverage is weak, make one narrower follow-up search instead of repeating the same query. Then stop.

## Call budget

- Make at most two search calls per user request: the initial search and one narrower follow-up.
- Exceed two calls only when the user explicitly asks for iterative or deep research.
- Do not fan out spelling variants into separate calls. Include aliases in one query.
- Treat empty or unrelated sources as an evidence limit. Report the gap rather than retrying repeatedly.
- When an entity remains ambiguous, list only supported candidates and ask for a website, country, or other identifier.

Example tool arguments:

```json
{
  "query": "What changed in the Model Context Protocol specification in 2026?",
  "sources": ["web", "academic"],
  "optimization_mode": "balanced",
  "stream": false
}
```

## Reliability

- Never invent a citation or URL. Use only sources returned by the tool or separately verified sources.
- Distinguish the generated answer from the underlying source evidence. Cross-check conflicts and high-stakes claims.
- Prefer one well-formed search over several broad calls.
- If the MCP tool is unavailable in an existing Claude Code session, tell the user to reconnect it with `/mcp` or restart Claude Code.
- The `mcp/perplexica-mcp` launcher selects the LM Studio chat model itself (`mcp/lmstudio-model`: prefers a resident model, JIT-loads `google/gemma-4-e4b` ~10 s when none is resident). A startup failure of the MCP server is therefore never "no model loaded" — check Vane first (`docker ps | grep infra-vane`, `~/.infra/bin/start`).
- Health check: `bin/bench-research --perplexica-only` in `~/.infra` runs three fixed ground-truth searches through the real launcher (~3–5 min).
