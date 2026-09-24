---
name: structural-decisions
description: Use before proposing or committing to any open-ended structural change — architecture, redesign, a syllabus or course spine, a strategy call, a backlog reprioritization, or any question whose answer is a shape rather than a fix. Triggers on "rough ideas", "propose options", "brainstorm", "high overview", "spine", "restructure", "redesign", "reprioritize", "which approach". Stops the default of jumping to a single answer.
---

# Structural decisions

Open structural questions have many defensible answers. One answer produced quickly is
indistinguishable from the right one until something challenges it. This skill supplies the
challenge.

## When this applies

The answer is a *shape* — an architecture, an ordering, a spine, a bet — not a fix with a
correct value. Tactical work does not need this.

## The method

**1. Brainstorm before proposing.** Invoke `superpowers:brainstorming` first. Explore intent
and constraints before generating any structure.

**2. Panel, with mandatory dissent.** Dispatch 2–4 agents with genuinely distinct lenses.
Pick lenses that want different things — the buyer, the maintainer, the customer, the
skeptic who argues nothing should be built.

Two rules make this work, and without them you get theatre:

- **Brief with evidence, not conclusions.** Give raw findings and let each lens infer. A panel
  handed your inference returns it four times with independent-sounding confidence — you have
  laundered one opinion into an apparent consensus.
- **Require a veto.** Each lens must name one item the others will likely rank highly and argue
  against it. Without a forced dissent slot, panels converge on whatever the brief implied.

This is the deliberate exception to WIP=1 — triangulation, not parallel work on one body.

**3. Probe the riskiest assumption.** Invoke `pol-probe-advisor` to name what must be true and
the cheapest test that would falsify it — before committing, not after.

**4. Compare explicitly.** With 2+ live alternatives, invoke `recommendation-canvas` so the
tradeoffs are visible rather than implied.

**5. Independent cross-check.** Dispatch `codex:codex-rescue` with the exact question and the
proposed plan. Never apply on top of its assessment without showing the user what it said.

## Reporting

Surface **convergence** (≥2 lenses agree — high confidence), **divergence** (one lens only — a
judgment call for the user, not something you silently resolve), and **every veto**, including
against your own recommendation. Then give one recommendation.

Never present a bundled "I applied X, Y, Z" without showing the multi-source basis.

## The gate

Structural changes apply only after explicit user approval. Never bundle tactical edits with
structural moves — they need separate approval, and mixing them denies the user a real choice
on the part that matters.

## Verify the panel

Panel output is evidence to check, not conclusions to adopt. A specialist's confident
recommendation can carry a latent bug; test the specific claim before acting on it.
