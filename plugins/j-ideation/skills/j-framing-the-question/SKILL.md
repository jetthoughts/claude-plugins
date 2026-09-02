---
name: j-framing-the-question
description: Turn a vague business, product, market, or UX request into a decision-ready brief (00-decision-brief.md) with one decision, one measurable outcome, target user, constraints, reversibility, decision owner, human decider, and "what would change our mind". Use as the first step of every /j-independent-ideation run or whenever a request has no clear decision attached. Refuses to proceed until the brief is complete.
---

# Framing the question

**Input**: `00-intake.yaml` (or the user's words). **Output**: `00-decision-brief.md` (template: `../j-independent-ideation/templates/decision-brief.md`).

## Procedure

1. Read `00-intake.yaml`. Read `.claude/artifacts/independent-ideation/*/11-decision-record.md` for prior decisions on the same topic; link them under Existing beliefs.
2. Write the decision as one sentence starting "Decide whether to …". If two decisions hide inside, split them and ask which one is first.
3. Write ONE desired outcome with metric, baseline (or UNKNOWN), target, horizon.
4. Name the target customer/user and the job they are trying to make progress on.
5. Fill constraints from intake. Missing budget or effort cap → ask; do not guess.
6. Classify reversibility: type-1 (irreversible or expensive) or type-2 (cheap, reversible). If unsure, type-1.
7. Build the criteria table (criterion, weight, measurement, evidence threshold). Weights sum to 1.0.
8. List existing beliefs; tag each FACT (with `E-nnn` from `01-existing-evidence.md`/ledger), INFERENCE, ASSUMPTION, or ESTIMATE.
9. Write "What would change our mind?" as a specific, observable result.
10. Write exclusions.
11. Set frontmatter `status: framing`, `decision_id` (`<YYYYMMDD>-<slug>`), owner, human decider, deadline.

## Hard gate

Do not hand off to research if any of these is empty: decision sentence, measurable outcome, deadline,
target customer/user, constraints, reversibility, decision owner, human decider, what-would-change-our-mind.
On failure: list the missing fields, ask only for those, stop.
