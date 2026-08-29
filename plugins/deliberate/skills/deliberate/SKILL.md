---
name: deliberate
description: "Run a grounded group deliberation that ends in a decision: gather evidence with mechanically independent scouts, build a verified evidence ledger, generate rival concepts, contest them adversarially, vote silently, and synthesize one call with its kill criterion. Use whenever a question needs more than one opinion and the answer must be defensible — choosing between options, 'what should we build/do next', strategy calls, vendor or approach selection, prioritising a backlog of ideas, running a decision workshop or Lightning Decision Jam, or any time someone asks for a panel, a council, multiple perspectives, or 'research this and tell me what to do'. Also use it to audit a decision already made. Domain-agnostic."
---

# Deliberate

A decision harness. It exists because the usual failure is not a lack of ideas — it is **a group that agrees for the wrong reason** and calls that agreement evidence.

Skip a stage and say which; do not skip the verification inside one.

**Every reply during a run opens with where the run is:** `stage 4 of 8 · CONTEST · 3 stages remain`.
A deliberation that stops at LEDGER has produced *findings*, not a decision — and findings presented
without that label read as a conclusion. **An unfinished run must say it is unfinished**, name the
stage it reached, and name what is still owed. Measured on the first live run: it halted after LEDGER
and reported evidence as though the question had been answered. It had not been.

```
FRAME → GOAL+METRIC → GATHER → LEDGER → IDEATE → CONTEST → DECIDE → ROADMAP
          ▸milestone1  (diverge) (converge)(diverge) (converge)  ▸milestone2
                        ↑           ↑         ↑          ↑
                   independent   4-eyes   lightning   debate,
                     scouts      verify    demos +      then
                                          mechanisms  SILENT vote
```

Lineage: the divergence/convergence spine is the Double Diamond; the silent generation, silent
voting and impact/effort ranking are Lightning Decision Jam; the goal-and-metric opening, Lightning
Demos, milestones and closing roadmap are Strategy Signal (AJ&Smart). What is added is the evidence
layer and the independence engineering — see the comparison at the end.

## The rule that does the work: independence is mechanical, not rhetorical

Spawning five agents with five different personas does **not** give five perspectives. They share a model, a context, and usually a source set — they are correlated by construction. Worse, a language model will produce a fluent, well-argued objection for *any* position on request, so "it dissented" is not evidence that it thought independently.

**Rank your de-correlation, and require level 2 or better on any decision that matters:**

| Level | Mechanism | Why it works |
|---|---|---|
| **1 — strongest** | **A different model or a different system.** `mcp__gemini__ask-gemini`, or Perplexity driven through `claude-in-chrome` | different weights, different retrieval, genuinely different priors |
| **2** | **A different corpus.** Give each scout a disjoint source set — separate NotebookLM notebooks, or internal-docs vs web vs primary-observation | a claim absent from your corpus cannot be produced from it |
| **3** | **A different tool.** One on web search, one on the browser, one on the internal index, one on the codebase | tools have different blind spots |
| **4 — weakest** | **A different lens or persona.** Prompt-level framing | free, and on its own it is theatre |

Most harnesses stop at level 4 and report the resulting agreement as corroboration. **Say in the output which level each seat achieved.** A panel that only differed at level 4 must report itself as one opinion sampled repeatedly.

**Gate: a run may not report an independence level it did not achieve, and may not skip a route because of time.** If the model seat fails, the browser route is attempted *before* the level is written down — a time-box is a reason to run fewer lanes, never a reason to claim a level you skipped the work for. Measured 2026-08-29: a benchmark run read this rule, hit the missing backend, declined the browser fallback citing its time-box, and reported level 3. The rule was present and prose lost to schedule pressure — the same failure it was written to describe.

**Level 1 has more than one route, so exhaust them before dropping.** If the model seat is unavailable, try the other independent system — a browser-driven one — *before* declaring the panel level 2. Measured 2026-08-29: the Gemini backend was missing, the panel silently continued without a level-1 seat, and the browser route that was already documented sat unused until the decider pointed at it. **A fallback you wrote down and did not take is the same as not having one.**

**Exercise the seat with a real question. A ping is not a model call** — `ping` echoed cleanly while `ask-gemini` failed outright on a missing binary.

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

## Roles and guidelines

