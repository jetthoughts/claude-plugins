---
name: lightning-demos
description: Run a Lightning Demos round (the Design Sprint step from Knapp's Sprint, as AJ&Smart runs it) — a timed research-and-show-and-tell that harvests one transferable mechanism from each of several real products, deliberately from outside your own industry, and leaves a board of ten to twenty big ideas to design from. Use this whenever someone needs inspiration before designing anything and would otherwise invent from scratch — "how do others solve this", "find examples", "we need fresh ideas", "what's out there", "look at comparables", "steal from other industries", "related worlds", before a solution sketch or concept round, or as the ideation step of a design sprint. Reach for it especially when a first idea already exists and everyone is anchored on it. Domain-agnostic; run it standalone or inside a sprint.
---

# Lightning Demos

A timed round where each person researches real products that already solve a *similar* problem — usually in a different industry — and shows the team the one part worth stealing. It ends with a board of ten to twenty big ideas that the next exercise designs from.

**Why it works.** Ideas that spark the best solutions come from similar problems in different environments. Three examples from your own industry produce three versions of what you already do. The exercise is also the cheapest anchoring cure there is: a room that has just seen fifteen real mechanisms stops arguing about the first one someone proposed.

It is *"a fun way to ignite creativity"* and runs perfectly well **standalone** — it does not need a sprint around it.

## The round

| # | Step | Time | What happens |
|---|---|---|---|
| 1 | **Frame** | 2 min | Restate the problem in one line. Everyone searches against *that*, not against a vague topic |
| 2 | **Research** | 20–30 min | Each person finds **1–3** products, apps, services or companies solving a similar challenge. **Silent, individual, online.** Not restricted to your industry |
| 3 | **Note** | during | Per example: the **name**, the **big idea**, the key takeaway |
| 4 | **Show and tell** | 3–5 min each | Present your favourites and say **why the idea works**. Use a timer |
| 5 | **Capture** | during | One person captures each big idea on the shared board |
| 6 | **Digest** | 5 min | Read the whole board before moving on. This is where the next round's ideas come from |

**Always use a timer.** People waffle when presenting, especially with a lot to get through — cap it at three big ideas in three minutes.

## The capture format

Headline above · the inspiring **component** sketched or screenshotted · the **source** underneath.

**Capture the component, never the product.** And keep the headline short enough to scan:

> **Good:** "Netflix's randomised video suggestion"
> **Bad:** "Netflix's revolving menu of suggestions, and a button that randomises the selection based on previous videos liked"

The detail is what the presenter says out loud. The board holds the idea.

## The three rules that do the work

**Don't decide and don't debate — capture anything that might be useful.** Judgment during the round kills the examples that only *look* irrelevant, which are the ones worth having. Sorting happens afterwards.

**Steal one mechanism, never the model.** "They do X plus AI, so we should do X plus AI" copies their team, their brand and their customers, none of which transfer. Take the specific behaviour.

**Reject the obvious ones.** *"It's easy for people to choose the easy ones, 'Apple' or 'Amazon'. We encourage going deeper and beyond."* The famous handful are famous *because* everyone already knows them, which is exactly why they carry no information.

**And do not limit the medium.** An idea doesn't have to be visual — a concept, something you heard, a policy, a pricing move, something your own team is working on all count. Write it down and put it on the board.

## Running it with agents

Everything above assumes people in a room. Four things change when the contributors are agents, and each fixes a failure this exercise is otherwise wide open to.

**A fetched URL, or it didn't happen.** A model will produce plausible, well-described, entirely remembered examples on request — that is a prior wearing a demo's clothes, and it is indistinguishable from research in the output. **Require at least three examples carrying a URL fetched during this run.** No new fetches, no round.

**One assigned domain per contributor.** Agents given the same brief return the same three examples, because they are sampling the same distribution. Naming a different industry for each — logistics, healthcare, gaming, aviation, hospitality, a regulated field — is what actually produces different big ideas. Same brief, same output; different corpus, different output.

**Shape the domains like the question.** An org-design question needs org demos, a pricing question needs pricing demos, an onboarding question needs onboarding demos. This matters more than it sounds: **the concept space inherits the demo domains.** Demo safety engineering and every concept comes back a monitoring primitive — each step passes its own check while the whole round answers a question nobody asked.

**Open it and look at it.** A description of an interface is not the interface, and the transferable part usually lives in what the thing *does* at the decisive moment. Where reviews exist, skim them: a slick interface with three one-star reviews describing the same failure is a different lesson from a slick interface that works.

Start with the cheapest tool that answers the question and escalate only on failure: **`WebFetch`** for the page's text and claims · `mcp__parallel__web_fetch` or `lightpanda` when it 403s or the content is JS-rendered · an external driver (`agent-browser`, `browser-use`, `Interceptor`, `remote-browser`, `playwright`) when you need to *use* the thing rather than read it · `chrome-devtools` `take_screenshot` or `screenshot` when you need to see it, and then actually read the image rather than reasoning from alt text · `BrightData` / `Apify` / `just-scrape` for a site that resists. **`claude-in-chrome` is not for this** — it drives the user's own logged-in browser and is reserved for the Perplexity research seat.

The homework tip transfers too. Human facilitators prefer participants research the night before, because 25 minutes is thin if you haven't thought about the problem. With agents the equivalent is a **pre-brief**: hand each lane the problem statement and its assigned domain before it starts searching, so its budget goes on looking rather than on orienting.

## What this is not

**It is not competitor research.** You are looking for a *mechanism* in a *different* context, not a feature matrix of your rivals. If everything on the board is a direct competitor, the round did not happen — re-run it with domains assigned.

**It is not a decision.** The output is a board, not a shortlist. Ranking, voting and choosing belong to whatever comes next — `ldj` for a fast prioritisation, `deliberate` when the answer has to survive being attacked.

**It does not settle a question of fact.** Demos are inspiration. If the disagreement is about what is *true*, you need evidence, not examples.

## Output

```
Big idea:        (the headline — short enough to scan)
The component:   (the specific mechanism, not the whole product)
Seen at:         (source, with a link)
From:            (which domain — must not be ours)
Why it transfers:
Why it might not:
```

Ten to twenty of these on one board, then a pause to read them all.

## Sources

Originator: Jake Knapp, *Sprint* (2016), the Tuesday "Lightning Demos" step — not fetched here, so the timings above rest on the two write-ups below (secondary, verified earlier). AJ&Smart's public LDJ page (retrieved 2026-09-13) does not cover Lightning Demos.

[SessionLab — Lightning Demos](https://www.sessionlab.com/methods/lightning-demos) · [Alvin Hermanto — Lightning Demo](https://alvinhermanto.medium.com/lightning-demo-a-fast-way-to-ignite-inspiration-in-a-design-sprint-10f6f751897f) (2021) · [Design Thinking Toolkit — Lightning Demos aka Related Worlds](https://designthinkingtoolkit.co/content/lightning-demos-aka-related-worlds). Originates with GV's Design Sprint (Knapp, Zeratsky & Kowitz).
