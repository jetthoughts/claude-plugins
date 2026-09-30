---
type: Template
title: PRD template — product discovery output
status: stable
---

# <PRD Title>

## Frontmatter

```yaml
id: PRD-YYYYMMDDNN
title: <one-line title>
status: draft | reviewed | approved
date: YYYY-MM-DD
owner: <who owns this PRD>
sources:
  - <path or URL>
  - <path or URL>
confidence_summary: <one line: overall confidence and any low-confidence areas>
buy_or_build: buy | build | hybrid
open_questions:
  - <question>
  - <question>
next_steps:
  - <actionable next step>
  - <actionable next step>
```

## 1. Problem

<What is broken or missing today. 2–5 sentences.>

**Outcome when done:** <what must be true — measurable where possible>

**Constraints:**
- <platform / budget / timeline / must-use / must-not-use>

**Surfaces:** <where it must run>

## 2. Users & Stakeholders

| Role | What they need | Priority |
|---|---|---|
| <role> | <need> | <P0/P1/P2> |

## 3. Requirements

### 3.1 Functional

| # | Requirement | Sourced / Assumption | Priority |
|---|---|---|---|
| F1 | <requirement> | <source or "assumption"> | <P0/P1/P2> |

### 3.2 Non-functional

| # | Requirement | Note |
|---|---|---|
| N1 | <performance / security / privacy / cost cap> | <note> |

## 4. Landscape (summary)

<2–4 sentences: what exists today, what the landscape table (in the work product) contains.>

**Key pattern observed:** <one line>

## 5. Critique (summary)

| Candidate | Verdict | Deciding factor |
|---|---|---|
| <name> | keep / auxiliary / drop | <factor> |

## 6. Validation (summary)

- **Critical claims:** <list, each with confidence band and source>
- **Low-confidence areas:** <list, each flagged>

## 7. Solution Outline

<What the chosen solution looks like — 1–3 paragraphs.>

## 8. Buy / Build Decision

**Decision:** <buy / build / hybrid>

**Rationale:** <why this path, 2–5 sentences>

**What is bought:** <list — service / platform / tool, with name>

**What is built:** <list — what we build, around what>

**Gaps the build addresses:** <list>

**Simplest viable MVP:** <one paragraph: the smallest thing that delivers the core outcome>

## 9. Open Risks

| Risk | Likelihood | Impact | Mitigation / Open question |
|---|---|---|---|
| <risk> | <low/med/high> | <low/med/high> | < mitigation or open question> |

## 10. Next Steps

1. <actionable step>
2. <actionable step>

## Appendix: Work Product Files

- `01-frame.md`
- `02-landscape.md`
- `03-critique.md`
- `04-validation.md`
- `05-decision.md`
