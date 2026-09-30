---
name: bos-intake
description: Normalize a business request into a governed work item.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-intake Skill

Convert an unstructured business request into a typed, governed work item in
the Git-backed Business OS. This skill only classifies and writes the work
item — it never executes the work, contacts anyone, approves anything, or
commits to Git (the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Work items directory: `/Users/pftg/dev/pkm/business-os/operations/work-items/`
- Canonical format carrier: this skill (per the Business OS root `AGENTS.md`).

## Use when

Use for new goals, requests, opportunities, incidents, or ideas that are not
already represented by a work-item ID. If a work item already exists, update
that file instead of creating a new one.

## Inputs

- Original request (verbatim, from chat or a captured note)
- Requester and desired outcome
- Applicable venture and deadline (may be unknown — record as open questions,
  never invent them)

## Procedure

1. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, `constitution/mission.md`, `constitution/authority-matrix.md`,
   `constitution/risk-policy.md`, `constitution/definition-of-done.md`,
   `constitution/escalation-policy.md`, and `strategy/quarterly-bets.md`.
2. Separate explicit facts from assumptions. Every assumption must be labeled
   as one in the work item.
3. Ask only questions that materially change scope, risk, or acceptance.
4. Assign the work item's `approval` class per the authority matrix
   (`READ`, `DRAFT`, `WRITE_INTERNAL`, `EXTERNAL`, `IRREVERSIBLE`) and set
   `risk_class` consistently per the risk policy: Low = `READ`/`DRAFT`,
   Medium = `WRITE_INTERNAL`, High = `EXTERNAL`, Critical = `IRREVERSIBLE`.
   Draft-destiny rule: `DRAFT` only when the output stays a non-landed draft;
   if the requested artifact is destined for a canonical Business OS path
   (tools/, operations/, constitution/, knowledge/), classify at least
   `WRITE_INTERNAL` even when the request says "just a draft".
5. Fill `evidence` with the paths the request came from when they exist — the
   inbox item, fixture, or source note (e.g.
   `evaluations/fixtures/FIX-001-....md`). Inline-traced facts without a
   source path leave the DoD evidence criterion half-closed; an empty
   `evidence: []` is correct only for purely verbal requests.

   **Fixture stop condition.** If any evidence path falls under
   `evaluations/fixtures/`, or the source id matches `FIX-\d+`, set
   `source_class: fixture` on the work item and **stop** — do not write the
   work item as a normal intake. Route to quarantine: copy the WI to
   `evaluations/quarantine/` and escalate to the owner. A fixture-derived work
   item must never reach `operations/work-items/` without explicit owner
   approval. This guard runs before step 6; it is not a field to fill, it is a
   gate that halts the procedure.
6. Write the work item with `patch` at `operations/work-items/<ID>.md` using
   the canonical format below. Derive the ID as `WI-YYYYMMDDNN` (zero-based
   counter within the day) and confirm uniqueness with
   `search_files target='files'` in the work-items directory before writing.
7. Stop at an approval gate if an `EXTERNAL` or `IRREVERSIBLE` action is
   implied — deny-on-silence: a draft or no answer is never consent. Record
   the gate as the work item's next required action. If authority is missing
   or policies conflict, set `status: escalated` with a `why` line per the
   escalation policy.

Canonical work-item format:

```markdown
---
id: WI-YYYYMMDDNN
title: <one line>
status: intake
owner: <accountable role; unassigned at intake>
requester: <who asked>
risk_class: <low|medium|high|critical>
approval: <READ|DRAFT|WRITE_INTERNAL|EXTERNAL|IRREVERSIBLE>
source_class: <real|fixture|synthetic>
evidence: []
acceptance: [<testable condition>]
updated: <YYYY-MM-DD>
---

# <title>

## Outcome
<the desired business result>

## Facts
<explicit, verifiable statements from the request>

## Assumptions
<labeled guesses, each marked for confirmation>

## Constraints
<deadline, budget, scope limits — only if known>

## Open questions
<only those that change scope, risk, or acceptance>

## Next approval required
<none | class + approver>
```

Status vocabulary (from the root `AGENTS.md`):
`intake|clarify|planned|approved|executing|verify|recorded|closed|escalated`.

## Queue policy (owner, 2026-09-22)

Everything new lands in triage/queue — nothing is handled ad hoc, including
the owner's own ideas posted to kanban. Triage scores every item by
impact/effort (ICE-style: impact 1-5, effort 1-5, score = impact/effort) and
reprioritizes the queue on every pass; the score and its one-line rationale go
in the work item. Also write the score to the card's kanban `priority` as
round(score × 10) (impact 4 / effort 2 → 20): pass `priority` to `kanban_create`
on a new card, and use `hermes kanban edit <id> --priority N` when you re-score.
The dispatcher runs the highest `priority` first and uses age only to break ties,
so a score kept only in the text does nothing (owner, 2026-09-26). WIP limit: ONE active project/epic at a time — the next
project's tasks are not promoted until the current one is recorded or
escalated. Worker-level concurrency is enforced separately
(`kanban.max_in_progress: 2`).

### ICE vs category — two axes, not a replacement

Background, definitions and worked examples: see `references/ice-vs-category.md`.
The `category` field is written to the work item frontmatter by the
`kanban-orchestrator` seat at promotion. If it is missing, promotion is
rejected — a missing category is not a license to dispatch.

## Output

Return the work-item path, short brief, unresolved questions, risk class,
approval class, and the next approval required.

## Failure modes

- Do not invent deadlines, budgets, customers, or approval.
- Do not use chat history as authoritative state; the file is the record.
- Do not execute the work during intake.
- Do not commit, push, or rewrite Git history — the owner commits.
- If the Business OS root is missing, stop and report — do not scaffold it
  during intake.
- If a required constitution file is missing, record that as the first open
  question and set `risk_class: high` until governance is confirmed.

## Verification

- All frontmatter fields present; `status`, `risk_class`, `approval` values
  are from their canonical vocabularies.
- File exists at `operations/work-items/<ID>.md` and `read_file` returns it.
- ID is unique in the work-items directory.
- Every fact traces to the original request; every assumption is labeled.
- No `EXTERNAL`/`IRREVERSIBLE` action was taken — the item stops at its gate.

## Research and opportunity routing (added 2026-09-22)

Every intake item references the opportunity flow doc
(`business-os/strategy/opportunity-flow.md`). Rules:

1. Research artifacts from intake become `business-os/knowledge/research/YYYY-MM-DD-<slug>.md`
   (frontmatter `type: Research`, `topics`, `applies_to`, `confidence`, `status`) and are
   registered the same day in `business-os/knowledge/research/INDEX.md` — one table line.
2. `applies_to` holds forward wikilinks to initiative/project notes; never maintain
   reverse-link fields (Obsidian backlinks give the reverse view).
3. Un-evaluated ideas go to root `ideas-bank.md`, not the kanban queue. Kanban triage is
   only for evaluated, ICE-scored items (owner rule: nothing ad hoc).
4. If needed research for an intake item is missing, create a research task
   (assignee researcher, triage) — do not invent conclusions.
