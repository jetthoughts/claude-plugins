---
name: bos-upwork-campaign
description: 'Run an Upwork campaign: profile audit and rewrite, jobs, bids, prefill.'
version: 0.8.0
author: pftg
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, upwork, sales, ego-browser]
    related_skills: [ego-browser, bos-quality-gate, humanizer]
---

# bos-upwork-campaign

Use for any Upwork card. upwork-operator does the work in Paul's session under its SOUL browser
rules. quality-guardian reviews every profile diff and bid packet as a separate `--parent` card.
Paul picks the lane, presses every Save/Submit, and talks to clients.

**Pace (Paul, 2026-10-15; extended 2026-10-16):** never act fast. Before every navigation, click,
fill or scroll, wait until the page has settled, then sleep 1–2 s (`page.waitForTimeout(1000 + Math.random() * 1000)`).
Never fire page loads back to back or in parallel. Scroll only to bring a section you are about to read
or edit into view. Mouse movement and scrolling added only to look human are out of scope: if Upwork
challenges the session, stop and hand it to Paul.

**Read back every Save from a fresh page load (2026-10-17).** If the field is unchanged after one retry, stop. Delete and re-add the item, or drop the field and record it in the after-state. Never probe with test text on a live page. Upwork discards service descriptions on save, and shows skills in its own order.

**Agency editor needs the agency context (2026-10-16).** The agency page at
`/agencies/<id>/` shows its edit pencils only while the browser is acting as the agency. Upwork offers that
switch only in the profile-picture menu, which the operator never opens. If the page has no edit controls,
stop after one look and ask Paul to switch to the agency profile. Never probe guessed URLs: two misses means stop.

## Records

In the project's records folder (its AGENTS.md names it):
- `campaigns/<slug>.md`: lane, buyer, rate floor/target/anchor, search seeds, extra gates, `## Learnings`.
  One `active`.
- `profile/<date>-<surface>-diff.md`: current text, proposed text, claim source for every number.
- `packets/<date>-<job>.md`: one per job that passes all filters.
- `ledger.md`: one row per packet. Outcome stays blank until seen.
Session log: `~/dev/hermes/projects/upwork/opportunities/<date>-session.md`, one line per opened
job: URL | stopped at | reason | scam/chance/fit.

**Front matter must parse strictly (Paul, 2026-10-16).** Keep each value to a short plain phrase and put
prose in the body. Double-quote any value that contains `: ` (title, surface, lane). The vault validator
auto-quotes loose colons on purpose, so it passes files that Tolaria and strict YAML readers reject.
After writing a record, run: `ruby -ryaml -rdate -e 'm=File.read(ARGV[0]).match(/\A---\n(.*?)\n---\n/m); YAML.safe_load(m[1], permitted_classes: [Date, Time]); puts "ok"' <file>`.
It prints `ok` or the line and column that breaks.

## Pre-validate (every new service or stack)

Write `## Pre-validation` in the campaign file. Each line needs a number and a source. The campaign
moves to `active` only when all five pass and Paul says go.
Start with a **market scan, no bids**. Read the work histories of engineers in the niche who
were hired recently: contracts started in the last 90 days, with title, billed rate (or
"hidden"), hours and whether still ongoing. That is the demand and price that actually changed
hands; job posts are a second lens. Read only: never message or invite engineers.
1. **Demand:** contracts started in the last 90 days in this niche, from the scan. As a second
   lens, ≥ 10 jobs from the last 14 days pass `references/filters.md` at or above the floor.
2. **Price:** the billed rates from the scan (≥ 3 proven engineers). The band sits at or below the
   proven ceiling.
3. **Margin:** floor × 0.85 − delivery cost ≥ $8/h.
4. **Supply:** a named person who delivers, or a sourcing pool plus vetting test that can staff
   within 7 days.
5. **Proof:** ≥ 1 verifiable case for this service or stack, or the gap is stated in every packet.
researcher seeds the niches and reads public pages and supply. upwork-operator reads profiles and jobs
in attended sessions. quality-guardian checks the ranked result.
A FAIL parks the campaign with its numbers. It is not retried unchanged.

