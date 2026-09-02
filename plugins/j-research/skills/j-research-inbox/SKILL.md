---
name: j-research-inbox
description: Save or publish research to Paul's Tolaria vault, and import research exports (Claude data export conversations.json, Perplexity/Perplexica/Gemini/NotebookLM Markdown exports, or hand-dropped Markdown/txt notes) into it. Use for "save/publish this research to my vault", "import my Claude/Perplexity/NotebookLM export", "process the research inbox", or when an agent (e.g. the local ldr MCP) has a finished research result to record.
---

# Research inbox normalizer

Converts research from various sources into one Markdown note per finding in the vault
(`~/Documents/pkm`), idempotently. Canonical source of truth stays the git-tracked vault;
OpenViking indexes it separately.

## Directory layout (in the vault)

```
research/_inbox/{perplexica,perplexity,claude,gemini,notebooklm,local}/   # drop exports here
research/_inbox/_done/<source>/                                          # processed inputs land here
research/quarantine/                                                     # failed inputs + <name>.reason.txt
research-<source>-<slug>.md                                              # output notes, at vault root
```

## Commands

```bash
python3 scripts/normalize.py ingest [--dry-run] [--vault PATH]
python3 scripts/normalize.py publish --source <s> --title <t> [--url <u>] [--tags a,b] < body.txt
```

`--vault` (or `RESEARCH_VAULT` env var) overrides the vault root; defaults to `~/Documents/pkm`.
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
