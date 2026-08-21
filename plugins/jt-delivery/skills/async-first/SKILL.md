---
name: async-first
description: Async-first communication SOP - written, discoverable artifacts are the default for every decision, finding, status change, and handoff; sync interaction is the exception and its outcome is written back same-day. Use when deciding where to record work state or how to hand off between sessions/agents.
---

# Async-first communication

**The rule**: a task is not done until its state is readable by a cold session
with zero questions. Written, discoverable artifacts are the default for every
decision, finding, status change, and handoff. Sync interaction (calls, live
approvals) is the exception — and its outcome gets written back the same day.

## Where things go

| What | Canonical surface |
|---|---|
| Decisions | the doc that owns the topic, with the reasoning (ADRs for architecture) |
| Findings | the PR they affect, with evidence (no PR yet → the commit message or the sprint's working doc) |
| Status | derived from git/PRs — never hand-maintained status docs |
| Handoffs | an explicit list in the artifact the next person will open |
| Durable learnings | the repo's knowledge base, same commit as the change |
| Cross-session decisions/corrections | persistent memory (searched before deciding) |
| Debt | named and listed where the work lives, never silent |

The consuming repo's CLAUDE.md may define more specific surfaces — those win.

## The two failure modes

1. **State rots.** A concept that stores STATE (counts, statuses, "current"
   anything) is stale by the next commit. Store REASONING; derive state from
   git.
2. **Batching loses the detail.** Write the artifact when the event happens,
   not at session end — the batch loses exactly the detail that made it worth
   recording.

## Handoff checklist

Before ending a work session: every decision recorded where its topic lives ·
open items listed with enough diagnosis that a cold session can execute ·
nothing exists only in chat scrollback · anything sync agreed today is written
back.
