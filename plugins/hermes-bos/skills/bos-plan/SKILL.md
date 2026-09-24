---
name: bos-plan
description: Decompose an approved work item into bounded, gated tasks.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-plan Skill

Decompose one owner-approved work item into bounded tasks, each with an owner
seat, a concrete output artifact, dependencies, a testable done condition, and
any approval gates its actions imply. This skill only writes the plan and
updates the work item's status — it never executes tasks, assigns work beyond
a seat's authority-matrix ceiling, approves its own plan, or commits to Git
(the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Plan carrier: `operations/work-items/<ID>-plan.md`, referenced from the work
  item (the work item stays the canonical state per the root `AGENTS.md`).

## Use when

Use when a work item the owner has approved to plan (status `approved`, or an
explicit go-ahead recorded in the item) needs a decomposition before
execution. Not for intake or clarification (that is `bos-intake` territory),
not for execution, and not for judging results (that is `bos-quality-gate`).

## Inputs

- Work item ID or path (`operations/work-items/WI-*.md`)
- Available seats (from `constitution/authority-matrix.md`) — owners are
  assigned from this roster, never invented
- Any constraints already recorded in the work item (deadline, budget, scope)

## Procedure

1. **Think from the end first.** Before writing a single task, state in one short
   paragraph what *done* looks like for this work item: the final outcome, the
   canonical artifact(s) it produces, and — crucially — how you will
   **verify** at the end that it actually worked (not just that you shipped
   something). Write this as the plan's `# Verification plan` block before the
   task list, so the decomposer is accountable to its own bar. The verifier is
   a separate seat (`bos-quality-gate`) unless the item is low-risk and
   self-verifiable by `read_file` against `constitution/definition-of-done.md`.
2. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, the work item itself, `constitution/authority-matrix.md`,
   `constitution/risk-policy.md`, `constitution/definition-of-done.md`, and
   `constitution/escalation-policy.md`.
3. Confirm the item is ready to plan: status `approved`, acceptance criteria
   present, no open question that changes scope, risk, or acceptance. If not,
   stop and set `status: clarify` (or `escalated` with a `why` line) instead
   of planning around gaps.
4. Derive one task per deliverable unit of work — small enough that its done
   condition is checkable by `read_file` on its output artifact. Cover every
   acceptance criterion with at least one task's done condition.
5. Fill each task with the fields below. Assign owners only from the
   authority matrix; a delegated task's owner must hold the class the task's
   actions imply (a subagent inherits its delegator's ceiling — matrix rule
   2). If no seat holds the required authority, that task becomes an
   escalation, not a guess.
6. Turn every implied `EXTERNAL` or `IRREVERSIBLE` action into an explicit
   gate task whose done condition is the recorded per-instance yes (and, for
   `IRREVERSIBLE`, an accepted `DEC-*` record per the risk policy). Gates
   must sort before the tasks that depend on them; deny-on-silence — a draft
   or silence is never consent, so a gate task is never auto-completed.
7. Check the dependency graph is acyclic and every task is reachable from the
   work item's outcome. Order tasks topologically.
8. Write the plan with `patch` to `operations/work-items/<ID>-plan.md` using
   the format below. Then update the work item: add the plan path to
   `evidence`, set `status: planned`, refresh `updated`.
9. Stop. Approval of the plan itself is the owner's act; record
   `Next approval required` on the work item (per-instance yes if any task is
   `EXTERNAL`/`IRREVERSIBLE`).

Verification plan block format (goes at the top of the plan file, before the
task list — this is the decomposer's end-state statement):

```markdown
# Verification plan

<one paragraph: what "done and working" means for this item, what the final
artifact(s) are, how you will verify end-to-end that it actually works (not
just that it was produced), and who performs the verification. Name the
verifier seat; for low-risk self-verifiable items this can be the producing
seat re-reading its output against `constitution/definition-of-done.md`.>
```

Task format:

```markdown
- id: <ID>-T<NN>
  owner: <seat from the authority matrix>
  output: <canonical file path the task produces>
  depends_on: [<task ids> | none]
  done: <testable condition, verifiable by reading `output`>
  approval_gate: <none | class + approver + recorded-yes condition>
```

## Output

Return the plan path, the **verification plan** (the end-state statement from
step 1, written up front so the decomposer is accountable to its own bar), the
task count, the task table (id, owner, done), the gate list with their required
approvals, any tasks that could not be assigned within the matrix (escalations),
and the work item's updated status.

## Failure modes

- Do not plan around unlabeled assumptions — push them back to the work
  item's open questions first.
- Do not assign owners outside the authority matrix or above a seat's class.
- Do not let a task's implied actions exceed its gate; burying an `EXTERNAL`
  step inside a `WRITE_INTERNAL` task is a defect the gate will catch.
- Do not mark the plan approved — planning is `WRITE_INTERNAL`, approval is
  the owner's.
- Do not commit, push, or rewrite Git history — the owner commits.
- If the authority matrix or risk policy is missing, stop and set the work
  item `status: escalated` with a `why` line; do not plan without governance.

## Verification

- Every acceptance criterion maps to at least one task's done condition.
- Test first: every task's done condition is a check (a command, a file assertion or a
  rubric line) written BEFORE the work; the task records it failing (RED), then passing (GREEN).
- No goal drift: the root's done condition quotes the requester's original goal verbatim. A
  task that proves only a narrower goal (e.g. "a proposal exists" for "make it work") is a
  defect; plan the verifying run instead, or ask.
- Every task owner appears in the authority matrix with the implied class.
- Dependency graph is acyclic; gate tasks precede their dependents.
- Plan file exists at `operations/work-items/<ID>-plan.md` and `read_file`
  returns it; the work item links it and shows `status: planned`.
- No `EXTERNAL`/`IRREVERSIBLE` action was executed — implied ones are gates.
- The plan file begins with a `# Verification plan` block that states the
  end state, the artifact(s), and the verification method — not just a task
  list.
