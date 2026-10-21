---
name: blog-next
description: >
  Decide WHAT to write next and whether it is worth writing - by auditing the
  content plan against live search data, rebuilding the plan when it fails the
  audit, researching primary sources, and gating an outline. This is the
  find-the-topic half of the pipeline; it never writes a post. Use whenever the
  user asks what blog post to write next, for the next post, a new post, a batch
  of posts, or a blog sprint; when they point at the content-plan queue; when
  they ask to groom, restock, rebuild or sanity-check the content plan; and when
  they name a topic themselves, because the premise audit is what catches a
  decayed row or a dedup collision before anyone spends a draft.
  NOT for LinkedIn posts (use j-linkedin-post:j-linkedin-post), course chapters (see
  docs/projects/2605-tech-for-non-technical-founders/60-69-policies/),
  landing/services pages (page-cro, landing-page-optimization), or revising a
  draft that already exists - that is blog-post-coordinator's job.
---

# Blog: what to write, and whether to write it

> **Run from the `jetthoughts.github.io` checkout.** Every path in this skill (`content/blog/`, `bin/`, `test/`, `.okf/`, `docs/`) is relative to that repo's root. LinkedIn drafts live in the separate `jetthoughts/linkedin-posts` repo (local `/Users/pftg/dev/linkedin-posts`) and belong to `j-linkedin-post:j-linkedin-post`.

Two halves, deliberately split. **You own "what and whether."** Drafting,
reviewing and shipping are the other half and belong to the agents below.

| Stage | Owner |
|---|---|
| A. Plan health + pick, or REBUILD the plan | **this skill** |
| B. Research | **this skill** |
| C. Outline + outline gate | **this skill** |
| Draft → 3 critics → cold-eyes → ship gates → commit | **`j-blog:blog-write` skill** |
| N-post sprint, cluster sweep, one PR, CI watch | `blog-batch-orchestrator` |

**If the user wanted a POST and you return a verdict, say so in one line and
name `j-blog:blog-write`.** This skill deciding not to write is a legitimate outcome,
but it is not what someone asking for a post expects, and leaving them to infer
the second half exists is how they end up thinking the pipeline is broken.

You produce one of three things, never a draft: a **topic row**, a **rebuilt
plan section**, or a **HOLD** saying the slot should not be spent.

**Read before starting; this skill does not copy them, so a correction lands
everywhere:**

- `docs/workflows/blog-pipeline.md` - canonical process. STEP 1-3 is Stages A-B.
- `.okf/workflows/analytics-access.md` - properties and every measurement trap.
  Stage A is unsafe without it.
- `docs/projects/2510-seo-content-strategy/20-29-strategy/20.09-content-plan-revision-aug-2026.md`
  - §13 is the live queue (§12 retired). §13a/§13d record the traps, including
  the ones that killed rows in this same file.

## The calendar - only when asked

**Pick topics on merit. Do not let the calendar veto a good one.** Spacing is a
scheduling question, and scheduling is `j-blog:blog-write`'s job when it sets `date:`.

Run this only when the request is about timing - "what should we publish next
week", "are we posting too often", or when you need a date for a SCHEDULED exit:

```sh
# `.?` in the old version of this ate the first digit, so 2026 posts came out
# as "026-..." and sorted below 2025 - the whole current year vanished from the
# top. 19 legacy posts carry only created_at, hence the alternation.
for f in content/blog/*/index.md; do
  d=$(grep -m1 -E '^(date|created_at):' "$f" \
      | sed -E "s/^[a-z_]+: *['\"]?([0-9-]+).*/\1/")
  echo "$d $(dirname $f | sed 's|content/blog/||')"
done | sort -r | head -25
```

Capacity is ~6/month across three streams (`20.09`). Three posts on one day
compete for the same reader and collapse into one impression of the blog, so
when a date IS being chosen, spread them.

## Stage A - find candidates, then audit them

**Search demand cannot generate topics on this property; it can only veto them.**
Two audits in Aug 2026 falsified the queue's own lead item, and the reason was
structural: the blog earns ~0.69 named non-brand clicks/day and the ICP is
absent from the query data (`vibe*` ≈ 200 impressions / 0 clicks). A
search-driven queue here returns HOLD forever. So generate candidates from the
three sources below, then use search to kill the bad ones.

### A1 - generate candidates (do this FIRST, before touching GSC)

