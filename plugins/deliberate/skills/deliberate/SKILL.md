---
name: deliberate
description: Run a grounded group deliberation that ends in a decision: gather evidence in disjoint lanes, build a verified evidence ledger, generate rival concepts, force a written dissent, and synthesize one call with its kill criterion. Use whenever a question needs more than one opinion and the answer must be defensible — choosing between options, 'what should we build/do next', strategy calls, vendor or approach selection, prioritising a backlog of ideas, running a decision workshop, or any time someone asks for a panel, a council, multiple perspectives, or 'research this and tell me what to do'. Also use it to audit a decision already made. Domain-agnostic.
---

# Deliberate

A decision harness. It exists because the usual failure is not a lack of ideas — it is **a group that agrees for the wrong reason** and calls that agreement evidence.

```
FRAME → GATHER → LEDGER → IDEATE → DECIDE
        (disjoint) (verify) (diverge)  (dissent, then call)
```

**Every reply opens with the stage:** `stage 3 of 5 · LEDGER`. A run that stops early says **UNFINISHED**, names the stage it reached, and names what is still owed. Findings presented without that label read as a conclusion, and once did.

**Skip a stage and say which. Do not skip the verification inside one.**

## What this file can and cannot do

It is prose, and prose is advisory. This project measured its rules drifting into up to five contradictory versions while its one script-enforced gate had zero violations. **Nothing here blocks anything.**

**Do not answer that by writing a checker.** A script is worth building only for something stable with a strict constraint — a file-format convention, a test over code, a result with a fixed shape. A deliberation is judgment work: any script enforcing it is written once, goes stale against the next real question, and then nobody runs it. That is a worse failure than advisory prose, because a dead gate looks like a live one. (Paul, 2026-08-30.)

**The lever that is left is brevity.** A rule survives by being read at the moment it applies, so the file has to stay short enough that reading it is cheap. Treat every rule below as one you choose to keep.

Consequence for whoever edits this file: **a new rule replaces an old one or it does not go in.** Appending a paragraph per incident is how the previous version reached 459 lines and stopped being read.

## Independence: report what you achieved, not what you attempted

Five agents with five personas are not five perspectives. They share a model, a context and usually a source set — correlated by construction. A model will also produce a fluent objection to *any* position on request, so "it dissented" is not evidence it thought independently.

**Do not claim a ranking. Claim a measurement.** Across 350+ models, errors agree ~60% of the time when both err, and *more capable* models are *more* correlated even across vendors; a nine-judge panel from seven model families carries roughly 2.2 effective independent votes against 4–6 for humans. A frontier-model panel buys far less than it looks like, and no published work ranks the mechanisms against each other.

In the output:

- **Name each seat's de-correlation mechanism** — different system · different corpus · different tool · different lens — and which it actually got.
- **Name the disagreement it produced.** Seats that agreed on everything are one seat. Report that.
- **Disjoint corpora are the only mechanism with a guarantee.** A claim absent from a corpus cannot be produced from it. Model diversity is a statistical hope; corpus disjointness is arithmetic.
- **Never report a level you skipped the work for.** A time-box is a reason to run fewer lanes, never a reason to claim a lane you did not run. A fallback you wrote down and did not take is the same as not having one.

**Order of operations (Paul, 2026-08-30): Claude subagents carry the lanes; a foreign model reviews them afterwards.** The subagents hold the repository, the closed decisions and the house rules — they produce the lanes, the ledger and the concepts. The foreign seat goes **on top**, briefed on facts only and told to refute: the `gemini` CLI, or Perplexity driven through `claude-in-chrome` — **that is what `claude-in-chrome` is for here, and the only thing.** Ordinary page-reading uses `WebFetch` and the external drivers listed under GATHER. Run instead of the lanes it reviews nothing; run first it anchors what it was meant to check.

**Working level-1 route on this machine:** `mcp__gemini__ask-gemini` is down (missing `agy`). Use `GEMINI_CLI_TRUST_WORKSPACE=true gemini -m gemini-3.1-pro-preview --skip-trust -p "$(cat prompt.txt)"` — the CLI's default model 404s, so name it. Exercise the seat with a real question; a ping is not a model call.

**On a blocked spawn, change the agent type — never the mechanism.** Running a lane inline because a hook refused an agent collapses the panel and makes the facilitator both author and checker of that lane.

## 4-eyes

**No stage output is accepted on the word of the agent that produced it, and the checker must have had different inputs.** Same-agent review returns "looks good"; same-input review returns the same blind spots.

