---
name: omniroute-manager
description: "Unified management of OmniRoute gateway (port 20128): MCP server, CLI tools, RTK context compression, model combos, API-key policies, health checks, and Context7 library docs. Use whenever you need to check gateway health, probe lanes, update combos/policies, configure RTK filters, invoke MCP tools, or fetch up-to-date library documentation via Context7."
---

# OmniRoute Manager

Single entry point for all OmniRoute operations. Consolidates the `omni-mcp`, `omni-cli-tools`, `omni-context-rtk`, `omni-inference`, and Context7 skills into one workflow.

## When to Use This Skill

- Gateway up/down, lane probes, combo health — run manual curl checks (see Gateway Health & Repair below)
- Update combos through the API/MCP, and policy.json via `bin/omniroute-policy`
- Configure RTK compression filters, test compression on prompts
- Invoke any of the 110 MCP tools (routing, budget, memory, skills, cache, admin)
- Manage CLI tool settings (Codex, Cline, Antigravity, etc.)
- Fetch library docs via Context7 API when you need current examples
- Audit API-key policies (the only real guard — catalog is not a control surface)

## Ask the source before you conclude

OmniRoute is `diegosouzapw/OmniRoute` on GitHub. Before deciding a route, tool or option does not exist, ask DeepWiki (`mcp__deepwiki__ask_question`, repo `diegosouzapw/OmniRoute`) and read the answer against the installed version (`npm view omniroute version` vs `omniroute --version`); then probe the gateway. Measured 2026-09-11 on 3.8.50: `POST|PATCH|DELETE /api/combos[/:id]` work with the **management token** `$OMNIROUTE_API_KEY` (201/200/200 on a disposable combo, read-back immediate); the subs and free keys get 403 `Invalid management token` there, and `/api/v1/combos` lists names without ids. The earlier "membership only via sqlite plus restart" finding used the wrong key.

## Quick Start

```bash
# Gateway health
curl -sf http://127.0.0.1:20128/api/health

# One-shot lane probe (model or combo id)
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/v1/chat/completions \
  -d '{"model":"free-cheap","messages":[{"role":"user","content":"ping"}],"max_tokens":8}' \
  | jq -r '.model // "ERROR"'
```

## Architecture Overview

```
OmniRoute Gateway (127.0.0.1:20128)
├── MCP Server          → /api/mcp/* (SSE + Streamable HTTP)
├── CLI Tools API       → /api/cli-tools/*
├── Context RTK API     → /api/context/rtk/*
├── Combo Management    → API /api/combos + MCP (gateway is canonical)
├── Policy Management   → policy.json + bin/omniroute-policy
├── Health               → GET /api/health (manual curl, see Gateway Health & Repair)
└── Admin Dashboard     → http://127.0.0.1:20128/dashboard (admin/omnirouter)
```

**Two API keys (stored in ~/.secrets):**
- `OMNIROUTE_FREE_KEY` (dev) — free lane only, $0.05/day cap
- `OMNIROUTE_SUBS_KEY` (subs) — free + Claude Max + Codex, no cap
- `OMNIROUTE_COGNEE_KEY` — Cognee extraction traffic, own tripwire

**Combo lanes** — read live via `omniroute_list_combos`; the table below is a 2026-09-09 snapshot, not state:
| Lane | Strategy | Head → Floor |
|------|----------|--------------|
| free-coding | priority | codestral → qwen3-coder-30b (LM Studio) |
| free-thinking | priority | nemotron-3-ultra-free → dots-3-note-preview |
| free-cheap | priority | gpt-oss-120b → qwen3.5-4b (LM Studio) |
| subs-coding | reset-aware | cc/claude-sonnet-5 → free-coding tail |
| subs-thinking | reset-aware | cc/claude-opus-5-high → nemotron-free-high |
| subs-cheap | reset-aware | cc/claude-haiku-4.5 → qwen3.5-4b |

---

## Workflows

### 1. Gateway Health & Repair

```bash
# Verify gateway responds
curl -sf http://127.0.0.1:20128/api/health

# Manual gateway start if it does not
~/.infra/services/omniroute/bin/start

# Probe a lane (must answer with a model id, not an error)
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/v1/chat/completions \
  -d '{"model":"free-cheap","messages":[{"role":"user","content":"ping"}],"max_tokens":5}' \
  | jq -r '.model // "ERROR"'
```

There is no automated doctor any more (Paul, 2026-09-11). Check by hand: gateway up, `free-cheap`
answers a probe, every combo a live Paperclip seat uses answers a probe, every live
`opencode_local` seat has `OMNIROUTE_API_KEY` bound. Fix what fails — start the gateway, or bind
the key to the seat.

