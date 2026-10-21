---
name: blog-write
description: >
  Actually WRITE and ship a blog post - draft, critics, gates, commit, PR. This
  is the delivery half of the pipeline; j-blog:blog-next decides WHAT to write and this
  writes it. Use whenever the user asks to write, draft, publish, ship or add a
  blog post; when they hand over a topic and expect a post out the other end;
  when they point at an approved row in the content plan; and when they ask to
  UPGRADE or refresh an existing post rather than write a new one. Also use when
  a /j-blog:blog-next run ended in a WRITE or UPGRADE verdict and nothing has been
  drafted yet.
  NOT for choosing the topic (use j-blog:blog-next), LinkedIn posts (j-linkedin-post:j-linkedin-post),
  course chapters, or landing pages (page-cro, landing-page-optimization).
---

# Blog: write it and ship it

> **Run from the `jetthoughts.github.io` checkout.** Every path in this skill (`content/blog/`, `bin/`, `test/`, `.okf/`, `docs/`) is relative to that repo's root. LinkedIn drafts live in the separate `jetthoughts/linkedin-posts` repo (local `/Users/pftg/dev/linkedin-posts`) and belong to `j-linkedin-post:j-linkedin-post`.

**You produce a published post.** Not a plan, not a recommendation. If you finish
without a committed post or a named blocker, the run failed.

`j-blog:blog-next` owns "what and whether." You own everything after that.

| Stage | Owner |
|---|---|
| Topic, research, gated outline | `j-blog:blog-next` |
| **Draft → critics → gates → commit → PR** | **this skill** |

**Read before starting; this skill deliberately does not copy them, so a
correction lands in one place:**

- `docs/workflows/blog-pipeline.md` - **canonical from STEP 4 onward.** Follow it
  step by step. Every blocking gate is defined there.
- `docs/90-99-content-strategy/strategy-analysis/90.11-voice-guide.md` - voice.
- `docs/90-99-content-strategy/strategy-analysis/90.10-icp-primary-website-target.md` - the reader.
- `.okf/content/claims-canon.md` - what you are allowed to say. A number with no
  in-repo source is a defect, not a detail, and so is a mechanism.

## The claim rule that catches the errors gates cannot

Fetch the source before you assert how something works. Not after, and not from
memory - training memory returns a confident sentence whether or not it is true,
which is the failure it cannot warn you about.

Reach for the instrument that matches the claim: **`context7`** for how a
library behaves (it reads the project's own docs and names real classes and
methods), **`WebSearch` then `WebFetch` the primary source** for a study or
statistic - press coverage of a study is not the study - and **NotebookLM** when
you need to interrogate a body of sources. `blog-pipeline.md` STEP 4f has the
full routing.

**Search for the rebuttal, not the confirmation.** Query for criticism and
failed replications of what you are about to assert. Searching for support
returns support; that is what it is for.

**This applies hardest when you are EDITING.** Deleting a bad claim and writing
a replacement feels like cleanup, so the replacement gets less scrutiny than
anything you write from scratch - and it is a fresh assertion carrying the same
burden. Claims-canon records the case: the same author wrote the same Propshaft
sentence twice on one day, wrong when it was framed as a fix, right when it was
framed as writing, because only the second one triggered "go read the README".

The mechanical gates cannot help you here. A ratchet counts invented SHAPES; a
wrong explanation has no shape. If a sentence says how something behaves and you
did not open its documentation in this session, either open it or soften the
sentence until it stops being a claim.

## What you need before drafting

A topic row with an angle, the research digest, and a gated outline. If you have
all three, start at STEP 4.

**If you don't, get them - do not draft anyway.** Run `j-blog:blog-next` first and come
back with its output. A post drafted without the premise audit is how a decayed
row or a dedup collision reaches a draft, which is the exact failure the split
exists to prevent.

**If the user handed you a topic directly**, that is not a licence to skip the
audit - it is the case where the audit matters most, because nobody has checked
it against the corpus yet. Run `j-blog:blog-next`'s Stage A on it, then continue here.

## New post or upgrade

Both are this skill's job, and the choice is `j-blog:blog-next`'s verdict, not yours.

- **WRITE** - a new post at `content/blog/<slug>/index.md`.
- **UPGRADE** - edit the existing post in place. Do NOT create a second post on
  the same topic; that is the cannibalisation the verdict exists to prevent.
  Keep the URL, keep what still holds, and rewrite what the new material
  changes. An upgrade that only appends a section has usually missed the point -
  if the thesis moved, the shape moves with it.

## Running the pipeline

