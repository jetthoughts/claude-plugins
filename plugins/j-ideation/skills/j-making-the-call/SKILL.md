---
name: j-making-the-call
description: Produce one auditable decision record (11-decision-record.md) with a GO, EXPERIMENT, RESEARCH-MORE, PIVOT, or STOP verdict, pre-mortem, kill criteria, preserved dissent, separate likelihood and confidence, and an explicit human-approval gate for type-1 decisions and external actions, validated by a deterministic script. Use as the last step of every /j-independent-ideation run; never to invent new facts or rewrite evidence.
---

# Making the call

Run as the `j-decision-agent` agent: reads final artifacts only; adds no facts; edits no evidence; never redefines success criteria after results; preserves dissent. Validator: `scripts/validate_decision.py 11-decision-record.md --ledger 03-evidence-ledger.jsonl`. Policy: `~/.claude/skills/j-independent-ideation/DECISION-POLICY.md`.

**Input**: `00-decision-brief.md`, `03-evidence-ledger.jsonl`, `04-contradiction-register.md`, `08-assumption-map.md`, `09-council/consensus-report.md` + `consensus-summary.json`, `10-experiment-portfolio.md`. **Output**: `11-decision-record.md` (template in `../j-independent-ideation/templates/`).

## Procedure

1. Pre-mortem: "Six months from now this failed. What early signals did we see?" Collect signals from three isolated contexts (`j-cold-eyes-reviewer`, `j-commercial-analyst`, `j-evidence-auditor`) BEFORE showing any answers to the others.
2. Convert each material signal into a kill-criteria row: metric, threshold, date (YYYY-MM-DD), owner, action. Set review cadence.
3. Choose exactly one verdict by the policy: GO only with evidence threshold met, no unresolved fatal assumption, acceptable economics/delivery, and human approval · EXPERIMENT when promising with a bounded test · RESEARCH-MORE when decisive info is obtainable and testing is premature · PIVOT when problem holds but segment/solution/channel/delivery/pricing fails · STOP when problem evidence is weak, buyers unreachable, economics or risk unacceptable, or kill criteria hit.
4. If the council disagrees: observed behaviour beats all model advice → cheap discriminating test ⇒ EXPERIMENT → reversible ⇒ smallest instrumented option → irreversible ⇒ research or human governance → purely aesthetic ⇒ design-system consistency or user test → tied ⇒ lower downside and faster learning.
5. Fill every section; likelihood and confidence in separate columns with the allowed words; council numbers from `consensus-summary.json`; dissent quoted, not summarised away.
6. Classify type-1/type-2. Type-1 or any external action: `human_approval: required`, present to the human decider, stop until approval is given in chat, then record `approved_by`.
7. Run the validator; fix errors; hand to j-learning-from-decisions.

Failure: validator errors → fix the record, never the evidence. Missing council or portfolio → verdict cannot be GO.