### 2. Combo Management

**The gateway owns combos (Paul, 2026-09-11).** `combos.json` and `sync-combos.py` are gone. Read and
change combos through the API and MCP — one source of truth, and the one an agent can reach.

```bash
# Read: membership, strategy, and measured success rate per member
#   mcp__omniroute__omniroute_list_combos  (add includeMetrics)
#   mcp__omniroute__omniroute_cost_report  (period=week)

# Change a combo
curl -s -X PATCH -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H 'Content-Type: application/json' \
  http://127.0.0.1:20128/api/combos/<id> -d '{"strategy":"priority"}'

# Read back — the write is not the state
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" http://127.0.0.1:20128/api/combos | jq '.[] | {name, strategy}'
```

**Write capability is partial — verified 2026-09-11.** You can read everything and change *strategy*,
but **you cannot change combo membership through MCP or the API**:

| Want | Route | Works? |
| --- | --- | --- |
| Read combos | `GET /api/v1/combos` (note: `/api/combos` 401s) or `omniroute_list_combos` | yes |
| Success rate / cost per member | `omniroute_cost_report` | yes |
| Change strategy | `omniroute_set_routing_strategy` | yes |
| Activate / deactivate | `omniroute_switch_combo` | yes |
| **Change members** | `PATCH /api/combos/:id {models, strategy}` with `$OMNIROUTE_API_KEY` (the management token); `/api/v1/combos/:id` has no update route and the subs/free keys are refused on `/api/combos` | **yes**, measured 2026-09-11 |

So membership changes go through `/api/combos/:id` with the management token; the sqlite write plus restart is the fallback only when the gateway is down, because a restart drops every in-flight seat call. Verify by `GET` and a 5-token probe afterwards.

**Setting `priority` without fixing member order makes things worse.** Measured 2026-09-11 on
`free-thinking`: with 36 members left in place, switching `auto`→`priority` took the lane from a
60-second answer to **no answer in 120 seconds**. `auto` at least steps past a slow head; `priority`
walks the stored order. Change membership *first*, strategy second — or do neither.

**Why the file went.** It declared `free-thinking` with 2 curated members on `priority` while the
gateway ran 36 on `auto`; the strategy had been changed at the gateway on 2026-09-05 and the file
never updated. The sync was one-way with no drift detection, and `sync-combos.py` had already
ceased to exist while this skill still documented it. A declared source nothing reconciles is a
drift generator.

**Key rules:**
- Free lanes use `priority` strategy (sequential cascade, local floor guaranteed)
- Subs lanes use `reset-aware` (balances 5h/weekly quota, hands off before exhaustion)
- `auto/*` prefixes are mapped via `model_combo_mappings`, rebuilt by the gateway; `auto` also auto-expands membership beyond the declared `candidatePool`
- **Probe after every change** — free providers delist without notice (2026-09-08: free-thinking lost all 6 members overnight)

### 2b. Rank a chain before you probe it

Probing every member live is one call each, pass/fail, current moment only — for a long chain that
is slow and thin. **Read the ledger first — one MCP call, a week of history, and a success
*rate* instead of a single verdict:**

```
mcp__omniroute__omniroute_cost_report(period="week")
```

It returns requests, success rate, latency and cost per provider **and per model**. Rank the chain's
members by `successRatePct`, cut everything at 0.00%, and probe only what survives.

**Two failure shapes this catches and live probing does not.**

*A chain ordered backwards.* Measured 2026-09-11: `free-thinking` held 36 steps. `opencode/big-pickle`
scored 98.33% while the model every seat was pinned to, `oc/nemotron-3-ultra-free`, scored 35.96%.
The good models existed and were not first.

**But rank from the ledger, then probe before promoting — the ledger is history, not state.** Same
day, `thinkingmachines/inkling-small:free` read **99.15%** over 4,728 requests and answered a live
probe with **403**: delisted since, exactly as the combo's own note had warned. Promoting on ledger
rank alone would have put a dead model at the head of the chain. Probe-verified that day:
`opencode/big-pickle` and `openrouter/nvidia/nemotron-3.5-lightning:free`.

*A provider that is entirely dead but still walked.* The same read showed `theoldllm` carrying ~20
aliases (`gpt_5*`, `gemini_*`, `claude_opus_4`, `claude_4_6_opus`…), each fired 780-850 times that
week at **0.00%**. ~15,000 wasted round trips against one provider, invisible until the ledger is
read by provider rather than by model.

