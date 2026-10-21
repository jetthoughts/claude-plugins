---
name: bos-closing-review
description: Refuse closure of an initiative or card until the 6-dimension × boundary-aware matrix passes against on-disk evidence in the same turn.
version: 0.1.0
author: pftg
platforms: [macos]
status: draft — pending RA peer-review
source_incident: INC-20261001-silent-completion-pattern
---

# bos-closing-review Skill

Worker-level refusal gate for any closure claim on a card, initiative, or
incident. Runs a **6-dimension × boundary-aware cross-check** before the
worker can transition the work item to a terminal state. Refuses the
transition if any dimension fails or if no seat in the room can verify a
dimension in the same turn.

The skill exists because the silent-completion pattern — a status claim
that contradicts an inspectable layer of state, accepted by gate-keepers
without checking — survives one echo. Any single closing-gate writer who
copies a prior claim without re-running the matrix reproduces the defect.
The skill makes re-running the matrix cheaper than copying.

## Use when

- Any worker attempts to transition a kanban card to a terminal state
  (`done`, `closed`, `accepted`, or equivalent) on any seat.
- Any agent writes a "PASS" / "shipped" / "closed" verdict for an
  initiative, incident, or shape-up summary.
- Any room discussion writes an acceptance gate at @user.

Not for: live operator actions (those go through `t_867424a0`-style
operator-action cards with paired verifier cards), config flips
(those go through PROPOSAL-* cards with pre-flight rules), or anything
the worker level cannot gate because it cannot run the underlying action.

## Why this is a separate skill, not a fold into `bos-quality-gate`

`bos-quality-gate` is per-task (PASS/FAIL on one artifact). Closing review
is per-initiative (cross-card, cross-system, multi-artifact, multi-system).
Different unit of work, different verb. Folding the two muddies the unit
and makes per-initiative gates harder to audit. CoS, OC, and the DM
incident card body (`INC-20261001-silent-completion-pattern` §165-184) are
explicit on this fork.

## Inputs

- Work-item ID or initiative ID being closed.
- The closing claim (verdict field, status transition, or prose summary).
- The producer seat (Hermes profile or human) attempting the closure.
- The producer's `result.artifacts` declaration if present.

## Procedure (6 dimensions, all required, no partial passes)

For each dimension, the skill runs an on-disk check and records the
**path `ls`'d in this turn** in the verdict file. A dimension passes only
if (a) the check succeeds against real artifacts and (b) at least one seat
in the room can independently re-run the check. If no seat can re-run a
dimension, the skill refuses closure and requires a verifier card with
pre-state + post-state sentinels (see `verifier-card discipline` below).

### Dimension 1 — DB card status

`hermes kanban show <id>` (or equivalent). Record status field, completed
timestamp, assignee. Pass: status = the closing claim's terminal value.

### Dimension 2 — Card body vs DB status

Read the card body. Compare to DB status. Pass: body text agrees with
status field (e.g., body says "applied 2026-10-01" and DB says `done`; not
"awaiting approval" and DB says `done`). Fail is case-in-point #2 in
INC-20261001-silent-completion-pattern — `t_b398410f` body says "awaiting
Paul approval" while DB says `done`.

### Dimension 3 — `result.artifacts` declaration

Read the producer's `result.artifacts` list. Each declared path is a
Dimension-4 candidate. Pass: every declared artifact has a resolvable
path. Fail: zero elements declared when the work item claims to produce
artifacts (a gap, not just a fail).

### Dimension 4 — File on disk at declared paths

For each declared path in Dimension 3: `ls -la <path>`. Record mtime, size,
file_type. Pass: every path resolves to a real file/dir matching the
producer's description. Fail is case-in-point #1 in the incident card —
three phantom paths in the original Rocks overview.

### Dimension 5 — INC linked-card status

If the work item links an INC card (via `incident: <id>` in frontmatter
or a comment), `ls` the INC file in `business-os/operations/incidents/`.
Read its `status:` field. Pass: `status: closed` with closure evidence on
disk. Fail: INC open while card is closing (this is the
INC-2026100101-vs-disk pattern the watchdog cleanup caught).

### Dimension 5b — Verdict-dishonesty gate (recipe 0 enforcement)

For any closing review or retrospective that writes a verdict file under
`business-os/evaluations/` or `business-os/functions/quality/`, the worker
MUST run the verdict-dishonesty verifier on the artifact before
`kanban_complete` is allowed:

```bash
python3 scripts/check_verdict_dishonesty.py <verdict-file>
```

