# Computer artifacts (files the tasks produced)

Companion detail for `j-perplexity-sync`. Artifacts are not on the thread pages and the Chrome
"Perplexity Thread Exporter" does not export them. They live at
`https://www.perplexity.ai/computer/artifacts`, grouped by month, and download natively.

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
   a script: an agent reads each artifact and files it per `j-triage` §Computer documents —
   project folder, `Belongs to`, link to the task that produced it (card menu `Open session` shows it),
   Takeaways, tier. Binaries (`.png/.zip/.pdf/.docx`) go to
   `~/Google Drive/My Drive/Documents/2. Resource/Perplexity artifacts/` and get a hub bullet with the path.
5. Commit in chunks of ≤25 files (the post-commit hook indexes at most 25 per commit).
   2026-09-03 baseline: 80 cards (Sep 41, Aug 7, Mar 34) → 64 vault files + 9 Drive files; 3 `Generated Document` cards not exportable.
