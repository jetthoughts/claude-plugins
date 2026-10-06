---
name: bos-research
description: Produce a sourced claim-evidence matrix. Use for any research, lookup, or question that needs verified facts — this skill owns the protocol and must be invoked before any search tool is called directly.
version: 1.0.0
author: pftg
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, research, evidence, claims, protocol]
    related_skills: [bos-research-incident, bos-research-index, j-research]
---

# bos-research Skill v1.0

Produce a sourced claim-evidence matrix for a bounded research question: every
material claim paired with its sources, a source quality tier, a confidence level,
and contradictions recorded side by side. Web facts are gathered on the
source-type routing ladder; the matrix is an internal draft artifact.

**This skill must be invoked before any search tool is called directly.**
Calling searxng, tavily, perplexica, or any other research tool without going
through this protocol is a protocol violation — the skill enforces decomposition,
channel routing, verification, and the three-contract deliverable that a raw
search does not.

## Key concepts

- **Research question** — a bounded, falsifiable question. Not a topic.
- **Claim** — one atomic, falsifiable statement. One row in the matrix.
- **Source tier** — primary > secondary > tertiary > unverified (see §8).
- **Channel** — the category of source being sought (web, academic, social, etc.).
  Different channels use different tools.
- **Phase** — Clarification → Gathering → Synthesis → Verification → Red-team.
  Deep research runs all five. Quick lookup (§10) runs only Gathering + Synthesis.
- **Deliverable** — the three-contract output (§8): evidence pack, source ledger,
  contradiction/confidence table.

## Research directory

- Business OS root: `~/dev/pkm/business-os`
- Default: `~/dev/pkm/business-os/knowledge/research/`
  (sources → `knowledge/sources/`, claims → `knowledge/claims/`)
- Placement table: `~/dev/pkm/Research-Notes/research-output-placement.md`
- Researcher seat scope: `READ`/`DRAFT` in `knowledge/**`; seats above that
  ceiling keep the file internal-only.
- Output filename: `knowledge/research/<YYYY-MM-DD>-<slug>.md`
  (slug from the question, hyphenated, ≤60 chars).

## Inputs

- Research question (bounded and falsifiable)
- Requesting work item or decision ID, if one exists
- Depth hint or deadline, if given (never invent one)
- Whether this is a quick lookup or a deep research pass (§10)

---

## §1 — Decomposition (D1–D5)

Before touching any search tool, decompose the question.

**D1. Rewrite the question into at most 5 atomic claims.** A good atomic claim
is answered by one bounded evidence package. "Research X" is not a question;
"Does X cause Y?" and "What is X's market size?" are.

**D2. Name the evidence surface up front.** For each claim, list:
- Candidate sources/channels to evaluate
- Verdict vocabulary you will use (adopt / adapt / skip with reason)
- Acceptance stop condition

This prevents scope creep mid-run.

**D3. Separate "must evaluate" from "nice to check."** Stop when every
must-evaluate claim has a verdict. Add a new claim mid-run only when a
material gap appears — not because a tertiary source turned up something
interesting.

**D4. Assign a source tier expectation per claim before reading.**
Primary (official docs, standards, filings), secondary (reputable press,
analyst), tertiary (blogs, forums, anecdote), unverified (single unattributed).
The tier is a pre-commitment — it prevents laundering a convenient source
as "just my judgment."

**D5. State the research mode.** Deep research (§2–§9) or quick lookup (§10)?
The mode determines which phases run.

---

## §2 — Channel routing (always, before ladder)

Match the channel to the right tool. Run all relevant channels for each claim.
Do not default to "web search" for every claim — academic, Chinese, social,
and real-time claims need different tools.

### Channel → Tool routing table

