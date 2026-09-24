---
name: bos-omniroute-ops
description: Read-only health review of the research infrastructure (OmniRoute gateway, searxng, perplexica, LDR), lane-strategy recommendations, and incident hotfix scheduling for model-routing and research-lane problems.
version: 0.3.0
author: pftg
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, omniroute, ops, incident-response, model-routing, research-lanes, searxng, perplexica, ldr]
    related_skills: [bos-incident-response, bos-daily-review, bos-intake, web-research-lanes]
---

# bos-omniroute-ops Skill

Review the research infrastructure for health, cost, and lane-strategy problems; recommend fixes; and schedule incident hotfixes through kanban triage. Scope covers four services:

1. **OmniRoute** model gateway (`http://192.168.178.66:20128`) — model routing, combos, API keys.
2. **searxng** (`http://127.0.0.1:8081`, Vane compose) — first-rung web search.
3. **perplexica** (`http://127.0.0.1:3000`) — cited-answer synthesis.
4. **LDR** (`~/.local/bin/ldr-mcp`, `ldr-web`) — local deep research.

Hermes seats are read-only against all service state; every change they find is packaged as a ready-to-apply instruction. The owner's operator session (Claude Code) may apply OmniRoute changes through the admin API with `OMNIROUTE_API_KEY` from `~/.secrets` (owner authorization 2026-09-23): back up `GET /api/combos` or `GET /api/resilience` first, change one thing, read it back, probe it.

- OmniRoute dashboard: `http://192.168.178.66:20128`; admin API on the same host (`/api/combos`, `/api/resilience`, `/api/settings`). `PATCH /api/resilience` takes only the changed section: the full object fails validation on a stored `comboCooldownWait.maxWaitMs`. `targetTimeoutMs` is per combo, not per lane.
- OmniRoute DB (read-only): `sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro"`
- Service catalogue: `~/.infra/bin/services --json` (machine-readable ports/health/start per service)
- Hermes fleet config: `/Users/pftg/.hermes/config.yaml` plus a separate copy per profile at `~/.hermes/profiles/<p>/config.yaml` (not symlinks since 2026-09-22). Change all of them: `hermes -p <p> config set ...`. Current routing: DEC-2026092302 (`hermes-balanced` / `hermes-economy` / `hermes-premium`).
- Fleet model switcher: `~/.hermes/bin/hermes-model-all show|set <provider> <model>`
- Research ladder policy: `~/.infra/.okf/references/research-routing.md` (searxng → tavily fallback; perplexica/wigolo off-ladder roles)
- Incident recipes: `bos-incident-response` (R1–R11)

## When to Use

Use when: a Hermes task fails with a model/routing error (503, ALL_TARGETS_SKIPPED, model 404, invalid_api_key); when a research task reports all search lanes failed; when reviewing gateway/research-lane health on a schedule; when the owner asks to reduce spend or improve routing strategy; when agents or kimi sessions are not using perplexica/LDR/searxng for research despite the ladder policy. Do not use for ordinary kanban progression (that is `bos-intake`) or for non-routing incidents (that is `bos-incident-response` with recipe `no-match`).

## Hard Rules

1. **Seats are read-only on OmniRoute.** Hermes seats never mutate the OmniRoute DB or call admin endpoints; their output is a findings report plus owner-action instructions. Only the owner or the owner's operator session applies changes, through the admin API or the dashboard, never by editing the DB.
2. **Never route to paid models without owner approval.** Paid lanes (OpenRouter paid, Codex/Claude subscriptions marked inactive, subs-* combos) are flagged, not enabled. Prefer free lanes and local models (LM Studio).
3. **Never print secrets.** Keys come from `~/.secrets` / `~/.hermes/.env` via env inheritance only; quote key names, never values.
4. **Do not touch the `hermes` API-key allowlist** (`api_keys.name='hermes'.allowed_combos = ["combo/*"]`, covering the three live combos `hermes-balanced`, `hermes-economy`, `hermes-premium`, DEC-2026092302) without owner sign-off — narrowing it silently breaks Paperclip seats and Hermes aux slots. Use `sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT allowed_combos FROM api_keys WHERE name='hermes';"` to verify current allowlist before quoting it.
5. Findings that block Hermes work become a kanban hotfix task (`--triage`) assigned to quality-guardian, following the `bos-incident-response` record format.

## Review Procedure

Run these steps in order. Each step names its source and its pass/fail signal.

### 1. Lane existence vs fleet config

Compare the models Hermes is configured to use against what OmniRoute actually serves.

