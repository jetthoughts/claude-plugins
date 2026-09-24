---
name: bos-daily-review
description: Summarize daily exceptions, blockers, and decisions needed.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-daily-review Skill

Produce the Chief of Staff daily review: a one-page reconciliation of
everything that needs attention today — exceptions, blocked or stale work
items, and decisions waiting on someone. The review only reads and
summarizes; it never edits work items, takes action, or commits to Git
(the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Reviews directory: `/Users/pftg/dev/pkm/business-os/operations/reviews/`
- Canonical format carrier: this skill

## Use when

Use at the start of the owner's day, after a batch of intake, or whenever a
current picture of "what needs attention" is requested. Not for grading
work (that is the `bos-quality-gate` skill) and not for executing fixes.

## Inputs

- Run date (default: today, `YYYY-MM-DD`)
- Seat (Hermes profile) producing the review
- Optional focus: a venture, function, or specific work-item set

## Procedure

1. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, `constitution/authority-matrix.md`,
   `constitution/escalation-policy.md`, and `constitution/risk-policy.md`.
2. Enumerate sources with `search_files target='files'`: every file in
   `operations/work-items/`, plus `operations/incidents/`,
   `operations/inbox/`, and `operations/decisions/` from the last 24 hours.
3. Classify each work item into exactly one bucket:
   - Exception — `status: escalated`, a linked incident, or a policy
     conflict named in the file.
   - Blocked — an active status (`planned|approved|executing|verify`)
     whose body names a blocker or a pending approval gate.
   - Stale — active status with `updated` 3 or more days before the run
     date.
   - Decision needed — a recorded `Next approval required` or open
     question that names who must answer.
4. Reconcile every entry against its source file: each table row cites the
   work-item path and the frontmatter value it relies on. The review reads
   only files — never memory or chat history as a source of state.
5. Write the review with `patch` at
   `operations/reviews/<YYYY-MM-DD>-daily.md`. If that file already exists,
   update it in place; never overwrite a different date's file.
6. List items whose implied action is `EXTERNAL` or `IRREVERSIBLE` under
   Decisions needed with the exact ask. Deny-on-silence: the review never
   treats silence or a draft as consent and takes no such action itself.

Daily review format:

```markdown
---
review: DAILY-<YYYY-MM-DD>
date: <YYYY-MM-DD>
seat: <profile>
work_items_total: <n>
exceptions: <n>
blocked: <n>
stale: <n>
decisions_needed: <n>
---

# Daily review — <YYYY-MM-DD>

## Exceptions
| Item | Why | Evidence |
|------|-----|----------|

## Blocked
| Item | Blocker since | Needed from |
|------|---------------|-------------|

## Stale
| Item | Last update | Status |
|------|-------------|--------|

## Decisions needed
| Item | Ask | From | By |
|------|-----|------|----|

## Owner summary
<one short paragraph: what was reviewed, where the review lives, what
needs the owner next>
```

## Output

Return the review path, the four bucket counts, the decisions-needed list
with the named decider, and the owner-summary paragraph.

## Failure modes

- Do not source state from memory or chat; every line reconciles to a
  file that `read_file` returns.
- Do not modify any work item, incident, inbox, or decision file — the
  review reports; state changes belong to the owning skill.
- Do not perform or trigger `EXTERNAL` / `IRREVERSIBLE` actions; flag them
  as decisions needed instead.
- Do not commit, push, or rewrite Git history — the owner commits.
- If the Business OS root is missing, stop and report — do not scaffold it.
- An empty day is a valid result: state "no exceptions" and keep the
  enumeration counts as evidence that the sources were checked.

## Verification

- File exists at `operations/reviews/<YYYY-MM-DD>-daily.md` and `read_file`
  returns complete frontmatter.
- Every table row cites a source path; `read_file` on that path shows the
  cited status.
- Bucket counts in the frontmatter equal the row counts in the sections.
- Re-running the enumeration against unchanged sources reproduces the same
  review content.
- No source file was modified — the review file is the only delta.
