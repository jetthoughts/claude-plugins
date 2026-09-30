---
name: j-perplexity-sync
description: Pull Paul's recent Perplexity threads and Computer artifacts into the vault. Use when the user asks to sync, import, back up or save their Perplexity sessions, threads or researches (e.g. "sync my last 2 days of Perplexity", "import the Perplexity threads from this week"), or when a research pass needs Perplexity results that only exist in the Perplexity library. Acquires into `_inbox`, then hands off to j-inbox. Not for running new Perplexity searches (use j-perplexica-search or j-deep-research).
---

# Perplexity → vault sync

**Acquire → `_inbox` → call `j-inbox`.** This skill drives the logged-in agent browser (BrowserOS,
`mcp__browseros-neo__*`), reads each thread's answer pane as Markdown, writes it into the research
inbox, and then stops: **`j-inbox` owns the normalizer and the vault layout**, so this skill calls it
and never writes a vault note itself.

This skill only *reads*. Never launch a Perplexity run from here, and never in **Computer or
orchestrator mode** anywhere (Paul, 2026-09-03) — a new run uses **Search**, **Deep Research** or
**Model Counseling** only. Capturing `/computer/tasks/<uuid>` pages that already exist stays correct.

## Destination (owned by `j-inbox`)

The vault is `~/dev/pkm`. `j-inbox` is the layout authority; for Perplexity its contract is
`evidence/perplexity/<project>/pplx-<id8>-<slug>.md` (`sessions/` when the thread names no project),
plus a bullet in the hub `evidence/perplexity/perplexity-library.md`. The hub is the source of truth
for "already synced": `grep -o 'pplx-[0-9a-f]\{8\}' …/perplexity-library.md`. `j-triage` selects
exactly `evidence/perplexity/*/pplx-*.md`, so a note written anywhere else is invisible to triage —
do not state or invent another path. Inputs are staged at
`~/dev/pkm/research/_inbox/perplexity/`.

## Procedure

1. **Collect known ids** from the hub. Open `https://www.perplexity.ai/library` with
   `mcp__browseros-neo__run`, keeping one `session` for the whole run. Library rows are React
   data-table rows with no anchors: scroll the rows' scroll container to the end until the row count
   stops growing (never click a "load more"-looking control — it navigates away), then extract each
   `main [role="row"]` path. Rows are newest first; the last cell holds the age (`3h ago`, `1d ago`).
   The full extraction recipe and its quirks live in
   [references/browseros-driving.md](references/browseros-driving.md).
2. **Select** paths inside the requested window whose 8-char id prefix is not in the hub.
   `/computer/tasks/<uuid>` pages are read the same way as threads and tagged `computer-task`.
   A session is not fully synced until its **artifacts** are too, and one Perplexity conversation can
   span more than one task id — see [references/computer-artifacts.md](references/computer-artifacts.md).
3. **Fetch** in `run` batches of 3 (the run cap is 30 s; each page needs ~6 s): `newPage(url)`,
   sleep 5.5 s (9 s on a cold browser), `browser.read(pid, { selector: 'main' })`,
   `browser.pages.close(pid)`. Pages over 5,000 chars are saved by the tool to
   `~/.browseros/tool-output/read-*.md` (path in the returned string); shorter pages come back
   inline, so re-read them without the selector to force a saved file. If a pane shows only the
   query, retry once after 4 s, else record it under `skipped`.
4. **Stage** `research/_inbox/perplexity/<uuid>.md` with frontmatter `source: perplexity`,
   `source_id`, `url`, `date` (ISO; from the pane's `Sep 2, 5:01 PM` line, else from the library
   age), `title` (H1 or the query's first 60 chars, always double-quoted — the vault's commit hook
   rejects unquoted colons), `project:` (the pane's first line shows `[<Project>/](…/spaces/…)`; omit
   when absent), then the body with the tool's `UNTRUSTED_PAGE_CONTENT` marker lines removed
   (drop the two marker lines line-wise, never with a `.*?` span regex — it deletes the body).
   Never write into `_done/` or the vault root; the normalizer owns that.
5. **Hand off to `j-inbox`** — run its normalizer from the vault root:
   `python3 ~/.claude/skills/j-inbox/scripts/normalize.py ingest`, or this plugin's copy at the
   j-inbox skill's `scripts/normalize.py`. It writes the `pplx-*` note in the project folder, adds
   the hub bullet, and prints `skip` for an id the hub already has.
6. **Commit** from the vault root (`Sync Perplexity: N threads`); the post-commit hook indexes them.
   Then run `j-triage` on the new notes, or leave them for the next triage run.
7. **Report**: items synced, skipped (with reasons), `citations_preserved` values, and remind that
   the vault's post-commit hook indexes at most 25 files per commit.

## References

- [references/browseros-driving.md](references/browseros-driving.md) — driving BrowserOS neo from scripts (persistent MCP session, `evaluate`/`read` field quirks, SSE parsing)
- [references/computer-artifacts.md](references/computer-artifacts.md) — Computer artifacts (bulk download, same-named cards, filing per `j-triage` §Computer documents, Drive binaries)

## Budget and failure

- One evaluate for the library plus one `run` per 3 items; 25 items is about 10 calls.
- A Cloudflare challenge or a login page means the BrowserOS profile lost its Perplexity
  session: stop and ask Paul to log in there; do not try another fetcher.
- `_done/` is gitignored in the vault (raw inputs are transient; the normalized notes are the record).
- A single thread can also be exported by hand: main pane `Session actions` → `Export as Markdown`
  (official, no extension, no credits); drop the file into `research/_inbox/perplexity/` with
  `source: perplexity`. **Rename it to `<thread-uuid>.md` the moment it lands**: the export is named
  after the thread title, so two sessions with the same title (re-runs, "Site Rebranding" ×2, the
  `.Md` cards) get the same filename and the later one overwrites the earlier. The id is in the
  thread URL. Same rule for artifacts: never strip ` (n)` before hashing; a same-named file with a
  different hash is a different artifact, and the uuid or `content_hash` is the identity, never the title.
