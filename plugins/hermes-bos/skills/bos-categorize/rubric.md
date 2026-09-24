# bos-categorize Rubric

This file contains the rubric used by the bos-categorize skill to assign a category to a triage card.

## 1. Decision Rubric Overview

The categorizer answers one question: **what is the cheapest reliable route to a correct answer?**
It does not answer the question itself — that is the downstream researcher's job.

### 1.1 Inputs

| Input | What it captures | How to obtain it |
|-------|------------------|------------------|
| **Task text** | The verbatim request — what the requester asked, with any constraints already in the body | Already present in the work item body / chat / kanban card. No extraction cost. |
| **Domain novelty** | Has this question (or a close variant) already been answered on this machine? How recent? How well-evidenced? | OpenViking `viking_search` + `INDEX.md` lookup in `business-os/knowledge/research/`. Cheap: corpus scan, no web rung. |
| **Blast radius** | If we get this wrong, what is the cost? (Reversibility × scope × exposure.) | Work-item metadata: `risk_class` (low / medium / high / critical) per `constitution/risk-policy.md`; approval class per `constitution/authority-matrix.md`; for kanban tasks the `priority` field and any explicit cost/time tag. |
| **Reversibility** | Can the deliverable be undone cheaply, or does it ship locked-in? | Approval class already encodes most of this — `READ`/`DRAFT` are reversible; `EXTERNAL`/`IRREVERSIBLE` are not. Pull from the work item frontmatter. |

### 1.2 Outputs

| Output | Meaning | Default follow-on action |
|--------|---------|--------------------------|
| **quick-lookup** | A bounded factual question; an already-answered variant exists locally; low blast radius and reversible | Run the cheapest rung available — `viking_search` + a single searxng probe if needed; do **not** spawn a researcher profile; answer inline. |
| **pre-research** | The question needs verification beyond local corpus but does not require multi-source triangulation; novelty or staleness is the main risk | Run a single searxng-first ladder pass on the local-first research ladder (see `~/.hermes/skills/local-deep-research/SKILL.md`); produce a 1-page note; do **not** fan out to a researcher seat unless the pass fails. |
| **deep-research** | The question is novel, decision-driving, has high blast radius, or touches multiple sources that disagree; reversible? no | Spawn a researcher task with the bounded evidence pack spec (`bos-research` skill); require source ledger, contradiction table, per-claim confidence; promote to a verifier review before delivery. |
| **workshop** | The question is ambiguous; the answer is a decision the owner must make; multi-stakeholder; benefits from a structured facilitation method (LDJ, continuous-discovery, GV sprint) | Spawn a delivery-manager task to design the workshop; pull from the multi-agent orchestration patterns memo (`2026-09-22-multi-agent-orchestration-patterns-memo.md`); run human-in-the-loop. |

### 1.3 Decision Logic (the Rubric Itself)

A 5-step procedure, designed to be auditable:

1. **Local analog check.** Query `viking_search` + `INDEX.md` for a prior research artifact on the same question. If a recent (≤ 90 days), high-confidence artifact exists, downgrade one step (workshop → deep, deep → pre, pre → quick, quick → quick).

2. **Reversibility filter.** If the work item's approval class is `EXTERNAL` or `IRREVERSIBLE`, the minimum category is `deep-research` (regardless of novelty). If approval is `READ` or `DRAFT`, proceed.

3. **Blast radius check.** If `risk_class` is `high` or `critical` OR `approval` is `EXTERNAL` or `IRREVERSIBLE`, upgrade one step (quick → pre, pre → deep, deep → workshop, workshop → workshop).

4. **Domain novelty check.** If domain novelty is high (no recent local artifact) AND blast radius is medium or high, upgrade one step (quick → pre, pre → deep, deep → workshop, workshop → workshop).

5. **Final categorization.** Apply the steps in order, then map the resulting step to the output category:
   - After step 1: if we downgraded, use that level; otherwise, start from the baseline of `quick-lookup`.
   - Apply steps 2-4, each potentially upgrading the category.
   - The final level maps to:
     - 0 steps above quick-lookup → `quick-lookup`
     - 1 step above → `pre-research`
     - 2 steps above → `deep-research`
     - 3 or more steps above → `workshop`

## 2. Confidence

Set `category_confidence` based on:
- **High**: All inputs are clear and unambiguous, and the rubric steps are deterministic.
- **Medium**: One input is ambiguous or relies on a judgment call (e.g., domain novelty borderline).
- **Low**: Multiple inputs are ambiguous or the rubric steps conflict.

## 3. Example Application

See the work-item-frontmatter-schema.md for an example of how the category fields are recorded.

## 4. Integration Point

The kanban-orchestrator (or a small pre-promotion hook) should call this categorization procedure before promoting a triage card to ready. If the categorization fails (e.g., missing inputs or rubric error), the card remains in triage and the owner is notified.
