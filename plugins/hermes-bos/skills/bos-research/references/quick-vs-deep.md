# Quick lookup vs deep research (§10)

Pick the right mode before starting. The mode determines which phases run.

## Decision tree

| Signal | Likely mode |
|---|---|
| 10+ tabs would be needed to answer manually | **Deep** |
| Ambiguous or multi-interpretation question | **Deep** |
| Claims will drive a decision | **Deep** |
| High compounding-error risk (multi-step claim chain) | **Deep** |
| Single fact, one URL answers it | **Quick** |
| Well-defined, narrow question | **Quick** |
| Low stakes, exploratory | **Quick** |

## What runs in each mode

### Quick lookup

- §4 Phase 2: Gathering (with T1–T4 if any claim survives into deliverable)
- §5 Phase 3: Synthesis
- **No clarification, no verification gate, no red-team pass**

Use this when the cost of the full protocol exceeds the cost of being
wrong. A quick lookup with ≥1 primary source is enough to answer
"What is the current version of lead-upwork-mcp?" (one PyPI page).

### Deep research

- §3 Phase 1: Clarification (if needed)
- §4 Phase 2: Iterative Gathering (T1–T4 enforced)
- §5 Phase 3: Synthesis
- §6 Verification Gate (re-search via different tool)
- §7 Red-Team Pass (5 adversarial tests)
- §8 Three-Contract Deliverable (evidence pack, source ledger, contradiction table)
- §11 Novelty Gate (≥3 NEW findings)

Use this when the question is open-ended, decision-driving, or
multi-step. Skipping verification for "speed" is how 5% per-step error
compounds to 63% failure on 100-step tasks.

## When to escalate from quick to deep

- The gathering phase surfaces ≥3 sources that disagree
- The synthesis surfaces a contradiction
- The user changes scope mid-run
- A new claim is added that wasn't in the original decomposition

The mode can change mid-run. Mark the transition explicitly in the
matrix header.
