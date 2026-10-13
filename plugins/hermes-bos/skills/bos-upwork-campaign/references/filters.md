# Upwork job filters (in order; stop at the first failure)

The bigger waste is jobs that never hire: 56% hire nobody, and 99.1% of chronic non-hirers show
"payment verified". Sources: vault `evidence/perplexity/jetthoughts-marketing/pplx-6de7584b-*`,
`pplx-260f1fb5-*` §5.3. The weights are priors; recalibrate them from the ledger.

## 1. Scam (sum points; ≥ 40 rejects)

| Points | Flag |
|---|---|
| 35 | Off-Upwork contact before a contract; free work, unpaid test, fee or equipment; ID or bank data; crypto, reshipping or "easy money"; asks to run or clone their repo or file (malware lure) |
| 25 | Payment not verified |
| 20 | Farmed-looking reviews |
| 15 | Joined the same day it posted; no hires but 3 or more open jobs; 0% hire rate with 5 or more posts |
| 10 | Vague post (< 60 words, no deliverable); budget far off for the scope; many proposals but nobody interviewed after 48 h; repost by a new client |
| 5 | Client country does not match the post |

Flags worth 35 points also get a note for Paul to report the post. Never press the report button yourself.

## 2. Chance

Reject if any of these holds: 5 or more posts with 0 hires; hire rate < 50% with 3 or more posts;
the post asks for a full estimate, plan or architecture; posted > 72 h ago with nobody interviewing,
or proposals last viewed > 3 days ago; > 20 proposals or ≥ 3 interviewing or already hired; the
client's average paid rate < 60% of the floor with 3 or more hires.

Score: start at 50, apply each line, then clamp to 0–100.

| Points | Signal |
|---|---|
| +15 | Past software hires at or above the floor |
| +10 each | Spent > $0; hire rate ≥ 70%; Business Plus or Enterprise; specific post (stack, problem, acceptance); < 10 proposals or posted < 2 h ago |
| +5 each | Fixed price with a budget; duration ≥ 3 months; has screening questions |
| −5 | New client, otherwise clean |
| −5 | No screening questions |
| −10 | No budget; low-fill client country |
| −15 | Reviews mention disputes, non-payment or scope creep |

## 3. Fit (0–100)

Reject outright if there is no budget path to the floor, the job is outside the campaign, or it
needs an engineer we cannot commit.

Score: offer and proof match 40, economics against target 25, client quality 20, competition 15.
