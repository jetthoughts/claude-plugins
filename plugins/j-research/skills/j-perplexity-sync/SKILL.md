---
name: j-perplexity-sync
description: Pull Paul's recent Perplexity threads into the vault. Use when the user asks to sync, import, back up or save their Perplexity sessions, threads or researches (e.g. "sync my last 2 days of Perplexity", "import the Perplexity threads from this week"), or when a research pass needs Perplexity results that only exist in the Perplexity library. Not for running new Perplexity searches (use j-perplexica-search or j-deep-research).
---

# Perplexity → vault sync

Perplexity has no export API. The sync drives the logged-in agent browser (BrowserOS,
`mcp__browseros-neo__*`), reads each thread's answer pane as Markdown, drops it into the
research inbox, and runs the normalizer. Everything is idempotent: a watermark file skips
threads already synced, and the normalizer's content hash skips unchanged bodies.

This skill only *reads*. Never launch a Perplexity run from here, and never in **Computer or
orchestrator mode** anywhere (Paul, 2026-09-03) — a new run uses **Search**, **Deep Research** or
**Model Counseling** only. Capturing `/computer/tasks/<uuid>` pages that already exist stays correct.

Paths: inbox `~/Documents/pkm/research/_inbox/perplexity/`; notes land in
`evidence/perplexity/<project>/pplx-<id8>-<slug>.md` (the vault's own convention, see its
AGENTS.md) and the hub `evidence/perplexity/perplexity-library.md` lists every captured id. The hub
is the source of truth for "already synced": `grep -o 'pplx-[0-9a-f]\{8\}' …/perplexity-library.md`.

## Procedure

1. Collect known ids from the hub. Open `https://www.perplexity.ai/library` with `mcp__browseros-neo__run`
   (`browser.pages.newPage(url)`, keep the `session`). Library rows are React data-table rows with
   no anchors; get every row's path with `mcp__browseros-neo__evaluate` on that page: scroll the rows'
   scroll container to the end until the row count stops growing (never click buttons: a
   "load more"-looking control navigates away), then for each `main [role="row"]` walk its
   `__reactFiber$` props (≤6 parents) and regex `/(search|computer/tasks)/<uuid>`. Rows are newest
   first; the last cell holds the age (`3h ago`, `1d ago`). 25 rows was the whole library on 2026-09-03.
2. Keep paths inside the requested window whose 8-char id prefix is not in the hub. `/computer/tasks/<uuid>` pages
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
   colons), `project:` (the pane's first line shows `[<Project>/](…/spaces/…)`; omit when absent →
   folder `sessions`), then the body with the tool's `UNTRUSTED_PAGE_CONTENT` marker lines removed.
5. Run `python3 ~/.claude/skills/j-research-inbox/scripts/normalize.py ingest`. It writes the
   `pplx-*` note in the project folder, adds the hub bullet, and prints `skip` for an id the hub
   already has.
6. Commit from the vault root (`Sync Perplexity: N threads`); the post-commit hook indexes them.
   Then run `j-research-triage` on the new notes, or leave them for the next triage run.
7. Report: items synced, skipped (with reasons), `citations_preserved` values, and remind that the
   vault's post-commit hook indexes at most 25 files per commit.

## Computer artifacts (files the tasks produced)

Artifacts are not on the thread pages and the Chrome "Perplexity Thread Exporter" does not export them.
They live at `https://www.perplexity.ai/computer/artifacts`, grouped by month, and download natively:

1. Open the page in BrowserOS, scroll to the bottom until every month group is rendered (they lazy-load).
2. Bulk: `act` click one card's `Select artifact` checkbox → a `Select all artifacts in <Month>` checkbox
   appears per group → tick the groups you want → `download` on the toolbar `Download` button. The tool
   captures one file; the rest land in `~/Downloads` as one file **per distinct filename** (same-named
   artifacts such as three `claude-code-business-os.md` or four `.Md` cards yield one file).
3. Same-named cards: per card, click its `Artifact options` → `Download` (the granular `download` tool
   on the menu item, or in `run` open the menu and press `ArrowDown`×(index+1), `Enter`). Cards whose menu
   has no `Download` item (`Generated Document`) cannot be exported; list them as skipped.
4. Stage the files: copy with names untouched (keep ` (n)` suffixes: stripping them made two different
   Business OS drafts overwrite each other on 2026-09-03), then dedupe by sha256. Filing is judgment work, not
   a script: an agent reads each artifact and files it per `j-research-triage` §Computer documents —
   project folder, `Belongs to`, link to the task that produced it (card menu `Open session` shows it),
   Takeaways, tier. Binaries (`.png/.zip/.pdf/.docx`) go to
   `~/Google Drive/My Drive/Documents/2. Resource/Perplexity artifacts/` and get a hub bullet with the path.
5. Commit in chunks of ≤25 files (the post-commit hook indexes at most 25 per commit).
   2026-09-03 baseline: 80 cards (Sep 41, Aug 7, Mar 34) → 64 vault files + 9 Drive files; 3 `Generated Document` cards not exportable.

## Budget and failure

- One evaluate for the library plus one `run` per 3 items; 25 items is about 10 calls.
- A Cloudflare challenge or a login page means the BrowserOS profile lost its Perplexity
  session: stop and ask Paul to log in there; do not try another fetcher.
- Never write into `research/_inbox/_done/` or the vault root directly; the normalizer owns that.
  `_done/` is gitignored in the vault (raw inputs are transient; the normalized notes are the record).
- A single thread can also be exported by hand: main pane `Session actions` → `Export as Markdown`
  (official, no extension, no credits); drop the file into `research/_inbox/perplexity/` with `source: perplexity`.
  **Rename it to `<thread-uuid>.md` the moment it lands**: the export is named after the thread title,
  so two sessions with the same title (re-runs, "Site Rebranding" ×2, the `.Md` cards) get the same
  filename and the later one overwrites the earlier — in `~/Downloads` the browser only adds ` (n)`.
  The id is in the thread URL. Same rule for artifacts: never strip ` (n)` before hashing; a same-named
  file with a different hash is a different artifact, and the uuid or `content_hash` is the identity, never the title.
