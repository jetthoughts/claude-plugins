---
name: bos-categorize
description: "Use when a triage card needs a category assigned before promotion. Implements the bos-categorize rubric to assign one of four categories: quick-lookup, pre-research, deep-research, workshop."
version: 0.1.0
author: kanban-orchestrator
platforms: [macos]
---

# bos-categorize Skill

This skill provides the procedure and rubric for categorizing a triage card in the Business OS.
It is run by the kanban-orchestrator (or any agent) before promoting a triage card to ready.

## Procedure

1. **Gather the four inputs** from the work item (kanban card):
   - **Task text**: The verbatim request from the work item body.
   - **Domain novelty**: Check if a recent (≤90 days), high-confidence artifact exists locally via `viking_search` + `INDEX.md` lookup in `business-os/knowledge/research/`.
   - **Blast radius**: Derived from `risk_class`, `approval` class, and `priority` field in the work item frontmatter.
   - **Reversibility**: Derived from `approval` class (READ/DRAFT are reversible; EXTERNAL/IRREVERSIBLE are not).

2. **Apply the rubric** (see `rubric.md` for the full decision logic):
   - The rubric is a 5-step procedure that maps the four inputs to one of four outputs.
   - The outputs are: `quick-lookup`, `pre-research`, `deep-research`, `workshop`.

3. **Record the result** in the work item frontmatter:
   - Set `category` to the chosen output.
   - Set `category_reason` to a one-sentence explanation of which rubric step(s) decided it.
   - Set `category_confidence` to High/Medium/Low based on the certainty of the inputs (optional).

4. **Reject promotion** if the categorization fails or the category is missing.

## Rubric

The rubric is defined in `rubric.md` within this skill directory. It encodes the four inputs, the decision logic, and the mapping to outputs.

## Example

Given a work item with:
- Task text: "What is the capital of France?"
- Domain novelty: Low (recent local answer exists)
- Blast radius: Low (reversible, low risk)
- Reversibility: High

The categorizer would output: `quick-lookup`.

## Implementation Note

This skill is meant to be used as a procedural guide. The agent should follow the steps above, using the tools available (viking_search, reading the work item frontmatter, etc.) to compute the category.

For automation, a script could be added to this skill that performs the categorization automatically, but the core value is the explicit rubric and procedure.
