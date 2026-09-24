---
name: bos-delegate
description: Write strict subagent briefs and consolidate results.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-delegate Skill

Construct a strict, self-contained brief for one delegated subagent run and,
on return, consolidate results against the brief's done condition with
conflicts surfaced rather than silently resolved. The brief is a contract:
the subagent gets exactly the inputs, ceiling, and return format it needs and
nothing beyond. This skill constructs and consolidates — it never grades the
final artifact (author ≠ verifier; `bos-quality-gate` applies the gate) and
never commits to Git.

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Delegation primitive: `delegate_task`; a subagent inherits the delegator's
  ceiling and never exceeds it (authority-matrix rule 2).

## Use when

Use when a planned task from a `bos-plan` decomposition (or an equivalent
bounded request) is ready to hand to a subagent — parallelizable work,
isolated investigation, or a deliverable better produced in a fresh context.
Not for `EXTERNAL` or `IRREVERSIBLE` actions (those stop at their gate), not
for grading results, and not for work the delegating seat could not itself
do.

## Inputs

- Task definition: task id, done condition, output path (from the plan)
- Owning work item ID (context and acceptance criteria)
- Running seat (determines the ceiling the brief inherits)

## Procedure

1. Read with `read_file`: the Business OS root `AGENTS.md`, the work item,
   the plan (`operations/work-items/<ID>-plan.md` if it exists),
   `constitution/authority-matrix.md`, and `constitution/risk-policy.md`.
2. Confirm the task's class: anything implying `EXTERNAL` or `IRREVERSIBLE`
   action is not delegable — stop at the gate instead (deny-on-silence).
3. Write the brief as a single self-contained prompt (no reliance on chat
   history — the file is the record) with exactly these sections:
   - **Context** — one paragraph: why, work item ID, venture.
   - **Inputs** — exact paths to read with `read_file` before starting;
     nothing required that is not listed.
   - **Task** — one bounded outcome, phrased as the artifact to produce.
   - **Constraints** — the inherited ceiling (classes allowed and forbidden),
     explicit stop conditions (missing input, authority doubt, repeated
     failure of the same step twice), and the hard rules: no external
     contact, no commits or pushes, no invented facts.
   - **Verification** — how the subagent checks its own output before
     returning (done condition, schema, links resolve).
   - **Return format** — `result` (done | partial | blocked), `artifacts`
     (paths written), `evidence` (source path or URL per material claim),
     `deviations` (what differed from the brief and why), `open_questions`.
4. Launch with `delegate_task`, one brief per subagent. Run independent
   briefs in parallel only when the plan shows no dependency between them.
5. On return, consolidate: check each return against the brief's done
   condition; reconcile artifacts and evidence; list deviations. Where two
   returns disagree on a material fact, keep both claims side by side with
   their evidence and mark the conflict unresolved — never pick silently.
6. Record the outcome on the owning work item (`evidence` plus a one-line
   result per task; `status` moves per the plan). Set `status: escalated`
   with a `why` line if a subagent exceeded its ceiling, produced an implied
   external action, or a material conflict needs the owner.

## Output

Return the consolidation table (task id, result, artifact paths), the
deviation list, the explicit conflict list (both positions + evidence +
"unresolved" marker), any ceiling breaches, and the work item's updated
state. If everything reconciled, say so in one line.

## Failure modes

- Do not brief beyond the delegator's own ceiling — inheritance flows down,
  never up.
- Do not let the brief depend on conversation context; a subagent gets files,
  not memories.
- Do not merge conflicting returns into a single smoothed answer; surface the
  conflict or escalate it.
- Do not treat a subagent's self-report as verification; the quality gate
  applies independently (author ≠ verifier).
- Do not fire-and-forget: every launched brief is consolidated or escalated
  in the same run.
- If the subagent returns secret-looking material (keys, tokens, personal
  data), do not write it to the repo — record the env var name only, per the
  risk policy.

## Verification

- Every brief had all six sections; every launched brief has a consolidated
  return or an escalation entry.
- Every returned artifact path exists (`read_file` or
  `search_files target='files'`).
- Material conflicts are listed with both positions and evidence — zero
  silently resolved disagreements.
- No `EXTERNAL`/`IRREVERSIBLE` action appears anywhere in the returns; the
  work item's evidence field links the new artifacts.