| Produced by | Checked by | The check is |
|---|---|---|
| a lane's findings | someone who did not gather them | **open the citation and read it** |
| the ledger | a second reader on a different corpus | is anything asserted that no row supports? |
| concepts | the dissent | does a substitute already do this? |
| the decision | the kill criterion | what observation retires this, and on what date? |

A review returning "looks good" has failed and is re-run. **Default to refuted when uncertain.**

**Then run it on yourself.** Before leaving any stage: *the rule I just enforced on someone else — does it hold for what I just produced?* Ten defects in one measured session traced to that question never being asked. Sourcing applies to the facilitator's own prose; prior work on disk is an input; an instrument that judges output is itself an output.

## Roles

A **facilitator** who owns the sequence and never argues the content · a **decider** who breaks ties and owns the outcome (not delegable) · **contributors** who produce.

**Together alone** is the principle underneath: produce in parallel and in silence, then share. Interacting groups generate measurably fewer ideas than the same people working separately — a large effect, replicated since 1991. Silence is not a style preference; it removes the mechanism by which the loudest position wins.

---

## Stage 1 — FRAME

One decision question, narrow enough to be researchable. Reject the vague form out loud:

- **No:** "find innovative ideas for X"
- **Yes:** "which recurring workflow among [specific actor] is underserved enough to justify testing a paid solution in 14 days?"

Write: the question · who decides · what a good answer must contain · what is out of scope · the date the decision expires. **If the question cannot fail, it is not a question.**

Then, before anyone looks at a solution:

- **The goal** — specific and dated. The horizon scales to the decision, not to the format; a two-week goal is one you can be wrong about quickly.
- **The metric** — the one number that moves if the goal is being reached, and what it reads today. If it reads "unknown", that is the first research question.

**Confirm the goal and the metric separately.** Bundled, a weak metric rides in on a strong goal.

**Show the frame to the decider and wait.** Every lane, row and concept inherits it, so a wrong default here wastes the whole run; every later stage can absorb a bad call, this one cannot. **When the question holds more than one reading, state both and say which you would take** — never silently pick. The tell is a phrase that only matters under one reading. If the host forbids ending a turn on a question, name your reading, mark the run **UNCONFIRMED**, and run on it so the decider can kill it in one line.

## Stage 2 — GATHER

**Resume before you gather.** Read what the repository already holds and check the project's closed-decision register *before* spawning anything. A KILL there is binding without new contradicting evidence, and an option it killed reappearing later is a defect, not a candidate. Cite prior corpora — file, date, lane — and re-run only a lane whose question has moved. Say what you did not re-run and the rule that forbade it. The pathology this prevents is measured here: *11 scans, 18 reports, 0 customers.*

Then three to five lanes, **each with a disjoint source domain**, briefed with **evidence and never with your conclusion** — a panel handed your inference returns it wearing independent-sounding confidence.

Run `Research` for the web lane rather than hand-rolling it; it already runs cross-vendor seats with URL verification. Use the internal index for prior work and a code-search tool for feasibility. Lane assignments and brief templates: `references/playbook.md`.

**Reading a page: start native, escalate only when it fails.** Each rung costs more than the one above it, so stop at the first that works.

| Need | Reach for |
|---|---|
| The text of a page, a quote, a figure | **`WebFetch`** — native, no setup. This is the default and covers most rows |
| `WebFetch` 403s or the content is JS-rendered | `mcp__parallel__web_fetch` (different fetcher, different result — it recovered a page `WebFetch` refused) · `lightpanda` when speed matters |
| What the page *does* — interaction, a flow, a logged-in view | an external driver: `agent-browser` · `browser-use` · `Interceptor` (real Chrome) · `remote-browser` (sandboxed) · `playwright` |
| A screenshot to actually look at | `chrome-devtools` `take_screenshot` · `screenshot` · then `web-design-reviewer` for a structured visual read |
| A site that resists, or extraction at volume | `BrightData` · `Apify` · `just-scrape` |

**`claude-in-chrome` is reserved for the Perplexity seat** and is not a general page-reader — it drives the user's own logged-in browser, which is a heavier and more intrusive instrument than any row above needs.

**Every lane returns rows, not prose:**

| Claim | Source (URL or openable path) | Date | Direct quote or figure | Type | Confidence | What this does NOT prove |
|---|---|---|---|---|---|---|

**A publication name is not a citation** — a reader cannot open it and the verifier has nothing to check.

**Every lane also returns what it looked for and did not find**, with the denominator. *Searched N, found 0* beats silence; a clean result often means nothing was measured.

## Stage 3 — LEDGER

One writer merges the rows. A **different** agent verifies by opening citations — not by reading the ledger.