```bash
# What OmniRoute serves (client view)
curl -s http://192.168.178.66:20128/v1/models -H "Authorization: Bearer $OMNIROUTE_FREE_KEY"

# What Hermes expects
grep -A5 '^model:' /Users/pftg/.hermes/config.yaml
```

Fail signal: a model in Hermes `model.default` or `providers.omniroute.models` absent from the served list. Currently expected: `kmc/k3` (session model), `cos-thinking` (auxiliary), `bos-main` (aggregator).

### 2. Provider connection health

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT provider, name, is_active, last_error, last_error_at FROM provider_connections ORDER BY is_active, provider;"
```

Flag: active=0 on a provider the strategy depends on (e.g. moonshot/Kimi Primary disabled while kmc/k3 is the session model); non-NULL recent `last_error` on active connections; rising `backoff_level`.

### 3. Error-rate scan

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT date(timestamp) d, status, COUNT(*) FROM call_logs WHERE timestamp > datetime('now','-7 days') GROUP BY d, status ORDER BY d DESC, COUNT(*) DESC LIMIT 30;"
```

Flag: any 5xx cluster repeating on one model/account (lane problem, not transient); 401/403 bursts (key problem → owner, never guess).

### 4. Cost / paid-lane audit

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT provider, account, SUM(tokens_in), SUM(tokens_out), COUNT(*) FROM call_logs WHERE timestamp > datetime('now','-7 days') AND provider NOT IN ('lm-studio') GROUP BY provider, account ORDER BY COUNT(*) DESC LIMIT 20;"
```

Flag: traffic on paid providers when free lanes were available; recommend combo-lane reorder (free-first) as an owner dashboard action.

### 5. Combo strategy check

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT name, sort_order FROM combos ORDER BY sort_order;"
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT data FROM combos WHERE name='cos-thinking';"
```

Compare each combo's lane order against the free-first policy. Note reset-aware handling: after an OmniRoute version update, verify combos still resolve to live connections (post-update lane drift is a known failure class).

**Reweight rules (daily scan).** Compute per-provider success and free-traffic share from call_logs (trailing 48h; the provider-is-a-combo-name rows are combo-exhaustion terminals, not provider traffic — exclude them):

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT provider, COUNT(*) calls,
     ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),2) share_pct,
     ROUND(100.0*SUM(CASE WHEN status BETWEEN 200 AND 299 THEN 1 ELSE 0 END)/COUNT(*),1) success_pct
   FROM call_logs
   WHERE timestamp > datetime('now','-2 days')
     AND combo_name IN ('free-coding','free-thinking','free-cheap','cos-thinking','agents-all','cos-default','cos-small')
     AND provider NOT IN ('cos-thinking','free-cheap','free-coding','free-thinking','subs-thinking','subs-coding','subs-cheap','bos-main','agents-all','cos-default','cos-small','auto')
     AND provider NOT LIKE 'combo/%'
   GROUP BY provider ORDER BY calls DESC;"
```

Rules — findings plus owner dashboard actions, never agent DB edits:

1. **70% success floor.** Any free provider <70% success over 24h -> demote its lane to fallback (below the healthy set), open a finding. Cross-check the 7-day error cluster first (recipe R2 is transient saturation) before demoting on one bad day.
2. **40% share cap.** Any free provider >40% of free-web traffic share over the trailing 48h -> trim toward the mean (lane demotion / widen rotation). On round-robin combos a persistent >40% share signals a dead sibling lane absorbing retries, not a spread problem — check sibling lanes first.
3. **Monthly re-baseline.** First review of each month, or on incident: re-baseline lane order from the trailing 7-day per-provider success table; record the table in the review file.

Strategy context: per PO decision (2026-09-23, t_df591360) free combos run `priority`/`round-robin`, not `weighted` — per-member weight fields are ignored by the deployed binary (v3.8.50) outside the `weighted` strategy. Phrase every reweight recommendation as a lane-order/strategy change for the owner; do not recommend setting weight fields.

### 6. Circuit breakers and rate limits

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT * FROM domain_circuit_breakers;"
```

Flag: open breakers on domains Hermes depends on.

### 7. Research-lane service health (searxng, perplexica, LDR)

Verify each rung of the research ladder is actually alive before blaming agent behavior:

```bash
curl -s "http://127.0.0.1:8081/search?q=hello&format=json" | python3 -c "import json,sys; print('searxng results:', len(json.load(sys.stdin).get('results',[])))"
curl -s -o /dev/null -w "perplexica providers: %{http_code}\n" http://127.0.0.1:3000/api/providers
~/.local/bin/ldr-mcp --help >/dev/null 2>&1 && echo "ldr: runnable" || echo "ldr: broken"
```

