---
name: cognee-memory
description: >
  Persistent agent memory via the Cognee Docker MCP stack (local graph on LM
  Studio minicpm-v-4.6 + Voyage embeddings; one shared graph for every MCP
  client). Use when the user asks to remember, recall, save to memory, what did
  we decide, store this fact, or when durable cross-session knowledge should
  outlive the session. Prefer this over ad-hoc notes for infrastructure facts
  and decisions.
allowed-tools: Bash
---

# Cognee memory (remember / recall / forget)

Memory lives in a Cognee knowledge graph, owned by the `cognee-backend`
container in `~/.infra`'s root docker-compose. Talk to it through the **Cognee
MCP server over HTTP** — there are two transports serving the same graph:

- **SSE**: `http://localhost:8001/sse` (what `~/.infra/.mcp.json` registers as
  the `cognee` MCP server; preferred for agents that have an MCP client)
- **Streamable HTTP**: `http://127.0.0.1:8002/mcp` (simplest for direct
  JSON-RPC from a shell via curl — single POST, no long-lived SSE connection)

Check health with `curl -sf http://127.0.0.1:8002/health` — expected
`{"status":"ok"}` (same from `:8001` and the backend on `:8080`).

## Tools (same on both transports)

MCP clients call `mcp__cognee__*`; direct JSON-RPC calls `tools/call` with
`name` + `arguments`:

| Tool | Arguments | Notes |
|------|-----------|-------|
| `remember` | `data`, optional `dataset_name`, optional `session_id` | Without `session_id`: full add+cognify (graph memory). With `session_id`: fast session-cache store. Pass `data` **or** `filename`+`content_base64` (≤10 MB upload), not both. |
| `recall` | `query`, optional `session_id` | Graph retrieval + small LLM answer. Evidence, not truth — cross-check `.okf/`. |
| `forget` | `dataset_name` \| `data_id` \| `everything: true` | Exactly one target. |
| `search_tools` / `call_tool` | — | Tool discovery/indirection on the cognee server. |

`dataset_name` defaults to a client-identity dataset (or `main_dataset`) —
**always pass `infra-memory` explicitly** for this repo's durable facts;
pass a different dataset for project-specific stores. One fact per remember
call, one paragraph of plain prose with ids/ports/dates inline. Session
memory: `remember` with `session_id`, recalled by `recall` with the same id.

## Calling over HTTP (no MCP client needed)

Three round trips: `initialize` → `notifications/initialized` → `tools/call`.
Keep the `mcp-session-id` from the initialize response and replay it on every
subsequent call. Verified 2026-09-10 against `:8002/mcp`:

```bash
BASE=http://127.0.0.1:8002/mcp
H1='Content-Type: application/json'
H2='Accept: application/json, text/event-stream'

# 1) initialize — grab the session id
SID=$(curl -sf --max-time 10 -D - -o /dev/null -X POST "$BASE" \
  -H "$H1" -H "$H2" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"agent","version":"1.0"}}}' \
  | grep -i '^mcp-session-id' | tr -d '\r' | awk '{print $2}')

# 2) initialized notification (no body, expect 202)
curl -sf --max-time 10 -o /dev/null -X POST "$BASE" -H "mcp-session-id: $SID" \
  -H "$H1" -H "$H2" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3) call a tool — remember (permanent graph memory, ~10-60s) or recall (~30-90s)
params=$(jq -nc --arg d "The decision was X because Y" --arg ds "infra-memory" \
  '{name:"remember",arguments:{data:$d,dataset_name:$ds}}')
curl -sf --max-time 180 -X POST "$BASE" -H "mcp-session-id: $SID" \
  -H "$H1" -H "$H2" -d "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":$params}" \
  | tr -d '\r' | grep '^data:' | sed 's/^data: //' | jq -r '.result.content[0].text'
```

The reply body is SSE-framed even on :8002 — `: ping` keepalive comments, then
`event: message` + `data: {json}` — so pipe it through
`tr -d '\r' | grep '^data:' | sed 's/^data: //'` **before** `jq`; piping the
raw body straight into `jq` fails with a parse error. Swap `remember` for
`recall` (`{query: $q}`) or `forget` (one of `dataset_name`/`data_id`/
`everything`) with the same framing.

Run remember/recall **SYNC with a generous timeout** — do not
background-and-forget, you want the confirmation line.

## MCP clients

If your client has the `cognee` MCP server registered, prefer the native
tools: `mcp__cognee__remember` / `mcp__cognee__recall` / `mcp__cognee__forget`
with the same arguments as the table above. All clients point at the shared
stack: SSE `http://localhost:8001/sse` (Claude Code, Cursor,
Codebuff/Freebuff) and streamable HTTP `http://127.0.0.1:8002/mcp` (Codex) —
see `.okf/services/cognee-mcp.md` for the exact files.

## When to use it

- A decision or constraint that future sessions must not re-derive: store it
  (and also update `.okf/` if it changes repo structure — cognee is the
  memory, the OKF bundle is the documentation; both, not either).
- Before answering "why is X set up this way": recall first, then verify.
- Do not store secrets, tokens, or anything that changes per session.
