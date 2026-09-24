---
name: bos-progress-report
description: Shape Up progress report per initiative, kanban to PKM.
version: 0.2.0
author: Paul Foldvary-Ghosh (pftg), Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [bos, delivery, progress, shape-up, pkm]
    related_skills: [bos-lens-router, bos-intake, bos-daily-review]
---

# bos-progress-report Skill

Emit a Shape Up-style progress report per initiative into `~/dev/pkm/business-os/operations/reviews/`. One rolling index (`progress-board.md`) plus one per-pass file (`progress-YYYY-MM-DD.md`). The index is the single file the owner opens in Obsidian.

## When to Use

- Owner wants a read-on-open progress snapshot per initiative, Shape Up style.
- Scheduled: cron job `progress-board` on delivery-manager, weekdays 08:00 Europe/Berlin (owner approved 2026-09-23, card t_09c6761e).
- Manual pass: `hermes -p delivery-manager` and ask for a `bos-progress-report` pass.

## Prerequisites

- Read access to `~/.hermes/kanban.db` (task_links for parent/child grouping, tasks for status/age).
- Read access to `~/dev/pkm/business-os/operations/incidents/*.md` (INC records).
- Read access to `~/dev/pkm/business-os/evaluations/*.md` (verdict/memo files).
- Write access to `~/dev/pkm/business-os/operations/reviews/`.

## Shape Up report contract (per initiative)

Each initiative section carries:

- **Initiative name** — the epic's title and id.
- **Appetite** — epic / cycle / shapeless (ongoing), inferred from title; mark as inferred.
- **Scopes** — done / in-progress / not-started, each listing the member tasks with id + one-line title + status.
- **Hill position per scope** — uphill = figuring out (todo/blocked/planning), downhill = executing (running/in-progress), shipped = done.
- **Blockers / unknowns** — surfaced SEPARATELY from done work. Pull from:
  - kanban tasks with status `blocked` in the initiative.
  - INC records whose id prefix matches the initiative's date range or topic (read the INC files; carry the verdict line).
  - Open evaluation memos (status: DRAFT or verdict: adjust/needs-work) touching the initiative.
- **Next step** — the single most concrete next action, with owner if known. Prefer a blocked task's unlock condition, a todo child's first step, or the oldest aging running task's blocker.

## Data sources (local, read-only)

1. **kanban DB** — `~/.hermes/kanban.db`. Group tasks by initiative family via `task_links` (parent_id → children). Fall back to title-prefix matching when a parent is absent. Never read from memory for task state — the DB is the source of truth.
2. **INC records** — `~/dev/pkm/business-os/operations/incidents/*.md`. Read the files; carry id, title, status, verdict, date.
3. **Evaluations** — `~/dev/pkm/business-os/evaluations/*.md`. Read frontmatter (status, verdict) and the first heading; link the file.

## Initiative set

An initiative is a kanban task that has children in `task_links` (an epic). Report every epic that is open, or that closed in the last 7 days. Tasks with no parent and no children, created or closed in the last 7 days, go under one "Loose tasks" section. Never keep a fixed list of initiatives here: the DB decides.

## Decisions waiting on Paul

The top section of `progress-board.md`, above every initiative. The owner reads this first, so it lists only what needs his answer. One entry per open decision, from:

- tasks in `triage` (need approving or refining into a task);
- tasks whose latest block event has kind `needs_input`, open or not;
- tasks closed in the last 14 days whose summary or latest comment asks owner questions (Q1, "decisions needed", "owner calls", an unblock reply format) with no later owner comment answering them. A card closing does not answer its questions.

Each entry: task id + title, the questions in one line each with the seat's recommendation and default, the file that holds the detail, and the exact reply format if the seat gave one. When nothing is waiting, write "Nothing waiting on you." Never drop an entry because it is old; it leaves only when answered.

## Procedure

1. **Read the kanban DB initiative tree.** Query `task_links` + `tasks` for every epic in the initiative set and its children. Also pull the epic's own row, its latest summary and comments, and its block events. Compute per-initiative: total tasks, done, running, blocked, todo, and hill position (blocked → uphill; running → downhill; all done → shipped; else uphill).
2. **Read INC records.** List all files in `operations/incidents/`; read each frontmatter (id, title, status, verdict, date, risk). Attach each INC to the initiative it most closely matches by title keyword; if none matches, place under a "Cross-cutting" line.
3. **Read evaluation memos.** List `evaluations/*.md`; for each, read frontmatter + first heading. Attach to an initiative by title keyword; else cross-cutting.
4. **Collect decisions waiting on Paul** per the section above.
5. **Render the per-pass report** `progress-YYYY-MM-DD.md` using the Shape Up contract above. Today's date = the run date (use the local clock).
6. **Render the rolling index** `progress-board.md`. "Decisions waiting on Paul" first, then one section per initiative, current hill status, link to the latest report (today's file). Overwrite the index on every pass so it is always the latest view.

## Output files

- `~/dev/pkm/business-os/operations/reviews/progress-YYYY-MM-DD.md` — full per-pass report.
- `~/dev/pkm/business-os/operations/reviews/progress-board.md` — rolling index, one section per initiative, link to latest report.

## Acceptance

- `progress-board.md` opens with "Decisions waiting on Paul", then reads as a Shape Up update without needing explanation: initiative name, appetite, scopes with hill positions, blockers separated from done, next step — per initiative.
- Both files exist after a pass and the index links to the per-pass file.

## Verification

- Re-run the pass and confirm both files are overwritten with today's date.
- Open `progress-board.md` and confirm every open or recently closed epic in the DB has a section with hill status + link.
- Confirm a closed task with unanswered owner questions still shows under "Decisions waiting on Paul".
- Confirm blocked tasks and open INCs appear under a "Blockers / unknowns" line, not buried in done scopes.

## Pitfalls

- **Don't conflate parent status with initiative status.** A parent may be `done` while children are `running` — read the children.
- **Don't invent initiative parents.** A task without a parent link goes under "Loose tasks", not under a guessed epic.
- **INC verdict ≠ task status.** An INC can be `closed` with verdict `fixed` — carry that, don't re-derive it from task state.
- **Done is not decided.** A seat can close a card whose questions nobody answered (t_a2a5b807, 2026-09-23). Read the comments, not only the status.
- **The pass is read-only on the board.** Never edit cron jobs, answer questions, or change task state from this skill.