1. **Live trend research.** What is the audience arguing about right now? The
   HN Algolia API is free and needs no auth:
   ```
   curl -s "https://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i%3E<epoch>,points%3E200&hitsPerPage=50"
   ```
   (compute `<epoch>` separately - inlining `$(date ...)` in the URL mangles it).
   Then `?query=<title>` to recover each story's real URL and HN id for citation.
   **Look for a cluster, not a single story.** One hot post is noise; five
   front-page posts arguing the same thing in three weeks is a conversation the
   audience is already having, and a post that enters it has a reason to exist
   that search data can never supply.
2. **Paul's raw material**, when he supplies it - one sentence about something
   that happened is a topic ("the agents cancelled half their backlog"). Treat
   this as the highest-value source when present; he may not always have it.
3. **Reddit** - where practitioners complain in their own words, which is the
   phrasing a search-purposed post needs. **The `.json` endpoint is BLOCKED**
   from this host - `reddit.com/r/<sub>/top.json` returns HTTP 403 with an HTML
   block page and `old.reddit.com` returns a 302 (both verified 2026-08-22).
   Do not put that curl in a script. Use `WebSearch` instead, which surfaces
   `old.reddit.com` threads WITH their comment text:
   ```
   web_search(search_queries=["reddit r/rails discussion this week",
                              "reddit ExperiencedDevs <topic> complaint"])
   ```
   Worth sweeping: `r/rails`, `r/ruby`, `r/laravel`, `r/webdev`,
   `r/ExperiencedDevs`, `r/LocalLLaMA`, `r/devops`. Read the COMMENTS, not the
   title - the top comment on a complaint thread is usually the real topic, and
   a thread with 200 comments and no accepted answer is an unwritten post.
   Quote the practitioner phrasing verbatim into the topic row; it is the one
   thing this source has that HN and our own work do not.
4. **X/Twitter** - no free API. Use `WebSearch` scoped to the site, or read the
   accounts that set the agenda for our stacks via `WebFetch` on nitter-style
   mirrors when reachable. If neither works, say so and lean on the other four
   sources rather than inventing a trend.
5. **Changelogs and release notes as a trend source** - a framework's own
   release is a dated, citable event with a built-in audience: Rails/Ruby
   releases, Laravel releases, and the security advisories for both. This is
   the highest-signal source for the under-covered stacks in A1.6.
6. **Under-covered stacks that already rank** - the cheapest expansion
   available. Measured 2026-08-22 across 620 posts: `rails` 114, `ruby` 100,
   `css` 16, `llm` 13, `react` 12 - against `postgres` 3, `laravel` 3,
   `tailwind` 2, `python` 2. **Thin does not mean unwanted.** The highest-
   impression uncited guide on the property is Laravel (19,841) and
   `langchain-python-tutorial` earns the best CTR of any high-impression page
   (15 clicks / 7,329). A fourth Rails post is the most expensive option on the
   board; a Laravel or Python one is the cheapest.
7. **Our real work** - this repo and `~/dev/elital`. The 2026-08-20 batch's best
   material was a commit-documented outage. Sanitize: shapes and lessons yes;
   prompts, model IDs, proprietary numbers no.

A candidate is only worth writing when an external hook meets first-hand
evidence. A hot topic we have nothing to say about is somebody else's post -
the cheap test: could the post be written entirely from the first five search
results?

### A2 - audit the candidates (search as veto, never as source)

1. **Pull live GSC/GA4** per `analytics-access.md`. Never query from memory of
   property IDs.
2. **Run every trap against your own numbers before quoting them** - the
   named-vs-page test (one-way: `named ≪ page` voids the page CTR; the converse
   licenses nothing), truncation, Trap C (page-level *position* is an artifact
   whenever the CTR is), Trap D (query-vs-query is the legitimate level;
   page-vs-page carries almost no signal).
3. **Are these impressions human?** Before treating volume as demand, look at the
   query strings. Combinatorial permutations of one stem, non-words, or 100+
   impressions at top-10 positions with a flat zero on clicks mean synthetic
   traffic, not demand you are failing to convert. `analytics-access.md` carries
   the tell and two worked examples.
