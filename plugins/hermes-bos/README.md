# hermes-bos

The Hermes Business OS standard operating procedures: the `bos-*` skills used by the Hermes
profiles (kanban-orchestrator, researcher, quality-guardian, delivery-manager).

Hermes reads them in place: every profile's `skills.external_dirs` includes
`/Users/pftg/dev/claude-plugins/plugins`. They are not in the Claude marketplace on purpose,
because they are Hermes procedures.

Moved here on 2026-09-24 (Paul: "we should have our skills in ~/dev/claude-plugin"). Before that
they lived only in `~/.config/skillshare/skills`, reached through the symlinks
`~/.hermes/skills/<name>` → `~/.agents/skills/<name>`, with no git history. Edits happen here;
a commit is the apply step.
