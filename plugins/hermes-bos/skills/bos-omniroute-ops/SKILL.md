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
    related_skills: [bos-incident-response, bos-daily-review, bos-intake, j-research]
---

# bos-omniroute-ops Skill

Review the research infrastructure for health, cost, and lane-strategy problems; recommend fixes; and schedule incident hotfixes through kanban triage. Scope covers four services:

Service inventory (four services, endpoints, DB/config paths, model switcher): see `references/service-inventory.md`.

Hermes seats are read-only against all service state; every change they find is packaged as a ready-to-apply instruction. The owner's operator session (Claude Code) may apply OmniRoute changes through the admin API with `OMNIROUTE_API_KEY` from `~/.secrets` (owner authorization 2026-09-23): back up `GET /api/combos` or `GET /api/resilience` first, change one thing, read it back, probe it.

- Research ladder policy: **owned by the `j-research` skill** (the front door). That ladder is
  `searxng` first → `tavily` as the announced metered fallback → built-in `web_search`/`web_extract`
  only if both fail; perplexica and wigolo are off-ladder roles, not rungs. Where this skill and
  `j-research` disagree, `j-research` wins. **Resolved 2026-09-30:** `~/.infra/.okf/references/research-routing.md`
  was revised and now states this same ladder (searxng first, tavily the single named metered fallback,
  everything else off-ladder). `j-research` remains authoritative if they ever diverge again.
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

Probe command (step 1): see `references/probes-and-commands.md`.

Fail signal: a model in Hermes `model.default` or `providers.omniroute.models` absent from the served list. Currently expected: `kmc/k3` (session model), `cos-thinking` (auxiliary), `bos-main` (aggregator).

### 2. Provider connection health

Probe command (step 2): see `references/probes-and-commands.md`.

Flag: active=0 on a provider the strategy depends on (e.g. moonshot/Kimi Primary disabled while kmc/k3 is the session model); non-NULL recent `last_error` on active connections; rising `backoff_level`.

### 3. Error-rate scan

Probe command (step 3): see `references/probes-and-commands.md`.

Flag: any 5xx cluster repeating on one model/account (lane problem, not transient); 401/403 bursts (key problem → owner, never guess).

### 4. Cost / paid-lane audit

Probe command (step 4): see `references/probes-and-commands.md`.

Flag: traffic on paid providers when free lanes were available; recommend combo-lane reorder (free-first) as an owner dashboard action.

### 5. Combo strategy check

Combo probes (step 5): see `references/probes-and-commands.md`.

Compare each combo's lane order against the free-first policy. Note reset-aware handling: after an OmniRoute version update, verify combos still resolve to live connections (post-update lane drift is a known failure class).

**Reweight rules (daily scan).** Compute per-provider success and free-traffic share from call_logs (trailing 48h; the provider-is-a-combo-name rows are combo-exhaustion terminals, not provider traffic — exclude them):

Reweight scan SQL (step 5): see `references/probes-and-commands.md`.

Rules — findings plus owner dashboard actions, never agent DB edits:

1. **70% success floor.** Any free provider <70% success over 24h -> demote its lane to fallback (below the healthy set), open a finding. Cross-check the 7-day error cluster first (recipe R2 is transient saturation) before demoting on one bad day.
2. **40% share cap.** Any free provider >40% of free-web traffic share over the trailing 48h -> trim toward the mean (lane demotion / widen rotation). On round-robin combos a persistent >40% share signals a dead sibling lane absorbing retries, not a spread problem — check sibling lanes first.
3. **Monthly re-baseline.** First review of each month, or on incident: re-baseline lane order from the trailing 7-day per-provider success table; record the table in the review file.

### 6. Circuit breakers and rate limits

Probe command (step 6): see `references/probes-and-commands.md`.

Flag: open breakers on domains Hermes depends on.

### 7. Research-lane service health (searxng, perplexica, LDR)

Verify the ladder's first rung and the off-ladder backends are actually alive before blaming agent
behavior. `searxng` is the rung; `perplexica` and `LDR` are off-ladder roles (per the `j-research`
ladder) and their health is checked here because agents depend on them, not because they are rungs:

Health probes (step 7): see `references/probes-and-commands.md`.

Pass signal: searxng returns >0 results, perplexica API 200, ldr-mcp starts without import crash. A `RequestsDependencyWarning` on ldr startup is noise, not failure — judge by whether the process serves.

### 8. Research-lane wiring audit (why agents skip the ladder)

Wiring checklist in most-common-cause order: see `references/wiring-audit.md`.

### 9. Cost leak: metered backends

Cost-leak check: see `references/wiring-audit.md`.

## Output

Write a findings report to `~/dev/pkm/business-os/operations/omniroute-reviews/YYYY-MM-DD-review.md` with:

- One section per step above: PASS/FAIL, evidence (query + decisive row), impact.
- Owner-action list: each item is a concrete dashboard/config instruction ("Dashboard → Connections → add Kimi OAuth, prefix `kmc`, model `k3`"; "set `web.search_backend: searxng` in `~/.hermes/config.yaml`"), never an agent mutation.
- A severity tag per finding: `critical` (Hermes cannot serve its default model), `high` (degraded/aux broken or ladder bypassed), `medium` (cost/strategy drift), `low` (cleanup).

For every `critical` or `high` finding, create a kanban hotfix task:

Hotfix task creation command: see `references/probes-and-commands.md`.

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
