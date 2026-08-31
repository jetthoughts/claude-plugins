---
name: contract
description: The JetThoughts autonomous delivery contract. Use when running any feature, fix, or idea to completion - it defines the intake path, the DISCOVER-to-LEARN loop, the evidence standard, 4-eyes roles (author never verifies own work), WIP=1, async-first artifacts, and stopping rules. Repo instructions (CLAUDE.md, AGENTS.md) always override this skill on conflict.
---

# The delivery contract

**What this is for: agents collaborating to find the truth.** A single agent
cannot find its own blind spot — it checks the thing it meant to build. Truth
comes from friction between agents with different jobs: separate the author
from the verifier, brief with evidence rather than conclusions, require a
dissent, and treat every finding as a claim that must itself survive.

**Precedence: the consuming repo's instructions override this skill on every
conflict.** This skill is the default, never the authority.

## 1. GOAL

> **GOAL:** `<one sentence, falsifiable, with the artifact named>`
> **DONE WHEN:** `<a command anyone can re-run, or an artifact anyone can open>`
> **NOT IN SCOPE:** `<the adjacent work you will be tempted into>`

If DONE WHEN cannot be written as something re-runnable, stop and rewrite the
goal. "Improve X" is not a goal. **NOT IN SCOPE is load-bearing** — most wasted
cycles are adjacent, defensible, and not asked for.

### 1a. Intake — from a raw idea to a running unit

1. **TRIAGE**: now / sequenced / backlog / groom-first. One-line verdict so the
   operator can override.
2. **SHAPE**: ambiguous or structural → groom first. Concrete → straight to GOAL.
3. **GOAL**: write §1's three lines. No re-runnable DONE WHEN → no dispatch.
4. **ORCHESTRATE by size** — the contract holds at every scale:
   - *trivial edit*: inline; a verifier agent still reviews before commit.
   - *one unit*: author agent + distinct verifier (§5).
   - *a feature*: commits proceed one at a time on the sprint branch, each
     independently reviewed; the sprint ships as ONE PR, size-capped per the
     repo's rules (JT default: ~500 changed lines of CODE; docs/logs exempt;
     oversized sprints split into sequential PRs, merge N before N+1).
   - *swarm scale*: NOT the default. With 3+ independent same-shaped units,
     PROPOSE it in the triage verdict; it activates only on explicit request,
     workers isolated in worktrees.
5. **The contract — non-negotiable regardless of orchestration shape**:
   feature branch + PR, never the default branch · rebase when it moves, never
   merge it in (backup ref first) · author ≠ verifier at every stage · gates
   matched to the diff type per the repo · async-first artifacts (§7) ·
   escalate only the irreversible or a genuine scope change (§8).

An orchestration that would break a contract line is scoped wrong — reshape the
work, never waive the line.

## 2. The loop

One pass per unit. The unit is a reviewed commit; never start unit N+1 before N
has landed.

```
DISCOVER → DECIDE → BUILD → VERIFY → SHIP → LEARN
     4-EYES gates EVERY stage, not just the last
```

| Stage | Output | Gate to leave it |
|---|---|---|
| DISCOVER | what is already true | a file:line or URL citation for every premise, read by a reviewer |
| DECIDE | the smallest unit that delivers value | you named what you are NOT doing |
| BUILD | the shortest working diff | it runs |
| VERIFY | evidence from the live artifact | a check that would FAIL if the work were wrong |
| SHIP | a reviewed commit; the sprint merges via its one PR | the repo's gate matrix for THIS change class, quoted with real numbers |
| LEARN | a durable learning captured, or an explicit "none this pass" | a cold session could repeat or avoid it |

Review weight scales with the stage's cost of being wrong, but none is zero. A
cheap stage gets one skeptical pass with a named lens — and leaves one line in
the record: lens, strongest objection, disposition.

**Continuous delivery**: every unit lands on its own — a reviewed commit safe
to merge alone; a unit that cannot land alone was scoped wrong. **Continuous
discovery**: DISCOVER runs every pass; what pass N learned changes N+1's scope.

## 3. Evidence standard

**Produce the check that would fail if the claim were false, and cite it.**

- **Measure the artifact, not a proxy.** Source ≠ what shipped; a green suite ≠
  no visual change; read the element that paints, not the one you selected.
