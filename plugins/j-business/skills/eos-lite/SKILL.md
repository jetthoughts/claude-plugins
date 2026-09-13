---
name: "EOS-Lite Operating System"
description: "Run a lean EOS-lite operating-system loop for a solo founder / small operation: update the weekly scorecard, check quarterly OKR/KRs, advance 90-day rocks, run the Issues IDS list, and walk the pipeline over a project's docs/workflows/operating-system.md. Use when running a weekly ops/business review, updating the scorecard or OKR, grooming rocks/issues, checking the sales pipeline, or when the user says 'run the OS', 'weekly review', 'scorecard', 'ops loop', or invokes /eos-lite."
metadata:
  version: "1.0.0"
  user-invocable: true
  argument-hint: "[weekly|okr|rock|issue|pipeline] (default: weekly)"
---

# EOS-Lite Operating System

## What This Skill Does

Runs the weekly operating rhythm for a lean operation (a solo founder plus a white-label/partner
delivery arm and AI execution) directly against a project's `docs/workflows/operating-system.md`.
It keeps five things honest and current: the **scorecard**, the **quarterly OKR**, the **90-day
rocks**, the **Issues (IDS)** list, and the **pipeline** — and it refuses to mark work "done"
without an independent cold-eyes check. It automates the review loop, not the judgment.

## Prerequisites

- A project with `docs/workflows/operating-system.md` in the EOS-lite shape (accountability chart,
  quarterly OKR, rocks, weekly scorecard, issues/IDS, pipeline). If missing, offer to scaffold it
  from `templates/operating-system.md` shape.
- Real numbers for the week. This skill will NOT invent metrics — a blank cell stays blank and
  becomes an Issue, never a guessed value.

## Quick Start

```
/eos-lite weekly
```

Runs the full 30-minute loop below and writes updates back into `operating-system.md`.
Sub-commands run one section: `/eos-lite scorecard`, `/eos-lite okr`, `/eos-lite rock`,
`/eos-lite issue`, `/eos-lite pipeline`.

## The weekly loop (mode: weekly)

Do these in order. Read `operating-system.md` first; edit it in place; keep edits surgical.

1. **Scorecard (5 min)** — for each metric ask the user for this week's real number. Mark
   green (hit) / red (missed). Any metric red **two weeks running** → auto-create an Issue (step 4).
   Never fill a cell you don't have a number for; leave it blank + flag it.
2. **OKR (5 min)** — re-read the Objective + KRs. Update each KR's status against the scorecard.
   If a KR can't be measured (no wired data source), that's an Issue, not a status.
3. **Rocks (5 min)** — for each 90-day rock, confirm it has a named next action + owner. A rock
   with no next action is stalled → Issue. Flag any rock whose deadline is now unrealistic.
4. **Issues / IDS (10 min)** — Identify, Discuss, Solve. Solve only the **single highest-leverage**
   issue this week; don't let the list grow. Record the decision in the Issues table.
5. **Pipeline (5 min)** — walk each lead through the funnel stages. Update stages; surface the
   leading indicator that matters most (usually **discovery calls booked**). If the pipeline can't
   be measured (no booking link / CRM), that is the top Issue until fixed.

Then write a one-line dated summary. If the project keeps a `.okf/log.md`, append an entry there.

## The cold-eyes gate (BLOCKING)

This operation's rule is **4-eyes, calibrated by reversibility** (see the runbook it serves).
Before you mark any runbook card or rock "Done" on the user's behalf:

- INTERNAL / reversible (scorecard, pipeline, issue notes) → run a LIGHT devil's-advocate check:
  "does this reflect reality or a wishful number?"
- PUBLIC / irreversible / expensive (published copy, pricing, paid spend) → do NOT clear it here;
  route to the heavy gate (`reflexion-critique` / `.okf/workflows/review-swarm.md`).
- A card is Done only when the critic's verdict is pasted **verbatim** into its handoff note.

Never self-certify a "pass". If you did the work, you do not also grade it.

## Sub-commands

- `weekly` (default) — the full loop above.
- `scorecard` — step 1 only.
- `okr` — step 2 only; use `lark-okr` methodology for structuring/wording KRs.
- `rock` — step 3 only.
- `issue` — step 4 only (IDS one issue).
- `pipeline` — step 5 only.

## Templates & reference

- Weekly review structure: `templates/weekly-review.md`
- Scorecard shape: `templates/scorecard.md`
- Full method + anti-patterns (why blanks-not-guesses, why cold-eyes, one-issue-per-week):
  `references/eos-lite-methodology.md`

## Troubleshooting

- **No `operating-system.md`**: offer to scaffold it; don't run the loop against nothing.
- **User has no numbers**: leave cells blank, log an Issue "no data source for metric X" — the fix
  is wiring the source, not guessing.
- **Loop feels heavy for a solo founder**: that's expected only if the OS itself is bloated —
  the loop is ~30 min. If a section has no signal (e.g. single-KR OKR), touch it and move on.