4. **Name the post's job, then apply the matching floor.** A post is written to
   rank, or to be a credible asset for a reader who already arrived from LinkedIn
   or a conversation. These are judged differently and conflating them is how the
   queue filled with rows nobody should have written.
   - **Search-purposed:** convert to clicks/day against the blog's non-brand rate
     (§13c: 62 named non-brand clicks / 90 days ≈ 0.69/day). Compute the ceiling -
     best-case position at a defensible CTR, minus what the topic already earns,
     minus cannibalisation. **A search post whose ceiling cannot move the number
     is not a post.** Say so and stop.
   - **Arrival-purposed:** the search floor does not apply and quoting it is a
     category error. The test is whether the piece would survive a sceptical
     founder reading it after a LinkedIn click - does it say something true that
     the competition does not, backed by work we actually did. Most trend-driven
     candidates are this kind. Say which kind it is in the topic row, so nobody
     later kills a good asset with the wrong metric.
5. **Dedup** per `blog-pipeline.md` STEP 1/3b. A filename grep is not a coverage
   audit - regexes are order-dependent and miss real pages. Confirm each hit and
   check whether two of our pages already split the query.
6. **Reconcile with §13.** N1 is a downgraded hypothesis, not a win.
7. **P0 gate** (20.09 §1): if outreach is stalled, content halts. Read the plan's
   own log - Paul overrode it 2026-08-20, scoped to one post - and report the
   gate's state plus his last call rather than halting on the rule alone.

**Overriding the queue:** only on *falsifiable* grounds - a dedup collision, a
dead page, a premise the numbers contradict. Record the verdict and the number
that killed it. Ordering *preference* is Paul's: flag it, take his row.

### When the audit kills the row - rebuild, do not dead-end

If the row fails, or the queue is dry, or the survivors all fail the demand
floor, **the deliverable becomes a rebuilt plan section**, not a shrug. Write it
into 20.09 as a new dated subsection. Each candidate carries:

- the live figure it rests on, with its pull date, window and property
- which traps were run against it, and what they returned
- the demand ceiling in clicks/day and what it is being compared to
- the dedup result, naming any page that already owns the query
- a verdict: WRITE / UPGRADE / FLAG / DO-NOT-WRITE, with the reason

Record DO-NOT-WRITE rows too, with their numbers. A row nobody logged gets
re-proposed from intuition next quarter.

**When live data cannot settle it, name the cheap experiment** instead of
guessing - a date/device split, a look at the live SERP for what sits above us,
a title test with a measurable before/after. Fifteen minutes of checking beats
a spent content slot.

**Gate Stage A before quoting it.** Its output is nothing but measurements, and
CLAUDE.md requires a measurement verified before it is reported. Hand a
`core-reviewer` the raw pulls and the row you propose - goal and artifact, never
your conclusion - and ask it to re-derive. Both Aug 2026 runs had a material
error caught here and nowhere earlier.

Stage A output: a topic row (slug, angle, live figures, demand ceiling, dedup,
reviewer verdict), a rebuilt plan section, or a HOLD.

## Stage B - research primary sources

**Fetch sources; do not recall them.** Training memory is not a citation.

**Start the slow one first.** NotebookLM deep research takes ~5 minutes and runs
server-side, so `research_start` it BEFORE the web searches and collect it at the
end. Running them in sequence wastes the whole five minutes; running them in
parallel makes the deep sweep free. This is the default, not an optimisation.

1. **NotebookLM deep research - fire this FIRST** (`notebooklm-mcp`). It searches
   the open web and returns ~40 sources with a synthesised report, which is a
   different instrument from `web_search`: it goes wider and returns things a
   3-6 word query never surfaces.

   ```
   server_info()                      # gate - see auth below
   research_start(query=..., mode="deep", title=..., source="web")
   #   mode: "fast" ~30s / ~10 sources · "deep" ~5min / ~40 sources, web only
   # ... do the web searches and the code mining while this runs ...
   research_status(notebook_id=..., task_id=..., max_wait=600)
   research_import(notebook_id=..., task_id=..., cited_only=True)
   notebook_query(notebook_id=..., ...)
   ```

   **`research_import` is not optional** - without it the sources are discovered
   but never enter the notebook, and `notebook_query` then answers from nothing.
   Prefer `cited_only=True`: the report's own citations are the sources that
   earned their place, and importing all 40 buries them.

   **Auth gate.** Check `server_info` first and read `auth_status` precisely:
   `configured` go · `not_configured` first-time setup · `stale` means expired,
   ask the user to run `nlm login` · `unverified` means THE CHECK failed, not the
   credentials - try the call anyway rather than sending them to re-auth.

