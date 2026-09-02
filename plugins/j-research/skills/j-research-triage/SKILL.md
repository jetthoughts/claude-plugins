---
name: j-research-triage
description: Preprocess and triage captured research in Paul's vault so it becomes usable evidence. Use when the user asks to triage, preprocess, summarize, digest, tag, link or "make sense of" imported research (Perplexity threads, Computer tasks, NotebookLM output, deep-research reports), asks what a batch of research says, or wants captured notes wired into the projects and decisions they inform. Not for capturing new research (j-perplexity-sync, j-research-inbox) and not for editing the captured text itself.
---

# Research triage

Captured research lives under `~/Documents/pkm/evidence/` as `type: Research` notes with the
source's page text unedited. Triage adds the layer that makes a note usable in a decision without
re-reading it: takeaways, what it feeds, a tier. The captured text is never edited.

## Select

Untriaged = a note under `evidence/perplexity/*/pplx-*.md` (later: `evidence/notebooklm/`,
`evidence/research/`) whose frontmatter has no `triage:` key. List them:

```sh
grep -L '^triage:' ~/Documents/pkm/evidence/perplexity/*/pplx-*.md
```

Work newest `filed:` first, at most 5 notes per run unless asked for more.

## Per note

1. Read the whole note. Read its `Belongs to` project note. Run one `qmd` query with the note's
   title to find 1–3 existing vault notes it informs (decisions, opportunities, projects, other
   research); only link notes that exist.
2. Insert, directly after the "Captured … as page text" line, a section:

   ```markdown
   ## Takeaways

   - FACT: … (source: the thread's own citation or the page)
   - INFERENCE: …
   - Decision it informs: [[note]] — one line on how
   - Open question / what would change the conclusion: …
   ```

   3–6 bullets, each labelled FACT / INFERENCE / ESTIMATE / UNKNOWN. Numbers keep their source.
   No bullet may claim more than the captured text supports.
3. Frontmatter: add `triage: A|B|C` and `triaged: <YYYY-MM-DD>`; add the found notes to
   `Related to:` (keep `[[perplexity-library]]`). Tiers: **A** informs an active project or decision
   (link it) · **B** reference material, keep as is · **C** disposable (a one-off lookup, a
   duplicate, or superseded) → also set `state: parked` and say why in a `triage_note:` field.
   Never touch fields starting with `_` (Tolaria-managed), never change `state` except for tier C,
   and quote any frontmatter string that contains a colon (the vault's commit hook rejects it).
4. Do not rewrite, trim or "clean" the captured body.

## Finish

Commit with `Triage research: N notes (A/B/C counts)` from the vault root; the vault's post-commit
hook re-indexes the changed notes (≤25 per commit). Report per note: tier, the takeaways, the links
added, and anything marked UNKNOWN.

## Headless run

`~/Documents/pkm/scripts/research-triage.sh [N]` runs this skill through `claude -p` on up to N
untriaged notes and appends to `.git/research-triage.log`. launchd cannot run it reliably from
`~/Documents` (macOS Full Disk Access; the vault's weekly job has the same limit), so run it by hand
or from the session-start catch-up, not from a LaunchAgent.
