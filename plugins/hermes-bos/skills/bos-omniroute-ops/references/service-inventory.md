# bos-omniroute-ops — service inventory and environment paths

Scope services (four):

1. **OmniRoute** model gateway (`http://192.168.178.66:20128`) — model routing, combos, API keys.
2. **searxng** (`http://127.0.0.1:8081`, Vane compose) — first-rung web search.
3. **perplexica** (`http://127.0.0.1:3000`) — cited-answer synthesis.
4. **LDR** (`~/.local/bin/ldr-mcp`, `ldr-web`) — local deep research.

- OmniRoute dashboard: `http://192.168.178.66:20128`; admin API on the same host (`/api/combos`, `/api/resilience`, `/api/settings`). `PATCH /api/resilience` takes only the changed section: the full object fails validation on a stored `comboCooldownWait.maxWaitMs`. `targetTimeoutMs` is per combo, not per lane.
- OmniRoute DB (read-only): `sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro"`
- Service catalogue: `~/.infra/bin/services --json` (machine-readable ports/health/start per service)
- Hermes fleet config: `/Users/pftg/.hermes/config.yaml` plus a separate copy per profile at `~/.hermes/profiles/<p>/config.yaml` (not symlinks since 2026-09-22). Change all of them: `hermes -p <p> config set ...`. Current routing: DEC-2026092302 (`hermes-balanced` / `hermes-economy` / `hermes-premium`).
- Fleet model switcher: `~/.hermes/bin/hermes-model-all show|set <provider> <model>`

## Strategy context (combo reweighting)

Strategy context: per PO decision (2026-09-23, t_df591360) free combos run `priority`/`round-robin`, not `weighted` — per-member weight fields are ignored by the deployed binary (v3.8.50) outside the `weighted` strategy. Phrase every reweight recommendation as a lane-order/strategy change for the owner; do not recommend setting weight fields.
