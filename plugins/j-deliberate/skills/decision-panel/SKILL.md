---
name: decision-panel
description: Governed group decision for Paperclip seats — one framed question, independent options, sealed ballots, source verification, one named Decision Voter, a version-bound decision packet on the card, and Paul as the only authority for consequential acts. Use when a card says "panel", when the method catalogue routes a decision here, or when more than one seat's judgment must be combined without one seat deciding from its own proposal.
---

# Decision panel

One question, several independent answers, one binding internal vote, and a packet a stranger can audit. Paperclip is the only control plane: the card carries everything as documents; nothing lives in chat or in a seat's memory.

**Scope, against `j-convening-the-council`.** This panel *binds*: one named Decision Voter casts the internal vote, and consequential packets end in board approval. The council is different in kind — a Delphi median that is advisory decision-support, never a voting machine. Need authority, use this; need structured critique, use the council.

## Roles (session functions, not hires)

| Function | Does | Never |
|---|---|---|
| Chief of Staff | frames the question, picks method and participants, sets risk class; records the packet when no conflict | votes on its own setup; is the Decision Voter |
| Facilitator | runs the method and timeboxes; opens the reveal | proposes options, votes, decides |
| Panelists (3–5) | each writes one option and one ballot, alone | reads another's option or ballot before the lock |
| Evidence Verifier | opens every cited source, reproduces the checks, marks each material claim supported / contradicted / unknown | repairs an option, then approves the repaired version |
| Decision Voter | reads locked options, ballots, verifier report, dissent, rubric; casts one binding internal vote | authors options, edits ballots or evidence, changes the rubric, adds an option after the reveal, authorises a protected act |

Default mapping for JetThoughts: Chief of Staff frames and records; Captain facilitates; Verifier verifies; Economist is the Decision Voter for internal decisions; Cold-Eyes-Reviewer (codex route) is the voter for consequential packets when resumed. Panelists come from the seats whose lens fits. A seat holds one function per decision.

## Risk class

`internal` (a choice inside the seats' own scope, reversible) or `consequential` (external, financial, legal, personnel, production, security, publishing, spending, or anything on the holds-test list). A consequential packet ends in a `request_board_approval` item for Paul; the Decision Voter's vote is a recommendation there, never an execution.

## The contract (document key `decision-contract`)

```
decision_id: <card identifier>
approved_goal: <the outcome this serves, one line, with its owner note>
question: <one decision question, answerable by choosing>
risk_class: internal | consequential
decision_owner: <seat or Paul>
facilitator: <seat>
panelists: [<seat>, <seat>, <seat>]
evidence_verifier: <seat>
decision_voter: <seat>
method: <from the method catalogue>
why_this_method: <why it fits this uncertainty and why a simpler one does not>
options_version: <revisionId of options-locked>
evidence_version: <revisionId of verification>
rubric_version: <revisionId of rubric>
ballot_deadline: <ISO time>
acceptance_or_success_measure: <what will be observed, by when>
human_gate: none | request_board_approval
budget: <max runs, max turns per run>
stop_conditions: <what ends the panel early>
```

## Order of play

1. **Frame.** Chief of Staff writes the contract. One question, one measurable outcome. No question, no panel.
2. **Method.** The smallest practice from the catalogue that resolves this uncertainty. A workshop because a skill exists is a defect.
3. **Facts.** Facilitator writes `facts` with what is known, each fact with source URL, retrieval date, excerpt; unknowns listed as UNKNOWN, not guessed.
4. **Independent options.** Each panelist writes `option-<seat>`: the proposal, its evidence, assumptions, strongest objection, falsifier. A panelist reads only the contract and `facts`.
5. **Lock options.** Facilitator writes `options-locked` listing each option document's `latestRevisionId`. Anything edited after this revision is a new round, not an amendment.
6. **Verify.** Evidence Verifier writes `verification`: every material claim across the options, its source, and supported / contradicted / unknown. A claim with no source URL and retrieval date is UNSUPPORTED and cannot carry an option.
7. **Sealed ballots.** Each panelist writes `ballot-<seat>` against the rubric: choice, rubric scores, evidence relied on, assumptions, strongest objection to their own choice, confidence 0–1, falsifier. A ballot that repeats another's reasoning is one perspective, not two votes; the Verifier flags it.
8. **Reveal.** Facilitator writes `ballots-revealed` with every ballot's revisionId and time. Ballots whose last revision is later than the reveal are void. Dissent is kept verbatim.
9. **Vote.** Decision Voter writes `decision`: SELECT <option>, REJECT ALL, EXPERIMENT <bounded test>, or NO DECISION (authority or evidence insufficient), with why the choice beats each alternative. Vote counts are input; evidence, downside, uncertainty and falsifiability decide.
10. **Gate.** Consequential: the packet goes to Paul as `request_board_approval` bound to the `decision` revisionId. Internal: proceed.
11. **Convert.** One owner, one experiment or deliverable card, acceptance evidence, appetite, stop condition. The packet names the card.
12. **Observe.** When the follow-up closes, the Recorder appends `observed` to the packet: predicted versus observed, and a learning proposal or "no change".

## Rubric (document key `rubric`, versioned)

Score each option 0–3 on: fit to the approved goal; evidence quality (verified sources, not assertions); downside if wrong; reversibility; cost to run; falsifiability of its claim. Tie: the Decision Voter picks the more reversible option or EXPERIMENT; never a coin, never a second silent rubric.

## Sealing, honestly

Paperclip documents are readable by every seat. Sealing is procedural: revision timestamps prove order, the run log proves what a seat read, and the Verifier compares. A seat that reads a ballot before the reveal is a defect recorded in the packet; the platform does not block it. Say so in every packet.

## Invalidation

A changed `facts` or `verification` revision after the reveal voids the vote; the Facilitator opens a new round from step 6. The Decision Voter may request a new round or choose EXPERIMENT; it may not add an option.

## The packet (document key `decision-packet`)

Exact question and outcome; method and why; options with authors; locked ballots; verification findings; dissent and rejected alternatives; final vote and rationale; human approval where applicable; follow-up owner and deadline; expected measure and falsifier; observed result; learning proposal or "no change". Every entry is a revisionId, not a paste.

## Autonomy ratchet

Every decision class starts at L0: propose and confirm. A class may be proposed for lighter review only after ten consecutive decisions approved without substantive human correction, source-verified, free of escaped defects, on the same rubric and skill revision. One correction resets to L0. Promotion is Paul's approval item. Protected acts never ratchet past their existing gate.

## Measures (always with denominators)

first-pass acceptance / decisions; substantive human edits / decisions; escaped false acceptances; false rejections; reversals; decisions with an observed outcome / decisions; hours from question to verified decision; experiments closed / opened; model plus review plus human-repair cost; method misuse; copied ballots / ballots. Unknown is not zero.