**Rules that follow:**
- A combo's length is a cost. Every dead step is latency on every exhausted request.
- **Never leave a paid model as the tail of a free combo.** `free-thinking` step 36 was
  `theoldllm/CLAUDE_4_6_OPUS`. It returned 403 every time so it cost nothing, but an exhausted chain
  reaching a working paid endpoint bills silently.
- Check the **seat default** separately from the chain. A seat pinned to a low-success model fails
  two calls in three even when the gateway is healthy and the chain is fine.
- `omniroute_cost_report` also returns `budget: {limit, remaining}`. `limit: null` means the gateway
  has no spend guard of its own, independent of any Paperclip budget.

### 3. Policy Management (API-Key Guardrails)

```bash
# Edit policy
vim ~/.infra/services/omniroute/policy.json

# Apply (requires manage-scope key)
~/.infra/bin/omniroute-policy
```

**Policy structure:**
```json
{
  "free": {
    "providerScopes": ["lm-studio/*", "groq/*", "openrouter/*", ...],
    "openrouterFreeModels": ["openrouter/cohere/north-mini-code:free", ...]
  },
  "subscriptions": {
    "providerScopes": ["cc/*", "claude/*", "cx/*", "cxa/*", ...]
  }
}
```

**Critical:** Only per-key `modelAccessMode: restricted` + `allowedModels` stops paid routing. Catalog entries do nothing. Combos and `auto/*` bypass model checks unless mapped.

### 4. MCP Server Operations

```bash
# List all 110 tools
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/mcp/tools | jq '.tools[].name'

# Core tool scopes
# health:         omniroute_get_health
# combos:         omniroute_list_combos, omniroute_get_combo_metrics, omniroute_switch_combo
# routing:        omniroute_simulate_route, omniroute_best_combo_for_task, omniroute_explain_route
# providers:      omniroute_get_provider_metrics, omniroute_check_quota, omniroute_route_request
# budget:         omniroute_set_budget_guard, omniroute_set_routing_strategy, omniroute_set_resilience_profile
# testing:        omniroute_test_combo
# memory:         memory_add, memory_search, memory_delete
# skills:         skill_invoke, skill_list, skill_describe, skill_register
# cache:          omniroute_cache_stats, omniroute_cache_flush
# admin:          omniroute_db_health_check, omniroute_sync_pricing, omniroute_get_session_snapshot

# SSE endpoint (for MCP clients)
curl -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/mcp/sse

# Streamable HTTP (preferred)
curl -X POST -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H "Content-Type: application/json" -d '{}' \
  http://127.0.0.1:20128/api/mcp/stream
```

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "omniroute": {
      "command": "npx",
      "args": ["-y", "omniroute", "--mcp"],
      "env": { "OMNIROUTE_KEY": "sk-..." }
    }
  }
}
```

### 5. Context RTK Compression

```bash
# Get current config
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/context/rtk/config | jq

# Update config (global defaultMode stays "off" — only combos override)
curl -X PUT -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"defaultMode":"off","cacheTtlMinutes":15,"comboOverrides":{"free-coding":"stacked","free-thinking":"stacked","free-cheap":"lite","subs-coding":"lite","subs-thinking":"lite","subs-cheap":"lite"}}' \
  http://127.0.0.1:20128/api/context/rtk/config

# List filters + diagnostics
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/context/rtk/filters | jq

# Test compression on a prompt
curl -X POST -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"YOUR_PROMPT_HERE","mode":"stacked"}' \
  http://127.0.0.1:20128/api/context/rtk/test | jq

# Import RTK TOML filter
curl -X POST -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"toml":"[filter]\nname=\"example\"\n..."}' \
  http://127.0.0.1:20128/api/context/rtk/import
```

**Compression modes:** `off` | `lite` | `standard` | `stacked` (RTK + Caveman full)
- Free lanes: `stacked` (aggressive, saves tokens on free models)
- Subs lanes: `lite` (preserves frontier reasoning quality)

### 6. CLI Tools Management

```bash
# List all CLI tool endpoints
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/cli-tools/status | jq

# Common tool configs (each has GET/POST/DELETE for settings):
# /api/cli-tools/codex-settings, /api/cli-tools/claude-settings
# /api/cli-tools/cline-settings, /api/cli-tools/antigravity-mitm
# /api/cli-tools/hermes-agent-settings, /api/cli-tools/pi-settings
# /api/cli-tools/jcode-settings, /api/cli-tools/qwen-settings
# /api/cli-tools/omp-settings, /api/cli-tools/smelt-settings

# Codex profiles
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/cli-tools/codex-profiles | jq