State both before starting; AJ&Smart's Strategy Signal opens this way because an unstated role is negotiated mid-session, which costs more than saying it.

**Roles:** a **facilitator** who owns the clock and the sequence and never argues the content · a **decider** who breaks ties and owns the outcome (in a one-person business this is the owner, and it is not delegable) · **contributors** who produce · a **scribe** who captures, and whose only job is capture.

**Guidelines:** work silently where the stage says silent · no discussion before the vote · every claim carries its source · disagree with the idea, never the person · the decider decides, the group informs.

**"Together alone"** is the principle underneath all of it: produce in parallel and in silence, then share. It is what makes fan-out worth more than a conversation.

Three facilitation mechanics that carry over from remote workshops, each with its reason:

- **One frame per stage.** A separate surface for each exercise gives a focal point and a sense of progress, and stops a stage's output contaminating the next. **Do not split one stage's output between chat and a file** — every channel switch loses someone.
- **A scribe who only captures.** In a remote room the facilitator sorting notes is *dead air* where nobody is guided. Same here: the agent running the stage should never be the one tidying its output.
- **Timebox, then check once.** Budget each stage, and when it is nearly spent ask whether anyone needs more rather than cutting hard. A silent overrun and a silent truncation look identical in the artifact.

## Stage 0 — FRAME

One decision question, narrow enough to be researchable. Reject the vague form out loud rather than proceeding:

- **No:** "find innovative ideas for X"
- **Yes:** "which recurring workflow among [specific actor] is underserved enough to justify testing a paid solution in the next 14 days?"

Write down: the question · who decides · what a good answer must contain · what is explicitly out of scope · the date the decision expires. **If the question cannot fail, it is not a question.**

### The frame is the decider's, not the facilitator's ▸ confirm before spawning

**Show the reframed question to the decider and wait.** This is the one place in the harness where
taking a defensible default and proceeding is wrong, and the reason is arithmetic: every lane, every
row and every concept inherits the frame, so a wrong default at stage 0 wastes the entire run. Every
later stage can absorb a bad call; this one cannot.

**When the question contains more than one reading, list them and say which you would take** — do not
silently pick. Measured 2026-08-29: *"design an AI business OS for JetThoughts-like companies"* holds
two readings — build it for ourselves, or sell it to companies of that shape. The facilitator picked
the second, spawned three lanes on it, and the decider's actual meaning was the first. Three lanes of
good evidence answered a question nobody asked.

The tell that a question has two readings: **a phrase that only matters under one of them.** "For
companies *like* us" is only load-bearing if you are selling; if you are building for yourself, the
comparison is decoration. When a phrase is doing that much work, stop and ask.

**Confirming costs one message. Not confirming costs the run.**

## Stage 0.5 — GOAL AND METRIC ▸ milestone 1

Strategy Signal spends its first third here, before anyone looks at a solution, and it is right to: **a group that has not agreed what winning looks like will ideate toward different finish lines and call the disagreement creativity.**

Write two things and stop until both are agreed:

- **Long-term goal** — optimistic, specific, and dated. *"In two years, [who] will [outcome] so reliably they stop [current workaround]."*
- **The metric** — the one number that moves if the goal is being reached, plus how it is measured and what it reads today. **If it reads "unknown", that is the first research question**, not a footnote.

**Milestone 1: goal and metric are agreed and written.** Nothing downstream may contradict them, and a concept that does not move the metric is out of scope regardless of how good it is.

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

**Rows that answer a different question get their own section, headed DROPPED.** When the frame moves — a reframe, a correction, a decider's ruling — the evidence gathered under the old frame is still true and still costly to have produced, and the temptation is to carry it forward because it is *there*. Do not. Name it, say which question it answers, keep it as evidence, and exclude it from the design. **Laundering evidence into a conclusion it does not support is the failure this whole harness exists to prevent**, and it is most tempting when the evidence is your own.

**Gate: no concept may be proposed before the ledger exists.** Ideas generated before evidence are priors wearing new words.

## Stage 3 — IDEATE

Diverge deliberately. Use `BeCreative` (verbalized sampling — several internally diverse candidates rather than one idea restated) and `Ideate` (multi-cycle generation with fitness testing) rather than asking for a list, which returns variations on the first idea.

### 3a — Lightning Demos, first

