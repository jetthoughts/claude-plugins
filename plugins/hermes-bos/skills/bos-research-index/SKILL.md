---
name: bos-research-index
description: Maintain the research catalog INDEX.md — register new research entries, audit drift, repair links, verify retrieval coverage. Use when a research artifact is produced, when the catalog looks stale, or when agents cannot find known research.
version: 0.1.0
author: pftg
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, research, index, pkm, maintenance]
    related_skills: [bos-intake, bos-research, bos-daily-review]
---

# bos-research-index Skill

Maintains the single research catalog at
`~/dev/pkm/business-os/knowledge/research/INDEX.md` (flow doc:
`~/dev/pkm/business-os/strategy/opportunity-flow.md`). The INDEX is the lookup point
for humans and agents; this skill keeps it true.

## When to Use

1. **Register** — after any research artifact lands in `business-os/knowledge/research/`.
2. **Audit** — on daily review, when research seems unfindable, or after bulk research runs.
3. **Repair** — when the audit finds drift.

Do NOT use it to move or reorganize the 5 legacy archive homes — they are listed once
in the INDEX and left alone.

## Register a new research file

1. Verify the file is at `business-os/knowledge/research/YYYY-MM-DD-<slug>.md` with
   frontmatter: `type: Research`, `topics`, `applies_to`, `confidence`,
   `status: raw|consolidated|actioned|superseded`. Fill missing fields from the file
   content; if `applies_to` is unclear, leave `[TBD]` rather than inventing a link.
2. Add one line to the canonical table in INDEX.md: file, topics, applies_to, status.
3. If the file is a RAW dump (chat export, unprocessed): mark status `raw` and add a
   follow-up need (extract or archive) in the same table line.

## Drift audit (daily review / on demand)

Check, in order:

1. **Unindexed files** — `ls business-os/knowledge/research/*.md` minus INDEX table
   rows = unindexed. Register each (or delete only if trivially empty; owner deletes).
2. **Broken applies_to** — every wikilink in the table resolves to an existing vault
   note or task id. Broken link = repair the target name or mark `[TBD]`.
3. **Aging RAW entries** — `status: raw` older than 7 days: escalate to a kanban task
   (assignee researcher, triage) to extract or archive.
4. **Duplicate slugs** — two entries covering the same topic with different dates:
   keep newest as `consolidated`, mark older `superseded` with a note.
5. **Retrieval coverage** — spot-check one entry via qmd (`collections: pkm`) and
   openviking `find`; both should return INDEX.md content. Lag up to 24h is normal
   (qmd indexes on its own cadence); a miss older than that is a finding.

## Verification

- Every file in `business-os/knowledge/research/` has exactly one INDEX line.
- Every INDEX line's file exists and its wikilinks resolve.
- No file from the legacy archive homes or excluded dirs (`.worktrees`, `.paperclip`,
  `node_modules`, `readwise`, `~/.hermes/kanban/workspaces`) is registered as current.
- qmd query for the INDEX title returns `business-os/knowledge/research/INDEX.md`.

## Pitfalls

- Registering legacy/archive content as current research — the INDEX lists legacy homes
  once at the bottom, never per file.
- Inventing `applies_to` links — `[TBD]` is the honest marker; repair happens in audit.
- Editing the INDEX without this skill's drift rules — the table is a ledger; rows are
  appended/updated in place, never re-sorted by hand without a reason noted in the row.
