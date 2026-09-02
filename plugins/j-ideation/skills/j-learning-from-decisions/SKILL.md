---
name: j-learning-from-decisions
description: Close the loop after research, an experiment, a launch, or a stop by appending expected vs actual results, threshold outcome, changed assumptions, confidence before/after, decision impact, surprises, follow-ups, and calibration notes to 12-learning-log.md without altering old decision records. Use when experiment results arrive, when a decision is revisited, or at the end of a /j-independent-ideation run.
---

# Learning from decisions

**Input**: `11-decision-record.md`, `10-experiment-portfolio.md`, new results or evidence. **Output**: appended entry in `12-learning-log.md` (template in `../j-independent-ideation/templates/learning-log.md`); new ledger items in `03-evidence-ledger.jsonl`.

## Procedure

1. Append one entry per result or event: expected result · actual result · threshold met (yes/no/inconclusive) · which assumption changed (`A-nnn`) · confidence before → after (low/moderate/high) · did it change a decision · surprise or anomaly · follow-up · score calibration note (were priorities/estimates well calibrated?) · evidence artifacts created (`E-nnn`).
2. Add every raw result to the ledger as T1 (observed behaviour, paid commitment) with provenance.
3. Never edit an old `11-decision-record.md`. If the verdict changes, create a new record in a new workspace and link both ways.
4. Update `manifest.yaml` status. If the result invalidates a fatal assumption, notify the human decider explicitly.

Failure: a result without a predefined threshold cannot be scored as pass/fail; log it as inconclusive and note the missing threshold as a calibration lesson.