### NotebookLM also makes VISUALS, not just text

`studio_create` builds artifacts from the notebook's sources and
`download_artifact` saves them. Verified signatures 2026-08-23:

```
studio_create(notebook_id=..., artifact_type="infographic",
              infographic_style=..., orientation="landscape")
studio_status(notebook_id=...)                 # poll until complete
download_artifact(notebook_id=..., artifact_type="infographic",
                  output_path="content/blog/<slug>/figure.png")
```

Types: `infographic` (PNG) · `mind_map` (JSON) · `slide_deck` (PDF/PPTX) ·
`data_table` (CSV) · `report` · `audio` · `video` · `flashcards` · `quiz`.
Poll `studio_status` after creating - generation is asynchronous.

**Where these earn their place:**

- `mind_map` BEFORE outlining. It shows how the sources cluster, which is the
  fastest way to see that your six planned H2s are really three.
- `data_table` to pull every number the sources state into one CSV, so the
  claim-verification pass has a checklist instead of a memory.
- `infographic` as a STRUCTURE draft - what a diagram of this argument wants to
  contain - not as the shipped asset.

**Two limits, and both matter.**

A generated infographic does not use the house palette
(`#0e0e14` ground, ruby `#cc342d`, purple `#a855f7`, labels INSIDE the diagram)
and will not match `.stitch/design.md`. Shipped covers and in-post figures are
still hand-built SVG exported to PNG with `rsvg-convert`, which is also what the
standing rule requires: the PNG is the artifact, not the source.

And the numbers inside a generated visual are **generated**. They carry exactly
the same burden as prose and are harder to notice, because a chart reads as a
measurement rather than as a sentence. Verify every figure in a generated visual
at its primary before shipping it, or do not ship it.

2. **To interrogate sources you already have** (rather than find new ones):
   `notebook_create` → `source_add` (`source_type: "url"`, `urls` takes a list)
   → `notebook_query`.

3. **Web search** per `blog-pipeline.md` STEP 3 - official docs, release notes,
   primary reports. This is Stage B's job; the coordinator starts at the writer
   and never re-runs research.

**A NotebookLM report is a LEAD, never a citation.** It is a synthesis over
sources it chose, and the same rule that governs a `web_search` excerpt governs
it: open the primary and quote from there. On 2026-08-22 two figures reached a
topic row through search excerpts - GitHub's "more than one in five code reviews"
and an ISSRE study's findings - and BOTH had to be re-fetched at source before
they could be written down. One of them, the study, turned out to say something
more interesting than the summary implied.
4. Ask what a draft needs: what changed and when, the official position, where
   practitioners disagree, the strongest counter-argument. Not "summarize this."
5. **Mine our real code** (this repo, `~/dev/elital`) for first-hand material.
   Sanitize: shapes and lessons yes; prompts, model IDs, proprietary numbers no.
6. Verify every statistic against its source - **and every mechanism too.** How
   a tool behaves is a claim, not context; it just reads as reasoning, so it
   gets waved through where a number would be challenged. Fetch the README or
   the release notes. Zero fabricated clients, stats,
   quotes or personas - `.okf/content/claims-canon.md` records "Sarah" as banned.
7. Internal links per `blog-pipeline.md` STEP 3b.

Stage B output: a sourced digest, one entry per claim: the claim, the primary
URL, the **exact supporting excerpt copied from the source**, and any caveat
the source itself states. The claim-verification lens diffs the draft's
sentence against the excerpt, not against memory of the source. Record what
the excerpt licenses, not just what it says: a study **demonstrates**, a
vendor **reports**, a correlation **suggests**, a projection **may** -
matching the verb to the evidence is accuracy, not hedging; the voice guide's
"never hedge" rule governs opinions, not sources. A claim whose excerpt you
cannot paste is a claim you have not verified.

## Stage C - outline, then gate it

Write the outline: hook shape, H2 sequence, what the reader does differently
after each section, where internal links land, the CTA.

**The outline carries a thesis, and the thesis must be falsifiable.** One
sentence a competent reader could disagree with. Before gating, answer four
questions in the outline itself:

- What flawed default does this correct, and who actually holds it? No named
  population, no thesis - §3's attribution test, applied to the post instead
  of the sentence.
