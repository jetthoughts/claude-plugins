---
name: bos-skill-evolution
description: Detect weak skills, evolve via GEPA, gate the diff.
author: pftg
---

# Skill Evolution Loop

Use when reviewing skill quality or after failure clusters: pick the ONE skill
most worth evolving, run GEPA on free lanes, gate the result through owner
review. Never evolve more than one skill per pass.

## 1. Detect (evidence, not vibes)

Score each candidate skill 0-2 per signal; highest total wins:

| Signal | Source | 2 points when |
|---|---|---|
| Failure rate | kanban `last_failure_error`, task_runs outcomes | >= 2 failures in last 20 runs |
| Usage | session logs, kanban `skills` column counts | used >= 5 times/week |
| Drift | `hermes skills list-modified`, file mtime | edited by hand >= 3 times/month |
| Impact | business criticality (intake, research, apply flows) | on a revenue path |
| Fitness signal | existing acceptance criteria / benchmark | has real ACs (golden dataset possible) |

Tie-break: prefer the skill WITH acceptance criteria — GEPA needs fitness
signal; deep-research (E1-E4) and bos-intake (WI gate verdicts) qualify today.

## 2. Evolve (free lanes, staged)

```bash
hermes-evolve-skill <name> --dry-run          # setup validation, zero cost
hermes-evolve-skill <name> --iterations 10    # free OmniRoute lanes
```

Live skill never mutated (wrapper stages to /tmp). Output lands in the
plugin's `./output` with before/after fitness.

## 3. Gate (owner decides)

- Improved fitness: draft a proposal (diff + fitness numbers) into
  `governance/proposals/`; owner approves; apply via `hermes skills install`
  or file copy; record in the skill's changelog note.
- Not improved: archive the output, note why in the kanban task. Do NOT retry
  the same skill within 30 days unless its failure signal doubles.

## 4. Cadence

Triggered, not scheduled: kanban-orchestrator runs detection during the
management-review (Fri) when a skill crosses 2 failure points, or the owner
asks directly. No dedicated cron.
