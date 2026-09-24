---
name: bos-decision-record
description: Record a governed decision with alternatives and evidence.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-decision-record Skill

Create a decision record in `operations/decisions/` that captures the
decision, the alternatives considered, the evidence and risks behind each,
the owner, and a review date. A record is memory, not permission: an accepted
`DEC-*` documents a choice — it never substitutes for the owner's explicit
per-instance yes on an `EXTERNAL` or `IRREVERSIBLE` action (deny-on-silence
binds every record). This skill writes the record only; it never executes the
decision and never commits to Git (the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Decisions directory: `/Users/pftg/dev/pkm/business-os/operations/decisions/`
- Canonical format carrier: this skill (per the Business OS root `AGENTS.md`).

## Use when

Use when a choice with material scope, risk, or reversibility consequences
needs to be recorded: strategy picks, tool or vendor choices, `IRREVERSIBLE`
actions that require a recorded decision before acting (risk policy), or any
escalation that ends in a ruling. Not for trivia with no competing options
and not for performing the decided action.

## Inputs

- Decision question (one sentence, falsifiable)
- Options on the table — at minimum the leading alternative and status quo
- Evidence available per option (source paths or URLs)
- Decision owner (per the authority matrix; unresolved ownership escalates)

## Procedure

1. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, `constitution/authority-matrix.md`, `constitution/risk-policy.md`,
   `constitution/escalation-policy.md`, and any directly relevant work item.
2. Frame the decision as a single question. List every serious alternative —
   including "do nothing" — with its expected outcome, evidence (each claim
   with a source path or URL; unsupported claims marked as such), and risks.
   Never trim an alternative just because one option looks obvious.
3. State the recommendation and its class implication: if executing the
   decision is `EXTERNAL` or `IRREVERSIBLE`, say which, and name the
   per-instance yes (plus, for `IRREVERSIBLE`, this record) as prerequisites.
4. Derive the ID as `DEC-<YYYYMMDDNN>` (zero-based counter within the day,
   mirroring the `WI-<YYYYMMDDNN>` convention in `bos-intake`) and confirm
   uniqueness with `search_files target='files'` in the decisions directory.
5. Write the record with `patch` at `operations/decisions/<ID>.md` using the
   canonical format below. Propose a `review_date` from the risk profile
   (sooner for `EXTERNAL`/`IRREVERSIBLE`, ~one quarter for internal) and
   label it `proposed` — the owner confirms or adjusts it.
6. Set `status` honestly: `proposed` until the owner answers;
   `accepted`/`rejected` only on the owner's explicit yes or no — silence is
   refusal, never acceptance. If this decision replaces an earlier one, set
   the old record's `status: superseded` in the same change and link both
   ways.
7. Link the record back: add it to the owning work item's `evidence` (or
   `Next approval required`) so the state machine stays coherent.

Canonical decision record format:

```markdown
---
id: DEC-<YYYYMMDDNN>
title: <one line>
status: <proposed|accepted|rejected|superseded>
owner: <decision owner per the authority matrix>
decision: <the chosen option, or "pending owner" while proposed>
alternatives: [<options considered, including status quo>]
evidence: [<source paths or URLs>]
review_date: <YYYY-MM-DD (proposed — owner confirms)>
updated: <YYYY-MM-DD>
---

# <title>

## Question
<the single decision question>

## Alternatives
<for each: option, expected outcome, evidence, risks>

## Decision
<chosen option + one-paragraph rationale; "pending owner" while proposed>

## Risks and mitigations
<top risks of the chosen option and how they are bounded>

## Consequences
<what this enables, what it forecloses, what must be true for it to hold>

## Review
<what would reopen this decision; review_date above>
```

## Output

Return the record path, ID, status, the options list with the recommendation,
the class implication (`EXTERNAL`/`IRREVERSIBLE` prerequisites), the proposed
review date, and the owner answer still required (if any).

## Failure modes

- Do not treat the record as retroactive consent — a decision to act still
  needs the per-instance yes at the gate.
- Do not record `accepted` on silence, a timer, or a draft; that is the
  abolished silence-equals-consent pattern.
- Do not invent evidence or soften an alternative's risks to make the
  recommendation look cleaner.
- Do not decide ownership questions yourself — a missing owner escalates per
  the escalation policy.
- Do not commit, push, or rewrite Git history — the owner commits.
- If the decisions directory or risk policy is missing, stop and report;
  do not scaffold governance mid-decision.

## Verification

- All frontmatter fields present; `status` is from the canonical vocabulary;
  `updated` is today.
- File exists at `operations/decisions/<ID>.md` and `read_file` returns it;
  the ID is unique in the directory.
- At least two alternatives (including status quo) with evidence and risks;
  every evidence entry resolves to a path or URL.
- No `EXTERNAL`/`IRREVERSIBLE` action was executed — prerequisites are named.
