---
name: bos-research
description: 'Produce a sourced claim-evidence matrix. Use for any research, lookup, or question that needs verified facts — this skill owns the protocol and must be invoked before any search tool is called directly.'
version: 1.4.0
author: pftg
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, research, evidence, claims, protocol]
    related_skills: [bos-research-incident, bos-research-index, j-research]
---

# bos-research Skill v1.1

Produce a sourced claim-evidence matrix for a bounded research question: every
material claim paired with its sources, a source quality tier, a confidence level,
and contradictions recorded side by side. Web facts are gathered on the
source-type routing ladder; the matrix is an internal draft artifact.

**This skill must be invoked before any search tool is called directly.**
Calling searxng, tavily, perplexica, or any other research tool without
going through this protocol is a protocol violation — the skill enforces decomposition,
channel routing, verification, and the three-contract deliverable that a raw
search does not.

## Key concepts

- **Research question** — a bounded, falsifiable question. Not a topic.
- **Claim** — one atomic, falsifiable statement. One row in the matrix.
- **Source tier** — primary > secondary > tertiary > unverified (see `references/matrix-format.md`).
- **Channel** — the category of source being sought (web, academic, social, etc.). Different channels use different tools.
- **Phase** — Clarification → Gathering → Synthesis → Verification → Red-team. Deep research runs all five. Quick lookup runs only Gathering + Synthesis.
- **Deliverable** — the three-contract output: evidence pack, source ledger, contradiction/confidence table.

## Research directory

- Business OS root: `~/dev/pkm/business-os`
- Default: `~/dev/pkm/business-os/knowledge/research/`
  (sources → `knowledge/sources/`, claims → `knowledge/claims/`)
- Placement table: `~/dev/pkm/Research-Notes/research-output-placement.md`
- Researcher seat scope: `READ`/`DRAFT` in `knowledge/**`; seats above that ceiling keep the file internal-only.
- Output filename: `knowledge/research/<YYYY-MM-DD>-<slug>.md`
  (slug from the question, hyphenated, ≤60 chars).

## Inputs

- Research question (bounded and falsifiable)
- Requesting work item or decision ID, if one exists
- Depth hint or deadline, if given (never invent one)
- Whether this is a quick lookup or a deep research pass
- **Research mode declaration** (required): `full` (web + corpus) or `corpus-only` (PKM only) or `web-only` (skip corpus)

## Research mode (the user picks, not the skill defaults)

The skill supports three modes. **The user/owner must declare the mode in the run input or the request itself.** The skill does not default to any one mode.

| Mode | When | What runs |
|---|---|---|
| `full` (default if the user does not say otherwise) | New question, or fresh web evidence is needed | corpus (openviking) first, then general-web ladder (searxng → tavily → web_search), then synthesis, then verification, then three-contract deliverable |
| `corpus-only` | User explicitly says "quote from the corpus" or "no new research" or "PKM only." Quote-synthesis, NOT research | openviking only; quote the corpus verbatim; cite source per quote; do not invoke general-web ladder; do not produce NEW findings; output is a quote-synthesis, not a claim-evidence matrix |
| `web-only` | User explicitly says "skip the corpus" or "fresh web only" | general-web ladder only; corpus is not invoked; for "I already know my corpus; find what's new" |

**Anti-patterns the skill guards against:**
- Treating "the user said no more research" as a skill-level rule. It is a per-run decision, not a skill default.
- Defaulting to corpus-only because the user said "use the PKM" once. The skill must invoke web research unless the user explicitly says `corpus-only`.
- Defaulting to web-only because the agent is in a benchmark/eval mode. The skill must invoke corpus unless the user explicitly says `web-only`.

## The 5 phases

### Phase 1: Decomposition (D1–D5)

Before touching any search tool, decompose the question. See
`references/decomposition.md` for the full D1–D5 protocol.

- **D1** — rewrite the question into ≤5 atomic claims
- **D2** — name the evidence surface, verdict vocabulary, stop condition per claim
- **D3** — separate must-evaluate from nice-to-check
- **D4** — pre-commit a source tier expectation per claim
- **D5** — state the research mode (deep vs quick lookup)

### Phase 2: Channel routing (always, before ladder)

Match the channel to the right tool. Run all relevant channels for each claim.
See `references/channel-routing.md` for the full 12-channel routing table.

**The research ladder (rung order for general web):**

1. `mcp__searxng__searxng_web_search` — free, ~0.8s, raw ranked URLs
2. `mcp__tavily__tavily_search` — **metered fallback, announce it in the answer**
3. Built-in `web_search` / `web_extract` — only when both above fail; name the failed rung

A metered tool is never used silently. If tavily was used, say so in the matrix header (`ladder_used: searxng+tavily`).

