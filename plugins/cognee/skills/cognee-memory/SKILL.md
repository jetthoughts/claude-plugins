---
name: cognee-memory
description: >
  Persistent agent memory via the Cognee MCP server (Cognee tenant in tenant
  mode; local graph on the OmniRoute free lane + LM Studio embeddings in local
  mode). Use when the user asks to remember, recall, save to memory, what did
  we decide, store this fact, or when durable cross-session knowledge should
  outlive the session. Prefer this over ad-hoc notes for infrastructure facts
  and decisions.
allowed-tools: Bash
---

# Cognee memory (remember / recall / forget)

Memory lives in a Cognee knowledge graph. The MCP server `mcp__cognee__*`
exposes it to MCP clients; every other agent uses the CLI, which speaks
JSON-RPC over stdio to the same server and therefore hits the same graph.

**Mode** is chosen by `~/.infra/mcp/cognee-mcp` itself: with
`COGNEE_BASE_URL`/`COGNEE_API_KEY` (in `~/.secrets`) it proxies to the Cognee
tenant; otherwise it runs locally on the OmniRoute free lane + LM Studio
embeddings. Both share the same tool surface. Check which one is active with
`~/.infra/bin/cognee status` — the tenant graph and the local graph are
**different stores**, so knowing the mode matters when results look stale.

## CLI (works from any shell, no MCP client needed)

```bash
~/.infra/bin/cognee remember "The decision was X because Y" [dataset]   # default dataset: infra-memory
~/.infra/bin/cognee recall "what did we decide about X?" [session_id]
~/.infra/bin/cognee forget dataset <name> | data <id> | everything
~/.infra/bin/cognee tools                                               # list MCP tools
~/.infra/bin/cognee status                                              # tenant or local mode?
```

- `remember` takes 30–180 s (LLM extraction); `recall` 60–150 s. Run them
  SYNC with a generous timeout — do not background-and-forget, you want the
  confirmation line.
- Text is one paragraph of plain prose. Facts, ids, ports, dates inline.
  One fact per remember call beats a wall of text.
- `recall` answers come from graph retrieval + a small LLM: they are evidence,
  not truth. Cross-check against the repo docs (`.okf/`) before acting.
- Datasets are namespaces. Use `infra-memory` for this repo's facts; pass a
  different dataset for project-specific stores.
- Session memory: `bin/cognee remember-session <session_id> "<text>"` and
  `bin/cognee recall "<query>" <session_id>` — ephemeral working memory.

## MCP clients

`mcp__cognee__remember` / `mcp__cognee__recall` / `mcp__cognee__forget` with
the same arguments (`data`+`dataset_name` / `query`+`session_id` /
`dataset_name`|`data_id`|`everything`). Registered at user scope in Claude
Code, Codex, Cursor, Windsurf, Gemini CLI, Antigravity and Claude Desktop by
the cognee step of setup (see `.okf/services/cognee-mcp.md`).

## When to use it

- A decision or constraint that future sessions must not re-derive: store it
  (and also update `.okf/` if it changes repo structure — cognee is the
  memory, the OKF bundle is the documentation; both, not either).
- Before answering "why is X set up this way": recall first, then verify.
- Do not store secrets, tokens, or anything that changes per session.
