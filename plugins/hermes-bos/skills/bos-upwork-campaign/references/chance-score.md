# Upwork chance score: will this client hire anyone, and could it be us?

Most bids are lost to jobs that never hire, not to scams. Of 617,336 resolved postings, 43.9%
hired someone. Chronic non-hirers (5 or more posts, zero hires) are 1.2% of volume. 99.1% of those
non-hirers show "payment verified", so that badge alone filters almost nothing.
(Sources: vault `evidence/perplexity/jetthoughts-marketing/pplx-6de7584b-most-of-the-upwork-project-8-from-10-are-scams-ass.md`
and `pplx-260f1fb5-doc-upwork-as-an-outstaffing-fixed-price-channel-for-jetthoughts.md` §5.3, which cite
the GigRadar 133,872-proposal dataset, the Upwork hire-rate help page and the Connects refund rules.
Base Connects are not refunded when a job expires unfilled.)

## Reject outright (low-chance gates)

Any one ends the job. Write the gate name as the reason.

| Gate | Rule |
|---|---|
| chronic-non-hirer | 5 or more jobs posted and 0 hires |
| low-hire-rate | Hire rate under 50% with 3 or more jobs posted |
| free-estimate | The post asks for a full estimate, architecture, plan or sample work inside the proposal |
| stale | Posted more than 72 hours ago with nobody interviewing, or the client last viewed proposals more than 3 days ago |
| crowded | More than 20 proposals, or 3 or more already interviewing, or a hire already made on a single-hire job |
| cheap-history | The client's average hourly rate paid is below 60% of the campaign floor and they have 3 or more hires (they buy cheap) |

## Chance score (0–100) for jobs that pass the gates

Start at 50, add or subtract, then clamp to 0–100.

| Signal | Points |
|---|---|
| Client has spent more than $0 (fills at 44–47% versus 36% for never-spent clients) | +10 |
| Hire rate 70% or more | +10 |
| Prior hires in software development at or above the campaign floor | +15 |
| Fixed price with a stated budget (50.5% fill) or hourly with a stated range (40.6%); no budget at all (35.1%) | +5 / 0 / −10 |
| Client is Business Plus or Enterprise | +10 |
| Stated duration 3 months or more | +5 |
| Screening questions present (their absence marks a low-effort post with many bidders) | +5 / −5 |
| Specific post: named stack, current problem, deliverable, or acceptance criteria | +10 |
| Under 10 proposals, or posted less than 2 hours ago | +10 |
| Client country with a low historical fill rate (e.g. India 26.7% versus US 47.5%) | −10 |
| Reviews from freelancers mention disputes, non-payment, scope creep or "never replied" | −15 |
| New client (joined in the last 30 days, no history) but with a specific post and verified payment | −5 (not a reject) |

Bid only when **chance ≥ 55**. A score of 45–54 is held for Paul: it goes in the session summary
with the reason, with no packet.

## Calibration

Every packet records its chance score. After every 30 submitted bids, compare the chance score of
bids that got a reply with those that did not. Change at most one weight per review, and note the
change and its reason in the campaign's `## Learnings`. The numbers above are starting priors from
vendor and Upwork data, not measured on JetThoughts bids.
