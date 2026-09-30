---
name: bos-research-incident
description: Detect, triage, and close research incidents (missed item, outdated, low confidence, AI slop) using a 3-variant re-research swarm, tool-score voting, and OpenViking memory. Use when a research output is rejected ("you missed X", "this is wrong", "improve research", "re-do", "not found"), or auto-triggered by confidence=Low, <2 independent sources, no dates, or a top known tool missing from OpenViking `research_notes`.
version: 0.2.0
author: pftg
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, research, incident, deep-research, tool-scoring, tavily]
    related_skills: [bos-research, j-deep-research, j-research, bos-incident-response, j-designing-experiments]
---

# Research Incident Workflow

When a research deliverable fails (missed item, stale data, low confidence, fabricated source), don't retry with the same tool chain. Open an incident, spawn 3 variant fan-outs with **deliberately different tool chains**, vote on candidates using past tool performance, verify the winner experimentally, and write the lesson back into OpenViking memory so the same gap does not recur.

This skill extends `bos-incident-response` (which handles *task-level* blocks) with the *research-output* class. Reuses its swarm machinery and incident file format; differs by entry trigger, the 3-variant pattern, and the OpenViking write-back surface.

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Incident files: `operations/incidents/INC-YYYYMMDDNN-<slug>.md` (same path as `bos-incident-response`)
- OpenViking memory surface: `research_notes/{topic}/`, `tool_scores/global`, `user_corrections/{topic}`, `known_gaps/{topic}` (all under `viking://user/default/`)

## When to use

Use when **any** of:

| Trigger | Source | Confidence needed |
|---|---|---|
| User says "you missed X", "this is wrong", "not found", "improve research", "re-do", "give better sources" | user message | none — always trust |
| Auto: confidence = Low | bos-research matrix | confirmed by reading the artifact |
| Auto: <2 independent sources per material claim | bos-research matrix | confirmed by reading the artifact |
| Auto: no publish/retrieval date on any source | bos-research matrix | confirmed by reading the artifact |
| Auto: a top known tool from `research_notes/{topic}/known_gaps.md` is missing | OpenViking read | cross-check with the result |
| Auto: novelty gate fail (<3 NEW findings) | j-research / bos-research novelty gate | confirmed by the gate line |

Do **not** use for: code/repo questions, single-fact lookups (`wigolo fetch` is enough), or research that already passed with the novelty gate.

## Inputs

