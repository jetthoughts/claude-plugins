# Architecture Snapshot

## Repository Map

| Module | Language | Symbols | Exported |
|--------|----------|---------|----------|
| `plugins/deliberate/deliberate-workspace` | python | 2 | 2 |
| `plugins/harness-setup/scripts` | python | 44 | 44 |
| `plugins/j-ideation/skills/j-convening-the-council/scripts` | python | 5 | 5 |
| `plugins/j-ideation/skills/j-designing-experiments/scripts` | python | 4 | 4 |
| `plugins/j-ideation/skills/j-making-the-call/scripts` | python | 4 | 4 |
| `plugins/j-ideation/skills/j-running-independent-research/scripts` | python | 2 | 2 |
| `plugins/j-research/skills/j-research-inbox/scripts` | python | 18 | 18 |

## Extraction Quality

- Files parsed: **133** / 203 seen (4 file(s) + 4 directory tree(s) skipped by ignore globs)
- Parse errors: 0

## Architecture Pattern

_No specific architecture pattern detected._

## Entry Points

- **main**: `plugins/harness-setup/scripts/harness.main` (plugins/harness-setup/scripts/harness.py)
- **main**: `plugins/j-ideation/skills/j-convening-the-council/scripts/aggregate_council.main` (plugins/j-ideation/skills/j-convening-the-council/scripts/aggregate_council.py)
- **main**: `plugins/j-ideation/skills/j-designing-experiments/scripts/score_portfolio.main` (plugins/j-ideation/skills/j-designing-experiments/scripts/score_portfolio.py)
- **main**: `plugins/j-ideation/skills/j-making-the-call/scripts/validate_decision.main` (plugins/j-ideation/skills/j-making-the-call/scripts/validate_decision.py)
- **main**: `plugins/j-ideation/skills/j-running-independent-research/scripts/validate_evidence.main` (plugins/j-ideation/skills/j-running-independent-research/scripts/validate_evidence.py)
- **main**: `plugins/j-research/skills/j-research-inbox/scripts/normalize.main` (plugins/j-research/skills/j-research-inbox/scripts/normalize.py)

## Dependency Rules

_No internal dependency rules detected._

## Critical Modules

_No cross-module dependencies detected._

---

*Generated at 2026-09-09T18:24:42Z in 237.4ms. 987 facts, 22 insights.*
