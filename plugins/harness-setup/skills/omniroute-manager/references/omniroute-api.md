# OmniRoute API Reference

Source: `GET /api/openapi/spec` or `docs/openapi.yaml`

## Base URL
```
http://127.0.0.1:20128
```

## Authentication
All endpoints require `Authorization: Bearer <token>` header.
Tokens: `OMNIROUTE_FREE_KEY`, `OMNIROUTE_SUBS_KEY`, `OMNIROUTE_COGNEE_KEY` (from `~/.secrets`)

---

## Health & Status

### `GET /api/health`
Gateway health check. Returns 200 if up.

### `GET /api/mcp/status`
MCP server status.

### `GET /api/mcp/audit`
MCP audit log.

### `GET /api/mcp/audit/stats`
MCP audit statistics.

---

## MCP Server (110 tools, 33 scopes)

### Transports
- **SSE:** `GET /api/mcp/sse`
- **Streamable HTTP:** `POST /api/mcp/stream` (preferred)
- **Tools list:** `GET /api/mcp/tools`

### Tool Scopes (pass via `--scope` or `X-Omniroute-Scope` header)
| Scope | Tools |
|-------|-------|
| health | `omniroute_get_health` |
| combos | `omniroute_list_combos`, `omniroute_get_combo_metrics`, `omniroute_switch_combo` |
| routing | `omniroute_simulate_route`, `omniroute_best_combo_for_task`, `omniroute_explain_route` |
| providers | `omniroute_get_provider_metrics`, `omniroute_check_quota`, `omniroute_route_request` |
| budget | `omniroute_set_budget_guard`, `omniroute_set_routing_strategy`, `omniroute_set_resilience_profile` |
| testing | `omniroute_test_combo` |
| memory | `memory_add`, `memory_search`, `memory_delete` |
| skills | `skill_invoke`, `skill_list`, `skill_describe`, `skill_register` |
| cache | `omniroute_cache_stats`, `omniroute_cache_flush` |
| admin | `omniroute_db_health_check`, `omniroute_sync_pricing`, `omniroute_get_session_snapshot` |

---

## Context RTK Compression

### `GET /api/context/rtk/config`
Returns current RTK configuration.

### `PUT /api/context/rtk/config`
Updates RTK configuration.
```json
{
  "defaultMode": "off",
  "cacheTtlMinutes": 15,
  "comboOverrides": {
    "free-coding": "stacked",
    "free-thinking": "stacked",
    "free-cheap": "lite",
    "subs-coding": "lite",
    "subs-thinking": "lite",
    "subs-cheap": "lite"
  }
}
```

### `GET /api/context/rtk/filters`
Lists RTK filters with load diagnostics.

### `POST /api/context/rtk/import`
Validates or installs an RTK TOML schema v1 filter file.
```json
{ "toml": "[filter]\nname=\"example\"\n..." }
```

### `POST /api/context/rtk/test`
Runs compression preview on text.
```json
{ "text": "YOUR_PROMPT", "mode": "stacked" }
```

### `GET /api/context/rtk/raw-output/{id}`
Reads retained redacted RTK raw output.

### `GET /api/context/rtk/discover`
Discovers available RTK filters.

### `GET /api/context/rtk/learn`
Shows learned compression patterns.

---

## CLI Tools

### `GET /api/cli-tools/status`
Lists all CLI tool endpoints and their status.

### Common Config Endpoints (each supports GET/POST/DELETE)
- `/api/cli-tools/claude-settings`
- `/api/cli-tools/cline-settings`
- `/api/cli-tools/codex-settings`
- `/api/cli-tools/codex-profiles` (GET/POST/PUT/DELETE)
- `/api/cli-tools/antigravity-mitm` (+ `/alias` GET/PUT/DELETE)
- `/api/cli-tools/hermes-agent-settings`
- `/api/cli-tools/pi-settings`
- `/api/cli-tools/jcode-settings`
- `/api/cli-tools/qwen-settings`
- `/api/cli-tools/omp-settings`
- `/api/cli-tools/smelt-settings`
- `/api/cli-tools/droid-settings`
- `/api/cli-tools/kilo-settings`
- `/api/cli-tools/letta-settings`
- `/api/cli-tools/openclaw/auto-order`
- `/api/cli-tools/logs`
- `/api/cli-tools/keys`
- `/api/cli-tools/guide-settings/{toolId}`
- `/api/cli-tools/runtime/{toolId}`
- `/api/cli-tools/backups` (GET/POST)

---

## Combo Management

### Files
- `~/.infra/services/omniroute/combos.json` — combo definitions
- `sync-combos.py` — syncs to gateway, builds `model_combo_mappings`

### Combo Structure
```json
{
  "combo-name": {
    "description": "...",
    "models": ["model-id-1", "model-id-2", "..."],
    "strategy": "priority|reset-aware"
  }
}
```

### Strategies
- **priority** — sequential cascade, first that answers wins. Free lanes.
- **reset-aware** — balances quota against 5h/weekly resets, round-robins similar scores. Subscription lanes.

### Auto-mapping
`sync-combos.py` creates `model_combo_mappings` entries:
- `auto/*reason*`, `auto/*think*` → `free-thinking` (priority 30)
- `auto/*` → `free-coding` (priority 10)

---

## Policy Management

### File
- `~/.infra/services/omniroute/policy.json`

### Structure
```json
{
  "free": {
    "providerScopes": ["lm-studio/*", "groq/*", "openrouter/*", ...],
    "openrouterFreeModels": ["openrouter/cohere/north-mini-code:free", ...]
  },
  "subscriptions": {
    "providerScopes": ["cc/*", "claude/*", "cx/*", "cxa/*", "no-think/*"]
  }
}
```

### Apply
```bash
~/.infra/bin/omniroute-policy
```
Requires `manage` scope API key.

---

## Admin Dashboard
```
http://127.0.0.1:20128/dashboard
Username: admin
Password: omnirouter
```

Features: Active connections, Key usage, Recent routing decisions, Policy management

---

## Provider Connections (13 total)

| Provider | Type | Status |
|----------|------|--------|
| LM Studio | Local | Active |
| OpenRouter | Cloud | Active (free models allow-listed) |
| Claude OAuth | Cloud | Active (subs lane) |
| Codex OAuth | Cloud | Active (subs lane) |
| OpenCode | No-auth gateway | Active |
| Cloudflare Playground | No-auth gateway | Active |
| Chipotle | No-auth gateway | Active |
| TheOldLLM | No-auth gateway | Active |
| UncloseAI | No-auth gateway | Active |
| AI Horde | No-auth gateway | Active |
| DuckDuckGo | No-auth gateway | Active |
| Felo | No-auth gateway | Active |
| Freebuff2API (vllm) | Local bridge | **Deactivated** (upstream 401) |
| NVIDIA NIM | Cloud | Active (only kimi-k3 verified) |

---

## Key Environment Variables
```bash
OMNIROUTE_BASE_URL=http://127.0.0.1:20128
OMNIROUTE_API_KEY=<from ~/.secrets>
PAPERCLIP_BASE_URL=http://127.0.0.1:3100/api
PAPERCLIP_COMPANY_ID=eeda44ae-eb2d-46ff-8b9b-a8e88486170c
```