Label every line: **Fact** (sourced, dated, checkable) · **Interpretation** (what we think it means) · **Assumption** (believed, unproven, named as such) · **Question** (still unknown) · **Conflict** (two sources disagree — record both).

**Conflicts are this stage's most valuable output.** Agreement between lanes that shared a corpus is not corroboration. If nothing conflicts, suspect the lanes were not disjoint and say so.

**Rows answering a superseded question go under a DROPPED heading.** They are still true and still cost something to produce, which is exactly why they get carried into a design they do not support. Name them, keep them as evidence, exclude them from the concepts.

**No concept may be proposed before the ledger exists.** Ideas generated before evidence are priors wearing new words.

## Stage 4 — IDEATE

### 4a — Lightning Demos ("related worlds")

**Go and look at the world before inventing.** A model will happily produce plausible examples from memory; that is a prior, not a demo.

**Gate: at least three examples must carry a URL fetched during this run, from outside the question's own domain.** No new fetches, no round.

Assign each contributor **a different domain**, and **shape the domains like the ask** — an org question gets org demos, a pricing question gets pricing demos. The concept space inherits the demo domains: demo safety engineering and you will concept watchdogs, and every stage will pass its own gate while the run misses the question.

**Run `lightning-demos` — it owns the procedure, and never restate it here.** What that skill adds and this stage depends on: reject the famous handful (they are the highest-probability answers, which is why they carry nothing) · steal the mechanism, never the model · capture a scannable headline plus the component and its source · **do not decide or debate during the round**, because judgment kills the examples that only look irrelevant. Aim for ten to twenty ideas before anything is assessed.

### 4b — Generate silently, then build on

**Seed the frame.** Open the ideation surface already populated with the ledger, the demo board, the goal and metric, and any concept previously killed and why. An agent handed a blank prompt fills it from its priors; an agent handed the ledger argues with it.

Two rounds, both silent:

1. **Diverge.** Ask each contributor for **a distribution of candidates with their probabilities**, not a list — a list returns the top of the distribution, which is everyone's first idea. Measured at 1.6–2.1× the diversity of direct prompting, and it costs one prompt.
2. **Build on.** Pass each contributor another's cards and have them extend those, silently. This is the mechanism with the largest measured advantage in LLM ideation — it beat the alternatives in 15 of 15 comparisons — and the one most harnesses omit. A single model switching roles captures ~70% of the multi-agent gain: **structure beats architecture.**

Generate rival **mechanisms**, not rival wordings. Lenses that produce genuinely different ones: inversion (achieve the outcome without the thing everyone uses) · remove / replace / reverse · adjacent transfer · 10× constraint · non-consumption · wedge (one high-frequency moment instead of the whole problem).

Each concept carries a card, rejected if a field is empty: **what it is · which evidence row it answers · which demo mechanism it borrows · how it actually works · the existing substitute · what is genuinely different · the most dangerous assumption · the smallest test that would falsify it.** "Different" means a different mechanism, not a different feature list.

**Lay all cards out together before judging any of them**, in the same shape and the same length. A card that is richer because its author wrote more wins on style, and style bias is now the dominant judging bias.

### 4c — The ask check

**Re-read the requester's verbatim words. Would this concept set read as an answer to them?** Not "does it move the metric" — a set can move the metric and answer a different question. If it does not answer the ask, return to 4a with domains shaped like the request. Do not contest the wrong set.

## Stage 5 — DECIDE

**Dissent is required, written, and never discussed.** Each contributor names the strongest case *against* the leading concept, independently and without seeing the others. Adversarial passes here have a 7-for-7 record of finding something the author missed; none ever returned an approval.

Run `sadd-judge-with-debate` for the pass, or spawn the adversary yourself with a facts-only brief. Either is fine — **saying which, in the record, is not.** A table entry is not an invocation: name the skill at the moment you need it or admit you hand-rolled it.

**Every dissent gets a disposition in the record: UPHELD, PARTLY UPHELD, or REFUTED, with the reason.** Without this the run logs the objection and proceeds on the original plan — defects identified, none remediated.

**Do not hold a debate before deciding.** Debate does not reliably beat cheaper aggregation; roughly 37% of position changes in it are noise rather than persuasion, and structurally-fluent-but-empty argument induces error adoption around 30%. Debate re-correlates the seats you just paid to de-correlate. Written dissent is not debate: it is produced in isolation and disposed of in writing.

**Do not tally a vote over agents.** An agent panel is ~2.2 effective votes, so a tally is one opinion counted three times with a number on it — and here it produced 0 valid tallies from 3 attempts, declared VOID twice for exactly this reason. When *humans* vote, dot-voting is the right instrument and `ldj` owns the procedure.