## Profile

There is one main profile per person (specialized profiles were retired 2026-05-28). Positioning per
campaign = headline, overview, 15 ordered skills, portfolio order, and Project Catalog listings: one per
service, each backed by a site page with a stated price (Paul, 2026-10-16). Agency first, then Paul's
freelancer profile. Every number cites
the project's claims source; uncited means it stays out.
Audit the live profile against `references/profile.md` first. The diff fixes only failed checks, so
a line that passes stays. Then review, fill the edit page, and `handOff("check, press Save")`.

## Jobs

1. Find jobs from the Nibwright feed first (Paul's saved search, polls hourly, notifies only; Paul presses Submit on Upwork), then the campaign's saved searches (payment verified, rate band, `proposals` ≤ 14, newest first).
   Open ≤ 8 jobs. Nibwright's match percentage is a hint, not a filter: every job still passes the filters below.
2. Filter each opened job with `references/filters.md`, in order, stopping at the first failure:
   **scam** ≥ 40 rejects; **chance** < 45 rejects, 45–54 is held for Paul (log line only);
   **fit** < 60 rejects. Then apply the campaign's extra gates.
   Exception: chance ≥ 70 and only the budget fails means bid a paid first phase
   (hours = budget ÷ target). Never cut the rate.
3. At most 2–4 bids per day. Most jobs should die in the filter.

## Bid

- Hourly if the scope is unclear or the code is inherited. Fixed only with acceptance criteria:
  senior hours × target + risk.
- Margin per hour = bid × 0.85 − delivery cost. Never bid where that is below $8.
- Say who delivers: a named, vetted engineer. Hourly contracts run on the delivering engineer's
  own profile (an agency member); fixed price may run on Paul's as business manager (Upwork
  agency rules). Never sell one person's hours when someone else does the work.
- Cover letter by `humanizer`, 100–180 words, skeleton and evidence in `references/bid-template.md`. The first
  two lines are all the client sees in the proposal list, so they carry their constraint in their own words.
  Then one verified proof item with a link, a bounded next step (for build jobs a small paid first phase, never
  free work), and one closing question that only someone who read the post could ask. No résumé opening,
  no stack list, no free plan, no "Hi, thanks for posting". An unknown screening answer becomes
  `[PAUL: answer needed]`.
- Screening questions: answer each in its first sentence, under 40 words, in the client's wording. If the
  post plants a keyword, it is the whole first line.
- Never put an email, Calendly link or any off-platform contact in a bid, a message or a file before a
  contract is active. It breaks Upwork's terms and risks the account.
- Speed matters on fresh posts: bid in the first hours while the post has under 15 proposals. A slow
  perfect letter loses to a decent early one.
- The proposal explains only part of the reply (the playbook's third-party sample says about 16%); the
  profile, fit and timing carry the rest. Do not polish a letter for a job that failed a filter.
- Log every bid with its variant (which opener, which proof, which length) so the weekly review can compare.
- No boost unless fit ≥ 85; state the extra Connects.
- Packet front matter: `job_url, checked_at, scam, chance, fit, bid{type,proposed,floor}, connects,
  status`. Body: why, cover letter, answers, risks.
- After review PASS: reopen the job, recheck that it is open and the Connects cost, fill the form,
  then `handOff("<title> | <bid> | <n> Connects | check and Submit")`. Write Paul's decision to the
  packet and the ledger. If it is unclear whether it was sent, check the proposal list before
  anything else.

## After a win

Within 24 hours send a written recap: scope, milestones, acceptance criteria, how often we report. Ask for
the review at delivery. Turn every finished contract into one case line (problem, what we did, result, a
quote if the client agrees) and one portfolio item, so the next bid has a proof link. Never share a login
to write bids: use the agency's business-manager role.

## Learn (weekly)

From the ledger: replies per chance band, Connects per reply, Connects per call, margin.
quality-guardian rereads 5 rejected and 5 unviewed bids. Change one variable per week and log it in
`## Learnings`. Each skill change adds a case under `fixtures/`.
