---
name: sync-perplexity
description: Sync Perplexity library threads into the vault. Arguments: optional window (e.g. "last 7 days", "last 2 days", "since 2026-09-01"), default "last 7 days".
---

Sync Perplexity threads per the `j-perplexity-sync` skill (invoke it now).

WINDOW: $ARGUMENTS

The skill drives BrowserOS to:
1. Read hub at `evidence/perplexity/perplexity-library.md` for already-synced IDs
2. Scrape library page for thread UUIDs in the requested window
3. Fetch each new thread's answer pane as Markdown
4. Write raw files to `research/_inbox/perplexity/<uuid>.md`
5. Run normalizer (`python3 ~/.claude/skills/j-inbox/scripts/normalize.py ingest`)
6. Report: synced count, skipped (with reasons), citations_preserved
7. Remind: post-commit hook indexes ≤25 files per commit

Artifacts: for every thread whose reply names a saved document, also fetch matching cards from `/computer/artifacts` by **task id** (never by title — titles repeat across unrelated tasks).

Optional window examples:
- `sync-perplexity last 7 days` (default)
- `sync-perplexity last 2 days`
- `sync-perplexity since 2026-09-01`