**Trigger pattern**: a line at the start of the verdict file declaring
`**Verdict: PASS**` (case-insensitive, anchored to start of line —
also matches `**Verdict:** **PASS (5/5)**`, `**PASS (5/5).**`, and
other bold-PASS headline forms) AND either a Markdown table row whose
`status` column cell contains one of `gap`, `partial-pass`,
`fail-uncertain`, `hedge`, `open-behind-hardstop`, `open-behind-block`,
OR a prose-narrative line containing any of:

- `remains open`
- `metric (remains )?(open|unmet)`
- `contract (text )?(is|does not|doesn't|does not) (satisfy|satisfies|close(s)?|meet(s)?)`
- `open-behind-(hardstop|hard-stop|block)`
- `path (b) ... (blocked|hardstop|hard-stop)`
- `do(es) not (close|satisfy|meet) (the )?runtime`
- `runtime-enforcement metric`

**Refusal**: exit 1 with per-row AND per-prose-line diagnostics naming
the file, line number, criterion id (for rows) or matched text (for
prose), and the offending status. The card's `kanban_complete` is
blocked on non-zero exit.

**Override**: requires an explicit comment of the form
`OVERRIDE: verdict-with-gap approved by <role> at <iso>` and re-running
the verifier after the override comment is added. Override is logged
in the verdict file's comment thread.

**Why this is a separate sub-dimension, not fold-into step 2**: the 6
dimensions check cross-card and cross-system claims; 5b is a
single-file self-consistency check on the verdict file itself. A
dishonest verdict (PASS + gap) was the 12th-iteration re-emergence of the
recipe 0 closing-defect lineage (per memory `mem_adaac499b383`); the
durable prevention is a verifier at verdict-file write time, not a
card-state reminder.

**Why narrative gaps are included**: the original verifier scanned
only table cells, but the recipe-0 closing-defect lineage includes a
sub-pattern where the matrix cells all say "PASS" while the prose
narrative explicitly says the original metric remains open ("runtime
metric remains open", "contract text does not satisfy the runtime
gate"). Such a verdict file reads as PASS to a casual reader and slips
past a cell-only gate. The narrative gap check catches both forms.
Verified against historical defects: `t_a0e858ec` (2026-10-11) and
`t_6afc32f4` (2026-10-11) both FAIL the narrative-gap check; the
incident `INC-2026101101` records this as the recipe-0 13th iteration
and links the verifier's expanded regex as the durable prevention
(Paul-closed by `t_f8c78940`, ASSUMPTION: hermes-agent runtime gate
remains blocked on the external-publication hard stop; rollback =
`git -C /Users/pftg/dev/claude-plugins revert eca6964`).

### Dimension 6 — Parent task verdict reconciliation

If the work item has parent tasks (`parents[].*` in kanban, or
`parent_card:` in frontmatter), read each parent's latest summary /
verdict field. Pass: every parent's verdict agrees with the closing
claim's verdict (e.g., parent says "CONDITIONAL PASS", child says
"CONDITIONAL PASS"; not parent says "CONDITIONAL PASS" and child says
"PASS"). Fail is the CoS R3 correction — parent `t_4ca8812e` summary
read "CONDITIONAL PASS" while the closing claim read "PASS".

## Boundary awareness (per OC and CoS)

For each of the 6 dimensions, name who can run the check from their seat:

| Dimension | Who can run | Boundary class |
|---|---|---|
| 1. DB card status | any worker with `kanban` tool access | none — universal |
| 2. Card body vs DB status | any worker with `kanban` + `read_file` | none — universal |
| 3. `result.artifacts` declaration | the producer seat only | producer-only |
| 4. File on disk | any seat with `terminal` access to the file's host | verifier-only if the artifact is on an operator host |
| 5. INC linked-card status | any worker with `terminal` access to `business-os/operations/incidents/` | verifier-only if the INC is in a vault the closing seat cannot read |
| 6. Parent task verdict reconciliation | any worker with `kanban` access to parent IDs | none if parent IDs are public |

If no seat in the room can re-run a dimension in the same turn, the skill
**refuses closure** and requires a verifier card with pre-state + post-state
sentinels. The verifier card must (a) run the dimension with sentinel
outputs (`OK: not registered` / `OK: gone` / etc., as in `t_96085284`),
(b) be assigned to a seat that can re-run the check, and (c) post its
result as a comment on the producer card before the producer's closure
attempt.

This is the **verifier-card discipline** subsection below.

## Worker-level refusal (default path)

When a worker attempts to mark a card `done`, `closed`, or any terminal
state on any seat, the worker runs this skill first. The skill:

1. Executes all 6 dimensions.
2. If any dimension fails OR has no verifiable seat in the room, refuses
   the transition with a defect list citing the failing dimension, the
   path it `ls`'d, and the boundary class that gates verification.
3. Records the refusal in the work item's comment log.
4. The worker reports the refusal in its task summary; the gate is mine
   (OC), the skill spec is mine (DM drafts, RA peer-reviews).

