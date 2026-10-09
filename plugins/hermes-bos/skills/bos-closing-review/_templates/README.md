# _templates/

Sample verdict-file templates that ship with `bos-closing-review`. The
verifier (`scripts/check_verdict_dishonesty.py`) is run against any
newly-written verdict file before the closing card is `kanban_complete`-d.

## clean-pass.md

Demonstrates a verdict file the verifier accepts (zero diagnostics):

- `**Verdict: PASS**` headline at the top.
- All matrix rows have `status: pass` or `status: fail` (no `gap`).
- Re-runnable evidence cited for every row.

Use this template when all checks pass cleanly. Save to
`business-os/evaluations/<card-id>-qg-verdict.md` (or
`business-os/functions/quality/<card-id>-qg-verdict.md`) before
`kanban_complete`.

## honest-inconclusive.md

Demonstrates a verdict file the verifier also accepts (zero diagnostics):

- `**Verdict: INCONCLUSIVE**` headline (NOT PASS).
- One row with `status: partial-pass`, fully disclosed.
- Operational consequences and durable-fix work cited.

Use this template when one or more checks have an unexplained gap.
Verdict MUST be `INCONCLUSIVE`, never `PASS`, when any row reports a
gap. This is the recipe 0 / closing-review rubric step 3 rule.
