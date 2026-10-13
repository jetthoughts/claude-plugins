---
name: bos-upwork-campaign
description: 'Run an Upwork campaign: profile, jobs, bids, prefill.'
version: 0.1.0
author: pftg
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, upwork, sales, campaign, ego-browser]
    related_skills: [bos-research, bos-lead-qualification, bos-quality-gate, ego-browser]
---

# bos-upwork-campaign

The procedure for the JetThoughts Upwork channel (Rock 2.3): keep the agency profile and Paul's
freelancer profile aligned to one active campaign, find jobs, validate them, choose the bid,
prefill it in Paul's Upwork session and hand the tab to Paul. Paul presses every Save and Submit.

## Use when

Any card about the Upwork channel: a campaign kickoff, a profile change, an `upwork session`
(job search and bids), a bid packet, an outcome update, the weekly channel review.
Not for: anything on another marketplace (open a card for kanban-orchestrator first).

## Team

| Seat | Owns | Never |
|---|---|---|
| kanban-orchestrator | Intake, splits the campaign into cards, routes them | Touches Upwork |
| researcher | Lane and offer research, competitor profiles off Upwork, rate evidence | Opens upwork.com |
| upwork-operator | Campaign file, profile diffs, job search, validation, bid ladder, packets, prefill | Clicks Save/Submit/Send/Boost/Buy |
| quality-guardian | Gates every profile diff and every bid packet (claims, economics, scam, policy) | Reviews its own work |
| delivery-manager | One Plane item assigned to Paul per batch of ready packets; outcome tracking | Edits packets |
| Paul | Approves the lane, saves profile changes, submits proposals, talks to clients | — |

## Records (vault: ~/dev/pkm/10-domains/business-os/ventures/jetthoughts/upwork/)

- `campaigns/<slug>.md`: one per campaign. Hypothesis, lane, ICP, ideal job, rate band (floor,
  target, anchor), search seeds, profile diff, status (`draft|active|paused|closed`). Only one
  campaign is `active` at a time.
- `packets/<YYYY-MM-DD>-<job-slug>.md`: one per job that passed validation (template below).
- `ledger.md`: one table row per packet: date, campaign, job URL, score, bid, Connects, Paul's
  decision (`submitted|edited|skipped`), outcome (`no-view|viewed|reply|call|offer|won|lost`),
  outcome date. Unknown outcomes stay blank, never zero.
- `profile/<YYYY-MM-DD>-<surface>-diff.md`: current text, proposed text, reason, the claim source
  for every number.
Working files (screenshots, raw page extracts) stay in ~/dev/hermes/projects/upwork/.

## Platform facts that shape the work (checked 2026-10-13; recheck if older than 90 days)

- Specialized profiles were retired on 2026-05-28. A "profile per campaign" therefore means: the
  agency headline and overview, agency services (max 10) and skills (max 15), portfolio order and
  featured clients, a Project Catalog listing (max 20) for the campaign's entry offer, and Paul's
  freelancer headline, overview and 15 ordered skills aligned to the same story. There is one
  main profile per person.
- Clients hire a named agency member; hourly work needs the delivering freelancer's own profile.
  Agency Connects are shared. Agency Plus costs $19.99/month.
- Freelancer service fee is 0–15%. To net N per hour at 15%, bid at least N / 0.85
  (net $70 needs gross $82.35).
- Connects cost $0.15 each; the base cost varies by job and can change while the job is live.
  A boost (up to 4 slots) is charged only if it wins a slot or the client engages.
- The Availability badge does not raise search rank. Response speed matters: Upwork advises
  replying within two hours.
- The automation policy (support article 43342677368467) forbids bots, extensions that read
  or change Upwork pages, auto-refresh, page monitors and background requests, and grants no
  exceptions. Paul has accepted that risk for attended, human-paced ego-browser work only. The
  upwork-operator SOUL's browser rules are the guard; follow them exactly.

## Stage 0: Campaign kickoff (kanban-orchestrator, researcher)

