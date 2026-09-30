# Operations

Which operation runs what — the workflow, skill or vault note it hands to.

| Operation | Runs |
| --- | --- |
| `next` | Read the Paperclip board (company JetThoughts, project *Job Seek Berlin*), take the top runnable card (`todo`, not blocked, earliest due), brief and run it, close the card with the check it names. Dispatch by hand — the `j-board-run` dispatcher is not installed (see Precedence) |
| `apply <url>` | **Load `jobseek-auto` and run the `jobseek-apply` workflow** with `{url, date}` — posting + company read, drafter, two cold-eyes lenses, staged to `drafter/_staged/` with a HANDOFF checklist. Stops at Paul's gate. (Was `j-apply-one-job`, which is not installed.) |
| `engage [company\|intake\|pick]` | One LinkedIn lane with Paul's gates: load the `j-linkedin-engage` skill. `intake` proposes lanes for newly applied companies (tracker + *Engage:* cards), `pick` finds today's post and drafts the comment for every lane at step 3. `next` uses the same skill whenever the top card sits in project *LinkedIn Engagement (Job Seek)* |
| `scan` | **Load `jobseek-auto` and run the `jobseek-sweep` workflow** with `{date, cadence}` — one agent per due channel, verifier dedup against the board, report + `state/` + vault mirror. Background and the board register: vault note `op-jobseek-source-and-qualify` — the boards come from the Drive register `22-job-boards_monitor.md` (Lane 1 weighted table, Lane 2 Rails section), never from memory; public boards via `lightpanda`, Cloudflare and login boards via BrowserOS neo, HN via the Algolia API |
| `conversation` | vault note `op-jobseek-prototype-conversation` |
| `prep` | vault note `op-jobseek-interview-rehearsal` |
| `review` | vault note `op-jobseek-weekly-review` |
