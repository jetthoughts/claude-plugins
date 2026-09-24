---
name: bos-incident-response
description: Classify blocked-task incidents and apply fix recipes.
version: 0.1.0
author: pftg
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, kanban, incident-response, blocked-tasks]
    related_skills: [bos-intake, bos-daily-review]
---

# bos-incident-response Skill

Classify a blocked or gave-up kanban task against a table of known fix recipes, apply or escalate per risk class, and record an incident file. Source of truth for recipes — extend it after every new incident class.

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Incidents directory: `/Users/pftg/dev/pkm/business-os/operations/incidents/`
- Canonical format carrier: this skill (per the Business OS root `AGENTS.md`)

## Owner-correction trigger (Paul, 2026-09-24): the only trigger for reflection

Reflection and incident review run **only when Paul says an agent was wrong**: in chat, a Plane
comment, a kanban comment, or through the overseer. They never run on a schedule. Cron jobs, the
curator and periodic auto-review are all off. On such a correction:
1. Quote Paul's words verbatim, with the date, on the affected card.
2. Create ONE incident-review card for kanban-orchestrator, with idempotency key
   `incident-<YYYYMMDD>-<slug>`. Its body is his words plus the facts, each with an evidence path.
   Template: /Users/pftg/dev/pkm/hermes-ecosystem/retrospectives/2026-09-24-incident-review.md,
   the first one (a 5-whys chain per fact, citing evidence; classes of cause; one mechanism per
   class, with a replay test; ≥ 3 NEW findings).
3. Run `/refine` in the affected profile's session to trigger the memory and skill review. It must
   be an INTERACTIVE session (`hermes -p <p> chat --resume <session_id>`, then type /refine).
   In one-shot mode (`-q "/refine" -Q`) the text is sent as a normal prompt: the agent "refined"
   a file instead (tested 2026-09-24). Its
   changes are staged, not applied (`skills.write_approval` and `memory.write_approval` are on);
   Paul or the overseer approves them.
4. Countermeasures are proposals. Nothing changes config, a SOUL or a skill until approved.

## When to Use

Use when a kanban task has `status` blocked or gave_up, or when triaging existing incident records in `operations/incidents/`. Do not use for ordinary task progression or for planning new work — that is `bos-intake`.

## Prerequisites

- Kanban board accessible via the `kanban_*` tools (read task `last_failure_error`, `gave_up` event payload, worker log tail).
- The two seeded INC examples in `operations/incidents/` read as format reference before writing a new one.
- Write access to `operations/incidents/` for new INC records.

## How to Run

1. Read the failure: task `last_failure_error`, `gave_up` event payload, and the worker's last log lines (via `kanban_show` + log file if present).
2. Run the recipe matcher (below) against the failure text.
3. Read the matched recipe's risk class and follow the action rule.
4. Write the INC record and comment the INC id on the task.
5. If the cause has appeared 3+ times across INC records, escalate to a postmortem swarm proposal.

## Quick Reference

### Recipe matcher

For each blocked/gave_up task, scan the failure text and worker logs for the patterns in the table below, in order. Pick the **first** recipe whose match clause fits. If none fit, classify as `no-match` and escalate — never improvise on medium+ risk.

### Risk → action

| Risk | Action |
|---|---|
| low | Apply the fix directly, then unblock the task. |
| medium or higher | Draft the fix, `kanban_request_review` to quality-guardian, then the owner approves (item assigned to Paul). Never self-apply. |

## Procedure

### 1. Read the failure

Pull the task's `last_failure_error`, any `gave_up` event payload, and the most recent worker log lines. Treat the error text as the primary match signal; log lines are secondary context (e.g. `Unknown skill(s)`, `Unknown toolsets`, model 404).

### 2. Match against the recipe table

Scan the failure text top-to-bottom against the match clauses below. Return the **first** recipe whose match clause fits. If none fit, classify as `no-match` and escalate — never improvise on medium+ risk.

When the failure text or the task's own comments reference **multiple** distinct causes (e.g. a subagent rejection loop *and* a concurrent 503 wave), match each cause independently and use the **highest** risk class among the matches as the incident's risk. Record every matched recipe id in the INC `recipe:` field (e.g. `R6 (lane model switch) + R2 (transient 503)`) and apply the action for the highest-risk hit: if any matched recipe is medium+, the whole incident is treated as medium+ (draft + review, never self-apply).