1. kanban-orchestrator opens a research card for researcher with a blind brief: the goal ("which
   Upwork lane should JetThoughts lead with at ≥ $70/h net"), the constraints and the prior
   research paths. It lists no candidate lanes (novelty gate: ≥3 new findings).
2. researcher returns lanes ranked with evidence: demand, competition, rate evidence, JetThoughts
   proof that exists today. quality-guardian gates it.
3. upwork-operator writes `campaigns/<slug>.md` from the winning lane. Choosing the lane is
   Paul's call: block `needs_input` with the recommendation, unless an approved SHAPE names the
   lane.

## Stage 1: Profile (agency first, then Paul's freelancer profile)

1. Read the live profile in ego-browser (one page load per surface) and save the current text to
   the diff file. Read competitor agencies' public pages off Upwork where possible.
2. Draft the diff: headline, overview opening, services, skills order, portfolio order, one
   Project Catalog entry offer. Every number or client name cites its source in the JT claims canon
   (`~/dev/jetthoughts.github.io/.okf/content/claims-canon.md`). No source means it stays out.
3. Review card for quality-guardian (`--parent` yours). On PASS: open the edit page, fill the
   fields, `task.handOff()` with the note "check fields, press Save". Record in the diff file
   what Paul saved.

## Stage 2: Job search (upwork-operator, attended `upwork session` card only)

1. Use the campaign's saved searches or the search URL with filters: `payment_verified=1`,
   hourly or fixed bands from the rate floor, `proposals=0-4,5-9,10-14`, `sort=recency`.
2. Read result cards, then open at most 8 job pages per session. Total Upwork page loads per card
   ≤ 20, with 5–20 s between actions.
3. Each opened job goes through Stage 3 immediately; nothing is stored about jobs that fail.

## Stage 3: Validate (hard gates first, then score)

Hard gates (any one fails the job, with the reason in the session log):
- scam score ≥ 40 from `references/scam-guard.md`;
- no budget path to the campaign floor (hourly max below floor; fixed budget / estimated hours
  below floor);
- skill or offer outside the campaign;
- more than 20 proposals, or the client is already interviewing 5 or more;
- the job needs Paul or a named engineer we cannot commit.

Score 0–100 for the jobs that pass:
- Fit 40: the posted problem matches the campaign offer and we have proof for it.
- Economics 25: budget and the client's average paid hourly rate against the target.
- Client quality 20: payment verified, hire rate, total spend, review language.
- Competition 15: proposal count, interviewing count, how recently the client viewed proposals.
Below 60 is a skip. 60 and above gets a packet.

## Stage 4: Bid

- Ladder per job: floor (campaign floor), target, anchor (≤ the job's budget ceiling). The job
  is skipped if floor > budget.
- Hourly when the scope is unclear or the work is inherited code. Fixed only with acceptance
  criteria; price = senior hours × target + risk, never just the posted number. Too big for the
  budget: offer a paid first phase, never a lower rate.
- Cover letter 75–120 words: the client's actual constraint in line one, one verified proof
  item, a bounded next step, one question. No résumé opening, no stack list, no free plan.
  Answer every screening question from vault facts; an unknown answer becomes
  `[PAUL: answer needed]`.
- Boost: never proposed by default. Recommend one only with score ≥ 85, noting the extra Connects.

## Stage 5: Packet, review, prefill, hand-off

Packet file `packets/<date>-<job-slug>.md`:

```
---
campaign: <slug>
job_url: <url>
checked_at: <ISO time the live page was read>
score: <n> (fit/econ/client/competition)
scam_score: <n> flags: [...]
bid: {type: hourly|fixed, floor: , target: , anchor: , proposed: }
connects: <n read from the page>
member: <named agency member who delivers>
status: draft|reviewed|prefilled|submitted|skipped
---
## Why this job
## Cover letter
## Screening answers
## Risks
```

1. quality-guardian review card (`--parent` yours) checks claims, economics, scam flags and tone.
2. On PASS, in the same attended session: reopen the job, recheck status and Connects, open the
   apply form, fill rate or bid, cover letter and answers, then `task.handOff()` with a note:
   "<job title> | bid <x> | <n> Connects | check and Submit". Keep the tab.
3. Paul submits, edits or skips. Write his decision to the packet and the ledger. If the result is
   unclear, set `submission_unknown` and check the proposal list before doing anything else.

## Stage 6: Learn (weekly, delivery-manager drafts, quality-guardian checks)

From `ledger.md`: Connects spent, views, replies, calls, contracts, cost per reply, cost per
call, margin. Open outcomes stay open. Change one variable per review (lane, filter, opening,
proof, price) and record it in the campaign file. A Paul edit to a packet is a lesson: note what
he changed and why in the campaign file's `## Learnings`.

## Fixtures

Each kaizen change to this skill adds one real input and its expected result under `fixtures/`.
