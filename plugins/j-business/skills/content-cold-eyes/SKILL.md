---
name: content-cold-eyes
description: Blocking review gate before any blog post, marketing copy, course content, or site content change is called done. Triggers on writing or reframing a post, editing marketing copy, or changing published content. Prevents shipping AI-sounding or off-voice content on the strength of a self-review.
---

# Cold-eyes content review

The agent that wrote the content cannot review its voice. It will rate its own phrasing as
natural because it chose it. A low slop score is necessary and not sufficient — structural
tells survive word-level cleanup.

## The gate

Before marking any content task done, dispatch parallel critics with distinct briefs:

**AI-feel detector.** Slop patterns and structural tells: the essay arc (hook → pivot →
thesis), anaphoric repetition, rule of three, slogany flips, sustained staccato, "the journey",
apologetic caveats. Watch especially for repeated 3–4 block parallel structures — channel
quartets, threshold bands, Keep/Revise/Cut, pass/fail tables. Those are writer-default tells
that word-level slop detection misses.

**Voice enforcer.** Against the project's voice guide. Three tests: the **who** test (every
sentence has a person doing something), the **show** test (concrete scenarios, not adjectives),
the **practitioner** test (named incidents, not generalizations).

**ICP reader.** Does this read for the actual target reader, or has the audience drifted to a
different segment? Tool jargon needs a first-mention gloss — what it is, what it costs, whether
technical help is needed.

**Cold reader.** No context, fresh eyes: what confuses, what doesn't land, what a hostile
forum would tear apart.

Use `slop-detector` and `humanizer` for the mechanical passes; they complement these critics
and don't replace them.

## Synthesis

Convergent findings (≥2 critics flag the same thing) are high-confidence and get fixed.
Divergent (one critic) is a judgment call — surface it rather than silently deciding.

Show the user convergence and divergence **before** declaring the task done.

After applying fixes, re-check the worst section with the critic that flagged it hardest.
A fix that wasn't verified is a hope.

## Anti-patterns

- Trusting the writing agent's self-review for voice.
- Treating a low slop score as sufficient.
- Marking content done before the user has seen the findings.
