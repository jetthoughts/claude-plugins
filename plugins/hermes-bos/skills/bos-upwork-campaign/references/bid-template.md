# Bid template for the audit lane (evidence from the vault, 2026-10-17)

Use this for Next.js, Supabase and AI-built-app audit jobs. Write the letter by hand from this skeleton, run it through `humanizer`, and press Submit yourself. 75 to 120 words.

## Skeleton

```
[Line 1 only if the post demands a keyword or phrase: that phrase, alone.]

You wrote "[their exact phrase]". In apps built fast on [their stack], that usually points to [one specific suspect: row-level security rules, a webhook that fails silently, a secret in the client bundle].

I audit this: auth and tenant isolation, secrets, payments and webhooks, data, deploy, tests. You get a written report in 5 days, each area rated red, yellow or green with a cost per finding, then a 45-minute call. Fixed price, [amount]. I review every finding; an engineer from my agency writes any fixes. Proof: [link to the Catalog listing or the Crosslake portfolio item].

[One question about their app that only someone who read the post could ask.]
```

Fill every bracket from the post. Every number in the letter must have a canon row or a live Upwork page behind it; the 5 days, the six areas and the 45-minute call are the live Catalog listing. Do not add the Rails pull-request claim, "15 years", titles or the three R&D offices: the canon has no row for them.

## Why this shape (sources, all in the vault)

| Choice | Evidence | Source |
| --- | --- | --- |
| Open with their problem, not credentials | "Diagnosis-first opening" is the 2026 pitch doctrine; credential-first openers read as templates | `Projects/upwork-outreach.md`, 2026-08-26 refresh |
| Attach a proof link | 9% reply with proof of work, under 1% without | same |
| 75 to 120 words, one question | Doctrine says 75 to 100 words and one question; the Next.js campaign research allows up to 250 but also says one real technical question only | same; `evidence/perplexity/jetthoughts-marketing/pplx-260f1fb5-doc-upwork-next-js-campaign-for-jetthoughts-positioning-profile.md`, "Proposal templates" |
| Required keyword alone on line 1 | Postings that demand an opening keyword filter template bidders; real competition is a fraction of the shown count | same research, targeting rules |
| Fixed-price audit as the offer | Diagnostic sidesteps the rate comparison with a $30 an hour cohort; audit queue was thin (5 proposals on the best posting) | same research, "Pricing structure" |
| Bid in the first hours | Freshest posting had 50+ proposals within 2 hours | same research |
| Human edit before send | 74% of hiring managers spot AI-written applications, and Upwork detects AI proposals | `Projects/upwork-outreach.md` |
| Fewer, targeted bids | 8 to 12 targeted bids a week beat 30 sprayed ones | `2026-10-13-kimi-ee-dev-agency-launch-playbook/research/agency_dim04.md` |
| Video only on jobs over $2K | 87-second personalized video: 23.7% conversion when watched, 0.8% when not | agency_dim04.md, GetMany data |
| Boost rarely | Up to 24% more likely to be hired, a ceiling; only when the cost is under 2% of contract value | agency_dim04.md, Upwork placebo auctions |

## Limits of this evidence

- Reply-rate figures come from third-party samples (GigRadar, 133,872 proposals; GetMany video data), not from our own bids. Our own record is zero replies in 100 bids in 2026 (`Projects/upwork-outreach.md`), so treat every percentage as a hypothesis for the 30-day test.
- The Perplexity templates in the vault contain claims the canon now forbids. Use the skeleton above, not the old text.
- Measure per template: replies per 15 bids, per the campaign decision rule on 2026-11-17.

## Variant for outstaffing and build jobs (Paul, 2026-10-17)

For jobs that want a developer or a team, not an audit. Same length, same rules.

```
[Line 1 only if the post demands a keyword: that phrase, alone.]

You wrote "[their exact phrase]". [One sentence naming the specific risk they did not mention and will hit.]

The engineer for this job: [name or role, one project shipped on their stack with its outcome, link to a public artefact if one exists]. We confirm the engineer and start date before you commit. [One sentence of our own proof, only if it is true and sourced.]

Rate [X] an hour or [Y] fixed, available from [date]. I review the work and answer to you for it.

[One technical question that only someone who read the post would ask.]
```

Where it comes from, in order of weight:
1. Governing doctrine: `Projects/upwork-outreach.md`, pitch doctrine 2026 (diagnosis-first, proof link, 75 to 100 words, one question, human edit).
2. `evidence/perplexity/ai-harness-setup/pplx-e01720c3-doc-jetthoughts-upwork-operating-kit.md`, "Proposal recipe": buyer's constraint, one verified proof item, bounded next step, one question; confirm the delivery engineer before committing; no free plan.
3. `evidence/perplexity/jetthoughts-marketing/pplx-260f1fb5-doc-upwork-for-outstaffing-what-actually-sells-and-how-to-win-th.md`, "Proposal template, senior full-stack": the first two lines decide, so no preamble and no credentials; name a risk they did not mention; link one real artefact. It asks for two questions and a rate and overlap line; we keep one question to stay inside the word limit.

Not used: the three templates in `pplx-260f1fb5-doc-upwork-next-js-campaign-for-jetthoughts-positioning-profile.md` (250 words, and they carry claims the canon forbids) and `Notes/upwork-1a-extended-formula.md` (superseded 2026-08-26).
