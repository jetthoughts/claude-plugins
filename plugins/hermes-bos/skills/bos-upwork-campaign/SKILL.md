---
name: bos-upwork-campaign
description: 'Run an Upwork campaign: profile, jobs, bids, prefill.'
version: 0.4.0
author: pftg
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, upwork, sales, ego-browser]
    related_skills: [ego-browser, bos-quality-gate, humanizer]
---

# bos-upwork-campaign

JetThoughts sells pre-vetted, self-managed subcontractors; Upwork is one channel. Every new
opportunity (service, tech stack) is pre-validated before its campaign goes `active`.

Use for any Upwork card. upwork-operator does the work in Paul's session under its SOUL browser
rules. quality-guardian reviews every profile diff and bid packet as a separate `--parent` card.
Paul picks the lane, presses every Save/Submit, and talks to clients.

## Records

Vault `~/dev/pkm/10-domains/business-os/ventures/jetthoughts/upwork/`:
- `campaigns/<slug>.md`: lane, buyer, rate floor/target/anchor, search seeds, extra gates, `## Learnings`.
  One `active`.
- `profile/<date>-<surface>-diff.md`: current text, proposed text, claim source for every number.
- `packets/<date>-<job>.md`: one per job that passes all filters.
- `ledger.md`: one row per packet. Outcome stays blank until seen.
Session log: `~/dev/hermes/projects/upwork/opportunities/<date>-session.md`, one line per opened
job: URL | stopped at | reason | scam/chance/fit.

## Pre-validate (every new service or stack)

Write `## Pre-validation` in the campaign file. Each line needs a number and a source. The campaign
moves to `active` only when all five pass and Paul says go.
1. **Demand:** ≥ 10 jobs from the last 14 days pass `references/filters.md` at or above the
   floor. Count them in one attended search session, or from jobs Paul pasted.
2. **Price:** billed rates (not listed rates) of ≥ 3 proven competitors in that stack. The band
   sits at or below the proven ceiling.
3. **Margin:** floor × 0.85 − subcontractor cost ≥ $8/h.
4. **Supply:** a named, vetted subcontractor, or a sourcing pool plus vetting test that can staff
   within 7 days. Self-managed means they own delivery without a JetThoughts PM.
5. **Proof:** ≥ 1 verifiable case for this service or stack, or the gap is stated in every packet.
researcher does 2 and 4 off Upwork, upwork-operator does 1, quality-guardian gates.
A FAIL parks the campaign with its numbers. It is not retried unchanged.

## Profile

There is one main profile per person (specialized profiles were retired 2026-05-28). Positioning per
campaign = headline, overview, 15 ordered skills, portfolio order, one Project Catalog offer. Agency
first, then Paul's freelancer profile. Every number cites
`~/dev/jetthoughts.github.io/.okf/content/claims-canon.md`; uncited means it stays out.
Diff, then review, then fill the edit page, then `handOff("check, press Save")`.

## Jobs

1. Run the campaign's saved searches (payment verified, rate band, `proposals` ≤ 14, newest first).
   Open ≤ 8 jobs.
2. Filter each opened job with `references/filters.md`, in order, stopping at the first failure:
   **scam** ≥ 40 rejects; **chance** < 45 rejects, 45–54 is held for Paul (log line only);
   **fit** < 60 rejects. Then apply the campaign's extra gates.
   Exception: chance ≥ 70 and only the budget fails means bid a paid first phase
   (hours = budget ÷ target). Never cut the rate.
3. At most 2–4 bids per day. Most jobs should die in the filter.

## Bid

- Hourly if the scope is unclear or the code is inherited. Fixed only with acceptance criteria:
  senior hours × target + risk.
- Margin per hour = bid × 0.85 − subcontractor cost. Never bid where that is below $8.
- Say who delivers: a named, vetted engineer. Hourly contracts run on the delivering engineer's
  own profile (an agency member); fixed price may run on Paul's as business manager (Upwork
  agency rules). Never sell Paul's own hours when a subcontractor does the work.
- Cover letter by `humanizer`, 75–120 words: their constraint first, one verified proof item, a bounded next step,
  one question. No résumé opening, no stack list, no free plan. An unknown screening answer becomes
  `[PAUL: answer needed]`.
- No boost unless fit ≥ 85; state the extra Connects.
- Packet front matter: `job_url, checked_at, scam, chance, fit, bid{type,proposed,floor}, connects,
  status`. Body: why, cover letter, answers, risks.
- After review PASS: reopen the job, recheck that it is open and the Connects cost, fill the form,
  then `handOff("<title> | <bid> | <n> Connects | check and Submit")`. Write Paul's decision to the
  packet and the ledger. If it is unclear whether it was sent, check the proposal list before
  anything else.

## Learn (weekly)

From the ledger: replies per chance band, Connects per reply, Connects per call, margin.
quality-guardian rereads 5 rejected and 5 unviewed bids. Change one variable per week and log it in
`## Learnings`. Each skill change adds a case under `fixtures/`.
