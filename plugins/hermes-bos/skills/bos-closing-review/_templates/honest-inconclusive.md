# QG verdict: <card-id> — honest INCONCLUSIVE template

**Verdict: INCONCLUSIVE** — N/M checks verified, K gaps honestly disclosed;
no blockers; durable-fix work filed for the gap class.

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
| C3 | <check 3> | partial-pass | <what can be proven; what cannot> | <method, with limitation> | medium |

## Defect list

| id | finding | severity | location | disposition |
|---|---|---|---|---|
| D1 | <gap description> | major | <verdict file §X> | open — durable fix filed as <card-id> |

## Closing checklist

- [x] all checks evaluated with evidence; gap honestly disclosed
- [x] no fabricated numbers / paths / outputs
- [x] verdict headline reconciles with matrix: K partial-pass → INCONCLUSIVE
- [x] durable fix filed for the gap class
- [x] no PO escalation

**Verifier**: run `python3 scripts/check_verdict_dishonesty.py <verdict-file>`
before `kanban_complete`. Expected: PASS, all rows clean (the headline
is INCONCLUSIVE, not PASS, so the gate does not fire).
