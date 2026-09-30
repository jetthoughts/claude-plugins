---
name: product-discovery
description: Run a product discovery pipeline — research the landscape, critique candidates, validate claims, decide buy/build, and produce a PRD. Use when a project idea needs a validated PRD before implementation.
version: 0.1.0
author: kanban-orchestrator
tags: [research, prd, product-discovery, buy-build]
---

# Product Discovery Pipeline

**Input:** a project brief — 1–3 sentences describing the problem, the desired outcome,
and any constraints (platform, budget, timeline, must-use/must-not-use).

**Output:** a PRD markdown file (template below) + a buy/build decision section, stored in
the project's `docs/` or `business-os/functions/<name>/prd/`.

**Pipeline (7 steps):**

```
frame → landscape → critique → validate → decide → prd → gate
```

**Stop conditions:**
- PRD produced and gate passed → done.
- Any step returns "insufficient information to proceed" → stop and flag the gap; do not
  invent facts.
- Owner says stop at any point → stop.

---

## Step 1 — Frame

Restate the brief in the contract shape (`j-delivery/contract`):

- **Problem:** what is broken/missing today.
- **Outcome:** what must be true when this is done (measurable where possible).
- **Constraints:** platform, budget, timeline, must-use, must-not-use, buy-or-build openness.
- **Surfaces:** where it must run (local, cloud, mobile, browser, API).
- **Hard stops:** anything that must not happen (send, publish, spend, consent, credentials).

If the brief is ambiguous, ask at most 3 clarifying questions; if still ambiguous, proceed
with stated assumptions labeled in the PRD.

**Output of this step:** a 5–8 line `01-frame.md` captured in the work product.

---

## Step 2 — Landscape

Research what exists today. Run in parallel where possible.

### 2.1 What to find

- **Direct competitors / alternatives** — tools or services solving the same problem.
- **Adjacent tools** — that solve part of the problem or a nearby problem.
- **User feedback** — reviews, forum threads, complaint patterns, feature requests.
- **Platform / API facts** — any service the solution would depend on.

### 2.2 Sources (in order)

1. **Local first:** `qmd` over `plugin-skills` / `skills` / `skills-share`; OpenViking
   `search` through indexed skills and knowledge. Check the latest capability catalog.
2. **Web research:** use the research ladder owned by the `j-research` skill — `searxng`
   first, then `tavily` as the announced metered fallback, built-in `web_search`/`web_extract`
   only if both fail (name the rung that answered; a metered rung is never silent).
   For each candidate tool: name, what it does, pricing model (if public), last update
   signal, reputation signal.
3. **Official docs** for any specific tool named: fetch the relevant doc page as markdown.
4. **One synthesis pass:** consolidate findings into a landscape table.

### 2.3 Landscape table shape

| Candidate | What it solves | How it works (1 line) | Pricing model | Last update / signal | Fit (strong/partial/none) |
|---|---|---|---|---|---|

**Output of this step:** `02-landscape.md` with the table + 3–5 bullet notes on patterns
observed (e.g. "everyone charges per seat", "no one solves X").

---

## Step 3 — Critique

Take the top 3–5 candidates from the landscape and run each through the **Tool Evaluator
checklist** (`bos-lens-router` § ToolEvaluator):

1. **Functionality** — does it do what we need, fully or partially?
2. **Security** — data handling, access model, any red flags.
3. **Integration** — how hard to connect to/from it.
4. **Performance** — speed, scale, latency claims (and whether sourced).
5. **Cost / TCO** — explicit cost + implied cost (integration, maintenance, lock-in).
6. **Adoption risk** — maturity, community/support signal, vendor stability.
7. **Exit / migration path** — how hard to leave.

**Output of this step:** `03-critique.md` — one short paragraph per candidate, each ending
with a verdict line: `keep / auxiliary / drop`, with the deciding factor named.

---

## Step 4 — Validate