| id | Match clause (first fit wins) | Risk | Fix |
|---|---|---|---|---|
| R1 | `workspace_kind=dir` AND `workspace_path` is NULL/missing | low | Set a static absolute `workspace_path` under a shared family dir in `~/.hermes/kanban/workspaces/`, create the dir if needed, reset `consecutive_failures`, then unblock the task. |
| R2 | cos-thinking `503` with `ALL_TARGETS_SKIPPED` or equivalent saturation message | low | Transient lane saturation — wait one dispatch cycle; if still failing after 30 min, probe the combo health and flag degraded lanes in the OmniRoute dashboard. |
| R3 | LM Studio model 404 / "model not loaded" / model-not-found in the error | low | Check the served models endpoint; if the model exists on disk but is unloaded, the task owner loads it in LM Studio; otherwise switch the lane to a different served model. |
| R4 | MCP server retry cooldown / connect failed / timeout in the error | low | Verify the service health endpoint (searxng, perplexica, notebooklm, etc.); degrade the lane in the work item rather than retry-looping. |
| R5 | missing key_env / 401 / "no active credentials" / auth failure | medium | Owner supplies the secret — never invent or inline keys. Block the task with a note pointing at the missing credential. |
| R6 | subagent output-contract rejection loop (3+ rejections in the log) | medium | Lane model too weak — switch the lane per the deep-research lane table (current default: local bonsai); record the model change in the INC. |
| R7 | dispatcher promoted task with open parents / stale gateway symptom | medium | Reclaim + block with a comment; likely stale gateway — recommend `hermes gateway restart` to the owner. |
| R8 | worker crash `pid not alive` repeated across runs | medium | Check the worker's last output for `Unknown skill(s)` or `Unknown toolsets` — fix the profile skill list or disabled list, then unblock. |
| R9 | gate/blocked task whose condition task has since completed | low | Unblock with a comment pointing at the completed condition's result; the worker re-evaluates. Seed: INC-2026092203. |
| R10 | worker respawn crash loop after `review_requested` (exit code 1, identical last output, 3+ repeats) | medium | Task already in review — likely stale gateway dispatcher state; recommend `hermes gateway restart`; recurrence = postmortem swarm. Seed: INC-2026092204. |
| R11 | task blocked on seat-authority conflict (SOUL hard limit "never edit", wrong seat for the work) | low | Reassign to the seat that holds the authority, unblock with context comment. Exception: edits to SOUL.md, SKILL.md, config or code have no agent seat — complete the card with the proposal path as the result and hand it to delivery-manager to file for owner approval in Plane (item assigned to Paul); never reassign such an edit to another agent. Seed: INC-2026092205. |

### 3. Apply or escalate by risk class

- **low**: execute the recipe's fix, then unblock the task. Verification is whatever the fix row names (e.g. "dir exists and task unblocks").
- **medium+**: draft the fix in a comment or review artifact, then hand off for 2-of-2 consensus review. Block the task with a note describing the proposed fix and the review link. Do not self-apply.

### 4. Record the incident

Write `INC-YYYYMMDDNN.md` into `operations/incidents/` mirroring the two seeded examples. Required frontmatter: `id`, `title`, `status`, `cause`, `recipe` (recipe id, or `no-match`), `risk`, `action`, `verdict`, `date`. Post the same INC id as a comment on the task. Set `status: closed` and `verdict: fixed, recipe validated` when the fix is verified; otherwise `verdict: escalated` or `verdict: open`.

Seeded examples to mirror:
- `INC-2026092201-workspace-null-path.md` — R1, low, fixed.
- `INC-2026092202-output-contract-loop.md` — R6 + R2, medium, fixed.

### 5. Repeat-class escalation

Scan existing INC records for the same cause. If the cause has appeared 3+ times, propose a postmortem swarm to the owner with a memo in `governance/proposals/`. Do not create the swarm inside this skill — surface the trigger.

## Pitfalls

- Matching more than one recipe — the matcher picks the first fit; do not apply two recipes to one incident.
- Self-applying a medium+ fix without review — medium+ always goes through 2-of-2 consensus first.
- Inventing or inlining a secret when R5 matches — the fix is to ask the owner, not to guess the key.
- Writing an INC record with a different format than the two seeded examples — mirror them field-for-field.
- Treating `no-match` as low risk — no-match is escalated, never improvised.

## Verification

- For each blocked/gave_up task processed, an INC record exists in `operations/incidents/` with all frontmatter fields present and a recipe id (or `no-match`).
- The INC id is also commented on the kanban task.
- Low-risk matches have an applied fix and the task is unblocked; medium+ matches have a review handoff and the task is blocked with a note.
- The recipe table's match clauses are checked in order and only the first fit is applied.
- No secret was invented or inlined for any R5 match.
