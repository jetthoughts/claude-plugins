---
name: bos-lead-qualification
description: Score a sales prospect against ICP with evidence.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-lead-qualification Skill

Turn an inbound or sourced prospect into a scored qualification record in
`functions/sales/` — five dimensions, each backed by cited evidence —
plus a clearly marked draft next action. The skill never contacts the
prospect: any outreach is `EXTERNAL` and stops at the owner's explicit
per-instance yes (deny-on-silence). It writes files only and commits
nothing.

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Sales function directory: `/Users/pftg/dev/pkm/business-os/functions/sales/`
- Canonical format carrier: this skill

## Use when

Use when a new prospect appears (inbound form, referral, outbound reply)
or when an existing lead record needs re-scoring after new evidence. Not
for sending anything — the output is a record and a draft.

## Inputs

- Prospect identity: person, company, and source channel (with date)
- Raw lead material (verbatim message, call notes, referral context)
- Venture (default: `jetthoughts`)

## Procedure

1. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, `constitution/mission.md`,
   `constitution/authority-matrix.md`, `constitution/risk-policy.md`, and
   `constitution/escalation-policy.md`.
2. Read the ICP definition at `functions/sales/icp.md` if present. If it
   is missing, record that as an open question in the record and score
   against the mission's stage and principles only — never invent ICP
   criteria.
3. Duplicate check with `search_files target='files'` in `functions/sales/`
   for the person and the company. If a lead record exists, update it;
   create a new one only for a genuinely new prospect.
4. **Fixture guard.** Read the work item's `source_class` and `evidence`
   paths. If `source_class: fixture` or `source_class: synthetic`, or any
   evidence path matches `evaluations/fixtures/**`, **reject** the prospect
   and record the rejection in the qualification record with reason
   `synthetic-source`. Do not score. Do not write a LEAD record. This guard
   runs before the duplicate check; a synthetic source never reaches
   `functions/sales/`.
5. Score five dimensions, 0–2 each (0 = none or no evidence, 1 = partial,
   2 = strong):
   - ICP fit — matches the ICP (or mission stage) on segment, size, stack.
   - Pain — a concrete, stated problem the firm can solve.
   - Urgency — a decision timeline or forcing event.
   - Authority — the contact can decide or decisively influences buying.
   - Reachability — a working channel exists (email, phone, warm intro).
   Every score cites its evidence inline (quote plus source path/URL).
   Unknown is scored 0 and marked "insufficient evidence" — never guessed.
6. Set `qualification`: `qualified` (total ≥ 7 and no disqualifier),
   `nurture` (3–6), `disqualified` (0–2 or a hard disqualifier), or
   `insufficient-evidence` (when scoring the unknowns by guess would
   change the band). Hard disqualifiers — asks for something the firm does
   not do, unethical use, no plausible budget path — are recorded verbatim.
   `rejected-synthetic` — the source is a test fixture or synthetic data
   (see the fixture guard in step 4). Hard band, no appeal, recorded with
   the fixture path. This band takes precedence over every other band.
7. Write the record with `patch` at
   `functions/sales/LEAD-<YYYYMMDDNN>-<slug>.md`, confirming ID uniqueness
   with `search_files` (counter zero-based within the day).
7. Draft the next action under `## Next action (draft — not sent)`: the
   concrete step, the audience, and the exact text or script. This is a
   `DRAFT` artifact — writing it sends nothing. Mark the record
   `owner_approval_required: EXTERNAL` for any outreach step.

Qualification record format:

```markdown
---
id: LEAD-<YYYYMMDDNN>
prospect: <name — company>
source: <channel + date>
venture: jetthoughts
icp_fit: <0|1|2>
pain: <0|1|2>
urgency: <0|1|2>
authority: <0|1|2>
reachability: <0|1|2>
total: <0-10>
qualification: <qualified|nurture|disqualified|insufficient-evidence>
disqualifiers: []
evidence: [<paths or URLs cited above>]
owner_approval_required: EXTERNAL
updated: <YYYY-MM-DD>
---

# <prospect>

## Source material
<verbatim message or notes>

## Scores
| Dimension | Score | Evidence |
|-----------|-------|----------|
<one row per dimension, quote + source>

## Disqualifiers
<verbatim or "none">

## Next action (draft — not sent)
<proposed step, audience, draft text; nothing here was sent>

## Open questions
<only those that change the score or the next action>
```

## Output

Return the record path, total score, qualification band, the weakest
dimension with its evidence, and the draft next action with its `EXTERNAL`
gate.

## Failure modes

- Do not contact the prospect or any third party — no sends, calls, DMs,
  or form submissions; outreach requires the owner's explicit per-instance
  yes.
- Do not score without cited evidence; a guessed score is a defect, not a
  favor.
- Do not invent ICP criteria, budget, timeline, or authority — record
  unknowns as insufficient evidence.
- Do not put personal data beyond what the lead material itself contains
  into the record; secrets never in files (env var names only).
- Do not commit, push, or rewrite Git history — the owner commits.
- If scoring depends on facts that change scope or risk (e.g. a claimed
  budget that cannot be verified), escalate per the escalation policy
  instead of guessing.

## Verification

- File exists at `functions/sales/LEAD-<id>-<slug>.md`; frontmatter is
  complete and `total` equals the sum of the five dimension scores.
- Every score row carries an evidence citation that `read_file` or
  `web_extract` resolves.
- The `qualification` band matches the thresholds in step 5.
- No message was sent — the record contains only a marked draft.
- The duplicate check confirmed no second record for the same prospect or
  company.