For every factual claim that drives the decision (pricing, capability, user volume, "best
in class", "most popular", release dates):

- **Source it.** Name the URL or doc line. If unsourced, mark `UNVERIFIED`.
- **Confidence band:** apply the deep-research bands —
  - 90–100 verified (primary source, checked)
  - 75–89 likely (secondary source, plausible)
  - 50–74 disputed (conflicting signals)
  - 25–49 weak (single unsourced claim)
  - 0–24 reject
- **Flag contradictions** between sources explicitly.

**Critical claims** (ones that change the buy/build decision) need confidence ≥ 85 AND
at least 2 sources OR one primary source with a verbatim quote.

**Output of this step:** `04-validation.md` — a claim table: claim, source, confidence,
flag. Any claim that fails the critical-claim threshold is named in the PRD's open risks.

---

## Step 5 — Decide

Produce a **buy / build / hybrid** decision with explicit rationale.

### 5.1 Decision rule (default)

- **Buy** if a single candidate (or clean combination) covers the core outcome at acceptable
  TCO and adoption risk, with no fatal gap.
- **Build** if no buy candidate covers the core outcome, or the gap is small enough to build
  around a platform, or buy creates unacceptable lock-in / cost at scale.
- **Hybrid** if a platform/service covers the bulk and a small build addresses the gap.

### 5.2 State explicitly

- What the chosen path covers.
- What it does NOT cover (gap list).
- What the simplest viable MVP version of the chosen path looks like.
- Open risks from the validation step that bear on the decision.

**Output of this step:** `05-decision.md` — the decision, rationale, gap list, simplest MVP
description.

---

## Step 6 — PRD

Write the PRD using the template (`references/prd-template.md`). Fill every section that the
pipeline produced; leave TBD only where the brief did not supply the information and it
cannot be inferred.

**PRD must include:**
- Frontmatter: `id`, `title`, `status`, `date`, `sources`, `confidence_summary`,
  `buy_or_build`, `open_questions`, `next_steps`.
- Problem statement (from frame).
- Users / stakeholders.
- Requirements (functional + non-functional), each sourced or marked assumption.
- Solution outline (from decision).
- Buy/build plan: what is bought vs built, with names.
- MVP scope: the smallest thing that delivers the core outcome.
- Open risks + mitigations.
- Next steps: what needs to happen to move from PRD to execution.

**Output of this step:** the PRD file.

---

## Step 7 — Gate

Before the PRD counts as done, run a self-check against this list:

- [ ] Every factual claim in the PRD is sourced or explicitly marked as an assumption.
- [ ] The buy/build decision has stated rationale (not just a label).
- [ ] The MVP scope is the smallest thing that delivers the core outcome (not a stretched
      version).
- [ ] Open risks are named, not hidden.
- [ ] No claim carries confidence < 50 without an explicit flag in the PRD.
- [ ] The PRD says what happens next, not just what was found.

If any check fails, fix it and re-check. If the gate cannot be passed because information is
genuinely missing, flag the gap in the PRD and stop — do not invent.

**External gate (when applicable):** for a PRD that will drive a build commitment, the
quality-guardian seat reviews the PRD. The PRD is not "approved" until that review passes.

---

## Reuse & delegation

- **Research (Steps 2–4):** may be delegated to the `researcher` profile via kanban if the
  brief is large enough to warrant a separate research card. When delegated, the researcher
  returns `02-landscape.md`, `03-critique.md`, `04-validation.md` as artifacts; this skill
  then runs Steps 5–7.
- **Ideation framing (Step 1):** may use `j-ideation` skills (`j-designing-experiments`,
  `five-whys`) when the problem is fuzzy.
- **Existing skills re-used inline:** `bos-lens-router` (Tool Evaluator checklist),
  `j-delivery/contract` (frame shape), `bos-incident-response` (when a step fails).

---

## What this skill does NOT do

- It does not send, publish, register, spend, or contact anyone (those are EXTERNAL/IRREVERSIBLE
  and need owner approval per the authority matrix).
- It does not commit or push to Git — the owner reviews and commits.
- It does not make the buy/build decision for you — it structures the decision and states the
  rationale; the owner approves the call.
- It does not run implementation — the PRD is the output, not the build.

---

## References

- PRD template: `references/prd-template.md`
- Tool Evaluator checklist: `bos-lens-router` SKILL.md § ToolEvaluator
- Contract/frame shape: `j-delivery/contract` SKILL.md
- Research ladder: `j-research` skill (owns the ladder: searxng → tavily announced → built-in).
  The consumer browser-session manual that used to live in the retired `web-research-lanes` skill is
  now `references/consumer-lanes.md` inside `j-research`, and is not part of the ladder.