Follow `blog-pipeline.md` STEP 4 → STEP 7. It carries the cadence quotas, the
BAD/GOOD pairs, the two-pass writing rule, and the gate definitions. Do not
paraphrase it from memory - open it.

The gates that most often get skipped, named here so they are not:

- **STEP 4e self-critique** (`reflexion-reflect`) before the critic panel.
- **STEP 4f claim sourcing** - name the URL you opened for every claim about how
  an external thing behaves. No gate covers this one.
- **STEP 5a anti-AI pass** before the review loop, not after.
- **STEP 5b slop gate: `slop >= 8/10`.** This is the blog scale, 0-10, higher is
  better. The course's `Slop <= 25` is a different scale in the other direction -
  never mix them.
- **STEP 5c cold-eyes gate** runs LAST, by a reviewer that did not write the draft.
- **STEP 6b pre-publish checklist**, then **STEP 7 validate**.

**Author ≠ verifier is the point of the panel.** Spawn a different agent type for
each critic role. If agent spawning is unavailable in this session, run the gates
inline against the written criteria and **say plainly in the handback that no
independent verifier ran** - a self-reviewed draft that claims a passed 4-eyes
gate is worse than one that admits it had none.

## Gates before commit

Content-only diff (markdown prose and frontmatter, no template/CSS/body HTML):
`bin/hugo-build` plus the rendered scroll gate, plus the unit suite master runs
after every merge:

```
ENVIRONMENT=production OUTPUT_DIR=_dest/public-test BASE_URL=/ bin/hugo-build
PRECOMPILED_ASSETS=1 HUGO_DEFAULT_PATH=_dest/public-test bin/rake test:unit
```

A declared `cover.png` that was never added builds fine; four posts shipped that
way on 2026-10-19 and turned master red
(`docs/incidents/25.05-master-red-2026-10-19-incident-record.md`). The suite's
`test_every_declared_cover_ships_in_its_post_bundle` reads every post's source,
so it also covers scheduled posts the production build leaves out. The visual
suites do not apply.

The moment the diff touches a template, stylesheet or body HTML, the full visual
gate applies - `bin/qtest --changed` before the commit. Check the actual diff,
not what you intended to change.

New media gets the visual gate in `blog-pipeline.md`: 1280x800 and 390x844, four
criteria scored, and the scores written into the commit message.

**The reading gate applies to EVERY post over 800 words, images or none.** Two
gates already cover that and neither is optional: `ruby bin/check-post-visuals`
(BLOCKING, `blog-pipeline.md` STEP 6b - a ratchet, so a new long post with no
diagram pushes the count over the floor and fails) and CLAUDE.md's
cognitive-load rule, which says measure screens-to-scroll and the longest
unbroken prose run in the browser instead of eyeballing them. Quote both numbers
in the handback, then look at the screenshot: numbers do not catch two labels
colliding inside an SVG, and that shipped into a PR on 2026-08-28 with every
measurement green.

## Ship

Feature branch, commit, `gh pr create` with the evidence. Never push to master.

**Say whether the post is LIVE or SCHEDULED.** Production skips future-dated
content, so a post dated ahead publishes on its date rather than now. **That is
a supported way to schedule (Paul 2026-08-22) - leave a future date alone unless
asked.**

The only real error is claiming gate evidence the gate could not have produced:
`bin/rake test:links` reporting zero errors across a build that excluded your
future-dated post has validated everything except your post. Fine for a
scheduled piece, wrong to quote as proof it is good.

**Do NOT wait for CI on a content-only PR** (Paul 2026-08-22). Prose and
frontmatter cannot move the app build, so local gates decide and you merge as
soon as they are green.

One thing does not come free: `content/**` triggers the link checker, and
internal links are exactly what a post adds. Run **`bin/rake test:links`**
locally in place of the wait. If you skip it, say so in the handback - the
master push-run still crawls, so a broken link becomes a fix-forward defect
rather than a caught one.

**End the handback with the local review link** - `http://localhost:<port>/blog/<slug>/`.
One dev server per session, never 1313:

```
PORT=$((20000 + RANDOM % 20000)) bin/dev
```

## What four cold-eyes reviewers found, and what it costs to skip them

Three posts shipped on 2026-08-22 having passed my own checks. A four-lens panel
then found defects in all three, and every category below is something no script
and no self-review caught.

**Numbers I was confident about were wrong.** A tool output was reproduced inside
a fence with one field silently edited. A `[snap_diff] 287 screenshots compared`
line took 287 from the *unit-test run count*. A link figure from today's run was
used to illustrate a fix that landed weeks earlier at a different number. Every
one felt remembered rather than invented, which is exactly why they survived.

