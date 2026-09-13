---
name: j-paperclip-ops
description: >
  Keep the Paperclip agent company healthy and unstick it when it stalls — one-command overview of
  every company (seats, money, open work, what is waiting on the human), plus the symptom-to-cause
  runbook for silent wakes, stranded cards, dead escalation paths, frozen instruction bundles and
  seats that stop mid-plan. Use this whenever someone asks how Paperclip is doing, what the board
  or the agents are up to, why a card is stuck, why an agent did nothing or ran and produced
  nothing, why something cannot be closed or deleted, why a run cost so much, or says a card shows
  Recovery/Failed, an agent is paused, an escalation path is paused, or a change to an agent had no
  effect. Also use it before and after any bulk change to seats, budgets or the board, and for the
  weekly maintenance sweep. For driving the API (routes, PATCH shapes) load j-paperclip; for how
  cards move between lists load j-board-flow.
---

# Paperclip ops

Paperclip is the control plane, not the work. Everything here exists because its failures are
**quiet**: a run reports `succeeded` having read nothing, a wake is dropped and never retried, a
closed card keeps pulling seats awake. Nothing alarms. So the job is to look on purpose, and to
distrust green.

## Start with the overview, always

```bash
export PAPERCLIP_TOKEN=...   # board token; see j-paperclip
curl -s -H "Authorization: Bearer $PAPERCLIP_TOKEN" http://localhost:3100/api/companies/eeda44ae-eb2d-46ff-8b9b-a8e88486170c/issues
curl -s -H "Authorization: Bearer $PAPERCLIP_TOKEN" http://localhost:3100/api/companies/eeda44ae-eb2d-46ff-8b9b-a8e88486170c/agents
curl -s -H "Authorization: Bearer $PAPERCLIP_TOKEN" http://localhost:3100/api/companies/eeda44ae-eb2d-46ff-8b9b-a8e88486170c/attention
curl -s -H "Authorization: Bearer $PAPERCLIP_TOKEN" http://localhost:3100/api/companies/eeda44ae-eb2d-46ff-8b9b-a8e88486170c/recovery-observability
```

Read these before answering any "how are we doing" question and before changing anything, so you
know what you changed: spend against cap, seats by status, open / in-progress / blocked cards, and
the attention feed (what is waiting on the human).

## The runbook

Match the symptom, not the story you form about it. Each row was measured on this install.

