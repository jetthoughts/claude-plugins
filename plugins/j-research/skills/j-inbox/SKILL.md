---
name: j-inbox
description: Save or publish research to Paul's Tolaria vault, and import research exports (Claude data export conversations.json, Perplexity/Perplexica/Gemini/NotebookLM Markdown exports, or hand-dropped Markdown/txt notes) into it. Use for "save/publish this research to my vault", "import my Claude/Perplexity/NotebookLM export", "process the research inbox", or when an agent (e.g. the local ldr MCP) has a finished research result to record.
---

# Research inbox normalizer

Converts research from various sources into one Markdown note per finding in the vault
(`~/dev/pkm`), idempotently. Canonical source of truth stays the git-tracked vault;
OpenViking indexes it separately.

## Directory layout (in the vault)

**This skill owns the vault's research layout contract.** `j-inbox` decides where a captured note
lands; `j-perplexity-sync` writes inputs and calls it, and `j-triage` reads what it produced. If
another skill's prose disagrees with the table below, this table wins.

```
research/_inbox/{perplexica,perplexity,claude,gemini,notebooklm,local}/   # drop exports here
research/_inbox/_done/<source>/                                          # processed inputs land here
research/quarantine/                                                     # failed inputs + <name>.reason.txt
```

Canonical destination per source type:

| Source (`source:`) | Destination | Notes |
|---|---|---|
| `perplexity` | `evidence/perplexity/<project>/pplx-<id8>-<slug>.md`, or `evidence/perplexity/sessions/` when the thread names no project | The one shape `j-triage` selects today. Also appends a bullet to the hub `evidence/perplexity/perplexity-library.md`. `id8` = first 8 hex chars of the Perplexity thread or task uuid; `kind: computer-task` for `/computer/tasks/<uuid>` captures. |
| `claude` | `research-claude-<slug>.md` (vault root) | One note per conversation from Claude's `conversations.json` export. |
| `gemini` | `research-gemini-<slug>.md` (vault root) | |
| `notebooklm` | `research-notebooklm-<slug>.md` (vault root) | `evidence/notebooklm/` is the planned home; **not migrated yet**. |
| `perplexica` | `research-perplexica-<slug>.md` (vault root) | Output of `j-perplexica-search`. |
| `local` | `research-local-<slug>.md` (vault root) | Ad-hoc synthesis and `j-research` "keep this" results. `evidence/research/` is the planned home; **not migrated yet**. |

Anything not in the table falls back to `research-<source>-<slug>.md` at the vault root. `<slug>` is
slugified from the title (or the source id), 60 characters max.

## Commands

```bash
python3 scripts/normalize.py ingest [--dry-run] [--vault PATH]
python3 scripts/normalize.py publish --source <s> --title <t> [--url <u>] [--tags a,b] < body.txt
```

`--vault` (or `RESEARCH_VAULT` env var) overrides the vault root. With neither set, `ingest` uses
the current working directory — run it from the vault root, `~/dev/pkm`.
`ingest` reads every file under `research/_inbox/<source>/` for the six known sources. Claude's
`conversations.json` export is split into one note per conversation (`chat_messages[].sender` /
`.text`); everything else is read as Markdown/txt with optional frontmatter (`source`,
`source_id`, `url`, `date`, `title`).

## Frontmatter contract

```yaml
type: Research
source: local
source_id: <input frontmatter source_id, or filename/conversation uuid>
date: <ISO date>
url: <if known>
tags: [a, b]
content_hash: <sha256 of the normalized body>
citations_preserved: true|false   # body contains at least one http(s) URL
imported: <ISO timestamp>
```
Body: an H1 title, then the content. `Related to:` wikilinks are not added automatically —
add them by hand when a note belongs to a project.

## Failure behaviour

Every file is handled independently. A failure (unparseable JSON, empty body, etc.) moves the
input to `research/quarantine/` with a sibling `<name>.reason.txt` and processing continues.
`ingest` exits 1 if anything was quarantined, 0 otherwise. Each processed item prints one line:
`ok|skip|quarantine  <path>`. `skip` means a note with the same `content_hash` already exists in
the vault — safe to re-run `ingest` on the same inbox.

Notes: `research/_inbox/_done/` is gitignored in the vault; input frontmatter `title` values containing a colon must be double-quoted or the vault's commit hook rejects the file.
