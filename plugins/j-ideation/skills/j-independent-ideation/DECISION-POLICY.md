# Decision policy

## Claim labels
FACT (cites `E-nnn` with URL/path/transcript/query provenance) · INFERENCE · ASSUMPTION · ESTIMATE (formula + range) · CONTRADICTION · UNKNOWN.

## Source tiers
T1 primary (interview, analytics, contract, pricing page, product docs, filing, source code, raw experiment result) ·
T2 credible practitioner/buyer (independent reviews, niche communities, RFPs, job posts, verified customer comments) ·
T3 vendor/consultant/marketing · T4 model prior, intuition, unverified assertion.
No High confidence on a decision that depends mainly on T3/T4.

## Likelihood vs confidence (always separate fields)
Likelihood: almost-no-chance · very-unlikely · unlikely · roughly-even · likely · very-likely · almost-certain.
Confidence: low · moderate · high. Never one numeric score.

## Evidence hierarchy (highest first)
1 observed user behaviour / controlled experiment · 2 paid commitment, pre-sale, LOI, real usage · 3 direct interviews with relevant participants ·
4 internal operational data · 5 corroborated external primary sources · 6 expert critique and competitor observation ·
7 multi-model council consensus · 8 founder preference.

## Doors
Type-1 = irreversible or expensive → explicit human approval before execution. Type-2 = cheap and reversible → test quickly when a measurable result exists.

## Verdicts
| Verdict | When |
|---|---|
| GO | evidence threshold met, no unresolved fatal assumption, economics/delivery acceptable, human decider approved |
| EXPERIMENT | promising, one critical uncertainty, bounded test exists |
| RESEARCH-MORE | decisive information is obtainable from internal data or credible sources; testing premature |
| PIVOT | problem supported; segment, solution, channel, delivery model, or pricing fails |
| STOP | weak problem evidence, buyers unreachable, unacceptable economics or risk, or kill criteria met |

## When the council disagrees
1 observed behaviour beats all model advice · 2 cheap discriminating test ⇒ EXPERIMENT · 3 reversible ⇒ smallest instrumented option ·
4 irreversible ⇒ research or human governance · 5 purely aesthetic ⇒ design-system consistency or user testing · 6 tied ⇒ lower downside, faster learning.

## Confidence ceilings for RICE
model consensus/internal opinion 0.30 · anecdote/competitor observation 0.40 · multiple customer problem signals 0.60 ·
prototype/usability 0.75 · behavioural experiment 0.85 · paid commitment/production 1.00.

## Priority formulas
Assumption priority = (impact × uncertainty × immediacy) × (1 − evidence strength).
Experiment priority = (EIG × decision importance) / ((cost+1)(duration days+1)(effort days+1)).
RICE = (reach × impact × capped confidence) / effort, only among candidates for the same outcome.

## External actions
No outreach, ads, publishing, lead contact, purchases, paid accounts, or production changes without explicit user confirmation in chat. Ever.
