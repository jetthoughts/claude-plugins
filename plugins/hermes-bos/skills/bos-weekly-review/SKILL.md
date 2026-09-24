---
name: bos-weekly-review
description: Compile the weekly evidence-tied review and next bets.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-weekly-review Skill

Produce the Chief of Staff weekly review for the ISO week just ended (when
run on Monday) or the current week: metrics computed from files,
commitments tracked, learnings captured, risks flagged, and next bets
proposed — every recommendation tied to evidence. The review writes one
file and commits nothing (the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Reviews directory: `/Users/pftg/dev/pkm/business-os/operations/reviews/`
- Pipeline source: `/Users/pftg/dev/pkm/business-os/functions/sales/`
- Canonical format carrier: this skill

## Use when

Use at a fixed weekly cadence (e.g. Monday morning), at the end of a
planning cycle, or when the owner asks "how did the week go". Not for
daily triage (`bos-daily-review`) or grading a single artifact
(`bos-quality-gate`).

## Inputs

- ISO week under review (`YYYY-Www`, e.g. `2026-W39`; default: the week
  of the run date)
- Seat (Hermes profile) producing the review
- Optional scope: venture or function to zoom into

## Procedure

1. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, `constitution/mission.md`, `constitution/risk-policy.md`,
   `constitution/definition-of-done.md`, and
   `constitution/escalation-policy.md`.
2. Compute metrics by enumeration — never from memory: work items per
   `status`, items opened and closed in the week (`updated` plus recorded
   transitions), gate verdicts in `evaluations/runs/`, leads by
   `qualification` value in `functions/sales/`, and open incidents in
   `operations/incidents/`.
3. Commitments: for each commitment made in the prior weekly review or in
   a work item, mark kept / missed / carried with the file path that
   proves it. A commitment without a verifying file is "missed — no
   evidence".
4. Learnings: what failed and why, each traced to a fixture or run note in
   `evaluations/`. A lesson with no run note or fixture behind it is an
   anecdote — label it as such.
5. Risks: items with `risk_class: high` or `critical`, all escalations,
   and anything touching money, credentials, legal, or production.
6. Next bets: at most three proposals, each of the form "do X because
   evidence E shows Y" with a path or URL for E. No evidence → no
   recommendation; record it as an open question instead.
7. Write the review with `patch` at
   `operations/reviews/<YYYY-Www>-weekly.md`, named for the ISO week under
   review (`date +%G-W%V` semantics of that week's Monday). If the file
   exists, update it in place.

Weekly review format:

```markdown
---
review: WEEKLY-<YYYY-Www>
week: <YYYY-Www>
seat: <profile>
period: <Monday>–<Sunday>
work_items_open: <n>
work_items_closed: <n>
gates_passed: <n>
gates_failed: <n>
leads_qualified: <n>
recommendations: <n>
---

# Weekly review — <YYYY-Www>

## Metrics
<each count with the directory it was enumerated from>

## Commitments
| Commitment | Made in | Result | Evidence |
|------------|---------|--------|----------|

## Learnings
<each with its fixture/run citation>

## Risks
<each with risk_class and path>

## Next bets
| Bet | Evidence | Approval needed |
|-----|----------|-----------------|

## Owner summary
<one short paragraph>
```

## Output

Return the review path, headline metrics, the commitments result, the top
risk, and the next-bet list with evidence pointers.

## Failure modes

- Do not present a metric, learning, or bet that lacks a file citation;
  label it unsupported or drop it — "evidence or it didn't happen".
- Do not let the review author grade its own work: where the weekly review
  itself becomes a graded artifact, a different seat applies
  `bos-quality-gate` (author ≠ verifier).
- Do not start, send, spend, or approve anything; the bets list what needs
  approval, nothing more.
- Do not commit, push, or rewrite Git history — the owner commits.
- If the week has no closed work and no gate runs, say so — a quiet week
  is a finding, not a gap to paper over.

## Verification

- File exists at `operations/reviews/<YYYY-Www>-weekly.md` with complete
  frontmatter.
- Every number in Metrics traces to an enumerated directory; re-counting
  reproduces it.
- Every row in Commitments and Next bets carries a path or URL that
  `read_file` (or `web_extract`) resolves.
- The `recommendations` count equals the Next bets row count.
- No other file was modified — the review file is the only delta.
