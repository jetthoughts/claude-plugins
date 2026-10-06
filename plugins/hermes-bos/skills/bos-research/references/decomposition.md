# Decomposition (D1–D5)

Decompose before any search tool call. Each step is a gate, not a suggestion.

## D1 — Rewrite into ≤5 atomic claims

A "research question" is not a topic. "Research Upwork" is a topic.
"Does Upwork's GraphQL API expose a submit-proposal mutation?" is a
bounded, falsifiable question. Each atomic claim must be:

- One bounded evidence package can answer it
- A yes/no or concrete answer is reachable
- It fits in one row of the matrix

**Bad:** "What tools help with Upwork lead gen?" — too broad, 100 tools.
**Good:** "What is the official Upwork API for submitting proposals?" — one URL answers.

## D2 — Name the evidence surface per claim

For each atomic claim, write down:

- **Candidate sources/channels** to evaluate (e.g., "Upwork Help Center
  for ToS, GitHub for lead-upwork-mcp, niche blog for community
  sentiment")
- **Verdict vocabulary** the agent will use (adopt / adapt / skip with
  a reason; or primary / secondary / tertiary / unverified for sources)
- **Acceptance stop condition** (e.g., "stop when 2+ primary sources
  confirm" or "stop when primary contradicts secondary")

This prevents scope creep mid-run.

## D3 — Must-evaluate vs nice-to-check

Split the claim list into two:

- **Must-evaluate** — every claim here gets a verdict, no exceptions
- **Nice-to-check** — only after must-evaluate claims are done

A new claim joins must-evaluate only when a **material gap** appears
(a contradiction, a primary source failing, an active miscalibration).
A tertiary source turning up something interesting is not a material
gap.

## D4 — Assign source tier expectation per claim BEFORE reading

For each claim, pre-commit to the source tier required:

- **Primary** (required for decision-driving claims): official docs,
  standards, filings, primary research — Upwork Help Center, PyPI
  page, GitHub README, official API docs
- **Secondary** (acceptable for adjacent claims): reputable press,
  analyst reports, vendor documentation
- **Tertiary** (acceptable for community signal only): blogs, forums,
  social posts
- **Unverified** (rarely acceptable): single unattributed claims

The tier is a pre-commitment. It prevents laundering a convenient
source as "just my judgment" after the fact.

## D5 — State the research mode

Pick one:

- **Deep research** — runs §2–§9 (full protocol: clarification,
  gathering, synthesis, verification gate, red-team, three-contract
  deliverable, novelty gate)
- **Quick lookup** — runs only §4 gathering + §5 synthesis (no
  clarification, no verification gate, no red-team)

Default is deep. Quick lookup only for narrow, well-defined questions
where the cost of running the full protocol exceeds the cost of being
wrong.

**When in doubt: deep.** The compounding-error problem (5% per-step
error → 63% failure on 100-step tasks) is real. The verification gate
catches it. Skipping it for a "small question" is how small questions
become wrong deliverables.
