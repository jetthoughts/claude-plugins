---
name: bos-initiative-overview
description: Executive cross-initiative health overview + Shape Up hill chart per initiative.
version: 0.1.0
author: pftg
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [bos, delivery, overview, hill-chart, shape-up, executive, health]
    related_skills: [bos-progress-report, bos-daily-review, bos-lens-router, bos-intake]
---

# bos-initiative-overview Skill

Emit an **executive overview** of every active initiative the owner has named — first read from the owner's phone — plus a **Shape Up hill chart per initiative**. The overview is the "what changed, what's healthy, what's stuck" surface; the hill chart is the per-initiative "where is this on the hill and what unblocks it" detail. Both land on a single page so the owner can scroll.

## Why this skill exists

The owner has asked (2026-10-08): "Learn to provide to me executive overview on all initiatives that I would understand the health. Research how others run this and revise yourself to allow to give me this overview. Then learn how to give hillchart progress summary per one initiative."

The existing `bos-progress-report` skill emits per-initiative Shape Up hill charts but lives as two artifacts (index + per-pass file) and was not designed for phone-first reading. This skill merges the index + per-pass into a single page and adds an **executive overview section at the top** so the owner reads the whole picture first, the per-initiative hill chart second.

## Sister artifacts

- `bos-progress-report` writes `progress-board.md` + `progress-YYYY-MM-DD.md` (per-initiative hill charts, two files). This skill emits the same per-initiative content but as a single page that opens with the executive overview.
- The `inventory-YYYY-MM-DD.md` cross-source rollup (kanban + DEC + INC + eval + governance + work-items) is the strategic view. This skill rolls that up too, in the executive overview section.
- Three layers, one rule: overview = this skill, hill-chart detail = `bos-progress-report`, cross-source reconciliation = inventory pass.

## What the executive overview section carries (per the 2026-09-29 meta-AGENTS.md "Stop bouncing scope to Paul" + the 2026-08-29 operator rule "give me high overview picture")

1. **One-line per initiative** with health traffic light (🟢 / 🟡 / 🔴):
   - `🟢` = on the hill, hill position stable, no age > 30 days without movement.
   - `🟡` = blocker present but < 7 days old; or hill position drift without blocker.
   - `🔴` = age > 7 days on the same status without an owner-step event; or two retries exhausted.
2. **The 4 numbers** (per PLANE.md "Hermes Mission Control"): kill rate, approval dwell, open one-off items assigned to Paul, oldest untouched actionable card.
3. **The cross-source count**: kanban active, DECs awaiting your yes, INCs open, evaluations open.
4. **Owner queue**: any Paul-bundle or 1-on-1 question surfaced in the last pass. Refers to Plane bundle by id (`HERM-76` etc.).
5. **What changed since last pass**: one paragraph; "shipped: X, in flight: Y, blocked: Z, deferred: W."

## What the hill chart section carries (per initiative)

- **Initiative name** + t-card root id (or DEC id).
- **Hill position** (per Shape Up Ch13; not %): `uphill` (figuring out, 0–40% unknown), `crest` (40–60% now-I-see-all), `downhill` (executing, 60–100% just-doing-it), `shipped` (done).
- **Appetite** (`SHAPE` epic / 2-week cycle / shapeless ongoing).
- **Scopes** (LEAFs done / in-progress / not-started), with t-card id + 1-line title + status.
- **Blockers / unknowns** — pulled from `kanban_blocked_needs_input`, INC files, and open evaluations.
- **Next step** — single most concrete next action with owner if known.
- **Healthy? (one sentence on what would move the indicator)** — health call is opinionated, not just data.

## When to Use