**Off-ladder roles:** `perplexica` (cited synthesis), `wigolo` (cached scoring),
`ldr quick_research` (deep multi-source synthesis). These supplement the ladder, they don't replace it.

### Phase 3: Iterative Gathering (T1–T4)

For each claim, gather sources iteratively — not a single search then synthesis.

**Multi-source triangulation rule (T1–T4):**
- **T1.** Retrieve at least two independent sources for any claim that survives into the deliverable. "Independent" means not cross-citations of the same origin.
- **T2.** Prefer primary for any claim that drives a decision.
- **T3.** Read the source, not only the search snippet. A phrase in 7 blogs from the same origin is one source, not seven.
- **T4.** When sources disagree on a number or a step, record the conflict before resolving it. Lower confidence to `low` while a material contradiction stands.

**Iterative loop** for each claim:
1. Search channel 1 → read top sources
2. If <2 independent sources found → search channel 2
3. If still insufficient → escalate to deep synthesis tool
4. Stop when ≥2 independent primary sources OR when all relevant channels exhausted

### Phase 4: Synthesis

Produce the claim-evidence matrix. One row per atomic claim.

**Source tiers:** primary / secondary / tertiary / unverified
**Confidence levels:** high / medium / low / unsupported

See `references/matrix-format.md` for the full schema, vocabulary, and verification checklist.

### Phase 5: Verification gate + Red-team pass (deep research only)

**A matrix without these two gates is a draft, not a deliverable.**

See `references/verification-redteam.md` for the full protocol:

- **§6 Verification gate** — re-search every deliverable claim with a different tool. If contradicted, log the contradiction and lower confidence. Do not silently correct.
- **§7 Red-team pass** — apply the 5-test checklist (inversion, cherry-pick, authority, recency, generalization) to every claim. Lower confidence when tests fail.

The compounding-error problem: a 5% per-step error rate compounds to 63% failure on 100-step tasks. These gates break the compounding.

## Three-contract deliverable

Every research output carries all three contracts. Missing any one = draft only.

1. **Evidence pack** — claims numbered, each paired with retrieved source(s) (URL, retrieval date, verbatim snippet) or marked `unsupported`. Confidence stated per claim. Contradictions surfaced before the conclusion.
2. **Source ledger** — every source used: title, publisher/author, URL, retrieval date, one-line relevance note. Sources checked and rejected: "checked, not used" with reason.
3. **Contradiction / confidence table** — claim, source(s), confidence, conflicting source with weight. Where sources conflict, state which was preferred and why.

## Mode decision

See `references/quick-vs-deep.md` for the full decision tree.

- **Deep research** — 10+ tabs needed, ambiguous, decision-driving, multi-step chain → runs all 5 phases
- **Quick lookup** — single fact, one URL, narrow, low stakes → runs only gathering + synthesis

**Default to deep.** The cost of skipping verification for a "small question" exceeds the cost of running the full protocol. The mode can change mid-run; mark the transition in the matrix header.

## §11 — Novelty gate

**The `## New findings` section must list ≥3 findings absent from both the brief and the prior research it cites, each marked `NEW` with its source.**

- Fewer than 3 new findings = **FAIL** ("a check, not research")
- Re-run with a sharper question
- Restating the brief's candidates or options does not count as new

## §12 — Per-claim check table (cross-check discipline)

**Every research deliverable must include a per-claim check table** that runs the cheapest check which FAILS if the claim is false. The check is run against the **primary artifact**, never against the agent's own summary. This is the cross-check skill (j-delivery) embedded in bos-research.

| Claim type | One-line check |
|---|---|
| "checks pass" / GREEN | Re-run the exact command on the REAL path (absolute, not a scratch copy); compare exit codes |
| A timestamp, or "elapsed N min" | `stat -f %Sm <file>` plus the run's start time. Convert any epoch with `date -r` |
| "N items" / "counts reconcile" | Compute the count yourself from the raw artifact (jq or python) |
| "content captured" | Open 2–3 random source URLs live; the first user message must appear on the page |
| "moved" / "backed up to ~/…" | `find` the real absolute path. A worker's `~` may be a different HOME |
| "recoverable from git" | `git log --all -- <path>`. Zero commits means it is not recoverable |
| "native feature" / a config key | Grep the installed source for the key, or read the table schema |
| "no side effects in the account" | Count the relevant items (chats, comments) live, before and after |
| "goal met" | Compare the done-when with the OWNER's original words, not the card's rewrite |

**Rules:**
- Sample randomly. Cite the check and its output in the verdict.
- A mismatch is FAIL plus an incident note.
- Mark every row not checked as UNVERIFIED.
- Another agent's PASS (or your own) is never proof.
- Do NOT write "✅" or "done" without showing the command that produced the ✅.

