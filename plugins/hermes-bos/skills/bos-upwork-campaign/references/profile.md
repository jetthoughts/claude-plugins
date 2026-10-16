# Profile: audit, then diff

Adapted from `sarmad-mughal/upwork-profile-optimizer-skill@upwork-optimizer` (read 2026-10-14). Kept what
fits a single main profile and cited claims; dropped specialized profiles (retired 2026-05-28) and the
catalog listings (now one per service, see SKILL.md § Profile).

## 1. Audit the live profile first

Read the live title, overview, skills, portfolio order and Catalog offer. Score each line below
pass / fail with the current text quoted. The diff fixes only the fails, so a good line survives.

| Check | Pass when |
|---|---|
| Title names a searched service | It leads with the specific service clients type for the campaign lane, not a generic role ("Developer", "Freelancer"). ≤ 70 characters. |
| First 150 characters | They state a service plus a result. Upwork search cards and Google show only this part. |
| Opening | It starts with the client's pain or a proof, not "I'm a X with Y years". |
| Proof early | 2–4 quantified results appear before the services list, each cited in the claims source. |
| Services specific | It names deliverables the way buyers search them ("security assessment", "SOC 2 readiness", "production readiness audit"), not categories. |
| Keywords placed | The lane's top search terms appear in the title, the first paragraph and the services list, read naturally, with no stuffing. Upwork indexes the whole overview. |
| Reliability signal | Long-term clients or contract length are stated, when true. |
| Delivery disclosed | It says who does the work (team plus accountable lead), per `upwork-campaign-prelude`. |
| Layout | Plain ALL-CAPS section headers, `→` lists, blank lines between sections. No emojis, no divider lines, no sign-off. |
| One CTA | The last line is one warm, direct invitation, not "feel free to reach out". |
| Human voice | The `humanizer` pass finds no AI tells (see section 3). |
| Catalog offer | Its title is searchable; the description is 2–3 sentences (what, how fast, what's included); deliverables are listed; a price anchor is set. |

## 2. Overview order for the diff

```
HOOK            2 lines: the buyer's pain or the strongest proof
WHO I WORK WITH 1–2 sentences, 2–3 client types at most
RESULTS         → 2–4 cited results
SERVICES        → specific deliverables, lane keywords
LONG-TERM       optional: longest engagements, repeat clients
HOW I WORK      one line, including who delivers
TOOLS           only the ones buyers search for
CTA             one line
```

Title format: `[Primary service] | [Service 2], [Service 3] & [Service 4]`, ≤ 70 characters.
Keep material from earlier profiles that still passes the audit (Paul: "do not drop all our previous
profiles"); dropping a live line needs his call, recorded in the diff.

## 3. Voice

Run `humanizer` on the title and overview. In addition, look for these profile-specific tells:
- vocabulary: "passionate about", "dedicated to", "commitment to", "in today's landscape", "at the intersection of", "seasoned expert", "move the needle"
- structure: every sentence the same length, tidy rule-of-three lists, paragraphs that end on a summary line
- claims: superlatives without a number. "Trusted by teams at companies doing $10M+/year" (cited) beats "industry-leading enterprises".

Last check: ask what makes the draft obviously AI-written, and fix that.

## 4. Diff file

`profile/<date>-<surface>-diff.md` holds, for each surface: the audit row (pass/fail with the quote), the current
text, the proposed text, and the claim source for every number. Uncited numbers stay out.