# Antigravity MITM proxy
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  http://127.0.0.1:20128/api/cli-tools/antigravity-mitm | jq
```

### 7. Context7 — Library Documentation

Fetch current docs for any library/framework instead of relying on training data.

```bash
# Step 1: Find library ID
curl -s "https://context7.com/api/v2/libs/search?libraryName=LIBRARY&query=TOPIC" | jq '.results[0]'
# → returns {id, title, description, totalSnippets}

# Step 2: Fetch documentation
curl -s "https://context7.com/api/v2/context?libraryId=LIBRARY_ID&query=TOPIC&type=txt"
```

**Examples:**

```bash
# React hooks
curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" | jq '.results[0].id'
# "/websites/react_dev_reference"
curl -s "https://context7.com/api/v2/context?libraryId=/websites/react_dev_reference&query=useState&type=txt"

# Next.js app router
curl -s "https://context7.com/api/v2/libs/search?libraryName=nextjs&query=routing" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=app+router&type=txt"

# FastAPI dependency injection
curl -s "https://context7.com/api/v2/libs/search?libraryName=fastapi&query=dependencies" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/fastapi/fastapi&query=dependency+injection&type=txt"
```

**Tip:** Use `type=txt` for readable plain text; default `json` includes metadata.

---

## Reference Files

- `references/omniroute-api.md` — Full API endpoint reference (from OpenAPI spec)
- `references/combos-current.json` — Snapshot of working combos for rollback
- `references/policy-current.json` — Snapshot of working policy for rollback
- `references/context7-examples.md` — More Context7 query patterns

---

## Common Tasks Cheat Sheet

| Task | Command |
|------|---------|
| Full health check | `curl -sf http://127.0.0.1:20128/api/health` |
| Probe single lane | `curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" http://127.0.0.1:20128/v1/chat/completions -d '{"model":"free-coding","messages":[{"role":"user","content":"ping"}],"max_tokens":5}' \| jq -r '.model // "ERROR"'` |
| Audit all combo members | probe each member with the call above |
| Read / change combos | `omniroute_list_combos` (MCP), then `PATCH /api/combos/:id` and read back |
| Edit & apply policy | `vim ~/.infra/services/omniroute/policy.json && ~/.infra/bin/omniroute-policy` |
| List MCP tools | `curl -s -H "Auth: Bearer $KEY" http://127.0.0.1:20128/api/mcp/tools \| jq '.tools[].name'` |
| Test RTK compression | `curl -X POST .../api/context/rtk/test -d '{"text":"...","mode":"stacked"}'` |
| Get library docs | `curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=useEffect" \| jq -r '.results[0].id'`, then `curl -s "https://context7.com/api/v2/context?libraryId=<id>&query=useEffect&type=txt"` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ConnectionRefused` on MCP | Gateway down | `~/.infra/services/omniroute/bin/start`, then `curl -sf http://127.0.0.1:20128/api/health` |
| Free lane ERROR 429/402 | Provider quota exhausted | Probe the lane directly; if persistent, `PATCH /api/combos/:id` with probed live members, then read back |
| Paid model served on free key | Policy not restricted | Check `modelAccessMode: restricted` + `allowedModels` in policy.json |
| `auto/*` hits a paid model | `auto` expanded membership past its `candidatePool` | Set the combo to `priority` with a probed member list via `PATCH /api/combos/:id`, then read back |
| Combo serves empty `.model` | Combo resolution OK, member failed | Probe each member with a real 1-token request to find the dead one |
| RTK not compressing | `defaultMode: off`, combos override | Check comboOverrides in `/api/context/rtk/config` |
| Context7 returns empty | Library not indexed or query too narrow | Try broader query; check `totalSnippets` in search result |

---

## Key Principles

1. **API key policy is the only guard** — Catalog, combos, hidden models don't stop explicit paid ids
2. **Probe before trust** — free providers delist silently, and the cost ledger is history, not state: a model can read 99% for the week and answer 403 today
3. **Two lanes, separate keys** — Free key cannot reach `combo/subs-*`; `allowedCombos` enforces
4. **Compression per lane** — Free gets `stacked`, subs gets `lite`; global default stays `off`
5. **Probe what seats actually ride** — a live 1-token request, not just what config says

---

## Integration Notes

- **Paperclip seats** ride OmniRoute via `opencode_local` adapter with `OMNIROUTE_API_KEY` secret ref
- **Cognee MCP** uses its own `OMNIROUTE_COGNEE_KEY` (free lane, own tripwire)
- **Freebuff2API** registered as `vllm` provider but **deactivated** (upstream token dead)
- **NVIDIA NIM** registered but only `nvidia/moonshotai/kimi-k3` verified; kept out of combos
- **Vane/SearXNG** on :8081, separate from OmniRoute — use `mcp__searxng__searxng_web_search` for web search