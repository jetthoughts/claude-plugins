---
name: framing
description: Frame a vague or structural request into a decision-ready brief — one decision sentence, one measurable outcome, owner, reversibility, weighted criteria, what would change our mind, a persona-voice problem narrative, and the shape-versus-fix approval gate. Use for rough ideas, propose options, restructure, redesign, which approach, or a request with no clear decision attached. Not for root-cause drilling — use five-whys; not for the call itself — use decision-panel, deliberate, or j-convening-the-council.
---

# Framing

Everything downstream inherits this. A frame fixes four things before anyone looks at a solution: the **decision** being made, the **outcome** that measures it, the **user** whose problem it is, and the **evidence** that would reverse it. A vague request that skips this step produces research nobody can act on and options nobody can compare.

Two shapes of framing, and most requests need both:

1. **The decision frame** — a decision sentence, a metric, an owner, criteria, and reverse triggers. Always required.
2. **The problem narrative** — the same problem told in the user's voice, so the team is solving a real problem and not a feature request in disguise. Required whenever the problem touches users.

A third gate triggers only for some requests:

3. **The shape-versus-fix gate** — when the answer is a *shape* (architecture, spine, ordering, bet) rather than a fix with a correct value, framing does not end at a brief; it ends at a proposal that needs explicit approval.

Apply them in order. Do not hand off to research until Part 1's hard gate passes.

## Part 1 — The decision frame

**Input**: `00-intake.yaml` (or the user's own words). **Output**: `00-decision-brief.md` (template in `../j-independent-ideation/templates/decision-brief.md`).

1. Read `00-intake.yaml`. Read `.claude/artifacts/independent-ideation/*/11-decision-record.md` for prior decisions on the same topic; link them under Existing beliefs.
2. Write the decision as one sentence starting "Decide whether to …". If two decisions hide inside, split them and ask which one is first.
3. Write ONE desired outcome with metric, baseline (or UNKNOWN), target, horizon.
4. Name the target customer/user and the job they are trying to make progress on.
5. Fill constraints from intake. Missing budget or effort cap → ask; do not guess.
6. Classify reversibility: type-1 (irreversible or expensive) or type-2 (cheap, reversible). If unsure, type-1.
7. Build the criteria table (criterion, weight, measurement, evidence threshold). Weights sum to 1.0.
8. List existing beliefs; tag each FACT (with `E-nnn` from `01-existing-evidence.md`/ledger), INFERENCE, ASSUMPTION, or ESTIMATE.
9. Write "What would change our mind?" as a specific, observable result — not "if the data says otherwise".
10. Write exclusions.
11. Set frontmatter `status: framing`, `decision_id` (`<YYYYMMDD>-<slug>`), owner, human decider, deadline.

**Hard gate — do not hand off to research if any of these is empty:** decision sentence, measurable outcome, deadline, target customer/user, constraints, reversibility, decision owner, human decider, what-would-change-our-mind. On failure: list the missing fields, ask only for those, stop.

## Part 2 — The problem narrative

Articulate the problem from the persona's point of view. This is not a requirements doc — it is a human-centered narrative that ensures you are solving a problem worth solving. Use `template.md` for the fill-in worksheet, and `examples/sample.md` for a worked good/bad pair.

```markdown
**I am:** [the persona — 3–4 concrete characteristics, not "busy professionals"]
**Trying to:** [the outcome they care about — a result, not a task]
**But:** [the barriers preventing that outcome]
**Because:** [the root cause, not the symptom]
**Which makes me feel:** [emotional impact, from research — not marketing copy]
```

Then record **Context & Constraints** (geographic, technological, time-based, demographic) and compress the whole thing into one sentence:

`[Persona] needs a way to [desired outcome] because [root cause], which currently [emotional/practical impact].`

**Quality checks.** Can you picture the person? Is "Trying to" measurable? Are the "But" barriers real, or just inconveniences? Is "Because" the root cause or a symptom? Do the emotions come from interviews or from invention? Read the final sentence aloud to someone who has the problem — they should say "yes, exactly".

**Anti-patterns — any of these means the frame is wrong:** solution smuggling ("the problem is we lack AI analytics") · a business problem in disguise ("our revenue is down") · a feature request ("users need a dashboard") · a generic persona every product could claim · a symptom mistaken for root cause ("the UI is confusing" — that drill is `five-whys`' job) · fabricated emotions ("empowered and delighted" is copy; real users are frustrated, overwhelmed, stuck).

Do not guess personas or emotions when there is no research: run discovery first. This frames user-facing problems; it is not a substitute for a PRD.

## Part 3 — The shape-versus-fix gate

**When this applies.** The answer is a *shape* — an architecture, an ordering, a spine, a strategy call, a reprioritization, a bet — not a fix with a correct value. Tactical work does not need this. Triggers: "rough ideas", "propose options", "brainstorm", "high overview", "spine", "restructure", "redesign", "reprioritize", "which approach".

Open structural questions have many defensible answers. One answer produced quickly is indistinguishable from the right one until something challenges it. This part supplies the challenge.

1. **Brainstorm before proposing.** Invoke `superpowers:brainstorming` first. Explore intent and constraints before generating any structure.
2. **Panel, with mandatory dissent.** Dispatch 2–4 agents with genuinely distinct lenses that want different things — the buyer, the maintainer, the customer, the skeptic who argues nothing should be built. Two rules make it work, and without them you get theatre:
   - **Brief with evidence, not conclusions.** Give raw findings and let each lens infer. A panel handed your inference returns it four times with independent-sounding confidence — one opinion laundered into apparent consensus.
   - **Require a veto.** Each lens must name one item the others will likely rank highly and argue against it. Without a forced dissent slot, panels converge on whatever the brief implied.
   This is the deliberate exception to WIP=1 — triangulation, not parallel work on one body.
3. **Probe the riskiest assumption.** Invoke `pol-probe-advisor` to name what must be true and the cheapest test that would falsify it — before committing, not after.
4. **Compare explicitly.** With 2+ live alternatives, invoke `recommendation-canvas` so the tradeoffs are visible rather than implied.
5. **Independent cross-check.** Dispatch `codex:codex-rescue` with the exact question and the proposed plan. Never apply on top of its assessment without showing the user what it said.

**Report convergence and divergence.** Surface convergence (≥2 lenses agree — high confidence), divergence (one lens only — a judgment call for the user, not something you silently resolve), and every veto, including against your own recommendation. Then give one recommendation. Never present a bundled "I applied X, Y, Z" without showing the multi-source basis.

**Verify the panel.** Panel output is evidence to check, not conclusions to adopt. A specialist's confident recommendation can carry a latent bug; test the specific claim before acting on it.

**The approval gate.** Structural changes apply only after explicit user approval. Never bundle tactical edits with structural moves — they need separate approval, and mixing them denies the user a real choice on the part that matters.

## Sources

- Decision frame and hard gate: the j-ideation framing stage skill, merged here.
- Problem narrative: adapted from `prompts/framing-the-problem-statement.md` in the [deanpeters/product-manager-prompts](https://github.com/deanpeters/product-manager-prompts) repo; grounded in Christensen's *Jobs to Be Done*, Osterwalder & Pigneur's *Value Proposition Canvas*, and Dave Gray's empathy mapping.
- Shape-versus-fix gate: the j-deliberate shape-versus-fix gate skill, merged here.
