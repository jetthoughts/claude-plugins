---
name: j-perplexity-sync
description: Pull Paul's recent Perplexity threads into the vault. Use when the user asks to sync, import, back up or save their Perplexity sessions, threads or researches (e.g. "sync my last 2 days of Perplexity", "import the Perplexity threads from this week"), or when a research pass needs Perplexity results that only exist in the Perplexity library. Not for running new Perplexity searches (use j-perplexica-search or j-deep-research).
---

# Perplexity → vault sync

Perplexity has no export API. The sync drives the logged-in agent browser (BrowserOS,
`mcp__browseros-neo__*`), reads each thread's answer pane as Markdown, drops it into the
research inbox, and runs the normalizer. Everything is idempotent: a watermark file skips
threads already synced, and the normalizer's content hash skips unchanged bodies.

Paths: inbox `~/Documents/pkm/research/_inbox/perplexity/`, watermark
`~/Documents/pkm/research/_state/perplexity.json` (`synced_ids`, `last_run`, `skipped`).

## Procedure

1. Read the watermark. Open `https://www.perplexity.ai/library` with `mcp__browseros-neo__run`
   (`browser.pages.newPage(url)`, keep the `session`). Library rows are React data-table rows with
   no anchors; get every row's path with `mcp__browseros-neo__evaluate` on that page: scroll the rows'
   scroll container to the end until the row count stops growing (never click buttons: a
   "load more"-looking control navigates away), then for each `main [role="row"]` walk its
   `__reactFiber$` props (≤6 parents) and regex `/(search|computer/tasks)/<uuid>`. Rows are newest
   first; the last cell holds the age (`3h ago`, `1d ago`). 25 rows was the whole library on 2026-09-03.
2. Keep paths inside the requested window that are not in `synced_ids`. `/computer/tasks/<uuid>` pages
   are read the same way as threads; tag them `computer-task`.
3. Fetch in `run` batches of 3 (the run cap is 30 s; each page needs ~6 s): `newPage(url)`, sleep
   5.5 s, `browser.read(pid, { selector: 'main' })`, `browser.pages.close(pid)`. Pages over 5,000 chars
   are saved by the tool to `~/.browseros/tool-output/read-*.md` (path in the returned string); shorter
   pages come back inline, so re-read them without the selector to force a saved file and cut the answer
   out from the first `[<Project>/](https://www.perplexity.ai/spaces/` anchor. If a pane shows only the
   query, retry once after 4 s, else record it under `skipped`.
4. Write `research/_inbox/perplexity/<uuid>.md` with frontmatter `source: perplexity`, `source_id`,
   `url`, `date` (ISO; from the pane's `Sep 2, 5:01 PM` line, else from the library age), `title`
   (H1 or the query's first 60 chars, always double-quoted: the vault's commit hook rejects unquoted
   colons), `tags: [perplexity, research]`, then the body with the tool's `UNTRUSTED_PAGE_CONTENT`
   marker lines removed.
5. Run `python3 ~/.claude/skills/j-research-inbox/scripts/normalize.py ingest`. Expect one `ok` per
   new item; `skip` means an identical body already exists.
6. Update the watermark: add the new IDs to `synced_ids`, set `last_run`, keep `skipped`.
7. Report: items synced, skipped (with reasons), `citations_preserved` values, and remind that the
   vault's post-commit hook indexes at most 25 files per commit.

## Budget and failure

- One evaluate for the library plus one `run` per 3 items; 25 items is about 10 calls.
- A Cloudflare challenge or a login page means the BrowserOS profile lost its Perplexity
  session: stop and ask Paul to log in there; do not try another fetcher.
- Never write into `research/_inbox/_done/` or the vault root directly; the normalizer owns that.
  `_done/` is gitignored in the vault (raw inputs are transient; the normalized notes are the record).
