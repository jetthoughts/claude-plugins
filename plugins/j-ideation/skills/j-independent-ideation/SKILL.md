---
name: j-independent-ideation
description: Daily entry point (/j-independent-ideation) for evidence-based decisions on new services, markets/ICPs/channels, features, experiment prioritisation, and UI/UX direction. Use whenever the user wants to find, assess, test, or decide on an opportunity, or asks "what should we build/offer/test next". Routes to the lower-level ideation skills, creates the decision workspace, and enforces the human decision gate. Do not use for implementation work or for research that has no decision attached.
---

# Independent Ideation (router)

Only daily entry point. Never run a lower-level skill outside a workspace this skill created.

## 1. Intake

Accept the intake block (see `templates/intake.yaml`). If it is missing or partial, ask only the minimum
questions to obtain ALL of: one decision, one measurable desired outcome, target customer/user, deadline,
named human decider, and what evidence would change the decision. Do not start research before these exist.

Classify `decision_type` and `reversibility`. Unknown reversibility → treat as type-1 until the brief says otherwise.

## 2. Create the workspace

`.claude/artifacts/independent-ideation/<YYYY-MM-DD>-<slug>/` — copy from `templates/`:

```text
00-intake.yaml  00-decision-brief.md  01-existing-evidence.md  02-research-plan.md
03-evidence-ledger.jsonl  04-contradiction-register.md  05-lightning-demos.md
06-opportunity-tree.md  07-concepts/{concept-A,B,C,concept-map}.md  08-assumption-map.md
09-council/{brief.md,round-1/,anonymized-rationales.md,round-3/,consensus-report.md}
10-experiment-portfolio.md  11-decision-record.md  12-learning-log.md  manifest.yaml
```

Always create: `00-decision-brief.md`, `03-evidence-ledger.jsonl`, `04-contradiction-register.md`,
`08-assumption-map.md`, `10-experiment-portfolio.md`, `11-decision-record.md`, `manifest.yaml`.
Create the rest only when the route below uses them. Record every skill and tool used in `manifest.yaml`.

## 3. Route

| decision_type | Sequence |
|---|---|
| new-service | j-framing-the-question → j-running-independent-research → j-scanning-lightning-demos → j-mapping-opportunities → j-generating-independent-variants → j-mapping-assumptions → j-convening-the-council → j-designing-experiments → j-making-the-call → j-learning-from-decisions |
| market | j-framing-the-question → j-running-independent-research → j-mapping-opportunities → j-generating-independent-variants → j-mapping-assumptions → j-convening-the-council → j-designing-experiments → j-making-the-call |
| feature | j-framing-the-question → **inspect product analytics + customer evidence first** (`01-existing-evidence.md`) → j-running-independent-research → j-mapping-opportunities (use `pm-product-discovery:opportunity-solution-tree`) → j-generating-independent-variants → j-mapping-assumptions → j-convening-the-council → j-designing-experiments → j-making-the-call |
| experiment | j-framing-the-question → read existing decision/opportunity/experiment artifacts in `.claude/artifacts/independent-ideation/` → j-mapping-assumptions → j-designing-experiments (prioritised portfolio) → j-making-the-call |
| ux | j-framing-the-question → evaluate UI context + behavioral analytics → j-running-independent-research only for factual gaps → j-scanning-lightning-demos → j-generating-independent-variants (UX archetypes) → j-evaluating-interfaces → j-mapping-assumptions → j-designing-experiments → j-making-the-call |

Invoke each step with the Skill tool by name. Each step reads its declared inputs from the workspace and
writes its declared outputs. Stop and report if a step's hard gate fails; do not skip ahead.

## 4. Finish

1. Run `~/.claude/skills/j-independent-ideation/scripts/validate.sh <workspace>`; fix every ERROR before presenting.
2. Present `11-decision-record.md` to the human decider. Type-1 verdicts and any external action wait for
   explicit approval in chat; record it in the frontmatter (`human_approval: approved`, `approved_by`).
3. Update `manifest.yaml` status and hand off with the exact next action.

## Non-negotiables (apply in every step)

- Label every substantive statement FACT / INFERENCE / ASSUMPTION / ESTIMATE / CONTRADICTION / UNKNOWN; FACT cites `E-nnn`.
- Likelihood and confidence are separate fields with the allowed words; never a single number.
- Ideators never see each other's concepts; reviewers never learn authorship; the decision agent adds no facts.
- Council consensus is advisory (rank 7 of 8 in the evidence hierarchy, see `~/.claude/skills/j-independent-ideation/DECISION-POLICY.md`).
- No outreach, ads, publishing, purchases, paid accounts, or production changes without explicit user confirmation.
- Use the repo's configured tools (Perplexica/SearXNG MCP, `research`, `research-deep`, `pm-*` plugins, semble, OpenViking); never hard-code tool settings.
