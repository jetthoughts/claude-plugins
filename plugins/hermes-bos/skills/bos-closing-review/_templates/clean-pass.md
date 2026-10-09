# QG verdict: <card-id> — clean PASS template

**Verdict: PASS** — 10/10 checks verified on disk, no blockers.

| field | value |
|---|---|
| card | <card-id> |
| parent | <parent-id>, `done` |
| assignee | quality-guardian |
| lens | Reality Checker (bos-lens-router) |
| verdict file | business-os/evaluations/<card-id>-qg-verdict.md |

## Evidence matrix

| # | claim or required check | status | evidence | how verified | confidence |
|---|---|---|---|---|---|
| C1 | <check 1> | pass | <path or output> | re-ran | high |
| C2 | <check 2> | pass | <path or output> | re-ran | high |
| C3 | <check 3> | pass | <path or output> | re-ran | high |

## Defect list

| id | finding | severity | location | disposition |
|---|---|---|---|---|
| (none) | — | — | — | — |

## Closing checklist

- [ ] all checks evaluated with evidence
- [ ] no fabricated numbers / paths / outputs
- [ ] verdict headline reconciles with matrix
- [ ] no PO escalation
- [ ] comment thread on the producer card updated

**Verifier**: run `python3 scripts/check_verdict_dishonesty.py <verdict-file>`
before `kanban_complete`. Expected: PASS, all rows clean.
