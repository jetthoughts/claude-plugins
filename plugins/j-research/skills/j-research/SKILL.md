---
name: j-research
description: The front door for any open-web research request in this vault. Use whenever the user says "research", "look into", "find out about", "dig into", "get me up to speed on", "give me research options", "start a research on", or names a topic and asks what tools/sources to use — before reaching for a specific tool (wigolo, j-perplexica-search, j-deep-research, Council, Research, research-deep, RivalSearchMCP, NotebookLM, Perplexity, brave-search, searxng, exa, OmniRoute web/x search) directly, since this vault has a dozen overlapping research tools and picking the wrong one wastes a round trip. Picks between three shapes — a quick cited answer, a multi-perspective discussion, or a menu of deeper options — and hands off to the tool built for that shape. NOT FOR searching this vault's own notes (use qmd), code in a repo (use semble/tokensave), a question a NotebookLM notebook already answers (query it directly), or a single already-known URL (use wigolo fetch directly).
---

# Research — entry point

This vault has more research tools than any one request needs: `wigolo` (local-first, the CLAUDE.md
default), `j-perplexica-search` / `j-deep-research` (the older local Perplexica/SearXNG/LDR stack),
`Council` / `deliberate` (multi-agent discussion), `Research` / `research-deep` (marketplace,
heavyweight), `RivalSearchMCP`, and NotebookLM for corpus-grounded questions. Guessing among them
per request is how a fast lookup ends up running a 90-second multi-agent investigation, or a topic
that needs three viewpoints gets one cited paragraph. This skill is the dispatcher: name the topic
once, pick the shape, hand off.

**Not a new research engine.** Every mode below routes to a tool that already exists — this skill
never does the searching itself.

## Step -1 — a marketplace router already owns some verticals

`claude-code-skills:cs-research` (`/cs:research`) is a second "research entry point" installed
in this account. It doesn't know about wigolo, NotebookLM, or Council — its job is routing to
six **output-shape specialists**: literature review (PICO/systematic), patent/prior-art, grants,
a due-diligence dossier, a course syllabus, or a social-sentiment pulse. If the topic is genuinely
one of those shapes, prefer its specialist (or this vault's own equivalent — `company-research`
for dossier-shaped asks, `social-media-trends-research` for pulse-shaped ones) over anything
below. Everything else — a plain open-web question with no fixed output shape — is this skill's
job, because it's the one that knows this vault's actual tool stack.

## Step 0 — is this actually open-web research?

- About this vault's own notes → `qmd query`/`qmd vsearch`, not this skill.
- About code in a repo → `semble`/`tokensave`.
- About a Drive project or a corpus already loaded into a NotebookLM notebook → query that notebook
  directly ([[notebooklm-corpora]] names which one).
- A single URL the user already has → `wigolo fetch` directly, no mode needed.

Only proceed past here for a genuinely open-web question with no fixed source.

## Step 1 — pick the shape

If the user's wording already picks one ("quick", "just look it up", "get different views",
"deep dive", "give me the options"), skip straight to it. Otherwise ask, with `AskUserQuestion`
when available, else a short numbered menu:

| Shape | When | Route |
|---|---|---|
| **Simple** | One focused question, one answer will do | `wigolo search`/`wigolo fetch` (cache first) → `j-perplexica-search` → keyed/cloud tier (`brave-search`, `searxng`, `exa`) only if both local ones are down, and say so out loud. |
| **Discussion** | The topic has real disagreement, or the ask is "what do people/experts think", "weigh the options", "get different views" | `Council` (QUICK mode by default, DEBATE for a harder split). If the output must end in one call with a kill criterion, not just viewpoints, escalate to `deliberate` instead. |
| **Other options** | The user wants to see the menu, or none of the above fits (need a full report, need explainable per-source scoring, need a private/paid API tradeoff spelled out) | See the table below — present it, let them pick. |

### Other options — the menu

| Tool | Pick it when |
|---|---|
| `j-deep-research` | One search answer was too thin; want a multi-source cited summary, still free/local, escalates cheapest-first (Perplexica → SearXNG → LDR). |
| `wigolo research` / `wigolo agent` | Need a structured, schema-shaped result pulled across many pages (a table, a comparison, an extraction), not prose. |
| `RivalSearchMCP research_topic` / `web_search` | Want per-result quality scoring and an explicit confidence signal (high/medium/low) rather than a synthesized answer. |
| `Research` skill (marketplace, 4 depth modes) | The topic genuinely needs iterative, multi-session investigation with its own persistent vault — heaviest option here. It fires an unrelated voice-notification `curl` to `localhost:31337` on invocation (harmless no-op if nothing's listening) — that's the tool's own baggage, not this skill's. |
| Perplexity, Search or Deep Research mode, via browser | Paul specifically wants a Perplexity thread (e.g. to capture into `evidence/perplexity/`). **Never Computer/orchestrator mode** for a new research task — that rule is load-bearing, not this skill's call to relax. |
| `mcp__brave-search__brave_web_search` / `brave_local_search` | Keyed cloud fallback when wigolo/perplexica are down or rate-limited; `brave_local_search` specifically for real-world places/businesses, not web pages. |
| `mcp__searxng__searxng_web_search` | Raw URLs fast (0.8s), no synthesis — when you want the link list yourself, not an answer. |
| `mcp__exa__web_search_exa` | Semantic/similarity search reads better than keyword search (e.g. "articles like this one"). |
| `mcp__omniroute__omniroute_web_search` / `omniroute_x_search` | Already routed through the OmniRoute gateway you're using for models — `x_search` specifically for X/Twitter. |

## Step 2 — after the tool answers

Keep whatever confidence/citation tagging the underlying tool already produces (wigolo's
`evidence_score`/`confidence`, Council's dissent, Research's `[HIGH]/[MED]/[LOW]`) — don't strip it
out when relaying the answer.

## Step 3 — offer to keep it (only if asked)

Nothing here auto-saves. If the user wants the result kept, write it as a normal captured-research
note (`type: Research`, `source`, `url`, `content_hash`) in the path the source implies — a
Perplexity capture goes through the existing `j-perplexity-sync`/`j-triage` pipeline, an ad
hoc synthesis goes in `evidence/research/`. Don't file it unasked.
