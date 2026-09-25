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

## Owner-correction trigger (Paul, 2026-09-24)

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

## Self-detected incident loop (Paul, 2026-09-25): the team finds and fixes its own failures

Paul, 2026-09-25 16:55: "they should be able to realise they are failing; they should initiate the
incident management and find a solution through group discussions … or even LDJ; they should
schedule and overview experiment/solution and revise if needed." Nobody waits for Paul to notice.
A no-match or a repeated failure is not escalated as it is: it enters this loop.

**1. Detect (any seat, and the stuck-guardian sweep as the safety net).** Open the loop when:
- T1: the same goal has failed on 2+ attempts (retries of one card, or sibling redo cards with the same goal; gave_up, crashed, protocol_violation, block_loop_detected, a worker stopping on its own failure rule, or an overseer/reviewer FAIL);
- T2: a reviewer finds an invented value, a self-review, or a narrowed goal;
- T3: the recipe table has no match.
The seat that notices creates ONE incident card itself: assignee kanban-orchestrator, idempotency key
`incident-<YYYYMMDD>-<goal-slug>`, body = the goal, every failed attempt (card id, run id, the
verbatim error with its time), and what was already tried. It blocks its own card with a link (a comment, never a parent link: a child waits for its parent to finish, and a stuck card never does). It
does not retry the same approach a third time.
Create the incident card with `--model hermes-premium` (the synthesizer decides; a free model skipped the whole
loop on 2026-09-25). In the SAME step create its closing gate: a review card, assignee quality-guardian,
`--parent <incident card>`, whose body is the closure proof:
- the swarm cards for this incident key exist and finished;
- an `EXPERIMENT:` card exists and its own review card passed;
- the ORIGINAL goal's metric, copied from the failing card's body (e.g. "57 chats deleted"), is met: quote the number from the artifact, not from a summary. Or: a reproduced cause proves the goal infeasible, and the incident is blocked for Paul with that evidence.
A closing summary that redefines the goal ("deletion phase done" with 0 deleted) is a FAIL: the reviewer opens a new incident (T2, narrowed goal) and links it. The orchestrator never judges its own incident closed.

**2. Investigate and discuss: agent-LDJ as a kanban swarm** (LDJ eval 2026-09-22 "ADAPT"; blind
writing beats debate, arXiv 2508.17536 and Diversity Collapse ACL 2026; agent dot-votes failed 0/3
in `Topics/management-methodologies.md`, so scores and a named decider replace the vote). The
orchestrator runs:
`hermes kanban swarm "<incident goal>" --worker researcher:"Blind A: what the runs actually did":five-whys --worker researcher:"Blind B: cause hypotheses from the tools and UI":five-whys,ego-browser --worker quality-guardian:"Blind C: cause hypotheses from skills, config and the card":five-whys --verifier quality-guardian --synthesizer kanban-orchestrator --tenant HERM --idempotency-key <incident key>-swarm`
- Each worker writes BLIND (never reads the other workers' notes): ≤ 3 problems and ≤ 3 fixes, each with an evidence path, and a 1–5 impact and 1–5 effort score. Every worker prompt carries the line: "Generate causes and fixes substantially different from the obvious one."
- A cause is a HYPOTHESIS until reproduced (automatic failure attribution finds the failing step only 14% of the time, arXiv 2505.00212). The verifier reproduces the top hypotheses and marks each reproduced / not reproduced, with the command and output.
- Models: the blind workers may run on the seat default (cheap and independent). The VERIFIER and the SYNTHESIZER make the judgments, so pin both to the strong model: `hermes kanban set-model <card> hermes-premium`, or create them with `--model hermes-premium`. On 2026-09-25 both were created on the free default and the overseer had to pin them; the free model had already skipped this loop once.
- The synthesizer is the named decider. It follows the `ldj` skill: take median scores, pick ONE problem, reframe it as "How might we …", place fixes on the impact/effort grid, and choose ONE experiment. Dissent is kept in the record.

**3. Experiment** (schema from `j-designing-experiments`). The synthesizer creates an `EXPERIMENT:` card: hypothesis, the one change, the metric with pass / fail / inconclusive thresholds, a timebox (one run or one day), budget, owner seat, rollback rule. It also creates a SEPARATE review card (assignee quality-guardian, `--parent <experiment card>`) with the proof command. Anything irreversible (deleting, sending, spending) runs first on a sample the owner approved, never on the full set.

**4. Revise.**
- PASS: the lesson becomes a new row in the recipe table below plus one fixture (a real input and expected outcome in `fixtures/`), proposed through `bos-skill-improvement` as a staged diff (skill text: the overseer approves; config or SOUL: Paul approves). Log expected vs actual with `j-learning-from-decisions`. Schedule one re-check card with `hermes kanban schedule` (critical: 7 days; others: 30 days); PASS there = zero recurrence.
- FAIL or inconclusive: the next-ranked hypothesis becomes the next experiment. After 3 experiments without a PASS, block the incident card for Paul with the full evidence (every hypothesis, reproduction result and experiment outcome) and one recommended next step.
- Record the whole loop in the incident file (`INC-YYYYMMDDNN.md`), appending one section per step (house rule 5: never overwrite).

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
5. If the cause has appeared 3+ times across INC records, or the recipe table has no match, open the self-detected incident loop (above).

## Quick Reference

### Recipe matcher

For each blocked/gave_up task, scan the failure text and worker logs for the patterns in the table below, in order. Pick the **first** recipe whose match clause fits. If none fit, classify as `no-match` and open the self-detected incident loop (never improvise a fix outside it).

### Risk → action

| Risk | Action |
|---|---|
| low | Apply the fix directly, then unblock the task. |
| medium or higher | Draft the fix, `kanban_request_review` to quality-guardian, then the owner approves (item assigned to Paul). Never self-apply. |

## Procedure

### 1. Read the failure

Pull the task's `last_failure_error`, any `gave_up` event payload, and the most recent worker log lines. Treat the error text as the primary match signal; log lines are secondary context (e.g. `Unknown skill(s)`, `Unknown toolsets`, model 404).

### 2. Match against the recipe table

Scan the failure text top-to-bottom against the match clauses below. Return the **first** recipe whose match clause fits. If none fit, classify as `no-match` and open the self-detected incident loop (never improvise a fix outside it).

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

Scan existing INC records for the same cause. If the cause has appeared 3+ times, open the self-detected incident loop (above); the swarm runs there and is not proposed to the owner.

## Pitfalls

- Matching more than one recipe — the matcher picks the first fit; do not apply two recipes to one incident.
- Self-applying a medium+ fix without review — medium+ always goes through 2-of-2 consensus first.
- Inventing or inlining a secret when R5 matches — the fix is to ask the owner, not to guess the key.
- Writing an INC record with a different format than the two seeded examples — mirror them field-for-field.
- Closing an incident by redefining its goal. Incident t_4aeb0a3f (2026-09-25) was marked "loop CLOSED, deletion phase done" with 0 of 57 chats deleted and no swarm or experiment. The closing gate above exists because of it.
- Treating `no-match` as low risk. A no-match is never improvised: it goes to the self-detected incident loop, where the fix comes from the discussion and is proven by an experiment.

## Verification

- For each blocked/gave_up task processed, an INC record exists in `operations/incidents/` with all frontmatter fields present and a recipe id (or `no-match`).
- The INC id is also commented on the kanban task.
- Low-risk matches have an applied fix and the task is unblocked; medium+ matches have a review handoff and the task is blocked with a note.
- The recipe table's match clauses are checked in order and only the first fit is applied.
- No secret was invented or inlined for any R5 match.
