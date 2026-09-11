---
name: j-offer
description: "Turn a capability into something someone can buy — name what it is, price and package it, decide the motion that reaches the buyer, and write the outreach. Use whenever the question is what should we charge, per-seat or per-project, how do we package this, what is the entry offer, who do we approach first, how do we reach them, should we discount, or what do we say to a prospect. Composes the pricing, deal, GTM and outreach skills rather than restating them. Not for finding out whether the market exists — that is `j-market`; not for public content — that is `j-publish`."
---

# j-offer

The entry point for *what someone can buy and how they hear about it*. It exists because offers here get written as descriptions of the work rather than as something with a price, a buyer and a first move — and a capability with no price is not an offer.

**Two hard boundaries, before anything else.**

**Nothing goes outward without Paul's approval on the exact text.** Draft it to a file, run `gitleaks detect --no-git -s <dir> --no-banner`, read it for names, emails, tokens, absolute paths and customer ids, and paste the scan with the draft. No agent and no seat holds the send.

**JetThoughts is in the planning stage and zero sends is deliberate.** Never frame 0 sends as a defect or propose a mechanism that routes around approval. Canonical: the vault's `jt-operating-system` note, § *The stage*.

## Run it

**1 — Check the ledger before inventing.** Does `j-market` already hold the segment, the buyer and who else sells this? If not, run that first — pricing set without a comparable is a number from nowhere. Read the vault's `claims-register` for anything already closed; a killed option reappearing is a defect, not a candidate.

**2 — Take the rungs the offer actually needs.**

| The question | Type this |
|---|---|
| Who to sell to first, and the wedge | `pm-go-to-market:ideal-customer-profile` · `:beachhead-segment` · `defining-icp` |
| What to charge, and how to package it | `commercial-skills:pricing-strategist` · `pm-product-strategy:monetization-strategy` · `pm-product-strategy:value-proposition` |
| Whether this specific deal makes margin | `commercial-skills:deal-desk` · `:channel-economics` |
| Which motion reaches this buyer | `pm-go-to-market:gtm-motions` · `enterprise-sales-motion` · `solo-founder-gtm` is dead — use `founder-sales` |
| The first handful of customers, by hand | `first-b2b-customers` · `founder-sales` — manual and unscalable is correct at this stage |
| A written outreach sequence | `marketing-skills:cold-email` — subject lines, opener, CTA, follow-ups |
| A partner or reseller tier | `commercial-skills:partnerships-architect` |
| Responding to an RFP, or a discount policy | `commercial-skills:rfp-responder` · `:commercial-policy` |
| A contract or proposal, DACH terms | `business-growth-skills:contract-and-proposal-writer` |

For a whole commercial question rather than one rung, `commercial-skills:cs-commercial-orchestrator` routes internally and forks the heavy intake out of this thread.

**3 — Every offer carries five fields or it is not an offer.** Name it · who buys it · what it costs and on what basis · what they get and by when · what it is instead of. A missing field is the one that gets argued about later.

**4 — Get it killed before it goes out.** `roast:roast` for the offer itself — five angles, one GO / RESHAPE / KILL, and the cheapest 48-hour test. `exec-challenger` when it is a JetThoughts executive move; it must return a dissent (vault-scoped agent — outside the pkm root use `cold-reviewer`). `content-cold-eyes` on any text that will be read by a buyer. A review that returns "looks good" has failed.

**5 — Land it.** Price and packaging decisions go to the note that owns them and to `claims-register` if they supersede a stated number. Anything with an owner and a date goes on the board (`j-paperclip`). Outreach text goes to a file for Paul, with its scan.

## Failure modes

| Symptom | What it means | Do |
|---|---|---|
| A price with no comparable | invented | find what two others charge, or label it `ESTIMATE` |
| The offer describes the work, not the outcome | it is a service description | rewrite from what the buyer gets, by when |
| "We could also…" in the offer | it is a menu, and a menu does not close | pick one entry offer; park the rest |
| An outreach draft with no route named | Route 1 and Route 2 have different buyers | name the route on every prospect |
| A send proposed without a scan | the publishing boundary | draft to a file, scan, hand to Paul |