- Original query and the failed artifact (path, run id, runner)
- Missing item X (user's words verbatim) or the auto-trigger that fired
- Time spent so far (for budget tracking)

## Procedure

### 1. Incident intake (acknowledge in 1 line, do not wait)

State the incident in one line: "Opening incident INC-YYYYMMDDNN: missed X / low confidence / stale." Create the OpenViking entries in **one batch**:

OpenViking artifact layout (create in one batch): see `references/artifact-templates.md`.

Mirror the kanban-side INC file at `operations/incidents/INC-YYYYMMDDNN-<slug>.md` with frontmatter (`id`, `title`, `status: open`, `cause: research-miss-X`, `recipe: no-match`, `risk: medium`, `action: 3-variant swarm`, `verdict: open`, `date`).

Do not run any search yet. Acknowledge, then triage.

### 2. Triage & root cause

Read the failed artifact and the prior research:

- `research_notes/{topic}/` — what we already had
- `tool_scores/global` — what worked before for this lane
- `user_corrections/{topic}` — what the owner has already corrected us on

Write `rca.md` (concise, ≤1 page):

`rca.md` body template: see `references/artifact-templates.md`.

Append `tool_scores/global` (increment `false_negatives` for tools that missed X). Read `tool_scores/global` first to weight later votes.

### 3. Re-research with 3 variants (max 3 rounds)

Spawn 3 researcher subagents in parallel via `delegate_task`. **Each uses a deliberately different tool chain** — same chains guarantee the same miss.

Researcher-profile default variant table (A Discovery / B Freshness / C Novelty): see `references/variant-chains.md`.

These are **deliberate diversity chains for the swarm**, not the general research ladder — the point of the 3-variant pattern is that the chains differ, so a re-run cannot reproduce the same miss. A fresh web fact outside the swarm still goes on the `j-research` ladder (`searxng` first → `tavily`, announced).

Each variant must:

1. Decompose the query into **4–6 sub-questions**, one of which is the user's missing item X as a *required target* (not optional).2. Deep-read the top 5 URLs (full text, not snippets). Use `web_extract` or `browser_open`, not just search snippets.
3. Return a structured table per sub-question:
   ```
   | candidate | URL | date | evidence quote | confidence |
   ```
4. Cap at 3 rounds. Round 1 returns, then **round 2 widens queries** (synonyms, adjacent domains, "alternative", "emerging", "open source", "2026") if X is still missing. Round 3 changes the tool chain if round 2 also failed.

Brief each subagent blind — do not pass it the failed artifact, just the original query + missing item X. Add: "List at least 3 findings that are not in this brief or the prior research. Mark each NEW with its source." (novelty gate)

Consolidate into `candidates.md`:

`candidates.md` layout: see `references/artifact-templates.md`.

#### Platform-aware variants (when the topic names a platform)

If the topic needs Reddit, Twitter/X, YouTube, GitHub, LinkedIn, Bilibili, XiaoHongShu, RSS feeds, etc., the platform lane runs **the same ladder `j-research` owns** — it does not get an order of its own: rung 1 `searxng_web_search` scoped with a `site:` filter, rung 2 `tavily_search` with `include_domains` (metered — announce it in the answer), rung 3 `agent-reach` **off-ladder**, only for what the general index cannot reach.
Platform ladder table (rung 1 `searxng` → rung 2 `tavily` → rung 3 `agent-reach`): see `references/platform-ladders.md`.

**Sub-rule:** never run `agent-reach` before the ladder has had its turn — `searxng` with a `site:` filter first, then `tavily` with `include_domains` (announced, metered). `agent-reach` is reserved for login-gated content, comment transcripts, or full RSS history that neither index reaches. This is the same order `j-research` states for a named platform; where they differ, `j-research` wins.

### 4. Voting

Score each candidate 1–5 on four axes:

| Axis | 1 | 5 |
|---|---|---|
| Evidence strength | 1 secondary source | 3+ independent primary sources |
| Recency | > 90 days | < 14 days (news) / < 30 days (tools) |
| Relevance | tangentially related | directly solves the query |
| Novelty | repeats the brief | includes missed item X and 2+ NEW findings |

Voting rule:

- Each variant votes for its own candidates. Weight = `tool_scores/global` score for that variant's tool chain (sum of `true_positives` minus `false_negatives`, min 1).
- The user's missing item X gets an **automatic +2 bonus** (treated as ground truth, not preference).
- Winner = highest weighted total. **Require winner ≥ 14/20** for verdict PASS. Below → run another research round (return to step 3) until round 3, then escalate.

Write `vote.md`:

`vote.md` table format: see `references/artifact-templates.md`.

### 5. Experiment & verify

For the top 2 winners:

1. Open the official docs/site with `browser_open` (or `web_extract` for static pages).
2. Extract install steps, pricing, last update date, maintainer activity.
3. If the topic is software, validate the install command or API shape against a local probe (`terminal` + a quick test script — never actually install unless the owner approved).
4. Mark VERIFIED or REJECTED with the exact reason and the probe output.

Write `experiment.md` with the verdict and the proof command + output.

### 6. Freshness re-check (before close)

```
searxng_web_search "<winning solution> updates last 7 days"  (time_range: week)
you-research "<winning solution> updates last 7 days"        (standard effort)
```

- New version or breaking change → update the recommendation in `resolution.md`, note the delta.
- No updates → note "verified current as of {date}" in `resolution.md`.

### 7. Loop gate

Done when **all** are true:

- Missing item X is found and listed with URL + date + evidence quote.
- Winner has High confidence and 2+ independent sources.
- Experiment = VERIFIED (or REJECTED with an explicit reason that another candidate passes).
- No new user objection.

If attempts < 3 and not done, return to step 3 with sharper queries and demoted tools (the variant that missed X last time gets a different chain this round). If attempts = 3 and not done, write `escalation.md` with what is blocked and what human input is needed, then block the kanban card.

### 8. Close and learn (write back to OpenViking)

On done, write `resolution.md`:

`resolution.md` body template: see `references/artifact-templates.md`.

Then write the corrections:

- `research_notes/{topic}/<slug>.md` — corrected answer, with the winner as the lead finding.
- `user_corrections/{topic}.md` — append `<date>: <X>` so future runs treat X as ground truth.
- `tool_scores/global` — increment `false_negatives` for tools that missed X, `true_positives` for tools that found it. Format: `tool:<name> {true_positives: N, false_negatives: N, last_seen: <date>, lanes: [...]}`
- `known_gaps/{topic}.md` — remove the fixed gap line. (Don't delete the file — keep the open gaps.)

Mirror the resolution into the kanban-side INC file: set `status: closed`, `verdict: fixed, recipe validated`, link `resolution.md`.

### 9. Output to user

Always return, in this order:

1. **Incident:** what failed and why (2 lines).
2. **Re-research:** the 3 variants tried (chains + round count).
3. **Vote results:** table of candidates with scores.
4. **Verified solution:** the final recommended steps, with URL + date.
5. **What changed vs previous answer:** the delta — what the variants found that the prior run missed.
6. **Memory:** "Logged to OpenViking `incidents/{date}/{id}/` and corrected `research_notes/{topic}/`."

## Failure modes

- **Single-variant retry.** "Try again with the same chain" reproduces the miss. Always run 3 chains in parallel, or escalate.
- **Burying X in the sub-questions.** X must be a *required target* in the decomposition, not an optional sub-question.
- **Snippet-only reads.** The top 5 results must be deep-read full-text. Snippets collapse novelty.
- **Promoting a winner that missed X.** The +2 bonus on X is non-negotiable. A winner without X cannot be the verdict, regardless of weighted total.
- **Closing without writing back to OpenViking.** The whole point is that the next run inherits the lesson. Skipping step 8 means the same gap recurs.
- **Inventing tools in the chains.** Use the tools that are actually enabled in `mcp_servers`. `references/variant-chains.md` names the defaults for the researcher profile; if a tool is missing locally, swap to the fallback row in the **Platform-aware variants** table (`references/platform-ladders.md`) and note the swap in `rca.md`.
- **Calling the failed output "fine, with caveats".** Caveats do not fix misses. Open the incident.
- **Running the variants sequentially.** They are independent — parallelize via `delegate_task` in one batch.
- **Reaching for `agent-reach` before the ladder.** `searxng` with a `site:` filter comes first, then `tavily` with `include_domains` (announced). Reserve `agent-reach` for login-walled or transcript-needing content the indexes do not reach.
- **Treating Tavily's free tier as unlimited.** Each `tavily_search` with `search_depth: advanced` costs 2 credits; budget rounds accordingly.

## Verification

- `incidents/{date}/{id}/` exists with `rca.md`, `candidates.md`, `vote.md`, `experiment.md`, `resolution.md` (and `escalation.md` if blocked).
- Winner has High confidence, 2+ independent sources, **includes X**.
- `tool_scores/global` updated (demoted the failing tool, promoted the finding tool).
- `user_corrections/{topic}` lists X; `research_notes/{topic}/` updated.
- Kanban INC file at `operations/incidents/INC-YYYYMMDDNN-<slug>.md` matches frontmatter schema, status=`closed`.
- The user-facing output follows the 6-line format in step 9, no editorial additions.

## Reference variants — by profile: see `references/variant-chains.md`.

Tavily setup for the researcher profile: see `references/variant-chains.md`.
