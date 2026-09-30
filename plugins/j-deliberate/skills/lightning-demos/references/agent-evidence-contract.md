# Agent evidence contract

The `lightning-demos` round is the method. This is the contract that makes its output auditable when the contributors are agents rather than people in a room.

## Five isolated roles

Spawn five `j-research-lead` agents in parallel, each with **ONE** role and no access to the others' output:

**direct-competitor · adjacent-industry · distant-industry · failed-or-negatively-reviewed · consumer-grade/low-friction**

Merge only after all five return. Never show one role another's findings before the merge.

## The fixed shape

Each agent returns exactly three demos saved to `05-lightning-demos.md`, in this shape:

```yaml
- demo_id: LD-01
  role: direct-competitor
  source: ""
  sector: ""
  mechanism: ""
  user_problem_solved: ""
  why_it_works: ""
  evidence_id: ""
  transferable_to_us: ""
  cost_or_complexity_to_adapt: low | medium | high
  risks_when_transferred: []
```

The workspace template is `plugins/j-ideation/skills/j-independent-ideation/templates/lightning-demos.md`.

## The rules

- **Every demo cites an `E-nnn`.** Add the source to the evidence ledger before the demo counts; an uncited row is not a demo.
- **≥30% of demos must come from outside the target industry**, and at least one must be a failure pattern carrying an explicit "what to avoid".
- **Extract the mechanism, job, incentive, interaction, or delivery model.** Reject entries that copy visual styling or a feature list.

## UNKNOWN on shortfall

A role that returns fewer than three sourced demos is recorded as **UNKNOWN** for that role. Never fill its slot from another role's output, and never pad the board to reach ten. A visible gap is cheaper than one papered over.