**The decider decides.** For two live alternatives, place them by two binary questions — *higher or lower on impact? further left or right on effort?* — which replaces an argument nobody has to defend out loud. Score openly if it helps, and keep **evidence quality as an explicit term**, or the best-argued concept beats the best-evidenced one.

Then write the record:

```
DECISION: proceed | iterate | pause | kill
Question · Decided by / date
Evidence: N rows, M independent sources, K conflicts unresolved
Independence: mechanism and disagreement achieved, per seat
Dissents and their disposition
What we now know · What remains assumed
The call, and why this one
Smallest next test · pass threshold · by when
KILL CRITERION: the observation that retires this, and the date it is checked
```

**A decision without a kill criterion and a date is an opinion.** And a kill date living only in prose is invisible — put it on whatever surface the project actually checks, or it passes unnoticed. That has already cost this project real time.

**Beware the ideation–execution gap:** ideas that look best on paper deflate most once built, and AI-generated ones deflate more than human ones. The kill criterion is the only defence, which is why no concept leaves without one.

**End on one surface** — goal · metric · the call · the roadmap · the kill date. Not the decision record; that is the audit trail. A decision spread across three documents is re-litigated because nobody can hold it at once. Sequence by what unblocks the most; anything unsequenced goes to a named backlog rather than staying ambiguously alive.

---

## Choosing the depth

Over-running this on a small question is its own failure.

| Cost of being wrong | Run |
|---|---|
| Reversible, cheap | FRAME → one lane → decide. Say you skipped the rest |
| Normal | 3 lanes · ledger + verify · one demo round · concepts · one dissent pass |
| Expensive or irreversible | 5 lanes including a foreign-model seat · demos with a domain per contributor · dissent from every seat · full record and roadmap |

**Running it light is the common case:** frame + metric → demos → concepts → dissent → one page. What does not change at any depth: the metric is agreed before anyone looks at a solution, the demos are fetched from outside the domain, dissent is written in isolation, and the run ends on one page with a kill date.

## Where the work is delegated

**Prefer the side-effect-free ones.** Measured 2026-08-30: 38 installed skills open with a mandatory `curl` to a `localhost:31337` notifier — nothing listens on that port and no permission rule covers it, so each invocation costs a prompt for a call that always fails. Several also run in a forked context and load a customization tree. That family is second choice here, not first (Paul, 2026-08-30).

| Stage job | First reach | Second choice |
|---|---|---|
| Panel briefing and forced veto | `structural-decisions` | — |
| Web gathering, cross-vendor seats, URL verification | — | `Research` (the one worth its friction — its verification machinery has no substitute) |
| Divergent generation | the lenses in 4b, inline | `BeCreative` · `Ideate` |
| Adversarial passes | `sadd-judge-with-debate` | `RedTeam` · `brutal-honesty-review` |
| Human dot-vote, impact/effort, actionability | `ldj` — owns the procedure; never restate it here | — |
| Cheapest falsifying test | `pol-probe` | — |

**A table entry is not an invocation.** Across twelve run artifacts every one of these was invoked zero times and every pass was hand-rolled — because "reach for this" in a table is not a step anyone takes. Name the skill imperatively at the moment the stage needs it, as stages 2 and 5 do, or hand-roll it deliberately. **Either is fine; not saying which, in the record, is not.**

## Failure modes

| Symptom | What it means | Do |
|---|---|---|
| Every lane agrees | lanes were not disjoint | re-run with separate corpora; report it |
| Nothing conflicts in the ledger | the corpus is one echo | add a different-corpus seat |
| A review returns "looks good" | failed review | re-run; default to refuted |
| Concepts arrive before evidence | priors wearing new words | discard and gate on the ledger |
| The run re-derives evidence already on disk | stage 2's resume rule was skipped | cite the prior ledger; re-run only the moved lane |
| A clean result with no denominator | nothing was measured | report *searched N, found 0* |
| The most articulate concept wins | rhetoric beat evidence | check evidence-quality was scored; normalise card length |
| Demo examples all from one industry, or all recalled | the demo round did not happen | re-run with fetched URLs and a domain per contributor |
| Concepts answer a narrower question than was asked | the concept space inherited the demo domains | re-run 4a with domains shaped like the request |
| The winner won on being cheapest to measure | testability selected the deliverable | say so out loud; that is a finding about the evidence, not a verdict |
| A dissent is recorded but nothing changed | no disposition was written | mark each UPHELD / REFUTED with its reason |
| The decision has no kill criterion | it is an opinion | do not record it as a decision |
| A seat reports a level it did not exercise | a ping is not a model call | exercise it, or report the level you got |

Lane assignments, brief templates and the full artifact formats: `references/playbook.md`.