**Do not start by inventing. Go and look at the world first — this stage is an online research pass, not a recall exercise.** It is the single highest-yield ideation step, the one most often skipped, and the one a model will happily fake from memory because it *can* produce plausible examples without searching.

**Gate: at least three examples must carry a URL fetched during this run.** An example you already knew is not a Lightning Demo — it is a prior. If the round produced no new fetches, the round did not happen, and IDEATE must not proceed.

Each contributor researches independently — around 25 minutes, or prepared in advance — and brings **three real examples of someone solving a structurally similar problem well**. Then a three-minute demo each: what it is, and what is good about it.

**The examples must come from outside the domain in question.** That is the whole mechanic. Ideas that spark the best solutions come from similar problems in different environments; three examples from your own industry produce three versions of what you already do.

**A demo is a product tour, not a summary.** In the room, someone screen-shares the actual thing. With agents that means: **find it, open it, look at it.** A description of an interface is not the interface — the transferable component usually lives in what the thing *does*, which text search will not surface.

The chain per example:

1. **Find** — `mcp__parallel__web_search` for candidates; `competitor-intel` when you need verified metrics rather than claims; `Apify` or `just-scrape` for structured extraction at volume.
2. **Open and see it** — a browser (`agent-browser`, `browser-use`, `Interceptor` for real-Chrome, `lightpanda` when speed matters) or `mcp__claude-in-chrome__*` / chrome-devtools `take_screenshot`. **Then actually read the screenshot** — the `Read` tool renders images, so look at it rather than reasoning about the alt text.
3. **Judge what you see** — `web-design-reviewer` for a structured visual read of a page; `screenshot` for capture. What is on screen at the decisive moment is the thing worth stealing.
4. **Hear what users say about it** — reviews and forums. A slick interface with three one-star reviews describing the same failure is a different lesson from a slick interface that works, and only the reviews tell you which.

The scribe captures **one big idea per demo** — a headline, **its source**, a **screenshot or sketch** of the component, and one line on what users say. Not the whole product: the one transferable part. Capture everything; discard nothing at this stage.

```
Big idea:              (headline — what's transferable)
Seen at:               (source, with a link)
From which domain:     (must not be ours)
The component:         (the specific mechanism, not the whole product)
Seen how:              (screenshot path | live tour | reviews only — say which)
What users say:        (one line, with a source)
Why it might transfer:
Why it might not:
```

**Lightning Demos are also a de-correlation mechanism**, which is why they sit here rather than being optional colour. Assign each contributor a **different domain to search** — one in logistics, one in healthcare, one in gaming, one in a regulated industry. That is level 2 on the independence ladder: different corpora produce genuinely different big ideas, where the same brief produces the same three examples. A demo round where everyone brought examples from one industry has not run.

### 3b — Concept creation

**Seed the frame before anyone creates.** AJ&Smart's rule, learned across hundreds of sprints: *"You don't start from a blank canvas."* They pre-fill the board from pre-interviews so the group edits rather than invents — it is faster, less intimidating, and produces better outcomes, because attention goes to the problem instead of to phrasing.

The agent version: **the ideation frame opens already populated** with the evidence rows, the big-idea board, the goal and metric, and any prior concepts that were killed and why. An agent handed an empty prompt fills it from its priors; an agent handed the ledger argues with it.

Now build concepts **from the big-idea board plus the evidence ledger**. Generate rival **mechanisms**, not rival wordings. Lenses that reliably produce genuinely different mechanisms:

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
Which big idea it borrows:         ← from Lightning Demos, with its source
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

**Vote on parts, not only wholes.** AJ&Smart deliberately avoid their whiteboard's built-in voting because it only accepts whole objects — they use dots so a vote can land on *one component inside* a concept, producing a heatmap. Keep that: a concept usually fails or succeeds on one mechanism, and a whole-concept vote loses which one. Record both the concept tally and which components drew the dots.

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

### Flow before detail

Before anything is specified, borrow the sprint's storyboard guard rail: **each contributor writes the winning concept as six steps, start to end** — high level, no detail. The decider picks one flow, mixing steps between versions if useful. That chosen flow is the skeleton everything else hangs on.

The reason is specific and it is the one AJ&Smart give: up to this point every discussion was cut short by process, but detail is where a group goes circular. Six steps agreed in advance are the guard rails that stop it. Then describe each step in shorthand — elements and content, no finished screens — which is Shape Up's **breadboarding**, and it keeps the argument about the mechanism rather than the wording.