| Channel | First tool | Fallback | Cost | Notes |
|---|---|---|---|---|
| General web (general facts, news) | `searxng` | `tavily` (metered, announce) | Free / metered | Rung 1 / rung 2 |
| Academic, biomedical, code errors | `ldr` with `engine: openalex \| pubmed \| stackexchange` | `searxng` | Free | |
| Cited synthesis paragraph | `perplexica` | `tavily` (metered, announce) | Free / metered | Off-ladder role |
| Cached, explainable scoring | `wigolo` | `searxng` | Free | Off-ladder role |
| Semantic / neural recall | `exa` | `searxng` | Metered | Announce |
| Real-time / current events | `you-research` | `searxng` with `time_range` | Metered | Announce |
| Independent index (non-Google/Bing) | `brave-search` | `searxng` | Metered | Announce |
| Reddit, Twitter, YouTube, GitHub, LinkedIn | `tavily` with `include_domains` | `agent-reach` (skill) | Free | Prefer tavily for cost/speed |
| Chinese-language sources | Kimi via `ego-browser` (logged-in session) | `searxng` | Free | Consumer lane |
| Primary documentation, libraries | `context7` or `deepwiki` | `searxng` | Free | |
| Our own corpus (notes, prior research) | `openviking` search, `qmd` query | — | Free | |
| Repo code and structure | `semble` | `openviking` | Free | |
| Deep multi-source synthesis | `ldr quick_research` | `perplexica` | Free | Off-ladder synthesis role |

**The research ladder (rung order for general web):**

1. `mcp__searxng__searxng_web_search` — free, ~0.8s, raw ranked URLs
2. `mcp__tavily__tavily_search` — **metered fallback, announce it in the answer**
3. Built-in `web_search` / `web_extract` — only when both above fail; name the
   failed rung

A metered tool is never used silently. If tavily was used, say so in the
matrix header (`ladder_used: searxng+tavily`).

---

## §3 — Phase 1: Clarification (deep research only)

Run this phase when the question is ambiguous, has multiple interpretations, or
would benefit from a structured research plan.

1. Ask up to 5 targeted follow-up questions to narrow scope.
2. For each clarification, state the expected evidence surface and source tier.
3. If the question is already specific and falsifiable, state "No clarification
   needed" and skip to §4.

