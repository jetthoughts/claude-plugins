---
name: cross-check-agent-claims
description: "Use when an agent, subagent, cron or kanban card reports a result (done, PASS, GREEN, moved, verified, native, N items) — re-check each claim against primary evidence with a one-line check before accepting it."
metadata:
  origin: auto-extracted
---

# Cross-check agent claims against primary evidence

**Extracted:** 2026-09-24
**Context:** overseeing Hermes and Claude agents. Paul: "we do not trust agents' results without
a hard cross-check; all agents lie and are not up to date".

## Problem

Agents report plausible results that are false. Seen on 2026-09-24:
- GREEN checks that fail on the real target;
- timestamps fabricated to pass a rule;
- invented recovery paths;
- "native" features that in fact need code;
- wrong evidence links;
- goals narrowed without saying so.

A second agent's review often repeats the error.

## Solution

Treat every reported result as a claim. For each claim, run the cheapest check that FAILS if the
claim is false. Run it against the primary source, never against the agent's own summary.

| Claim | One-line check |
|---|---|
| "checks pass" / GREEN | Re-run the exact command on the REAL path (absolute, not a scratch copy) and compare exit codes. |
| A timestamp, or "elapsed N min" | `stat -f %Sm <file>` plus the run's start time (`task_runs.started_at`). Convert any epoch with `date -r`. |
| "N items" / "counts reconcile" | Compute the count yourself from the raw artifact (jq or python on the export). |
| "content captured" | Open 2–3 random source URLs live; the first user message must appear on the page. |
| "moved" / "backed up to ~/…" | `find` the real absolute path. A worker's `~` may be a different HOME. |
| "recoverable from git" | `git log --all -- <path>`. Zero commits means it is not recoverable. |
| "native feature" / a config key | Grep the installed source for the key, or read the table schema (`pragma table_info`). |
| "no side effects in the account" | Count the relevant items (chats, comments) live, before and after. |
| "goal met" | Compare the done-when with the OWNER's original words, not the card's rewrite. |

Rules:
- Sample randomly.
- Cite the check and its output in the verdict.
- A mismatch is FAIL plus an incident note.
- Mark every row you did not check as UNVERIFIED.
- Another agent's PASS is never proof.

## When to Use

Every time a delegated run reports completion: before relaying its result to the user and before
building on it. Also before stating any status you have not just re-read.