| Symptom | What is actually true | Fix |
| --- | --- | --- |
| Run says `succeeded`, but the agent clearly read nothing | A wakeup does not put an issue into the run context even when handed `issueId`. No project resolved, so the run opened in an empty fallback dir — and that cwd is then saved on the session and preferred next time | Assign the card to the seat (assignment is what carries the workspace). Wake with `{"forceFreshSession": true}` to drop the poisoned cwd. Read the run log's **first line** to confirm the workspace |
| Card assigned, seat never moves | The seat was paused at assign time: the server logs *failed to wake agent on issue update … status paused* and never retries | Unpause first, then assign or re-assign. Order matters |
| A seat keeps waking with nothing to do | A `done`/`cancelled` card still holds an assignee | Clear `assigneeAgentId` on closed cards (read `/api/companies/:id/issues` and filter `status` done/cancelled with `assigneeAgentId` set). 109 such rows were why one seat failed repeatedly on a cancelled card |
| A card you just cleared goes `blocked` again with a fresh recovery action | Its assignee is a **paused** seat. Paperclip retries the continuation, finds no live execution path, and re-strands it — resolving the recovery action alone does not break the loop, because the assignee is still dead | Unpause the seat (or reassign the card) **first**, then resolve. Pausing a seat that holds open cards is what starts this |
| A run dies at launch with `workspace_validation_failed` | The card has **no project**, so no execution workspace could be persisted before the adapter started. Cards created by agents and routines do not inherit one — measured three times on 2026-09-05 (JET-217, JET-224, and a status-card compile task) | Give the card a project and that project's workspace, then resolve the recovery action. Check open cards for a missing `projectId` before they fail |
| Card shows Recovery or Failed and neither UI nor PATCH clears it | A recovery action (`stranded_assigned_issue`, `active_run_watchdog`, `missing_disposition`) is pending and owns the card | `POST /api/issues/:id/recovery-actions/resolve` with `{"outcome":"restored\|false_positive\|blocked\|cancelled","sourceIssueStatus":"todo\|done\|in_review\|blocked"}` — the field is `sourceIssueStatus`, not `issueStatus` (checked against `/api/openapi.json`, 2026-09-07); `resolutionNote` is optional, `note` is not a key. A plain `PATCH /api/issues/:id {"status":"todo"}` also clears a `missing_disposition` action (measured 2026-09-06). A stuck watchdog is `DELETE /api/issues/:id/watchdog` |
| Seat stops mid-plan | Almost always budget or turns, not a defect. Budget policies enforce even when the overview says `paused: true` — that flag mirrors the *agent's* status, not the policy's | `GET /companies/:id/budgets/overview`, `maxTurnsPerRun` on the agent |
| `PATCH /api/agents/:id` fails with `expected record, received undefined` | `GET /api/agents/:id/configuration` redacts `modelProfiles.*.adapterConfig`, so a read-modify-write loses it | Restore before writing: `\| if .modelProfiles then .modelProfiles \|= with_entries(.value.adapterConfig //= {}) else . end` |
| Instruction-bundle change has no effect | The bundle is injected only into a **fresh** session; a resumed one keeps the cached copy | Wake with `forceFreshSession: true`, then assert the new line appears in the run log |
| "Escalation path is paused" warning | The seat's `reportsTo` points at a paused seat | Unpause the parent or repoint `reportsTo` (note: `reportsToAgentId` is silently ignored) |
| A seat branches in the real checkout and sweeps someone's edits | `workspaceStrategy` lives in the agent's `adapterConfig` and defaults to `project_primary` | `{"type":"git_worktree"}`, and set the workspace's `defaultRef`/`repoRef` or worktree creation stops on an unresolved base ref |
| Trivial work billed at premium rates | Model per seat is set in `adapterConfig.model`, and nothing tiers it for you | Reserve the expensive model for judgment seats; everything mechanical goes a tier down |
| The laptop crawls or freezes while agents run | A local model is loaded with a huge context — measured 2026-09-05: `minicpm-v-4.6` at 262144 ctx, 4-way parallel, JIT-loaded on every OpenViking query. Paperclip was not the caller | `lms ps` for the loaded model and its context, then `lsof -nP -i TCP:1234` for who is actually connected. `lms unload --all` frees it; fix the client's config, not Paperclip's |
| A seat is meant to run on the free gateway but bills or burns the CPU locally | Its `adapterConfig.model` names the provider directly (`lmstudio/...`), which bypasses OmniRoute even when the gateway is declared in `PAPERCLIP_OPENCODE_PROVIDERS` | Set `model` **and** `PAPERCLIP_OPENCODE_SMALL_MODEL` to a combo (`omniroute/free-cheap`); the combo's own last entry is the local floor, so local stays the fallback rather than the default |
| The free lane suddenly fails everywhere | Usually the upstream daily quota, not local config — configuration that worked an hour ago did not rot | Check the gateway's own usage page before touching any Paperclip setting |
| Cards blocked with `acpx_turn_failed`; run log shows `API Error: 400 ... not available in the active live catalog` or `504 ... rate-limit execution expiration` | Lane failure, not an agent failure. 400 = a combo member left the provider's live catalog (config; free providers delist without notice — 2026-09-08 all 6 `free-thinking` members died overnight). 504 = OmniRoute killed a queued request at its own `requestQueue.maxWaitMs` deadline (transient rate limit; the seat never got a turn) | 400: probe the combo's members with a real 1-token request, swap dead ones in `services/omniroute/combos.json`, sync. 504: raise `maxWaitMs` (15s -> 120s measured 2026-09-08), or `0` on combo members so a full lane falls through. Both: resolve the recovery action (`restored`, `sourceIssueStatus` `todo`) and the card requeues. A transient 504 never needs a human decision. A human or seat reading the board applies this classification and requeues the card by hand — there is no scheduled sweep any more (Paul, 2026-09-11) |

## Distrust green

- A frozen run log is not a hung run. The capture stops after an oversized tool result (measured 2026-09-12: 254 KB, right after a 200 KB `qmd get`); the seat kept working for seven minutes. Judge liveness by the seat transcript's mtime (`~/.claude/projects/<worktree-slug>/*.jsonl`) or the browser tab before cancelling.
- A green run status is not evidence a seat saw a repo — the run log's first line is.
- A declared MCP server is not a connected one, and an undeclared one is not necessarily missing:
  probe inside a run rather than reading `config.toml`.
