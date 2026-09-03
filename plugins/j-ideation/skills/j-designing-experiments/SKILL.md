---
name: j-designing-experiments
description: Convert the riskiest assumptions and council disagreements into a ranked, bounded experiment portfolio (10-experiment-portfolio.md) of experiment cards with thresholds, budget, duration, owner, and next actions, scored by Experiment Priority and evidence-capped RICE via a deterministic script. Use inside /j-independent-ideation after assumptions or the council, for experiment-prioritisation runs, or whenever a plan proposes building before testing.
---

# Designing experiments

Method aids: `pm-product-discovery:brainstorm-experiments-new` / `:brainstorm-experiments-existing`. Scoring: `scripts/score_portfolio.py 10-experiment-portfolio.md` (stdlib). Card schema: `../j-independent-ideation/templates/experiment-card.yaml`.

**Input**: `08-assumption-map.md`, `09-council/consensus-report.md` (if any), `00-decision-brief.md`. **Output**: `10-experiment-portfolio.md`.

## Allowed patterns

Customer problem interview · JTBD interview · expert interview · competitor/search-demand test · landing-page smoke test · fake-door · pricing/WTP interview · proposal/pre-sale test · concierge pilot · Wizard-of-Oz · channel response test · technical spike / code spike (time-boxed, throwaway code, ends in a written verdict against the hypothesis) · paper/Figma prototype · first-click · five-second comprehension · tree test/card sort · moderated/unmoderated usability session · A/B only with adequate traffic and instrumentation.

## Procedure

1. For each top-priority or fatal assumption and each council disagreement, write one card. Every field filled: hypothesis, falsification condition, method, sample target, primary + guardrail metrics, success/failure thresholds, inconclusive rule, duration, budget, effort, owner, instrumentation, privacy/legal checks, decision unlocked, next-if-pass/fail/inconclusive.
2. Add scoring inputs: `expected_information_gain` 1–5, `decision_importance` 1–5, `evidence_basis` (model-consensus ≤0.30 · anecdote ≤0.40 · customer-signals ≤0.60 · prototype ≤0.75 · behavioral ≤0.85 · paid ≤1.00). Use `[low, high]` ranges where inputs are uncertain; never fake precision.
3. Put cards in a ```json block; run the script; paste the ranking.
4. Recommend: one experiment to run now · one contingency · experiments not worth running and why · every card needing human approval (`requires_human_approval: true` for anything that contacts people, spends money, publishes, or touches production).
5. Prefer the smallest test that could disprove the riskiest assumption over any build.

Failure: script reports missing fields → fix the card; a card without a failure threshold is not an experiment.
