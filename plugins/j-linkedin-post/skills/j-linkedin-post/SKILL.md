---
name: j-linkedin-post
description: Use when writing or revising a LinkedIn post for Paul Keen (https://www.linkedin.com/in/paul-keen/) - drafting from a voice memo or idea, running the editorial feedback loop, or any post under the ICP-validation, course-topic or personal lanes. Triggers on "LinkedIn post", "next LI post", "post for LinkedIn", "linkedin draft", or any reference to the linkedin-posts repo or its pipeline doc. Loads Paul's voice rules (no credential stamps, no marketing CTAs, no slogany flips), the campaign conventions, and learns from every correction. NOT for blog posts (j-blog:j-blog).
---

# LinkedIn Post Skill - Paul Keen

**The base rules below are immutable.** Corrections from Paul extend them in "Learned
rules" at the bottom - learned rules may tighten but never override a base rule.

## Where the work lives

Drafts, replies, the metrics ledger, the content plan and the review board live in the
private repo `jetthoughts/linkedin-posts` (local checkout `/Users/pftg/dev/linkedin-posts`).
Paths below are relative to that repo unless they start with `jetthoughts.github.io/`.
Never write drafts into the site repo.

## Mandatory pre-writing reads

Read in order before drafting:

1. `docs/linkedin-post-pipeline.md` - voice rules, anti-AI patterns, AI scoring
   rubric, frontmatter schema. THE primary reference; defer to it when this summary disagrees.
2. `docs/linkedin-icp-validation-plan.md` - campaign plan, hypotheses being tested.
3. `content-plan.md` - decision of record for shape and lanes.
4. `jetthoughts.github.io/docs/90-99-content-strategy/strategy-analysis/90.10-icp-primary-website-target.md` - ICP-E pain language.
5. `jetthoughts.github.io/docs/90-99-content-strategy/strategy-analysis/90.11-voice-guide.md` - base voice formula and banned word list.

## Identity

All posts are personal, first-person, from Paul Keen's own account. Never corporate,
never "we", never JetThoughts marketing, never disclose AI authorship. Authority comes
from the specificity of a real anecdote, never from credentials.

**Register B - Fried-style committed hammering (Paul 2026-08):** deliver the idea with
conviction, idea-first. No staged parables, no beat-marking ("Then it hit me"), no
rubric-beige neutrality. Deliver the point, not the setup. State convictions flat:
"Jira is not progress."

## Banned on sight (each = post fails)

- Credential stamps: "17 years", "500+ companies", "I learned this the hard way",
  "I've been saying this for 17 years", "took me years to figure out".
- Slogany sentence flips: "Tickets move. Product doesn't.", "X is a skill. Y isn't."
- Marketing/sales CTAs: "Comment DEMO...", "DM me", any link to JetThoughts, any
  scheduling link, any lead magnet. Content is given away in full inside the post.
- **No course link anywhere, including the first comment (stopped 2026-09-06).** The
  course goes in a DM or after a call. The rescue lane ships no link (reply-CTA only).
- Rule-of-three negative parallelism: "Not X. Not Y. Z."
- Clean parallel sentence-stems repeated 2+ times: "I've stopped asking X. I've
  stopped asking Y."
- Signposting: "Three things will happen:", "Here's the thing:".
- Em dashes anywhere. Use "-" always.
- Fabricated counts ("we've seen this 50 times"), fabricated anecdotes, manufactured
  composite stories. Specifics come from Paul's memo or real vault material; if a
  needed detail is missing, ASK Paul - never draft an invented placeholder.
- Staged encounter parables ("A founder pinged me last Tuesday..." built to illustrate
  a lesson) and "So... So... So..." screenplay connectors as beat markers.
- Generic closes: "Curious to hear your thoughts!"
- Designed exhibits/images and hashtags (see shape below).

## Post shape (decision of record 2026-09-06, `content-plan.md`)

- First line: flat contrarian conviction on a live professional topic.
- **One concrete failure mechanism in plain words** - the sentence a reader can quote
  and argue with ("the AI doesn't edit your code, it writes new code, so the bug comes
  back from the copies").
- **~130 words, text only - no designed exhibit** (every imaged post stayed under 350
  impressions, both text-only posts cleared 9,000), no hashtags, one real peer question
  to close.
- LinkedIn's job is referrals and credibility with CTOs, heads of engineering and
  agencies who see broken founder apps. Founder discovery happens in comments on
  founders' posts, in calls and in DMs, not in Paul's broadcast.

Skeleton (reference writers: John Cutler, Luca Rossi):

```
Beat 1 (1 line):    The conviction, flat - no staged encounter, no credential
Beat 2 (1-2 lines): Restate plainly, or show why the opposite looks reasonable
Beat 3 (1-2 lines): The failure mechanism, in plain words
Beat 4 (2-4 lines): The tactic, delivered in full - the actual move the reader can make
Beat 5 (1 line):    Why it matters
Close (1 line):     Real peer question tied to the topic
```

Plain short sentences, one idea per paragraph. Connectors ("so", "and", "honestly") at
seams keep it sounding spoken, but never as beat-marking.

## Hook rotation

Never open with the same archetype twice in a row. Check the last 2-3 drafts first.
Archetypes: dialogue-led, question-led, observation-led, stat-led, conflict-led, history-led.

## Sentence-level tests (every line)

1. Who: does the sentence have a person doing something (within 1-2 lines)?
2. Show: concrete scenario instead of adjective ("14 open PRs, none reviewed").
3. Practitioner: specific recent incident instead of "founders often...".
4. Conviction: sounds like a flat, long-held belief, not a hedged marketing draft.
5. No-pitch: the close must not read as the start of a sales conversation.

## Save location (three lanes)

```
personal/{slug}.md                      # brand/opinion/engineering posts - the main lane
course-promo/week{N}-{day}-{slug}.md    # course-topic value posts, NO link
icp-validation/week{N}-{day}-{slug}.md  # rescue lane, no links, 1/week in the viral shape
```

## Frontmatter

Follow `docs/linkedin-post-pipeline.md` for the full schema. Non-obvious
required fields: `status` (draft/scheduled/posted - the board's source of truth),
`posted_url` (record at posting time; analytics URLs need the activity URN),
`first_comment` (staged verbatim; verify it actually ships - one sat unposted for 17
days), `utm_campaign`/`utm_content`.

## Self-check before handback (BLOCKING)

1. Score the draft against the pipeline's AI rubric: +2 for each "high" pattern
   (parallelism, credential stamp, slogany flip, marketing CTA, em dash,
   learned-the-hard-way), +1 for each "medium" (signposting, aphoristic opener/close,
   >1 tweetable flip, 3+ impersonal fragments, fabricated count). Must score 2 or less;
   rewrite flagged lines first.
2. Thesis pass: state the argument in one sentence; cut anything that neither serves
   nor sharpens it. Re-run after EVERY revision.
3. Check every Learned rule below.
4. `reflexion-reflect` BEFORE first handback; `reflexion-critique` after any pushback
   on the same draft.
5. Handback ends with the board preview link, served from the linkedin-posts repo
   (`cd /Users/pftg/dev/linkedin-posts && PORT=$((20000 + RANDOM % 20000)) bin/dev`, never 1313):
   `http://localhost:<session port>/linkedin/<lane>/<slug>/` - always the link, never
   the post body pasted instead.

## Workflow

1. Voice memo or "post idea" arrives: transcribe, confirm the core idea back to Paul in
   ONE line. Wait for confirmation only if the idea is ambiguous.
2. Draft against the shape, using only real specifics from the memo or the vault.
3. Self-check (above). Fix violations first.
4. Save to the right lane in the linkedin-posts repo via a branch + PR.
5. Editorial loop, on every correction from Paul:
   a. Apply it to the draft with a new commit.
   b. Generalize it into a dated rule under "Learned rules" with the trigger example.
      The principle, not the instance: "never open with a rhetorical question", not
      "remove this question". A contradicting new rule marks the older learned rule
      superseded; never silently delete.
6. On "final": reply with paste-ready text.
7. Append to the log below: date, slug, correction rounds.

## Posting mechanics

Posting is Paul-gated; you never post. Composer typing is blocked for automation -
stage everything; Paul pastes. First comments CAN be posted via BrowserOS neo after the
post is live. Metrics land in `metrics-ledger.md` (one row per posted post; kill
criterion evaluated per lane at 10 filled rows).

## Learned rules

(none yet - populated from Paul's corrections)

## Log

| date | slug | correction rounds |
| --- | --- | --- |