- `GET /api/agents/:id` returns null for `reportsTo`, `heartbeat` and `canCreateAgents` whatever
  they really are. `/configuration` is the honest view.
- Comments are what an agent chose to publish; the run-log ndjson is what it did. When they
  disagree, the log wins.
- A seat is ready for a real card only when three reads agree, taken after its last config
  change (bundle, skills, lane, trust, env, workspace strategy): its probe produced the seat's
  real job in miniature with its real tool — the job's own output, never a read; the record of
  the run's model calls (whatever serves the seat: a gateway's call log today, the provider's
  usage log otherwise) shows the intended model answering for the whole run, no fallbacks; and
  one real one-turn run through the seat's exact model path answered after the last change to
  that path. Any of the three changes, the probe reruns. (2026-09-12: a probe with no browser
  step, a gateway feature switched on by another session, and a trust change after the probe
  cost a night.)

## Lane health

There is no automated repair path any more (Paul, 2026-09-11) — check and fix the lane by hand.
Gateway up (it does **not** survive a reboot): `curl -sf http://127.0.0.1:20128/api/health`. A
lane probe is one `curl` POST to `/v1/chat/completions` with `max_tokens` 5, reading `.model` off
the answer — run it for `free-cheap` and for every combo a live (non-paused) seat rides, since a
combo that only exists on paper strands every seat on it and `/v1/models` never lists combos, so
the probe is the only check. Combo membership: `GET /api/v1/combos` or the `omniroute_list_combos`
MCP tool; changing membership is a write to `combos.data` in `~/.omniroute/storage.sqlite`
followed by `omniroute stop` and `~/.infra/services/omniroute/bin/start`. No local model loaded at
a size and parallelism that freezes the machine: `lms ps` for what is loaded, `lsof -nP -i
TCP:1234` for who is connected, `lms unload --all` to free it.

## Reading run logs: the rules live here, the counting does not

Comments are what a seat published; the log is what it did. **Four signatures, each from a failure
that actually happened**, and each is a rule you apply rather than a number a tool decides:

| Signature | Why it is a defect | What it looked like |
| --- | --- | --- |
| A **control-plane write to a non-local or placeholder host** | The write went nowhere, `curl` exited 0, and the run reported success | `PUT https://paperclip-api.example.com/api/status-cards/…` — the card sat `compiling` for an hour |
| A Paperclip API call with **no `-f`/`%{http_code}` and no read-back** | Unreachable host, 400 and 200 all exit 0; the run is reporting a belief | every seat that "updated" a card it never checked |
| A **tool error swallowed mid-run** | The run continued as if it had not happened, so the output is built on a gap | `"status":"error"` inside a `tool_use` part |
| A run that produced **one or two lines** | Started and died — capacity spent, nothing produced | 30 of 195 runs in one day |

**Calls to GitHub, a job board or Google are ordinary work and are never judged** — only writes to
the control plane. That distinction is the whole reason this gate is worth reading: the first
version flagged 97 things, most of them a seat doing its job, and a gate that cries wolf gets
ignored within a day.

Count by hand: list every `.ndjson` under
`~/.infra/services/paperclip/data/instances/default/data/run-logs/<companyId>/<agentId>/`, grep
each for the four signatures above, and state the denominator — how many logs you actually read —
since that is exactly the part a human or model skips. Read every flagged log by hand, quote the
offending line into a card, and file evidence only — the retro makes the change, one at a time, with
a kill signal.

When the scanner starts firing on ordinary work, **tighten its patterns rather than learning to
ignore it**. When a failure slips past it, add one signature — widening it by one per retro is the
measure of whether this loop is alive.

## Skills for seats that are not Claude Code

`claude_local` seats inherited `~/.claude/skills` for free — 882 of them, measured — **until 2026-09-12**, when every seat moved to `engine: cli` with `--setting-sources=project,local` to stop "Prompt is too long"; since then a seat-style launch answers `Unknown skill` for `ldj`, `lightning-demos` and `deliberate` in both the pkm and .infra roots (probed 2026-09-13). **So today every seat inherits nothing from the user scope**, the same as `opencode_local` and `codex_local`, so anything they must know is delivered through
Paperclip's own catalog:

1. `POST /api/companies/:id/skills` with `{name, slug, markdown, sharingScope:"company"}` — the
   body is the SKILL.md with its frontmatter stripped.
