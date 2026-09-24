---
name: bos-lens-router
description: Pick one agency-agents lens per work item, never all.
author: pftg
---

# Lens Router

Use when a work item needs a specialist perspective: research, QA verdict,
governance ruling, growth campaign, delivery planning, persona change.

Source library: `msitarzewski/agency-agents` (reviewed 2026-09-22,
`kb/hermes/05-community/agency-agents-review.md`). Adopted persona skills:
`agency-chief-of-staff`, `agency-evidence-collector`, `agency-research-synthesist`.

## Rules

1. Pick **one** lens from the map. Never inject the whole roster — overlap
   and prompt bloat weaken governance.
2. Record the chosen lens in the work item's evidence pack or result.
3. The lens shapes the deliverable; it never grants authority. Approval
   classes and the seat's own authority stay as configured.
4. If two lenses fit, take the one with the narrower deliverable.

## Lens map

| Profile / work type | Lens (upstream pattern) | Default deliverable |
|---|---|---|
| kanban-orchestrator | Agents Orchestrator, Project Shepherd, Studio Producer | execution brief, dependency map, handoff, status report |
| researcher | Trend Researcher, Feedback Synthesizer, Tool Evaluator, Knowledge Graph Engineer | evidence pack, source ledger, contradiction/confidence table |
| quality-guardian | Reality Checker, Test Results Analyzer, Tool Evaluator | verdict, evidence matrix, defect list |
| growth-operator | Outbound Strategist, Content Creator, SEO Specialist, Offer & Lead Gen Strategist | ranked opportunities, experiment brief, draft assets, measurement plan |
| delivery-manager | Project Shepherd, Senior Project Manager, Meeting Notes Specialist | charter, milestone plan, RAID log, owner-ready update |
| governance-auditor | Automation Governance Architect, Compliance Auditor | constraint inventory, blast-radius report, ruling |
| soul-curator | Prompt Engineer, Persona Walkthrough Specialist | persona diff, invariant inventory, rollback/hash record |

## Reality Checker defaults (QA lens)

- Default verdict is NEEDS WORK; PASS requires reproducible evidence.
- Treat perfect scores and "zero issues" claims as evidence gaps until verified.
- Screenshot proof is required only for UI work.

## Tool Evaluator checklist (any tool/MCP/provider/agent recommendation)

Functionality, security, integration, performance, cost/TCO, adoption risk,
exit/migration path. All seven, every time — used by `agent-prevalidate`.
