---
name: deliberate
description: "Run a grounded group deliberation that ends in a decision: gather evidence with mechanically independent scouts, build a verified evidence ledger, generate rival concepts, contest them adversarially, vote silently, and synthesize one call with its kill criterion. Use whenever a question needs more than one opinion and the answer must be defensible — choosing between options, 'what should we build/do next', strategy calls, vendor or approach selection, prioritising a backlog of ideas, running a decision workshop or Lightning Decision Jam, or any time someone asks for a panel, a council, multiple perspectives, or 'research this and tell me what to do'. Also use it to audit a decision already made. Domain-agnostic."
---

# Deliberate

A decision harness. It exists because the usual failure is not a lack of ideas — it is **a group that agrees for the wrong reason** and calls that agreement evidence.

Five stages, each ending in an artifact a different agent has checked. Skip a stage and say which; do not skip the verification inside one.

```
FRAME → GATHER → LEDGER → IDEATE → CONTEST → DECIDE
        (diverge) (converge) (diverge) (converge)
         ↑ independent  ↑ 4-eyes   ↑ rival    ↑ debate then
           scouts         verify     mechanisms  SILENT vote
```

## The rule that does the work: independence is mechanical, not rhetorical

Spawning five agents with five different personas does **not** give five perspectives. They share a model, a context, and usually a source set — they are correlated by construction. Worse, a language model will produce a fluent, well-argued objection for *any* position on request, so "it dissented" is not evidence that it thought independently.

**Rank your de-correlation, and require level 2 or better on any decision that matters:**

| Level | Mechanism | Why it works |
|---|---|---|
| **1 — strongest** | **A different model.** Route one seat through `mcp__gemini__ask-gemini` or `brainstorm` | different weights, different training, genuinely different priors |
| **2** | **A different corpus.** Give each scout a disjoint source set — separate NotebookLM notebooks, or internal-docs vs web vs primary-observation | a claim absent from your corpus cannot be produced from it |
| **3** | **A different tool.** One on web search, one on the browser, one on the internal index, one on the codebase | tools have different blind spots |
| **4 — weakest** | **A different lens or persona.** Prompt-level framing | free, and on its own it is theatre |

Most harnesses stop at level 4 and report the resulting agreement as corroboration. **Say in the output which level each seat achieved.** A panel that only differed at level 4 must report itself as one opinion sampled repeatedly.

## The 4-eyes rule

**No stage output is accepted on the word of the agent that produced it, and the checker must have had different inputs.** Same-agent self-review returns "looks good"; same-input review returns the same blind spots. Concretely:

| Produced by | Checked by | The check is |
|---|---|---|
| scout's findings | a verifier that did not gather them | **open the citation and read it** — does the source say what the row claims? |
| the evidence ledger | a second reader on a different corpus | is anything asserted that no row supports? |
| concept cards | the red team | does a substitute already do this? |
| the vote | the tally rule | did voters share a source set? then it is not a vote |
| the decision | the kill criterion | what observation would retire this, and on what date? |

A review that returns "looks good" has failed and is re-run. Default to refuted when uncertain.

## Stage 0 — FRAME

One decision question, narrow enough to be researchable. Reject the vague form out loud rather than proceeding:

- **No:** "find innovative ideas for X"
- **Yes:** "which recurring workflow among [specific actor] is underserved enough to justify testing a paid solution in the next 14 days?"

Write down: the question · who decides · what a good answer must contain · what is explicitly out of scope · the date the decision expires. **If the question cannot fail, it is not a question.**

## Stage 1 — GATHER

Spawn scouts in parallel — three to five, more only if the corpora genuinely differ. **Assign each a disjoint source domain**, and record its independence level.

Set up the evidence spine first, because it is what stops laundering:

1. `mcp__notebooklm-mcp__notebook_create` — one notebook per decision.
2. `mcp__notebooklm-mcp__source_add` — add each source as it is found (url, text, drive, or file).
3. `mcp__notebooklm-mcp__notebook_query` — ask questions **against those sources only**. Answers come back grounded with citations, so a claim that is not in the corpus cannot be produced from it. This is tool-enforced grounding rather than an instruction to be honest.
4. `mcp__notebooklm-mcp__cross_notebook_query` — when scouts hold separate notebooks, this is how you check whether they actually disagree, and about what.
5. `mcp__notebooklm-mcp__research_start` / `research_status` / `research_import` for its own deep-research pass on a hard question.

Other tools by lane, so lanes stay disjoint: `mcp__parallel__web_search` and `web_fetch` (open the page for exact wording) · `mcp__plugin_qmd_qmd__query` for internal/prior work · a browser MCP for what a page actually does — pricing, onboarding, public behaviour · `mcp__plugin_github_github__search_code` for feasibility · `mcp__gemini__ask-gemini` for the different-model seat.

**Every scout returns rows, not prose**, and every row carries what would let someone else refute it:

| Claim | Source (URL/id) | Date | Direct quote or figure | Type | Confidence | What this does NOT prove |
|---|---|---|---|---|---|---|

**Each scout must also return what it looked for and did not find.** An absence is a finding — and it is the only defence against a clean result that means nothing was measured. Say the denominator: *"searched N, found 0"* beats silence.

Run `Research` (multi-agent web research with mandatory URL verification) for the web lane rather than hand-rolling it.

## Stage 2 — LEDGER

One writer merges the rows. A **different** agent verifies by opening citations — not by reading the ledger.

Then label every line, and never let two of these wear the same clothes:

- **Fact** — sourced, dated, someone could go and check it
- **Interpretation** — what we think the fact means
- **Assumption** — believed, unproven, and named as such
- **Question** — what we still do not know
- **Conflict** — two sources disagree; record both, resolve or flag

**Conflicts are the most valuable output of this stage.** Agreement across scouts that shared a corpus is not corroboration; disagreement between disjoint corpora is real information. If nothing conflicts, suspect the lanes were not disjoint and say so.

**Gate: no concept may be proposed before the ledger exists.** Ideas generated before evidence are priors wearing new words.

## Stage 3 — IDEATE

Diverge deliberately. Use `BeCreative` (verbalized sampling — several internally diverse candidates rather than one idea restated) and `Ideate` (multi-cycle generation with fitness testing) rather than asking for a list, which returns variations on the first idea.

Generate rival **mechanisms**, not rival wordings. Lenses that reliably produce genuinely different mechanisms:

- **Inversion** — achieve the outcome without the thing everyone uses
- **Remove / replace / reverse** — cut a required step, change who buys, run the workflow backwards
- **Adjacent transfer** — a mechanism that works in an unrelated field
- **10× constraint** — an order of magnitude less time, cost, expertise or risk
- **Non-consumption** — what would serve people currently doing nothing, or using a spreadsheet
- **Wedge** — solve one high-frequency moment instead of the whole problem

Each concept is a card, and the card is rejected if a field is empty:

```
Concept:
Which evidence row it answers:     ← must cite the ledger
Mechanism (how it actually works):
Why now (what changed):
Existing substitute:
What is genuinely different:
Most dangerous assumption:
Smallest test that could falsify it:
```

**"Different" means a different mechanism, not a different feature list.**

## Stage 4 — CONTEST

Two passes, in this order, and the order matters.

**Debate first.** `Council` runs a real multi-round debate where agents respond to each other's actual points. Friction is the product here. Separately, `RedTeam` runs parallel adversaries against the strongest concept — searching for substitutes, prior failed attempts, adoption friction, and disconfirming evidence. `brutal-honesty-review` when the work needs its weakest part named without cushioning.

**Then vote silently.** Everyone commits their vote without seeing others'. Debate is for information; open voting is for anchoring. Three dots per voter, maximum two on any one item, so a voter must either concentrate or spread.

**A vote is void if the voters shared a source set.** That is not a guideline — a tally over correlated voters is a chorus with a number on it. Where a script enforces this (`bin/verify-sprint-round` in a repo that has it), let the script refuse. Where none exists, state each voter's sources next to the tally so the reader can refuse it themselves.

**Every voter states one thing that would change their vote.** A voter who cannot name it did not deliberate.

## Stage 5 — DECIDE

Score openly, and keep the numbers provisional — their job is comparability and transparency, not precision. Weight what matters for the question; a defensible default:

```
priority = 0.25·pain + 0.20·frequency + 0.15·willingness-to-pay
         + 0.15·differentiation + 0.15·feasibility + 0.10·evidence-quality
         − risk penalty
```

**Evidence quality is a scored term on purpose.** Without it the best-argued concept wins rather than the best-evidenced one.

Then write the record — this is the harness's memory, and it is what stops the next cycle rediscovering a dead end:

```
DECISION: proceed | iterate | pause | kill
Question:
Decided by / date:
Evidence: N rows, M independent sources, K conflicts unresolved
Independence achieved: level per seat
What we now know:
What remains assumed:
The call, and why this one:
Smallest next test · pass threshold · by when:
KILL CRITERION: the observation that retires this, and the date it is checked
What would have changed the decision:
```

**A decision without a kill criterion and a date is an opinion.**

## Choosing the depth

Match the machinery to the cost of being wrong. Over-running this on a small question is its own failure.

| Cost of being wrong | Run |
|---|---|
| Reversible, cheap | FRAME → one scout → decide. Say you skipped the rest |
| Normal | 3 scouts, ledger + verify, concepts, one RedTeam pass, vote |
| Expensive or irreversible | 5 scouts including a different-model seat, cross-notebook conflict check, Council + RedTeam, silent vote, full record |

## What this improves on in Lightning Decision Jam

LDJ is a fast, well-designed human workshop — problems, silent solution writing, dot voting, effort/impact grid, action steps. Its silent-generation and silent-voting mechanics are kept here because they solve real anchoring problems.

What it assumes, and this harness supplies instead:

- **LDJ assumes participants already carry the knowledge.** Stages 1–2 make that an artifact rather than an assumption, and verify it.
- **LDJ assumes participants are independent people.** With agents that is false by default, which is why independence is engineered and its level reported.
- **LDJ ends at "action steps".** This ends at a falsifiable test with a threshold and a kill date.
- **LDJ has no verification.** Here nothing passes a stage on its author's word.

Use LDJ when humans in a room already hold the evidence and need to converge in an hour. Use this when the evidence has to be produced and the conclusion has to survive.

## Failure modes to watch for

| Symptom | What it means | What to do |
|---|---|---|
| Every scout agrees | lanes were not disjoint | check with `cross_notebook_query`; re-run with separate corpora |
| Nothing conflicts in the ledger | the corpus is one echo | add a different-model or different-corpus seat |
| The red team returns "looks good" | failed review | re-run; default to refuted |
| Concepts arrive before evidence | priors wearing new words | discard and gate on the ledger |
| A clean result with no denominator | nothing was measured | report *searched N, found 0* |
| The most articulate concept wins | rhetoric beat evidence | check the evidence-quality term was actually scored |
| No kill criterion | it is an opinion | do not record it as a decision |

Longer reference — worked lane assignments, NotebookLM call sequences, and the full artifact templates: `references/playbook.md`.