2. Add `company/<companyId>/<slug>` to that seat's `adapterConfig.paperclipSkillSync.desiredSkills`.
3. It installs on the seat's **next fresh run** (`state` goes `missing` → `installed`).
   `POST /api/agents/:id/skills/sync` needs `{"mode":"replace","desiredSkills":[...]}` — both fields,
   the list copied from the seat's `adapterConfig.paperclipSkillSync.desiredSkills` (measured 2026-09-06).
4. **Updating a delivered skill (measured 2026-09-06):** `PATCH …/skills/:id {markdown}` returns 200
   and changes nothing; writing the `sourceLocator` file changes nothing served; `POST …/versions`
   creates an empty current version. What works: `PATCH …/skills/:id/files` with
   `{"path":"SKILL.md","content":<body, frontmatter stripped>}`, then `GET …/skills/:id` to confirm the
   served `markdown` carries the change, then sync the seats (step 3).

Delivered today: `paperclip-ops`, `paperclip-api`, `board-flow`, `verify-before-you-report`, `house-rules`.

**House rules are the one harness-agnostic instruction (Paul, 2026-09-06).** The original is the
vault note `paperclip-house-rules.md`; the catalog skill `house-rules` is its delivery, listed in
every live seat's `desiredSkills` on all three adapters. A rule that applies to every seat goes
there and nowhere else; a bundle keeps only what is specific to its seat. The sweep re-imports the
note when the served markdown differs. It is deliberately not in `~/.claude/skills`, so Claude
seats get one copy, not two.

**The catalog is a delivery, never a second original.** `~/.claude/skills` owns the text; a catalog
entry is a copy, refreshed by re-importing when the original changes. Never edit a skill inside
Paperclip — that is how two versions of one rule start disagreeing. And **never import a skill that
`claude_local` seats already inherit**: they would get a same-name duplicate competing with the
original, which is the drift this rule exists to prevent.

## Maintenance sweep

There is no scheduled sweep any more (Paul, 2026-09-11) — a human or seat reads the board by hand
and repairs what it finds. What to repair: a stale assignee on a closed card, a
`missing_disposition` recovery action, a seat left in `error`, a `stranded_assigned_issue` whose
run log carries a lane-failure signature (2026-09-08 incident) — a 504 queue-deadline is a
transient rate limit, so the card is requeued with no decision needed; a 400 catalog error means a
dead combo member, so the lane gets a real probe — answering again means requeue, still dead means
the seat moves to its fallback lane (`free-* -> subs-*`) and the card requeues, no live fallback
means a human refreshes the combo. Leave alone a stranded card whose run log carries no
lane-failure signature (that absence is a judgment call, and re-queueing into the same failure is
how the 2026-09-08 pileup grew), and a dirty or unmerged worktree (that tree is the only copy of
work that never reached main — the strand-on-branch defect, JET-293, escalated as one line rather
than N notifications).

Run this weekly, or before handing the board to anyone:

0. Probe every lane in use with a real 1-token request (see Lane health above) **before** reading
   the board — a dead lane makes every stuck card one root cause, not N, and requeued cards just
   strand again.
1. Read `/issues`, `/agents`, `/attention` and `/recovery-observability` for the company and clear
   every stuck row left over from the checks above.
2. Attention feed to zero, or say plainly which items are parked and why. An item sitting there is
   a human decision nobody has taken, not a task.
3. Any seat with no completed work in 30 days: say so. A roster that only grows is sediment.
4. Backup age — `/api/health` carries `databaseBackup.latestBackup.ageHours`; over ~26h is stale.
5. Spend against cap, and whether the split by seat matches what those seats actually do.
6. A worktree whose card is closed, whose branch is merged into the default ref, and whose tree is
   clean can be pruned; leave a dirty or unmerged one alone.

## What not to do

Do not add a second queue, a mirror of card state into the vault, or a script for a gate a human
holds. A scheduler was tried (`pcsweep`, 2026-09-06 to 2026-09-11) and retired: Paul decided
against custom ops scripts (2026-09-11), so the sweep is read by hand again. Every one of those has
been tried here and became the thing that drifted. When the flow itself is the defect — a step that
lets a wrong row through — change the flow and say so, rather than patching the single row.

Routes and PATCH shapes: `j-paperclip` (`references/api.md`). Card movement: `j-board-flow`.