Same shape as `bin/verify-sprint-round` refusing structurally invalid
input. The skill does not judge quality — it refuses incomplete or
unverifiable claims.

## Verifier-card discipline (destructive-ops subsection)

The worker-level refusal is the right gate for the **normal closure path**.
It is NOT the right gate for the **destructive-ops path** — operator-action
cards (`launchctl unload`, `rm` of LaunchAgent artifacts, any command
that touches launchd). Two reasons:

1. The worker cannot run destructive ops at all. Two gates in series:
   worker fence (runtime block) + house rule 12 (policy).
2. Running destructive ops requires the operator's `session context`, which
   is not visible to the worker.

For destructive ops the skill requires:

1. **Pre-state capture** on the operator-action card body (e.g.,
   `launchctl list | grep -i watchdog`, `ls -la ~/.infra/bin/hermes-watchdog`,
   `ls -la ~/Library/LaunchAgents/*.plist`) recorded BEFORE the op runs.
2. **Operator-action card** with explicit boundary citation (e.g.,
   "Runtime fence + house rule 12 + single-query mode block this from
   worker context; operator runs in interactive terminal.").
3. **Verifier card** auto-created as the operator-action card's child.
   Verifier card runs post-state checks with sentinel outputs
   (`OK: not registered` / `OK: gone` / `OK: gone`).
4. **PASS only on sentinel match.** Any non-zero exit or non-sentinel output
   returns FAIL with the failing command + the operator-action card id,
   so the operator can re-run the missing step.

Positive control: `t_867424a0` (operator-action, done 17:24 by
delivery-manager) + `t_96085284` (verifier, done 17:30 by quality-guardian,
3 sentinels PASS). INC-20261001-silent-completion-pattern §135-155.

## Meta-loop check (CoS addition)

For every closing review, the skill asks:

> "This card closes an incident in class X — does the fix's own closure
> evidence avoid class X?"

If the proposed fix's evidence is in the same defect class as the
incident it closes, the skill flags it. Precedent: INC-2026100101 (silent
watchdog) → PROPOSAL-021 (silent register-then-unregister with zero
observable output). The fix recapitulated the bug. The skill must catch
this at write time, not after the next incident in the class.

## CoS Edit 1 — load-time gate for LaunchAgents and cron prompts

NOT in scope of this skill. Separate work, owner: chief-of-staff proposes,
governance-auditor rules on persona scope, delivery-manager implements.

The shape: a load-time structural check on `~/Library/LaunchAgents/*.plist`
that rejects any plist whose body lacks an `EnvironmentVariables` block
when the script invokes `hermes` or `~/.infra/bin/*`. Same shape for cron
prompts: a cron-template reviewer rejects any prompt body lacking an
evidence-step command. kanban-orchestrator applies it (apply, commit,
quality-guardian review after; `~/.hermes/governance/escalation-policy.md`).

## Failure modes

- Do not modify the closing claim to make it pass. The gate that grades
  is not the hand that fixes.
- Do not approve work produced by the same seat running the gate (same
  rule as `bos-quality-gate`).
- Do not perform destructive ops to satisfy Dimension 4. The
  verifier-card discipline is the only path that runs destructive ops.
- Do not invent paths to satisfy Dimension 4. Every path recorded in the
  verdict file must be one the worker `ls`'d in the same turn.
- If the work item's parent / INC / artifact path is unreadable from
  the closing seat's sandbox, refuse closure with a verifier-card
  requirement; do not silently proceed.

## Verification

- Re-running the 6 dimensions reproduces the identical defect list.
- Every defect cites (1) which dimension, (2) the path / kanban id it
  observed, (3) the boundary class that gates verification.
- Verdict is consistent with the rule: `PASS` iff all 6 dimensions pass
  AND at least one seat in the room can independently re-run each
  dimension. `FAIL` otherwise.
- The skill's verdict file lands in `business-os/operations/reviews/`
  with a path the OC can `ls` in the next turn.

## Source of truth

- Incident: `business-os/operations/incidents/INC-20261001-silent-completion-pattern.md`
  (3 cases today, threshold met, self-detected loop open).
- Positive control: `t_867424a0` + `t_96085284` (INC-2026100101 cleanup).
- Origin discussion: All-hands chat 2026-10-01 (this room).

## Status

Drafted 2026-10-01 by delivery-manager. Pending: (a) RA peer-review of
the 6-dimension matrix against real kanban data; (b) one real closing
review run against INC-2026100101 closure using this skill to prove the
contract catches the failure on real artifacts; (c) @user approval on
single-skill scope vs. two-skill split (recommendation: single skill,
single verb, single contract).