Pass signal: searxng returns >0 results, perplexica API 200, ldr-mcp starts without import crash. A `RequestsDependencyWarning` on ldr startup is noise, not failure — judge by whether the process serves.

### 8. Research-lane wiring audit (why agents skip the ladder)

When "agents/kimi don't use perplexica/LDR/searxng" is the symptom, check wiring in this order — most common causes first:

1. **Hermes web backend bypass**: `grep -A3 '^web:' /Users/pftg/.hermes/config.yaml`. If `search_backend: exa`, Hermes' built-in web tool goes straight to the metered paid API and never touches searxng. That is a config-policy conflict with the searxng-first ladder — flag as `high`.
2. **MCP wiring**: confirm `searxng` and `perplexica` entries exist under `mcp_servers:` in the same config and are not `enabled: false`.
3. **Skill presence**: `ls ~/.hermes/skills | grep -i 'research\|lanes'` — the `local-deep-research` skill lives only in `~/.agents/skills` (kimi scope); Hermes profiles need a Hermes-side skill or SOUL line to reach LDR.
4. **SOUL ladder line**: researcher SOUL references the ladder; verify other research-touching profiles (growth-operator, delivery-manager) name it too, or they will default to the built-in web tool.
5. **Kimi side**: `~/.kimi-code/mcp.json` carries searxng/perplexica — if a kimi session skipped them, check whether `[experimental] tool-select` deferred them (loaded on demand only).

### 9. Cost leak: metered backends

Any of `web.backend: exa`, `web.search_backend: exa`, or tavily usage beyond the single-fallback role is a cost leak under the free-first policy. Cross-check `call_logs` for exa/tavily traffic volume when the backend config disagrees with the ladder.

## Output

Write a findings report to `~/dev/pkm/business-os/operations/omniroute-reviews/YYYY-MM-DD-review.md` with:

- One section per step above: PASS/FAIL, evidence (query + decisive row), impact.
- Owner-action list: each item is a concrete dashboard/config instruction ("Dashboard → Connections → add Kimi OAuth, prefix `kmc`, model `k3`"; "set `web.search_backend: searxng` in `~/.hermes/config.yaml`"), never an agent mutation.
- A severity tag per finding: `critical` (Hermes cannot serve its default model), `high` (degraded/aux broken or ladder bypassed), `medium` (cost/strategy drift), `low` (cleanup).

For every `critical` or `high` finding, create a kanban hotfix task:

```bash
hermes kanban create "<title>" --triage --assignee quality-guardian --created-by owner --body-file - <<'EOF'
<body: finding, evidence, proposed owner action, verification step>
EOF
```

and record an INC file per `bos-incident-response` when the finding caused (or is causing) blocked kanban tasks.

## Pitfalls

- Judging a lane with a tiny prompt. groq passed a short tool-call probe but rejects anything over ~3,291 tokens (HTTP 413). Probe candidate lanes with a ~25k-token prompt plus a forced tool call, and time them.

- Editing OmniRoute DB or calling admin endpoints — forbidden; package as owner instructions instead.
- Trimming the `hermes` API-key allowlist because the session model changed — auxiliary slots still use cos-thinking; a narrow allowlist silently breaks vision/compression/title.
- Declaring a lane dead from one 503 — check the 7-day error cluster first (recipe R2 is transient saturation).
- Blaming agents for skipping perplexica/LDR before checking service health and `web.search_backend` config — wiring audits come before behavior conclusions.
- Recommending paid lanes as the first fix — always propose free/local alternatives first, paid only with owner approval.
- Recommending weight-field edits on non-`weighted` combos — a no-op at dispatch (v3.8.50); recommend lane-order/strategy changes instead.
- Reporting without the PKM write — the review file is the human visibility layer; a finding that exists only in chat is lost.
- Trusting lm-studio as "the always-available floor" without cross-checking `lms ps` — combo lanes that reference non-resident models 502 on most calls and poison every combo that ends in them. Verify lane model against actually loaded models.

## Verification

- Review file exists under `business-os/operations/omniroute-reviews/` and is readable in PKM.
- Every FAIL has evidence (query output quoted) and a concrete owner action.
- Critical/high findings have a corresponding `--triage` kanban task.
- Research-lane findings state service health first, wiring second, agent behavior last.
- No secret value appears anywhere in the report or the kanban body.
