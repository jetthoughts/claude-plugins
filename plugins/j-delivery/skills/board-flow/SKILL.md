---
name: board-flow
description: How agents and sessions coordinate work on a task board the JetThoughts way — Backlog → Ready → In Progress → Code Review → Verify → Done, pull right-to-left and top-to-bottom, one card in progress per agent, two in flight, never move a card back, split what outgrows its time box, and a fixed list of what to do when the WIP limit is hit. Use this whenever you pick the next task, move or comment on a card, report status, decide who acts next, or find a stale, blocked or oversized card — on Paperclip, Linear, GitHub Projects, a markdown kanban, or a plain TODO list — and whenever the user says board, kanban, backlog, ready, in progress, in review, WIP, sprint, stale, "what next" or "what should I pick up". Also use it when several agents share one board and someone must decide which card each takes.
---

# Board flow

The board is the team's shared memory of who does what next. Its lists are the delivery pipeline;
a card moves only forward; finishing beats starting. Everything below exists so that a cold
session, a second agent or Paul can look at the board and know the next action without asking.
Source: [Delivery Flow for Distributed Remote Teams](https://jetthoughts.com/blog/delivery-flow-for-distributed-remote-teams-agile-kanban/)
and [What to do when the WIP limit is reached](https://jetthoughts.com/blog/what-do-for-developer-when-wip-limit-reached-agile-kanban/).
The consuming repo's own board rules override this skill on conflict. Tool-specific status names
are in [references/boards.md](references/boards.md).

## The lists

| List | Meaning | Who moves a card in | Gate to leave |
|---|---|---|---|
| Backlog | wanted, ordered by the product owner or decision-maker | the owner | everything needed is written on the card |
| Ready | what will be delivered this week/sprint; built at kickoff by confirming detail and splitting top items into ≤2-day tasks | the team at kickoff | a `GOAL / DONE WHEN / NOT IN SCOPE` block a stranger could execute (contract §1) |
| In Progress | one card per worker, self-assigned from the top of Ready | the worker who pulls it | a diff or artifact exists and is handed to review |
| Code Review | a second pair of eyes reviews; the author never reviews own work | the author, when the artifact is ready | reviewer's written verdict with evidence (contract §5) |
| Verify | QA/operator confirms the change does what was asked and nothing else broke | the reviewer, on pass | the verifier's written confirmation; on a gated run, the human approval |
| Done | merged/approved/deployed | the human who holds the merge or approval | — |

Agent boards keep the same six lists even when the tool has fewer statuses: map them, do not drop them
(references/boards.md). "Blocked" is not a list: a blocked card stays where it is with a `Blocked by:` line
and the name of who acts next.

## Pull order: right to left, top to bottom

Take the rightmost list that has a card you can act on, then the top card in it. Code Review before Ready,
Verify before Code Review. The reason: a card in review is nearly done and costs the team a wait; a card in
Ready costs nothing until it is started. Starting new work while review queues grow is the bottleneck this
flow exists to prevent.

Moving a card: put it at the **bottom** of the next list so the tenth card stays tenth. A card labelled
**High** goes to the **top** of the next list instead. Never move a card back; if work must return (review
rejected, verification failed), it keeps its list and gains a comment saying what is missing and who acts.

## WIP limits — for agents as for people

| Limit | Value | What it is for |
|---|---|---|
| In Progress per worker | 1 | one thing finished beats two half-done |
| In flight per worker (In Progress → Done) | 2 | the second is waiting on review; a third means you are outrunning your reviewers |
| Time box per card | 2 working days for a person; one run (the `maxTurnsPerRun`/budget of the agent) for an agent | an alarm, not a deadline: it says "split this" |

Exceeding a limit is information: it shows the bottleneck (usually review). A limit is never silently
exceeded — report it on the card and act on the list below.

**When a card outgrows its box, split it in progress**: keep the part that can land now in the current
card, extract the rest into new Backlog cards, re-prioritise them, and say so in the card's comment.
Never let a card silently run into a second box.

## When you hit the WIP limit — in this order, and never new logic

First finish your own part: a card of yours that outgrew its box is split and its landable half handed to
review before anything else, because that is finishing, not starting, and it lowers your in-flight count.
Then, with nothing of yours left to push:

1. Help finish cards in Code Review or In Progress: review, propose a fix, ask the clarifying question,
   unblock. Finishing someone else's card moves the whole board.
2. Groom the Backlog: close stale or redundant cards, confirm the next cards have everything needed,
   ask the questions now so the next pull is clean.
3. Group related small cards into one epic so they flow as one unit.
4. Update documentation and agreements with what this week's questions revealed.
5. Small, non-critical, closeable changes (formatting, lint, a harmless upgrade) — last resort, rare.

Nothing on this list adds new features. A worker at the limit who starts new logic hides the bottleneck
instead of clearing it.

## Bugs zero

A critical bug that needs a hotfix stops the pipelines and is fixed first. Bugs walk the same lists
(Ready → In Progress → Code Review → Verify) with the **High** label, so they go to the top of each list
instead of the bottom.

## Stale cards

A card is stale when: an In Progress card has had no code or comment for two days · a card has no owner
of the next action · a Backlog card has not been touched in two to three months. Stale cards are waste:
prioritise closing them, or write the next action and owner on them so they stop being stale.

## Card hygiene the agents rely on

- Every card carries its status in its comments, not in chat: the last comment says what happened,
  what is next, and who acts (`async-first`).
- A card that leaves Ready has `GOAL / DONE WHEN / NOT IN SCOPE`; a card that reaches Done has a
  reviewer's verdict and a verifier's confirmation from someone other than the author (contract §5).
- Handoff between agents is a status change plus one comment; the receiving agent reads the card, not
  the sender's session.
- If you must violate the flow (skip a list, move a card back, exceed a limit), report it on the card
  **before** doing it, with the reason. A recorded violation is a decision; a silent one is a defect.

## Example — an agent choosing its next card

Board: Ready has A (top) and B; Code Review has C (authored by another agent) and D (authored by you);
Verify has E waiting on the human. You have one card In Progress.

1. Rightmost first: Verify's E belongs to the human — skip. Code Review's C is reviewable by you — take C.
   D is yours, so you cannot review it.
2. After C's verdict, you still hold one In Progress card and one in review (two in flight). Do not pull A.
3. Finish your In Progress card, hand it to Code Review (bottom of the list, or top if High). Now two in
   flight and nothing In Progress: pull A only if your in-flight count is below two; otherwise go to the
   WIP-limit list and groom B.
