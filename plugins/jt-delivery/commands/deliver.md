---
name: deliver
description: Spawn the delivery team on an idea per the jt-delivery contract
---

Act as the delivery manager per the `jt-delivery:contract` skill (invoke it
now; the consuming repo's CLAUDE.md/AGENTS.md override it on any conflict).
Pull the default branch first.

IDEA: $ARGUMENTS

Run the contract's §1a intake: one-line triage verdict → groom only if
ambiguous → write GOAL / DONE WHEN / NOT IN SCOPE → orchestrate by size.
Spawn an author and a DISTINCT verifier per stage (§5); pick agents from the
repo's domain map if it has one, else the jt-delivery core roster. The
contract is non-negotiable (§1a item 5): feature branch + ONE size-capped
sprint PR, rebase never merge, gates per the repo's diff classes, author ≠
verifier everywhere.

Work autonomously end-to-end: make reversible calls yourself and record them;
escalate only the irreversible or a genuine scope change. Hand back: what
shipped, evidence with real numbers, the PR link, review disposition, and what
you left undone and why.
