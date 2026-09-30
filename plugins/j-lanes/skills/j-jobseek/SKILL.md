---
name: j-jobseek
description: "Run the Berlin job search — read the board, pick the operation that is due, run it, and stop at anything only Paul can do. Use whenever the ask is run the job search, what is next on Job Seek, take the top card, apply to this posting, engage this company on LinkedIn, scan the boards, rehearse for a screening, or run the weekly review. Reach for it before touching jobseek-pipeline.md or the Job Seek Berlin project. Not for the board sweep or a single application — those lanes live in the jobseek-auto skill, which is not installed on this machine; until it is restored, every operation here runs by hand (see Precedence)."
---

# j-jobseek

> **Precedence (Paul, 2026-09-18): the sweep and the application lanes now live in the
> `jobseek-auto` skill** (`/Users/pftg/dev/jobseek-lab/.claude/skills/jobseek-auto`, symlinked
> user-level) and its two dynamic workflows, `jobseek-sweep` and `jobseek-apply`. Load that skill
> for `scan` and `apply <url>`. This skill keeps the board dispatch, the LinkedIn lanes, the
> interview rehearsal and the weekly review.
>
> **Three routes below are dead**: `j-board-run`, `j-apply-one-job` and `j-linkedin-engage` are
> referenced but **not installed on this machine** — the `j-lanes` plugin ships `j-jobseek` and
> `j-venture` only (verified 2026-09-18). Until they are restored, `next` means read the board
> and dispatch by hand, and `engage` is Paul's lane.

Drives the system under the vault note `find-an-eng-leading-job`. The procedures live in the Operation notes; this skill decides which one is due, runs it, and records the result. It does not restate them.

Say which operation to run — `next`, `apply <url>`, `engage [company|intake|pick]`, `scan`, `conversation`, `prep`, `review` — or say nothing and it auto-picks by state (below).

## Hard stops — not preferences

- Never click a final submit or join button.
- Never tick a Privacy Policy / Terms consent box.
- Never create an account, whatever permission is offered.
  Existing accounts are fine: BrowserOS neo (`mcp__browseros-neo__run`) carries Paul's LinkedIn and join.com sessions, so Easy Apply and join.com forms are usable channels (Paul, 2026-09-02).
- Never send email. Draft only. Sending needs fresh, explicit permission for that specific send, in this conversation.
- NotebookLM is strictly read-only — no create, edit, delete, share or download.
- Never message a person who has not seen Paul's name first. Engage with their posts, or the posts of people they follow, before any connection note or DM (Paul, 2026-09-02).
- Never send or post any message to a person without showing Paul the exact text and getting his confirmation in this conversation. Short, natural, one ask; respect their time and privacy.
- Every outbound message and every filled form gets a cold-eyes review first — `cold-reviewer` (vault-scoped agent), or `codex:codex-rescue` for a different vendor. *Gemini was listed here until 2026-09-12: both its doors were measured dead — the MCP connects then fails in its `agy` backend, the CLI dies in `_doSetupUser`.* Draft → review → fix → show Paul → wait.

Hitting one is not a failure and does not end the run. Write the row into `jobseek-pipeline.md` with `owner: paul` and a `due:`, then carry on with everything else. Report the queue at the end.

## Route

**Always read `jobseek-pipeline.md` first** — it is the state. Then:

Each operation and where it runs (workflow, skill or vault note): see `references/operations.md`.

**Hand-off to Paul (Paul, 2026-09-03).** When a card needs him, assign it to him and add a comment with exactly what to do or the simplest unblock: the click, the link, the one-line question. The card is the hand-off, not the chat. Take it back when his part is done.

**Read the board first (Paul, 2026-09-03).** At the start of every session, after a context reset or a browser restart, read the Paperclip project *Job Seek Berlin* (`GET http://localhost:3100/api/companies/eeda44ae-eb2d-46ff-8b9b-a8e88486170c/issues`, `in_progress` first) before doing anything else, and resume from the top in-progress card. A resumed session that acts from memory instead of the board is how a half-filled form or a stale verdict gets repeated.

**Board cycle (Paul, 2026-09-03).** One board at a time, depleted (every kept posting has a stage-3 verdict), then the next by rank in `22-job-boards_monitor.md` §0, then start over. Critical boards get a daily stage-2 read of new postings regardless; a deadline inside the cycle jumps the queue.

**Triage before doing (Paul, 2026-09-03).** A new ask is carded in Backlog first, then placed against the board; it runs now only if it beats the top card or corrects a rule. The board stays small: a card is what, the check that closes it, one link, under ~8 lines. Reasoning, research and long updates go in a vault or Drive note the card links to. One line per status change, not a paragraph. Board shape (Paul, 2026-09-03): the minimum number of cards; subtasks only under the current sprint epic; the *Next* epic carries prework only; *Future* epics carry rough ideas only — no children until they become the sprint.

With no operation named, pick by state, first match wins:

0. **The daily sweep first** (Paul, 2026-09-03): if the *Daily board sweep* routine has not run today (it fires 08:00 weekdays; check its last run), run `scan` over every board in the Drive register `22-job-boards_monitor.md` (Lane 1 table and the Lane 2 section) that is due by its cadence, write the day's stage-2 file and the register's *Last swept* column, comment the counts on the card, and open a separate card only for a row that reaches stage 3 or needs Paul. Then run `python3 .claude/skills/j-linkedin-engage/scripts/intake.py` from the vault root, every session — a newly applied company with no lane is a card that does not exist yet. Then a runnable card on the Paperclip board → **next**. The board is the queue; the operations above are what the cards call.
1. Any company at `stage: screening` → **prep**. A loop is scheduled; it is the only time-critical branch.
2. Monday, or the review has not run in seven days → **review**.
3. Fewer than two conversations logged this week → **conversation**. This is the metric the search is judged on.
4. Otherwise → **scan**.

Say which branch you took and why, in one line, before running it.

## Before writing anything outbound

Load the vault note `research-berlin-target-seat` and check the framing against it. Three known-bad patterns are still live in existing artifacts and will be copied if you reuse them:

Small is never a kill on its own — engineering-team size is a **ceiling** (Paul, 2026-09-05), so the hands-on rule is what disqualifies; the seed–Series A founding-engineer **pitch** stays banned (2026-08-25). The three known-bad patterns, verbatim: see `references/outbound-patterns.md`.

`1. Area/Job Seek/20-applying_role-filter.md` is **superseded** — it screens for hands-on builder seats. Do not qualify with it until it is rewritten.

Artifacts live on Drive, not in the vault: CVs at `~/Google Drive/My Drive/Documents/0. Projects/2607 - Job Seek - Berlin/CVs/`. For Executive-level forms attach `Paul Keen - CV - CTO and Director of Engineering.pdf`.

## Team — who handles the next card

The roster and the dispatch-by-card-kind table lived in the `j-board-run` skill, which is **not installed on this machine**. Until it is restored, `next` reads the board and dispatches by hand (see Precedence).

## Finish

Update `jobseek-pipeline.md` in the same run — stages, the two counts, any new `owner: paul` row. Do **not** copy those numbers into `find-an-eng-leading-job.md`; that note carries the decision and the state, the pipeline carries the rows.

Then report three things and nothing else: what ran, what moved, what is waiting on Paul.

**Card comments and bodies are markdown Paul scans on a phone** (Paul, 2026-09-03, after a one-paragraph stage-2 comment): first line bold with the verdict or state; then bullets, one fact each; one ask, bold, at the end; paths in backticks; under ~10 lines. A wall of prose with semicolons goes into a note or a Drive file, and the comment links it.
