# Changelog

## 0.4.0 - 2026-09-24

- `contract` §10, no-code work: research, choose and configure tools with risk
  tiers (the owner approves the exact change for anything paid, external,
  shared-config or irreversible), snapshot, dry-run, apply exactly, read back,
  and three extra checker lines. `/innovate` kicks it off. A separate
  innovation-cycle skill was drafted, then folded in here, because a second copy
  of the rules drifts (cold review, 2026-09-24).
- `contract` §5: the default reviewer is `j-cold-eyes-reviewer`
  (`cold-reviewer` does not exist).
  Research: pkm `business-os/knowledge/research/2026-09-24-agile-innovation-cycle-no-code.md`.

## 0.3.0 - 2026-09-03

- New `board-flow` skill: the JetThoughts Kanban delivery flow for agents and
  sessions — Backlog → Ready → In Progress → Code Review → Verify → Done, pull
  right-to-left and top-to-bottom, one card In Progress per worker, two in
  flight, never move back, split at the time box, the ordered WIP-limit list
  (help reviews first, never new logic), bugs zero, stale cards, violations
  reported before they happen. `references/boards.md` maps the lists onto
  Paperclip, Linear, GitHub Projects, markdown kanban and a session TODO list.
  Source: the "Delivery Flow for Distributed Remote Teams" and "WIP limit
  reached" posts. `contract` §6 and `/deliver` now point at it.

## 0.2.0 - 2026-08-21

- Core agents gain methodology stances (operator request): XP for
  coder/reviewer/tester (test-first, small safe steps, stop-the-line),
  Shape Up for planner (fat-marker shaping, appetite not estimate,
  circuit breaker, vertical slices), Lean for researcher and flow
  (validated learning, riskiest-assumption-first, finish over start).


## 0.1.0 - 2026-08-21

Initial extraction per jetthoughts.github.io ADR-0005.

- `contract` skill: the delivery contract (GOAL/intake, DISCOVER-to-LEARN
  loop, evidence standard, 4-eyes, WIP=1, async-first, scope, learn) -
  genericized from docs/workflows/autonomous-delivery-prompt.md par.1-9.
- `/deliver` command: kickoff parameterized by $ARGUMENTS.
- `async-first` skill: communication SOP.
- Core agents: coder, reviewer, researcher, planner, tester (author/verifier
  roles).
- Precedence: consuming-repo instructions override the plugin everywhere.