> Before you put a number in a fence, open the artifact that produced it and copy
> the line. Numbers you "remember measuring" are the dangerous ones - you did
> measure something, just not this.

**Cited but never spent.** Two of three posts listed a source in the footer that
the body never engages. A citation nobody uses is dressing, and one of ours had
its claim on the cover image while the post never told the story.

**A source's own words checked, its attribution not.** "Responsible Statecraft
traced it" - they reported it; a NewsGuard analyst traced it. "Both publish their
error bars" - one does. Verifying the quote is not verifying the sentence around
the quote.

**Commands shipped without running them.** A `for f in content/blog/**/index.md`
loop matches nothing in bash without `shopt -s globstar` - it reports success
having checked zero files, in a post about checks that check nothing. Run every
command you publish, in a clean shell, and show what it returned.

**The macro-rhythm, which is the actual slop.** Every H2 ended on a one-sentence
aphorism paragraph. Sentence lengths varied; the choreography did not -
"evidence, evidence, punchline, white space, next heading", five times a post,
three posts. And all three opened on the identical two-beat reveal: flat claim,
one-line rug-pull. Individually each works. As a set, a reader hears the machine.

> Read two consecutive sections aloud. If they land the same way, one of them
> has to change shape - not wording.

**Cross-post repetition.** The same Laravel anecdote carried two same-day posts;
all three closed on the same pitch. The ICP reviewer's verdict: "as a subscriber
I'd feel I read one post three times."

## Run the panel, do not self-review

Four lenses, spawned as separate agents of a DIFFERENT type than the writer:

1. **ICP cold read** - give it `90.10`, ask where it stops reading and what it
   would cut. Require three cuts per post.
2. **Voice and AI tells** - give it `90.11` and STEP 5a. Ask for what a regex
   cannot see: prose that is grammatical, on-pattern and lifeless.
3. **Competitor standard** - give it `blog-writer-reference-samples.md` and have
   it FETCH two current competitor posts, so it compares against writing rather
   than a summary.
4. **Claim verification** - every external claim fetched at the primary, every
   in-repo number checked against the artifact that produced it. Where the
   research digest carries a source excerpt (`j-blog:blog-next` Stage B), diff the
   draft's sentence against the excerpt, not against memory of the source.
   Trace every footer source to the sentence that spends it - a citation the
   body never engages is dressing, not evidence.

Brief each with goal and artifact, never with your conclusions. Require each to
name something it would cut; a panel returning three approvals was not asked a
real question. Run them in parallel and wait for all four before editing, or you
will fix the same post four times.

## A verdict binds to a version, not to the session

Record every gate result as `gate: verdict @ <sha>`. If HEAD has moved since,
that verdict is stale for the gates named below and they count as UNRUN. Saying
"the panel approved it" about a draft since restructured is not a lie told on
purpose; it is what happens when a result lives in memory rather than against a
commit. On 2026-08-28 a four-lens panel reviewed a draft, the post was rewritten
three times after operator corrections, and it reached a merge-ready PR with one
reviewer having read the shipped text.

| What you changed | Re-run |
|---|---|
| Structure, section order, the thesis | Reading gate, slop score, one cold-eyes lens |
| A claim, a number, a citation | Claim verification for that claim |
| Sentences inside one section | The greps, on the changed text - they ran against the old words and re-running is free. A replacement sentence that asserts anything is a claim change, row 2. |

**The slop score is a floor you re-measure, not a badge you keep.** Below 8 it
does not ship, and an 8 taken before a restructure is worth nothing after one.

**Expensive gates are the ones that get skipped.** Greps cost one command so
they run constantly; the browser gate and the panel cost real time, so they
slide to the end and then off. When a change is structural, run the expensive
one FIRST.

## Three exits, and only three

- **SHIPPED** - committed, PR open, gate verdicts quoted with their numbers.
- **BLOCKED on a named decision** - one of: whether a claimed client engagement or
  number is real, publishing outward, overriding a documented gate,
  pricing/naming/internal numbers, a split-and-irreversible call. Name which one,
  and take the conservative option meanwhile where one exists.
- **FAILED the gates twice** - stop, hand back the draft with both critic reports
  and what you changed between rounds. Do not iterate a third time silently; two
  failed rounds on the same draft usually means the outline was wrong, which is
  `j-blog:blog-next`'s problem and not something more prose will fix.

**HOLD is not an exit here.** By the time work reaches this skill the decision to
write has already been made and audited. If you find a reason the post should not
exist, that is a falsified premise - say so explicitly and hand it back to
`j-blog:blog-next` rather than quietly producing nothing.
