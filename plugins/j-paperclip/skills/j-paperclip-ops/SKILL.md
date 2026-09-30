---
name: j-paperclip-ops
description: "Keep the Paperclip agent company healthy and unstick it when it stalls — one-command overview of every company, plus the symptom-to-cause runbook for silent wakes, stranded cards, dead escalation paths and frozen instruction bundles. Use when asked how Paperclip is doing, why a card is stuck, why an agent did nothing, why a run cost so much, or after any bulk change to seats or budgets. Not for driving the API — that is `j-paperclip`."
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

Full symptom → cause → fix table: see `references/runbook.md`.

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
Gateway up (it does **not** survive a reboot): `curl -sf http://127.0.0.1:20128/api/health`. A LAN model connection that 502s while `curl` still answers 200 is a runtime connect failure (bun tries mDNS IPv6 first), not a dead host — test with `node -e "fetch(…)"`, fix with the IPv4 literal, or deactivate the connection live: `omniroute providers edit <name> --inactive` (measured 2026-09-14, jora).

A lane probe is one `curl` POST to `/v1/chat/completions` with `max_tokens` 5, reading `.model` off the answer — run it for `free-cheap` and for every combo a live (non-paused) seat rides, since a combo that only exists on paper strands every seat on it and `/v1/models` never lists combos, so the probe is the only check.

Do not "restore" jora as the floor host: reactivate it only after `node -e "fetch(…)"` to jora proves the path *and* its serving context is raised on-site — then `omniroute providers edit jora --active` re-adds it as a second floor host for redundancy, never as a replacement. The floor is load-bearing local residency: if LM Studio idle-unloads bonsai, the next floor call JIT-loads a 27B on this Mac while seats run (504 class). Watch `lms ps` + memory on the first multi-seat run; if pressure shows, reload bonsai at ~131k — every worker seat's measured peak fits under that. **Do not re-add bonsai as a `cos-thinking` floor**; it stays floor for `free-thinking`/`free-cheap` worker seats only. Any probe of bonsai must use `max_tokens >= 1500` (reasoning model: at small budgets it burns them all thinking and returns empty content with `finish_reason: length` — looks alive, proves nothing).

No local model loaded at a size and parallelism that freezes the machine: `lms ps` for what is loaded, `lsof -nP -i TCP:1234` for who is connected, `lms unload --all` to free it.

Lane topology, measured probes and combo CRUD: see `references/lane-health.md`.

## Reading run logs: the rules live here, the counting does not

Comments are what a seat published; the log is what it did. **Four signatures, each from a failure
that actually happened**, and each is a rule you apply rather than a number a tool decides:

The four signatures and what each looked like: see `references/run-log-signatures.md`.

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

The sweep checklist, step by step: see `references/weekly-sweep.md`.

## What not to do

Do not add a second queue, a mirror of card state into the vault, or a script for a gate a human
holds. A scheduler was tried (`pcsweep`, 2026-09-06 to 2026-09-11) and retired: Paul decided
against custom ops scripts (2026-09-11), so the sweep is read by hand again. Every one of those has
been tried here and became the thing that drifted. When the flow itself is the defect — a step that
lets a wrong row through — change the flow and say so, rather than patching the single row.

Routes and PATCH shapes: `j-paperclip`'s `references/api.md`. Card movement: `board-flow`.