## §13 — Aggregate channels log

**Every research deliverable must include an `## Aggregate channels log` section** that records: (a) which channels were requested, (b) the actual response, (c) whether the response was used, and (d) why a non-response was a gap. This is the audit trail for cross-agent trust.

Format per row:

```
| Channel | Requested | Response | Used? | Gap reason |
|---|---|---|---|---|
| openviking viking_search "..." | yes | 12 files | yes | — |
| mcp__tavily__tavily_search | yes | "not a known tool name" | no | tool-name resolution gap (INC-2026100607) |
| mcp__qmd__query "..." | yes | 0 results | no | qmd index empty (INC-2026100604) |
| mcp__perplexica__search | yes | "MCP server unreachable after 3 retries" | no | server down (INC-2026100606) |
| mcp__wigolo__* (cached scoring) | yes | "not a known tool name" | no | tool-name resolution gap (INC-2026100607) |
| mcp__parallel__web_search | yes | 8 results | yes | — |
| mcp__brave_search__brave_web_search | yes | "API 422 SUBSCRIPTION_TOKEN_INVALID" | no | API key issue |
| mcp__exa__web_search_exa | yes | 15 results, 77 KB | yes | — |
| mcp__ldr__quick_research | yes | timeout 300s | no | LM Studio not warm (INC-2026100605) |
```

**Rules:**
- A response is a request's actual output, not a description of what the tool *would* do.
- "Used?" is yes/no; if no, the gap reason must name the incident.
- The log lives in the matrix; the incidents live in `operations/incidents/`. Cross-reference by ID.
- **Tool-name resolution rule (added v1.4, INC-2026100607 lesson):** if a `tool_call` returns "not a known tool name," do NOT file a tool-name-resolution incident immediately. First run `tool_search --queries "<server> <verb> <object>"` and use the returned invokable name. `mcp list` shows server status; `tool_search` shows the actual invokable tool name. They are different primitives. Filing a "name resolution gap" before running tool_search is a wrong-name-guess, not a real gap. The five prior "uninvokable" tools (tavily, agent-reach, you-research, notebooklm, wigolo) were re-tested this way on 2026-10-07: 2 of 5 (tavily via omniroute, notebooklm via tool_search) were actually reachable; 3 of 5 (agent-reach, you-research, wigolo) are genuinely missing and need config additions.

## §14 — Status-report discipline

**Never write "✅", "done", "moved", "verified", or "PASS" without re-reading the artifact in the same turn.** The cheap check is: don't write completion state on a state I haven't just re-fetched.

When a state cannot be re-read (e.g., a Plane item the agent cannot access), don't fake the check. Write the path forward instead: "Awaiting per delivery-manager" or "Approve/Revise/Defer reply path open."

State move ≠ comment. A comment can exist without the state moving. Only the state is the source of truth for workflow position. Cross-check every status report that uses ✅, "done", "moved", or "applied."

## Field research sources

`references/field-research.md` documents the production-grade standard sources
the protocol is built on:

- **Anthropic multi-agent research** (2025-06-13) — T1 rule, isolation
- **OpenAI deep research** (2026-04-08) — three-phase loop, iterative gathering
- **Perplexity deep research** (2025-02) — research plan first
- **Webcite verification architecture** (2026-02-15) — verification gate, compounding error
- **Cognition red-teaming** (2026-04) — red-team pass
- **Ptah + CiteGuard-RAG** (arXiv 2025-12) — citation fidelity

When a claim cites "the field's 2026 standard," this is the underlying evidence.

## Failure modes

- **Protocol violation** — calling any search tool before invoking this skill
- **Metered tool silently** — using tavily, exa, brave-search, or you-research without announcing it in the matrix header
- **Single-source claim at high confidence** — T1 requires ≥2 independent sources
- **Contradiction resolved by convenience** — lowering confidence while a material contradiction stands, not burying it
- **Guess instead of unsupported** — recording a claim as fact when no source was found
- **Matrix as decision** — the matrix informs; it does not decide
- **Secrets in output** — no key material, credentials, or PII in the matrix

## Additional resources

### Reference files

- **`references/decomposition.md`** — D1–D5 protocol in full
- **`references/channel-routing.md`** — 12-channel routing table + ladder + off-ladder roles
- **`references/matrix-format.md`** — full schema, source tier + confidence vocabulary, verification checklist
- **`references/verification-redteam.md`** — §6 + §7 detailed protocol
- **`references/quick-vs-deep.md`** — mode decision tree
- **`references/field-research.md`** — Anthropic, OpenAI, Perplexity, Webcite, Cognition, Ptah citations
- **`references/tool-name-cheatsheet.md`** — invokable `mcp__*` tool names (NOT what `mcp list` shows)
