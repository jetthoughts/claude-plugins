---
name: j-running-independent-research
description: Structured, cited research for a decision brief using internal artifacts first, then the local keyless search stack (Perplexica, SearXNG and Local Deep Research MCPs, research and research-deep skills, semble, OpenViking), producing 02-research-plan.md, 03-evidence-ledger.jsonl, and 04-contradiction-register.md with tiered, labelled evidence and an independent falsification pass. Use inside /j-independent-ideation after the brief exists, or whenever a decision needs sourced evidence rather than opinion.
---

# Running independent research

**Input**: `00-decision-brief.md`. **Outputs**: `01-existing-evidence.md`, `02-research-plan.md`, `03-evidence-ledger.jsonl`, `04-contradiction-register.md`.
Validator: `scripts/validate_evidence.py <workspace>`.

## Source order (always)

1. Repo + prior decision artifacts (`mcp__semble__search`, tokensave, OpenViking `search`).
2. Internal customer evidence, sales notes, support, proposals, analytics exports (paths from intake).
3. Existing product/service implementation and technical constraints.
4. External via the local keyless stack, in this order (see `j-deep-research` for budgets and measured latencies): `mcp__perplexica__search` (≤2 calls per question, `j-perplexica-search` rules) → `mcp__searxng__searxng_web_search` for raw ranked URLs → `mcp__ldr__quick_research` for a cited multi-source summary of one sub-question (≈2–3 min each) → the installed `research` / `research-deep` skills for multi-source outlines.
5. Remote fallbacks only where 1–4 leave a factual gap: `RivalSearchMCP` (keyless), then `WebSearch`. Record the limitation in `02-research-plan.md` when a local tool is down.

## Mode

quick = 3–5 subquestions (triage) · standard = 6–10 (competitor/feature/channel) · decision-grade = 10–20 (major service, market, material investment). Pick from brief reversibility and budget; record it.

## Lenses (cover each; mark UNKNOWN when nothing is found)

Customer/JTBD · problem severity, frequency, urgency, consequences · demand and purchase signals · direct/indirect competitors, substitutes, DIY, do-nothing · pricing, willingness to pay, margins, delivery cost · distribution and buyer access · technical feasibility and dependencies · legal, privacy, security, regulatory · strategic fit and reusable agency assets · falsification (facts that would make this unattractive).

## Procedure

1. Write `02-research-plan.md` BEFORE any broad search: one row per subquestion with a confirmation query and a disconfirmation query.
2. Run the two tracks separately. Do not let confirmation results shape disconfirmation queries.
3. Append one JSON object per evidence item to `03-evidence-ledger.jsonl` (schema: `../j-independent-ideation/templates/evidence-ledger.jsonl`). Tier honestly: T1 primary, T2 practitioner/buyer, T3 vendor/marketing, T4 model prior or intuition.
4. Fill `04-contradiction-register.md`. If empty, state why and which disconfirmation queries ran.
5. Falsification pass: spawn `j-evidence-auditor` and `j-cold-eyes-reviewer` agents (fresh context, brief + ledger only) to hunt omissions and counterevidence; add their findings as ledger items.
6. Numeric market/revenue claims: source + formula + assumptions + scenario range, labelled ESTIMATE. Never a single number.
7. Run the validator; fix errors; report warnings (T3/T4-only conclusions, no contradictions in >15 sources).

## Failure behaviour

Tool unavailable → use the next source in order, log the gap, lower confidence. No evidence for a lens → UNKNOWN, never a guess.