- **Test the instrument.** Ask what the command returns if the claim were
  FALSE — if it cannot differ, it is a ritual. Run a positive control and a
  negative control; a known-positive returning nothing means the instrument is
  broken, not the codebase.
- **Baseline of the baseline**: measure at the merge base and compare failure
  SETS, not pass/fail — the signal is the difference your change makes.
- **Beware the batch**: screen bulk results for the outlier hiding among
  expected changes.
- **Do not freeze decaying numbers into durable prose.**
- **Prefer description to prescription**: "X emits Y" is checkable; "run Z to
  prove Y" smuggles in an unstated universal.

## 4. Do not trust priors — research

0. **Memory first.** Search persistent memory for prior decisions and
   corrections on the topic. A stored correction outranks fresh reasoning; a
   stored decision is not re-litigated without new evidence.
1. **In-tree.** The answer is usually already written down; arguing from the
   model's own recollection instead of looking is the recurring error.
2. **Then the world.** Current docs and targeted research; take the best
   available pattern, not the first plausible one.
3. **Cite what you used.** A decision with no citation is a guess wearing
   confidence.

**Exploit tools that already exist** before writing one — a home-grown
instrument is the most expensive thing in this contract (see §5's stopping
rule).

## 5. Four eyes, and zero trust

**Every change is WRITTEN by one agent and VERIFIED by a different one.** The
author never produces the evidence for its own claim; the session's own
self-review never counts as the second pair of eyes.

| Role | Does | Must not |
|---|---|---|
| Author | makes the change, states the claim, hands over its REASONING | produce the evidence for its own claim |
| Verifier | independently re-derives the evidence, runs ≥1 measurement the author did not run | accept the author's conclusions as evidence |

Brief the verifier with the goal, the artifact, AND the author's reasoning —
a blind verifier reproduces the author's instrument error; the assumptions are
the attack surface. What the verifier must not inherit is the author's
*confidence*: it re-derives, it does not confirm.

The review lands **before the artifact leaves the workshop**: a plan before the
operator sees it, a diff before commit, a finding before it is reported, a
measurement before it is quoted.

**No reviewer available?** Fall back agent → external tool → peer session →
human; if none is reachable, ship marked **UNREVIEWED** — disclosure, never a
silent skip.

- **Panels must disagree by construction** — distinct lens per reviewer;
  independent agreement is valid, manufactured disagreement is not.
- **Ask for measurements, not verdicts** — a critic who returns a count cannot
  be argued with.
- **Re-review after fixing** — round N's fixes introduce round N+1's defects.
- **Findings are claims too** — reproduce before accepting, against the
  artifact cited, not a copy.
- **Stopping rules**: one CLEAN round stops the loop; round three on an
  instrument you invented means delete it; the same blocking question three
  passes running means you are waiting on a decision, not stuck on execution.

## 6. WIP = 1

One unit in flight. One PR open — the sprint's. Parallelism in exactly three
places: reviewer panels judging one artifact · a knowledge-maintainer riding
the same commit without touching the work's files · explicitly-requested swarm
workers, each in its own worktree. Otherwise never run parallel agents over the
same body of work. Before fanning out, check what is IN FLIGHT — an agent also
collides with any unmerged branch touching its files. Brief every agent with
the branch state, not just the task.

## 7. Async-first

A task is not done until its state is readable by a cold session with zero
questions. Decisions → the doc that owns them, with reasoning. Findings → the
PR, with evidence. Handoffs → an explicit list in the artifact the next person
opens. Debt → named, never silent. A concept that stores STATE rots; one that
stores REASONING does not.

## 8. Scope, and when to stop

- Deliver the scope asked for; if part is blocked, finish the rest and say
  plainly what you left and why.
- A loop can iterate but cannot re-scope; if the specification is wrong, say so
  and stop.
- Decisions you are authorized to make, make — record the reasoning, ship,
  keep it reversible. Parking a reversible call on a human is a gate that
  never opens.
- Escalate only what is genuinely irreversible or genuinely theirs.

## 9. Learn, every pass

Both directions: what failed and what worked. Write it where it will be read
again — the repo's knowledge base in the same commit as the change, plus
persistent memory for decisions/corrections/state (that is what §4 step 0
searches; an unstored decision is invisible to the next pass). Store what a
competent successor could not derive. **Correct, do not accumulate** — two
contradictory records are worse than none.
