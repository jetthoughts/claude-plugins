# Verification gate (§6) and red-team pass (§7)

These are the two gates that make a matrix a deliverable, not a draft.

## §6 — Verification gate (deep research only)

**This is the 2026 production-grade standard. A matrix without this gate is a draft, not a deliverable.**

### Architecture

Search → Synthesize → **Verify** → Cite
(Source: [Webcite, 2026-02-15](https://webcite.co/blog/deep-research-agents-verification/))

### The compounding-error problem

"A 5% per-step error rate compounds to 63% failure on 100-step tasks."
(Webcite, citing LangChain State of Agent Engineering Survey 2025)

The verification gate exists to break this compounding. Each claim that
survives into the deliverable is independently re-checked.

### Per-claim verification steps

1. Re-search the key factual claim using a **different tool** than the
   one that found the original source.
2. Check: does the second source confirm, contradict, or qualify the
   claim?
3. For any claim driving a decision: additionally check citation
   fidelity (is the source actually saying what the claim says it
   says?).
4. Flag: confirmed / contradicted / qualified / unverified.

### If verification contradicts the synthesis

- Do NOT silently correct.
- Record the contradiction in the contradiction table.
- Lower confidence to `low`.
- Do NOT remove the claim — mark it `unsupported` with both sources
  named.

### Verification tool rotation

| If gathered via | Verify with |
|---|---|
| `searxng` | `tavily` or `exa` |
| `tavily` | `searxng` or `brave-search` |
| academic engine | different academic engine |
| `openviking` / `qmd` | re-read the source URI directly |

**Never verify with the same tool that produced the original result.**

## §7 — Red-team pass (deep research only)

Before finalizing, run an adversarial pass on your own findings.

### Red-team checklist (apply to each claim)

1. **Inversion test** — is the opposite claim equally well-supported? If
   yes, the evidence is thin.
2. **Cherry-pick test** — are you citing only sources that support the
   claim? Did you suppress a source that qualified it?
3. **Authority test** — is the source an interested party? (Vendor
   benchmarks, self-reported data, paid reports = lower confidence.)
4. **Recency test** — is the source current enough for the claim? A
   2019 source may not reflect a 2026 landscape.
5. **Generalization test** — does a case study generalize to the
   question's scope, or are you extrapolating?

For each claim that fails a red-team test, add a note in the confidence
column and lower confidence appropriately.

### Source

Cognition, "Multi-Agents: What's Actually Working," April 2026.
Cognition recommends red-teaming own findings before delivery.

## Why both gates

- **Verification gate** catches fabrication (cited claim not actually
  in the source) and contradiction (second source disagrees).
- **Red-team pass** catches overconfidence (one-sided evidence,
  over-generalization, vendor-bias inflation).

A claim that passes both is durable. A claim that fails either is
flagged, not removed — the deliverable's value is the audit trail, not
the conclusion.
