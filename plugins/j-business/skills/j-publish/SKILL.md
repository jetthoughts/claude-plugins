---
name: j-publish
description: "Say something in public and have it land — name and brand it, plan the content, write the post or article, strip the AI tells, and get it reviewed before it goes out. Use whenever the job is write a LinkedIn post, a blog article, a landing page, naming or brand voice, a content plan, SEO or AI-search visibility, social presence, or 'how do we talk about this'. Composes the branding, content, SEO and social skills and routes every outward draft through review and Paul's approval. Not for pricing or outreach to a named prospect — that is `j-offer`."
---

# j-publish

The entry point for *anything a stranger will read*. It exists because published text is the one output where being fluent and being wrong look identical, and because this vault's own rule is that nothing goes public without Paul's approval on the exact text.

**The gate, before any of the craft.** Public means an issue, comment, PR, gist, post or review on any site or repository, including ones Paul owns. Write the exact text to a file, run `gitleaks detect --no-git -s <dir> --no-banner`, read it for names, emails, tokens, absolute paths, company and customer ids, and paste the scan alongside the draft. **Agents and seats never hold the publish step.** (Paul, 2026-09-11, after a seat filed an upstream issue under his account.)

## Run it

**1 — Name what it is for.** Which reader, and what changes for them. A post with no reader is written to the author's own priors and reads like it.

**2 — Take the rung the job needs.**

| The job | Type this |
|---|---|
| Naming a thing, or brand voice and rules | `naming-and-branding` · `marketing-skills:brand-guidelines` · `marketing-skills:business-name-fit` |
| Deciding what to publish over a season | `content-strategy` — Pulizzi's content mission and editorial calendar |
| Writing a full piece end to end | `content-production` — brief, draft, SEO, readability, internal links · `blog-post` for structure · `blog-writing-guide` |
| Marketing copy that has to convert | `copywriting-core` · `marketing-skills:copywriting` · `positioning` when the claim itself is unsettled |
| A LinkedIn post in Paul's voice | `j-linkedin-post` — the house voice rules; do not hand-roll this |
| Engaging before contacting anyone | `j-linkedin-engage` — **not installed on this machine**, so do this by hand; never DM a target first |
| Social beyond LinkedIn, or what is trending | `social-content` · `marketing-skills:social-media-manager` · `content-trend-researcher` · `social-media-trends-research` |
| Being found — search and AI answers | `seo-audit` · `ai-seo` · `marketing-skills:schema-markup` · `geo-content-publisher` |
| A landing page that must convert | `landing-page-optimization` · `marketing-skills:page-cro` |

**3 — Strip the tells.** `humanizer` on any draft a model wrote; `slop-detector` when unsure. AI writing patterns are the fastest way for a reader to discount a claim that is otherwise true.

**4 — Cold eyes, always.** `content-cold-eyes` before calling any outward text done — it is the house instrument for exactly this. `cold-reviewer` when the piece makes a factual claim that a reader could check. A review returning "looks good" has failed and is re-run.

**5 — Verify inherited claims.** Any number, client name, result or quote carried over from an older artifact is re-verified against its source before it goes out again. This vault has shipped a stale claim more than once by copying a paragraph forward.

**6 — Hand to Paul.** The file, the scan, and one line saying what changed since the last version. He publishes.

## Failure modes

| Symptom | What it means | Do |
|---|---|---|
| A draft with a metric nobody sourced | inherited or invented | open the source or cut the number |
| "In today's fast-paced world" | the model wrote it, not you | `humanizer`, then read it aloud |
| A post that could have been written by any agency | no specific claim in it | cut until one claim remains that only we can make |
| An agent about to post, comment or open an issue | the publishing boundary | stop; draft to a file and hand it over |
| Voice drifts from earlier posts | the house rules were not loaded | `j-linkedin-post` owns the voice; load it |