### Milestone 2 and the roadmap

**Milestone 2: the chosen concepts are named.** Then sequence them — Strategy Signal ends on a roadmap rather than a decision, because a decision with no order of operations is re-litigated the following week.

| When | What | Who | The metric it moves | Kill date |
|---|---|---|---|---|

Sequence by **what unblocks the most**, not by what is most exciting. Anything not on the roadmap goes to a named backlog rather than staying ambiguously alive.

## Choosing the depth

Match the machinery to the cost of being wrong. Over-running this on a small question is its own failure.

| Cost of being wrong | Run |
|---|---|
| Reversible, cheap | FRAME → one scout → decide. Say you skipped the rest |
| Normal | 3 scouts, ledger + verify, one Lightning Demo round, concepts, one RedTeam pass, vote |
| Expensive or irreversible | 5 scouts including a different-model seat, cross-notebook conflict check, Lightning Demos with a domain assigned per contributor, Council + RedTeam, silent vote, full record and roadmap |

## What is borrowed, and what is added

Both AJ&Smart formats are well designed for their job. Nothing here replaces them; the additions exist because the participants are agents rather than people.

| Taken from | What | Why it is kept |
|---|---|---|
| **Lightning Decision Jam** | silent solution writing · dot voting before discussion · impact/effort ranking | they solve anchoring, and anchoring is worse among agents, since later speakers read earlier output |
| **Strategy Signal** | roles and guidelines stated up front · long-term goal and metric *before* solutions · Lightning Demos · explicit milestones · closing roadmap | a group that has not agreed the finish line ideates toward different ones; a decision with no sequence gets re-litigated next week |
| **Double Diamond** | the diverge/converge spine, problem diamond before solution diamond | it is the same line the multi-agent evidence draws — fan out on divergence, single-thread on convergence |

**What both formats assume, which is false with agents:**

- **That participants already carry the knowledge.** In a room of experienced humans this is roughly true. Stages 1–2 make it an artifact instead, and verify every citation.
- **That participants are independent minds.** This is the load-bearing one. Same model, same context, same sources means correlated by construction, so independence is engineered and its level is reported rather than assumed.
- **That the output is action steps.** This ends at a falsifiable test with a threshold and a kill date, because an action step nobody can fail is not a decision.
- **That someone verifies.** Neither format has a verification stage. Here nothing passes on its author's word.

Use LDJ when humans in a room already hold the evidence and need to converge in an hour. Use Strategy Signal when a human team needs a strategy day. Use this when the evidence has to be produced first and the conclusion has to survive being attacked.

## Failure modes to watch for

| Symptom | What it means | What to do |
|---|---|---|
| Every scout agrees | lanes were not disjoint | check with `cross_notebook_query`; re-run with separate corpora |
| Nothing conflicts in the ledger | the corpus is one echo | add a different-model or different-corpus seat |
| The red team returns "looks good" | failed review | re-run; default to refuted |
| Concepts arrive before evidence | priors wearing new words | discard and gate on the ledger |
| A clean result with no denominator | nothing was measured | report *searched N, found 0* |
| The most articulate concept wins | rhetoric beat evidence | check the evidence-quality term was actually scored |
| Lightning Demo examples all from one industry | the demo round did not run | re-run with a different domain assigned per contributor |
| Big ideas describe features, not mechanisms | nobody opened the product | require a screenshot or a live tour per card |
| Concepts do not move the agreed metric | milestone 1 was skipped or ignored | out of scope, however good |
| No kill criterion | it is an opinion | do not record it as a decision |
| The decider corrects the frame after lanes ran | stage 0 was never confirmed | confirm the frame next time; file the rows as DROPPED, do not reuse them |
| A level-1 seat "verified" but never asked a real question | a ping is not a model call | exercise it, and exhaust the other level-1 route before dropping |

**Which skill to reach for at each stage — the full routing table is in `references/playbook.md`.** Reach for it rather than improvising: roughly sixty installed skills cover parts of this harness, and re-implementing one by hand is the failure this whole repository exists to stop. Measured on the first live run: the facilitator drove a browser manually for a deep-research pass while `perplexity-researcher-reasoning-pro` sat installed and unused.

Longer reference — worked lane assignments, NotebookLM call sequences, the stage routing table, and the full artifact templates: `references/playbook.md`.
