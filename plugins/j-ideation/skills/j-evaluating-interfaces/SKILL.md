---
name: j-evaluating-interfaces
description: Evaluate UI/UX concepts without confusing aesthetics, model preference, and usability — context gate, split Nielsen heuristic passes (1–5 and 6–10), cross-screen consistency pass, conventions guard, accessibility and state resilience, behavioral framing (perception, memory, action), and conversion of disagreement into representative-user tests. Use inside /j-independent-ideation ux runs after variants exist, or whenever someone asks which design is "best".
---

# Evaluating interfaces

AI reviewers are not end users. They produce hypotheses and heuristic risks; representative-user behaviour settles important UX choices.

**Input**: persona, JTBD and critical task, screenshots/prototype/UI code/flow description, device requirements, accessibility constraints, design system, analytics and known feedback, business outcome; `07-concepts/`. **Outputs**: `09-council/consensus-report.md` (UX heat map) and appended cards in `10-experiment-portfolio.md`.

## Phases

1. **Context gate** — refuse aesthetic scoring without target user, task, and success outcome. Ask for missing source material.
2. **Per-screen heuristic pass** — `j-ux-heuristic-evaluator` ×2 in isolation: one for Nielsen 1–5, one for 6–10. Record only likely violations. Each issue: heuristic, severity 0–4, affected task, user impact, screen/reference, evidence/rationale (`E-nnn` where observed), recommendation, confidence (low/moderate/high).
3. **Cross-screen pass** — `j-information-architecture-reviewer` reviews the ordered flow for terminology, hierarchy, spacing, control placement, state transitions, interaction logic; deduplicates repeats.
4. **Conventions guard** — a separate reviewer marks findings that merely criticise platform conventions or mistake decorative UI for controls as `CONVENTION CHECK REQUIRED`. Never delete them silently.
5. **Accessibility and resilience** — `j-accessibility-auditor`: keyboard, focus, semantics, contrast where data permits; loading, empty, error, permission-denied, success states; mobile/responsive.
6. **Behavioral framing** — for each material issue state the effect on perception (notice), memory (understand), action (complete/abandon).
7. **Decision rule** — no vote on style. Convert each meaningful disagreement into a representative-user test card (first-click, five-second, task completion, usability session, preference-with-why, tree test/card sort, fake-door, A/B). Severity 0 findings are excluded from priority. The human decider gets the heat map plus the test plan.

Failure: context gate unmet → stop with the list of missing inputs.