**Source:** Perplexity Deep Research generates a detailed research plan before
delivering results. OpenAI Deep Research runs intent clarification as its first
phase. ([Analytics Vidhya, 2025-02](https://www.analyticsvidhya.com/blog/2025/02/perplexity-deep-research/);
[AgentMarketCap, 2026-04](https://agentmarketcap.ai/blog/2026/04/08/openai-deep-research-enterprise-autonomous-research-agent))

---

## §4 — Phase 2: Iterative Gathering (not one-shot)

For each claim, gather sources iteratively — not a single search then synthesis.

**Multi-source triangulation rule (T1–T4):**
- **T1.** Retrieve at least two independent sources for any claim that survives
  into the deliverable. "Independent" means not cross-citations of the same
  origin. (Source: Anthropic multi-agent research system, 2025-06-13)
- **T2.** Prefer primary for any claim that drives a decision. (Source: bos-research
  evaluation, LDJ eval)
- **T3.** Read the source, not only the search snippet. If you cite a URL, you
  must have retrieved it this run. A phrase in 7 blogs from the same origin
  is one source, not seven.
- **T4.** When sources disagree on a number or a step, record the conflict
  before resolving it. Use the contradiction table. Lower confidence to `low`
  while a material contradiction stands; never resolve by choosing the more
  convenient source.

**Anthropic's isolation rule:** Each subagent reads its assigned slice in its
own context window, compresses to 1,000–2,000 tokens, and returns only the
summary — not the raw evidence — to the lead researcher. This prevents
cross-contamination and enforces the T1 rule structurally.
(Source: [Anthropic, 2025-06-13](https://www.anthropic.com/engineering/multi-agent-research-system))

**Iterative loop:** For each claim:
1. Search channel 1 → read top sources
2. If <2 independent sources found → search channel 2
3. If still insufficient → escalate to deep synthesis tool
4. Stop when ≥2 independent primary sources OR when all relevant channels exhausted

---

## §5 — Phase 3: Synthesis

Produce the claim-evidence matrix. One row per atomic claim.

**Claim structure:**
- Atomic and falsifiable (not "X is important")
- Answerable by the evidence gathered
- Each paired with its sources, tier, and confidence

**Source tiers:**
| Tier | Definition | Examples |
|---|---|---|
| `primary` | Official docs, standards, filings, primary research | API docs, SEC filings, W3C specs, IEEE standards |
| `secondary` | Reputable press, analyst reports | Reuters, Gartner, McKinsey, Nature peer review |
| `tertiary` | Blogs, forums, anecdote | Twitter/X, Reddit, Hacker News, personal blogs |
| `unverified` | Single unattributed claim | "A source said...", anonymous, no citation |

**Confidence levels:**
| Level | Definition |
|---|---|
| `high` | 2+ independent primary sources, no active contradiction |
| `medium` | 1 primary or several secondary, minor disagreement across sources |
| `low` | Tertiary or unverified only, or active material contradiction |
| `unsupported` | No source found at any tier; never dropped, never guessed |

---

## §6 — Verification Gate (deep research only)

**This is the 2026 production-grade standard. A matrix without this gate is
a draft, not a deliverable.**

Verification independently checks each synthesized claim before it reaches
the user.

**Architecture:** Search → Synthesize → **Verify** → Cite
(Source: [Webcite, 2026-02-15](https://webcite.co/blog/deep-research-agents-verification/))

**The compounding error problem:** "A 5% per-step error rate compounds to 63%
failure on 100-step tasks." (Webcite, citing LangChain State of Agent
Engineering Survey 2025)

**Verification steps per claim:**
1. Re-search the key factual claim using a **different tool** than the one
   that found the original source.
2. Check: does the second source confirm, contradict, or qualify the claim?
3. For any claim driving a decision: additionally check citation fidelity
   (is the source actually saying what the claim says it says?).
4. Flag: confirmed / contradicted / qualified / unverified.

**If verification contradicts the synthesis:**
- Do not silently correct. Record the contradiction in the contradiction table.
- Lower confidence to `low`.
- Do not remove the claim — mark it `unsupported` with both sources named.

**Verification tools (different from gathering tools):**
- If gathered via `searxng` → verify with `tavily` or `exa`
- If gathered via `tavily` → verify with `searxng` or `brave-search`
- If gathered via academic engine → verify with a different academic engine
- Never verify with the same tool that produced the original result

---

## §7 — Red-Team Pass (deep research only)

Before finalizing, run an adversarial pass on your own findings.

**Red-team checklist (apply to each claim):**
1. **Inversion test:** Is the opposite claim equally well-supported? If yes,
   the evidence is thin.
2. **Cherry-pick test:** Are you citing only sources that support the claim?
   Did you suppress a source that qualified it?
3. **Authority test:** Is the source an interested party? (Vendor benchmarks,
   self-reported data, paid reports = lower confidence.)
4. **Recency test:** Is the source current enough for the claim? A 2019
   source may not reflect a 2026 landscape.
5. **Generalization test:** Does a case study generalize to the question's
   scope, or are you extrapolating?

For each claim that fails a red-team test, add a note in the confidence
column and lower confidence appropriately.

**Source:** Cognition, "Multi-Agents: What's Actually Working," April 2026.
Cognition recommends red-teaming own findings before delivery.

---

## §8 — Three-Contract Deliverable

Every research output carries all three contracts. Missing any one = draft only.

### Contract 1: Evidence pack
- Claims are numbered, each paired with retrieved source(s) (URL, retrieval date,
  verbatim snippet) or marked `unsupported`.
- Confidence stated per claim with reason, not hedged.
- Contradictions surfaced before the conclusion, never buried.

### Contract 2: Source ledger
- Every source used: title, publisher/author, URL, retrieval date,
  one-line relevance note.
- Sources checked and rejected: listed as "checked, not used" with reason.
- No plausible-but-unretrieved URL appears as a citation.

### Contract 3: Contradiction / confidence table
- Short table: claim, source(s), confidence, conflicting source with weight.
- Where sources conflict, state which was preferred and why.
- If no conflict: state so explicitly.

---

## §9 — Matrix Format

```markdown
---
title: <research question>
type: claim-evidence-matrix
date: <YYYY-MM-DD>
author: researcher
status: draft
mode: <deep-research | quick-lookup>
requesting: <WI-/DEC- id or "owner-direct">
channels_used: <list of channels invoked>
ladder_used: <searxng | searxng+tavily | searxng+tavily+builtin — with reason>
---

# <title>

## Research question
<original question>

## Decomposition
- Claim 1: <atomic claim>
- Claim 2: ...

## Clarification (deep research)
<questions asked / "No clarification needed">

## Channel routing log
| Claim | Channel | Tool used | Result |
|---|---|---|---|
| ... | ... | ... | ... |

## Claims

| # | claim | sources | tier | confidence | verification | contradictions |
|---|---|---|---|---|---|---|
| 1 | <atomic, falsifiable> | <URLs, dates> | primary/secondary/tertiary/unverified | high/medium/low/unsupported | confirmed/contradicted/qualified/unverified | C<NN> or none |

## Contradictions
- C<NN>: <position A (source, tier)> vs <position B (source, tier)>;
  resolution evidence: <what would settle it>

## Gaps
<facts that could not be sourced at any tier — stops here, not guessed>

## Red-team notes
<results of §7 adversarial pass>

## Bottom line
<3–5 sentences: what the evidence supports, at what confidence, what remains open>

## New findings
- NEW: <finding absent from brief and prior research> — source: <URL>
- NEW: ...
- NEW: ...

*<3 required or result is FAIL (novelty gate)*

## Source ledger
| source | title | publisher | URL | retrieved | relevance |
|---|---|---|---|---|---|
| S1 | ... | ... | ... | YYYY-MM-DD | ... |
| ... | ... | ... | ... | ... | ... |

## Checked, not used
- <source> — reason: <why rejected>

## Verification log
| claim | gathering_tool | verification_tool | result |
|---|---|---|---|
| ... | ... | ... | confirmed/contradicted/qualified |
```

---

## §10 — Quick lookup mode (shallow research)

For single-fact questions or questions with a narrow, well-defined scope.

**Phases that run:** Gathering (§4) → Synthesis (§5) — no clarification,
no verification gate, no red-team pass.

**Criteria to decide between deep research and quick lookup:**
| Signal | Likely mode |
|---|---|
| 10+ tabs would be needed to answer manually | Deep research |
| Ambiguous or multi-interpretation question | Deep research |
| Claims will drive a decision | Deep research |
| High compounding-error risk (multi-step claim chain) | Deep research |
| Single fact, one URL answers it | Quick lookup |
| Well-defined, narrow question | Quick lookup |
| Low stakes, exploratory | Quick lookup |

---

## §11 — Novelty gate

**Paul (2026-09-24):** The `## New findings` section must list at least 3
findings absent from both the brief and the prior research it cites, each
marked `NEW` with its source.

- Fewer than 3 new findings = **FAIL** ("a check, not research")
- Re-run with a sharper question.
- Restating the brief's candidates or options does not count as new.

---

## Failure modes

- **Protocol violation:** Calling any search tool before invoking this skill.
- **Metered tool silently:** Using tavily, exa, brave-search, or you-research
  without announcing it in the matrix header.
- **Single-source claim at high confidence:** T1 requires ≥2 independent
  sources for deliverable claims.
- **Contradiction resolved by convenience:** Lowering confidence while a
  material contradiction stands — not burying it.
- **Guess instead of unsupported:** Recording a claim as fact when no source
  was found.
- **Matrix as decision:** The matrix informs; it does not decide.
- **Secrets in output:** No key material, credentials, or PII in the matrix.

---

## Verification checklist

Before returning the result:

- [ ] Every claim row has a source column entry or `unsupported`
- [ ] Source tiers use only the vocabulary: primary / secondary / tertiary / unverified
- [ ] Confidence levels use only: high / medium / low / unsupported
- [ ] Ladder rungs actually invoked match `ladder_used` in the header
- [ ] All metered tool use announced in `ladder_used` and in the answer
- [ ] Contradiction table has both positions with sources for every conflict
- [ ] New findings ≥ 3 (deep research mode) or marked as quick lookup
- [ ] Verification log completed for deep research mode
- [ ] Red-team notes completed for deep research mode
- [ ] File written to `knowledge/research/<YYYY-MM-DD>-<slug>.md`
- [ ] File path returned with claim count, contradiction list, gaps, bottom line