- Would the counterargument's holder sign your statement of it?
- Where does the advice stop applying? These boundary conditions feed the
  "When NOT to" section blog-pipeline STEP 4 already requires.
- What will the post NOT cover? One line, so scope creep is visible at review.

"Testing matters" cannot be false in any situation - that is a topic, not an
argument; send it back to Stage A.

Apply `blog-pipeline.md`'s cut test here, where a cut costs a line instead of a
section. Pick a cadence anchor and hook shape from
`docs/workflows/blog-writer-reference-samples.md`, checked against recent
siblings so the post does not repeat an overused shape - that file and STEP 4b
own the current count.

**Gate it: author ≠ verifier.** A different agent type than whoever wrote the
outline - `core-reviewer`. Brief it with goal and artifact, never your
conclusions; ask for measurements. A panel handed your inference returns it
wearing independent confidence.

An outline that fails is rewritten before any prose exists.

## Hand off - and keep going

**Default is unattended.** A gated outline is not a place to stop and wait; hand
it straight on and let the gates decide. Paul asked for delivery without a human
in the loop (2026-08-22), and the stop list below is the whole of what he still
owns.

**One post** → **INVOKE the `j-blog:blog-write` skill NOW.** Not "recommend it", not
"name it in the handback" - call it, in this same run, via the Skill tool:

```
Skill(skill="j-blog:blog-write", args="<slug> - topic row 20.09 §<N>, premise audited: yes")
```

Pass the topic row, the research digest, the approved outline, and
`premise audited: yes`. That skill owns STEP 4 onward and delegates to
`blog-post-coordinator` when agent spawning is available.

**Ending a run by telling the user to run `/j-blog:blog-write` themselves is a FAILED
run, not a handback** (Paul 2026-08-23). Someone who asked for a post and
received a topic row reasonably concludes the pipeline is broken. The ONLY
reasons not to invoke it are the exits below - HOLD, SCHEDULED-and-parked, or
BLOCKED - and each needs its evidence. "The outline gate could not run" is not
one of them: say so and invoke anyway, because `j-blog:blog-write` runs its own gates
and a stated gap is worth more than a stalled pipeline.

**Several posts** → `blog-batch-orchestrator` with N; it runs Stages A-C per row.

Session dev server, once, never 1313: `PORT=$((20000 + RANDOM % 20000)) bin/dev`.

Pass `model` explicitly on every spawn. Both agents declare `model: fable`; if a
fable spawn fails, fall back to `opus` and say you did.

Full unattended contract, including the completion promise and why it must be
about gates rather than quality: `docs/workflows/autonomous-delivery-prompt.md`
§"Running CONTENT unattended".

## Four exits, and only four

A run ends in exactly one of these. **Two exits are not enough** - a loop whose
only outcomes are "shipped" or "try again" will always ship something. But
three were not enough either: with only SHIP / HOLD / BLOCKED, a good topic that
merely collides with this week's calendar gets recorded as DO-NOT-WRITE and is
lost. That happened on 2026-08-22 and Paul corrected it - **a spacing conflict
is a scheduling decision, not a verdict on the topic.**

- **SHIPPED** - gates green, committed, PR open, verdicts quoted.
- **SCHEDULED** - the topic is good and the slot is not. Hand it to
  `j-blog:blog-write` NOW with an explicit future `date:` in the frontmatter; a
  future-dated post is normal scheduling, and production skips future content
  until the date arrives (`bin/hugo-build` builds it, `rake test:links` does
  not). Pre-writing is the point: the research is hot today and cold in a
  fortnight. Pick the date by running the calendar snippet above - the next gap of >=3
  days. Record the date and the reason for it in the topic row.
  **Use this whenever the only objection is "we just published something like
  this"** - that is exactly the case it exists for.
- **HOLD, with evidence** - a terminal success, not a failure. Every candidate
  failed its floor, or the queue is dry after rescopes. Record the numbers that
  killed each one so nobody re-proposes them from intuition next quarter. Never
  invent a topic to fill the slot; on 2026-08-22 two runs correctly ended here.
- **BLOCKED on a named decision** - one of the five below, named explicitly, with
  the conservative option already taken meanwhile where one exists.

**What genuinely needs Paul** (everything else: decide, record, continue):
whether a claimed client engagement or number is real · publishing outward ·
overriding a documented gate · pricing/naming/internal numbers · split and
irreversible calls. A figure you cannot source is not a decision for him - drop
the claim.
