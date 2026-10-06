# Field research — the production-grade standard sources

When a claim cites "the field's 2026 standard," this is the underlying
evidence. Always cite the original source, not a paraphrase.

## Anthropic — multi-agent research system (2025-06-13)

https://www.anthropic.com/engineering/multi-agent-research-system

**What it proves:** the orchestrator-worker architecture with isolated
context windows per subagent.

- 90.2% breadth improvement over single-agent baseline
- Subagents in separate context windows, compress to 1,000–2,000 tokens
- Prompt isolation rules prevent cross-contamination
- Citation at prompt level (sources cited where claims are made)
- Single-threaded writes to the final deliverable
- T1 rule (≥2 independent sources per claim) is enforced structurally
  by the isolation rule

**Use this in bos-research for:** the T1 triangulation rule, the
"isolation" framing, and the citation-at-prompt-level pattern.

## OpenAI — deep research workflow (2026-04-08)

https://agentmarketcap.ai/blog/2026/04/08/openai-deep-research-enterprise-autonomous-research-agent

**What it proves:** the three-phase loop (clarification → iterative
gathering → synthesis).

- Phase 1: intent clarification (asks follow-up questions)
- Phase 2: iterative source gathering, 5–30 Bing-grounded searches, 5–30 min
- Phase 3: synthesis with inline citations

**Use this in bos-research for:** the §3 clarification phase, the §4
iterative gathering pattern.

## Perplexity — deep research (2025-02)

https://www.analyticsvidhya.com/blog/2025/02/perplexity-deep-research/

**What it proves:** generating a research plan before execution.

- Perplexity produces a detailed research plan first
- Then executes multi-step retrieval + synthesis
- Plan visible to user; can be redirected

**Use this in bos-research for:** the §3 clarification phase + the
"research plan first" pattern.

## Webcite — verification architecture (2026-02-15)

https://webcite.co/blog/deep-research-agents-verification/

**What it proves:** Search → Synthesize → **Verify** → Cite is the
production architecture.

- 57% of orgs report quality as the top concern for AI agents
- 5% per-step error compounds to 63% failure on 100-step tasks
- Verification must use a different tool than gathering

**Use this in bos-research for:** the §6 verification gate, the
compounding-error problem, the tool-rotation rule.

## Cognition — red-teaming own findings (2026-04)

Cognition, "Multi-Agents: What's Actually Working," April 2026.

**What it proves:** red-team your own findings before delivery.

- Apply adversarial tests (inversion, cherry-pick, authority,
  recency, generalization) to every claim
- Lower confidence when tests fail; do not remove the claim

**Use this in bos-research for:** the §7 red-team pass.

## Ptah + CiteGuard-RAG (arXiv, 2025-12)

Verifier-agent acceptance function:
- Empirical grounding
- Citation fidelity
- Cross-modal consistency

**Use this in bos-research for:** the citation-fidelity check in §6
verification (step 3).

## PKM / vault methodology

- `1._Research_proce_2more_6e5825d1.md` — D1–D5 decomposition
- `1.2_Multi-source_triangulation_T1T4.md` — T1–T4 triangulation rules
- `2026_agentic_rese_2more_8e1d4c8e.md` — 2026 field findings
- `Hermes_Desktop_research_methodology_memo.md` — methodology memo

The T1–T4 rules in `bos-research` §4 are an exact port of the PKM
T1–T4 rules. The D1–D5 decomposition in §1 mirrors the PKM D1–D5
shape. When in doubt, the PKM files are the original; the skill is a
re-statement.

## How to cite these in the matrix

In the source column: `<URL> (date) — short evidence note`

Example: `https://www.anthropic.com/engineering/multi-agent-research-system (2025-06-13) — 90.2% breadth improvement, T1 rule via isolation`

Don't paraphrase these in the claim column. The whole point of citing
is the link. If a paraphrase is in the claim, the verification gate
re-reads the source.
