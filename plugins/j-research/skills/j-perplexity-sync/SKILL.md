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

1. Read the watermark. Open `https://www.perplexity.ai/library` in a new BrowserOS tab
   (`tabs action=new`, keep the returned `session`). Read `main` as markdown: rows carry the
   title and a relative age (`3h ago`, `1d ago`). Library rows are not anchors; get thread
   IDs from the sidebar instead: `read format=links selector=nav` lists
   `/search/<uuid>` links in the same recency order as the library.
2. Keep the `/search/<uuid>` IDs whose age is inside the requested window and that are not
   in `synced_ids`. `/computer/tasks/<uuid>` pages are a different page type; leave them out
   and record that in the report.
3. For each kept ID: `tabs action=new url=https://www.perplexity.ai/search/<uuid>
   background=true`, then `read format=markdown selector=main includeLinks=true`. Answers
   over 5,000 characters are saved by the tool to `~/.browseros/tool-output/read-*.md`; use
   that file as the body. The first line of the pane holds the query and the local time
   (`Sep 2, 5:01 PM`); take the date from it. If the pane shows only the query, the answer
   did not render: retry once after `wait for=time value=4000`, else add the ID to
   `skipped` with the reason.
4. Write `research/_inbox/perplexity/<uuid>.md` with frontmatter `source: perplexity`,
   `source_id`, `url`, `date` (ISO), `title` (the thread's H1 or the query's first 60
   chars, always double-quoted: the vault's commit hook rejects unquoted colons), `tags: [perplexity, research]`, then the body with the tool's
   `UNTRUSTED_PAGE_CONTENT` marker lines removed.
5. Run `python3 ~/.claude/skills/j-research-inbox/scripts/normalize.py ingest`. Expect one
   `ok` per new thread; `skip` means an identical body already exists.
6. Update the watermark: add the new IDs to `synced_ids`, set `last_run`, keep `skipped`.
7. Report: threads synced, skipped (with reasons), the notes' `citations_preserved` values,
   and remind that the vault's post-commit hook indexes at most 25 files per commit.

## Budget and failure

- One library read plus one tab and one read per thread; 15 threads is about 30 calls.
- A Cloudflare challenge or a login page means the BrowserOS profile lost its Perplexity
  session: stop and ask Paul to log in there; do not try another fetcher.
- Never write into `research/_inbox/_done/` or the vault root directly; the normalizer owns that.
  `_done/` is gitignored in the vault (raw inputs are transient; the normalized notes are the record).