- Owner asks "how are initiatives going?", "status?", "summary", "overview", "give me the picture."
- Pre-sitting or pre-decision briefing.
- Phone-first read (single page; ≤ one screen on a 6.7" phone at default font).
- Not for: cross-source deep-dive (inventory pass is better); kanban tactical moves (the kanban itself is the surface).

## Prerequisites

- Read access to `~/.hermes/kanban.db` (kanban is the dispatch layer).
- Read access to `~/dev/pkm/business-os/` for DECs, INCs, evaluations, knowledge, decisions, retro, stuck-sweeps, governance.
- Read access to `~/dev/pkm/10-domains/business-os/operations/reviews/progress-board.md` (the existing rolling index this skill refreshes).
- Write access to `~/dev/pkm/10-domains/business-os/operations/reviews/` for the new "initiative-overview-YYYY-MM-DD.md".

## Procedure

1. Pull the kanban.db non-done card set. Group by parent (initiative / epic). For each group: count leaves done, in-progress, blocked, todo; compute hill position from `started_at` vs `completed_at` and from `task_links.parent_id`.
2. List DEC files at `~/dev/pkm/10-domains/business-os/operations/decisions/`. For each, parse `status:` (accepted / pending / proposed / DECIDED-but-awaiting-yes).
3. List INC files at `~/dev/pkm/10-domains/business-os/operations/incidents/*.md`. For each, parse `status:` (open / planned / closed / done).
4. List evaluation files at `~/dev/pkm/10-domains/business-os/evaluations/*.md`. For each, parse frontmatter `verdict:` (PASS / FAIL / CONDITIONAL PASS / DRAFT).
5. Pick the active initiatives. The criteria are: any of (a) kanban open ≥ 1 leaf on the epic, (b) DEC pending or proposed, (c) INC open, (d) at least one Paul item awaiting yes. Idle shipped initiatives go to a "shipped since last pass" line.
6. Render the executive overview (5 lines per the contract above).
7. Render the hill chart per initiative.
8. Compute the 4 numbers (per PLANE.md):
   - **Kill rate** = cancelled / closed (last 90 days; bounded).
   - **Approval dwell** = age of the oldest item assigned to Paul (days).
   - **Open one-off items assigned to Paul** = count; max 3 per PLANE.md Rule 3.
   - **Oldest untouched actionable card** = oldest non-done non-JOBS card (days; bounded to actionable columns).
9. Write the file at `~/dev/pkm/10-domains/business-os/operations/reviews/initiative-overview-YYYY-MM-DD.md`.
10. Optionally update the rolling `progress-board.md` so the link from `bos-progress-report` lands on this overview too.

## Output format (single page, ≤ one phone screen for the executive section)

```markdown
# Initiative overview — YYYY-MM-DD HH:MM Europe/Berlin

**Source of truth:** kanban.db + DEC/* + INC/* + evaluations/*. Health = 🟢 🟡 🔴 per house rules below.

> One-line per initiative (hill position, health, next step)

| Initiative | Hill | Health | Next step |
|---|---|---|---|
| Cognee indexing chain | shipped | 🟢 | none — closed |
| Job-search agent | downhill | 🟡 | re-scan with career-ops; no Rails-fit HoE surfaced today |
| Plane.so cleanup | downhill | 🟡 | M3 in flight; 7 Pierre M + 7 DEC mirrors queued |
| SOUL apply chain | uphill | 🟡 | closing-review gate QG-closing-gate retries exhausted; live SOUL is correct |
| | | | |

**The 4 numbers** (per PLANE.md "Hermes Mission Control"):
- Kill rate: 0.0% (0 cancelled / N closed)
- Approval dwell: 0d (oldest Paul item: HERM-76, age 0d)
- Open one-off items assigned to Paul: 1 (HERM-76)
- Oldest untouched actionable card: t_xxx, age Nd

**Cross-source:** kanban active = 44; DECs awaiting yes = 4; INCs open ≈ 14; evaluations open = 17.

**Owner queue (last pass):** HERM-76 "Paul: waiting on you (Hermes)" — 6 kanban + 4 DEC bullets. Bundle option D = no bundle (skipped).

**What changed since last pass:** shipped X, in flight Y, blocked Z, deferred W.

---

## Per-initiative detail (Shape Up hill chart)

### Cognee indexing chain
- **Appetite:** SHAPE 1+2 (epic).
- **Hill position:** shipped.
- **Scopes:** all done; archived.
- **Blockers:** none.
- **Next step:** none.
- **Healthy? 🟢:** yes.

### Job-search agent
- **Appetite:** ongoing (daily sweep).
- **Hill position:** downhill.
- **Scopes:** t_b80db252 (today's sweep), t_4219ae60 (re-scan + filter), t_5aa04c53 (sync tracker), t_56259e7e (career-ops reverify).
- **Blockers:** none on kanban; runtime = Rails-only filter strictness (no Rails-fit HoE posted today).
- **Next step:** tomorrow's daily sweep + top-3 candidates surfaced.
- **Healthy? 🟡:** running, but no Rails-fit HoE = the strict filter is working against us on Rails.

### Plane.so cleanup
- **Appetite:** SHAPE.
- **Hill position:** downhill.
- **Scopes:** t_7a3d1ac0 (charter, blocked on owner-yes); t_c767b035 / t_b7793762 / t_a9a40f6e (reassigned to quality-guardian; in flight); t_21b9771d (Paul-bundle HERM-76 done).
- **Blockers:** owner-yes on per-item action list (M2) and bundle (D = skipped).
- **Next step:** quality-guardian finishes the 7 Pierre M + 7 DEC mirror writes.
- **Healthy? 🟡:** in flight, paused once on owner-yes; resumed per Q1/Q2 = yes.

### SOUL apply chain
- **Appetite:** ongoing governance.
- **Hill position:** uphill.
- **Scopes:** t_97163869 (route-or-schedule) supersede-closed; t_8cb137f3 (no-trace) applied live; t_9faacc44 (QG review) retries-exhausted; t_39874290 (QG no-trace review) retries-exhausted.
- **Blockers:** scaffolding-rot reviews gating a stale sha.
- **Next step:** archive the stale reviews; do not re-attempt; collapse to `bos-comm-check` skill as the durable check.
- **Healthy? 🟡:** the rules landed on live SOUL; reviews are noise now.

(One block per initiative.)

```

## Pitfalls

- **Don't dump the kanban.** The overview is opinionated; raw card counts are not.
- **Don't quote the DEC list.** List DECs awaiting your yes; that's the 4-number owner's queue, not the whole decision log.
- **Don't lie about health.** 🟢 only when there's evidence on disk; default 🟡 if any uncertainty. Per house rule 8 (your summary never contradicts your artifact), health is a judgment backed by disk evidence.
- **Don't run on every chat exchange.** The overview is a scheduled or per-event task. A daily cron at 08:00 Europe/Berlin on `delivery-manager` is the planned cadence.
- **Don't lock this skill behind an approval gate.** The owner's standing rule (2026-09-29): "use both [subagents and profiles], but start with subagents. Don't create 6 profiles on day 1." This skill runs in the existing delivery-manager lane; no new profile.

## Verification

- File opens; ≤ 200 lines; executive section ≤ 30 lines.
- 4 numbers present and reconciled against `~/.hermes/kanban.db`.
- Each initiative section has a 1-line Next step.
- Health traffic light justified by a 1-line "Healthy?" sentence per initiative.

## Acceptance

- Single page output, ≤ 30 lines executive + ≤ 12 lines per hill-chart block.
- The owner reads it in Obsidian Mobile or Telegram; the executive section fits on one screen at default font.
- The 4 numbers are computed from current kanban.db, not from a cached snapshot.

## Change log

- 2026-10-08: v0.1.0. First version. Born from owner ask "executive overview on all initiatives that I would understand the health" + "hillchart progress summary per one initiative." Supersedes nothing; sits next to `bos-progress-report`.