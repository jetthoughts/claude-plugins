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
export PAPERCLIP_TOKEN=...                               # board token; see j-paperclip
~/.claude/skills/j-paperclip-ops/scripts/pcstat          # active companies
~/.claude/skills/j-paperclip-ops/scripts/pcstat --all    # include archived
~/.claude/skills/j-paperclip-ops/scripts/pcstat jet      # one company by name
```

One screen per company: server and deployment mode, spend against cap, seats by status, open /
in-progress / blocked cards, the attention feed (what is waiting on the human), and a `problems`
block that names each stuck thing with the call that clears it. Read it before answering any
"how are we doing" question and before changing anything, so you know what you changed.

Archived companies are hidden by default and are a common source of confusion: cards there cannot
be worked and the UI will not let anyone clear them. If someone says "I can't delete or close
this", check `--all` first — the item is usually in an archived company.

## The runbook

Match the symptom, not the story you form about it. Each row was measured on this install.

| Symptom | What is actually true | Fix |
| --- | --- | --- |
| Run says `succeeded`, but the agent clearly read nothing | A wakeup does not put an issue into the run context even when handed `issueId`. No project resolved, so the run opened in an empty fallback dir — and that cwd is then saved on the session and preferred next time | Assign the card to the seat (assignment is what carries the workspace). Wake with `{"forceFreshSession": true}` to drop the poisoned cwd. Read the run log's **first line** to confirm the workspace |
| Card assigned, seat never moves | The seat was paused at assign time: the server logs *failed to wake agent on issue update … status paused* and never retries | Unpause first, then assign or re-assign. Order matters |
| A seat keeps waking with nothing to do | A `done`/`cancelled` card still holds an assignee | Clear `assigneeAgentId` on closed cards (`pcstat` lists them). 109 such rows were why one seat failed repeatedly on a cancelled card |
| A card you just cleared goes `blocked` again with a fresh recovery action | Its assignee is a **paused** seat. Paperclip retries the continuation, finds no live execution path, and re-strands it — resolving the recovery action alone does not break the loop, because the assignee is still dead | Unpause the seat (or reassign the card) **first**, then resolve. Pausing a seat that holds open cards is what starts this |
| A run dies at launch with `workspace_validation_failed` | The card has **no project**, so no execution workspace could be persisted before the adapter started. Cards created by agents and routines do not inherit one — measured three times on 2026-09-05 (JET-217, JET-224, and a status-card compile task) | Give the card a project and that project's workspace, then resolve the recovery action. `pcstat` now lists workspace-less open cards before they fail |
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

## Distrust green

- A green run status is not evidence a seat saw a repo — the run log's first line is.
- A declared MCP server is not a connected one, and an undeclared one is not necessarily missing:
  probe inside a run rather than reading `config.toml`.
- `GET /api/agents/:id` returns null for `reportsTo`, `heartbeat` and `canCreateAgents` whatever
  they really are. `/configuration` is the honest view.
- Comments are what an agent chose to publish; the run-log ndjson is what it did. When they
  disagree, the log wins.

## The lane repairs itself now

`~/.infra/bin/omniroute-doctor` (add `--check` to change nothing) is the whole health-and-repair
path for the free model lane: gateway up — it does **not** survive a reboot — free lane answers a
real probe, every live opencode seat declares the provider its model names and has its key bound, no
local model loaded at a size and parallelism that freezes the machine. It repairs the first and
third; everything else it reports.

The **Local Model Router Operator** owns it on a schedule (08, 11, 14, 17, 20 Berlin), logging to
the standing card *LANE — OmniRoute health*, and **only when it repaired something or something
needs a human** — a healthy check is silent. That seat runs on `lmstudio/qwen3.5-4b-mlx` on purpose:
a seat that repairs the gateway cannot depend on the gateway, or the repair never happens when it is
most needed. It may start the gateway, re-assert policy and combos, bind an existing key, and unload
a runaway model. It may never mint a key, widen the allowlist, add a provider, or move a seat to a
paid lane — those raise `ask_user_questions` and stop.

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

`~/.infra/bin/runscan [hours]` does the counting — 195 logs in a second, with the denominator
printed, which is the part a model does badly: it skips, it varies run to run, and it cannot honestly
say how many it read. **The script counts; you judge.** Read every flagged log by hand, quote the
offending line into a card, and file evidence only — the retro makes the change, one at a time, with
a kill signal.

When the scanner starts firing on ordinary work, **tighten its patterns rather than learning to
ignore it**. When a failure slips past it, add one signature — widening it by one per retro is the
measure of whether this loop is alive.

## Skills for seats that are not Claude Code

`claude_local` seats inherit `~/.claude/skills` for free — 882 of them, measured. **`opencode_local`
and `codex_local` seats inherit nothing**, so anything they must know is delivered through
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

The mechanical half runs itself now. `~/.infra/bin/pcsweep` (add `--check` to change nothing) is
scheduled by `dev.pftg.pcsweep.plist` at 08:10 and 20:10, logging to `~/.infra/.git/pcsweep.log`,
and notifies **only** when something needs a human — a clean sweep is silent (JET-289).

It repairs what is mechanical and reversible: a stale assignee on a closed card, a
`missing_disposition` recovery action, a seat left in `error`, and a worktree whose card is closed,
whose branch is merged into the default ref, and whose tree is clean. It **lists** everything else —
every other recovery kind, a blocked card with no unblock owner, a card with no execution workspace,
a seat near its budget cap, and every worktree it kept with the reason. Worktree roots come from the
board's own workspaces (`GET /projects/:id/workspaces` → `cwd`, `defaultRef`), so a new repo is swept
without editing the script.

Two things it deliberately does not do: guess which blocked card was a transient infrastructure
error (that is a judgment, and it re-queues into the same failure), and force a dirty or unmerged
worktree (that tree is the only copy of work that never reached main — the strand-on-branch defect,
JET-293, 18 of them as of 2026-09-07, escalated as one line rather than 18 notifications).

Run the rest by hand, weekly, or before handing the board to anyone:

1. `pcstat` — clear every line in `problems` that `pcsweep` left.
2. Attention feed to zero, or say plainly which items are parked and why. An item sitting there is
   a human decision nobody has taken, not a task.
3. Any seat with no completed work in 30 days: say so. A roster that only grows is sediment.
4. Backup age — `/api/health` carries `databaseBackup.latestBackup.ageHours`; over ~26h is stale.
5. Spend against cap, and whether the split by seat matches what those seats actually do.
6. `~/.infra/bin` scripts — kill rule is 0 references (launchd, `.zshrc`, another script, or a doc
   naming it): `grep -rl "bin/<name>" ~/.infra ~/.dotfiles ~/Documents/pkm`. A script with none →
   delete it and its `~/.infra/README.md` row.

## What not to do

Do not add a second queue, a mirror of card state into the vault, or a script for a gate a human
holds. (A scheduler was on this list until 2026-09-06, when Paul asked for one: `pcsweep` is the
single exception, and it holds because it repairs only mechanical, reversible rows and hands every
judgment back. A second scheduler, or one that decides anything, is still the thing that drifts.) Every one of those has been tried here and became the thing that drifted. When
the flow itself is the defect — a step that lets a wrong row through — change the flow and say so,
rather than patching the single row.

Routes and PATCH shapes: `j-paperclip` (`references/api.md`). Card movement: `j-board-flow`.
