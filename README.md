# JetThoughts Claude Code plugins

Marketplace repo. Install:

```bash
claude plugin marketplace add jetthoughts/claude-plugins
claude plugin install j-delivery@jetthoughts
claude plugin install unfix@jetthoughts
```

## j-delivery

The autonomous delivery contract (4-eyes, evidence standard, WIP=1) as a
load-on-demand skill, the `/deliver` kickoff command, the async-first SOP,
and the core author/verifier agent roster. The consuming repo's own
instructions (CLAUDE.md / AGENTS.md) override the plugin on every conflict -
the plugin is the default, never the authority.

Canonical origin: `jetthoughts/jetthoughts.github.io` ADR-0005; that repo
keeps its project-specific appendices (tool snapshot, domain map, gates).

Versioning: semver git tags; consumers upgrade deliberately via
`claude plugin update`. CHANGELOG per plugin.

## unfix

Jurgen Appelo's unFIX pattern library for organisation design - Bases, the
seven Crew types, Forums, Captains, Chiefs, Chairs, and the sixteen Role
Attributes - written from unfix.com rather than from a remembered summary.
Includes a section on applying it to an AI-agent organisation that separates
what transfers from what degenerates, because Chiefs are defined by
recruitment and compensation and agents have neither.

Use it for org structure, team topology, decision rights, reteaming, or
naming the seats in an agent org.

## Adding a skill to this repo

Skills authored for JetThoughts live here and are symlinked into
`~/.claude/skills/<name>`, so the repo is the single source of truth and the
skill still resolves at its usual path:

```bash
mkdir -p plugins/<name>/{.claude-plugin,skills}
mv ~/.claude/skills/<name> plugins/<name>/skills/<name>
ln -s "$PWD/plugins/<name>/skills/<name>" ~/.claude/skills/<name>
```

Then add `.claude-plugin/plugin.json`, a `CHANGELOG.md`, and an entry in
`.claude-plugin/marketplace.json`.

**Vault-coupled skills stay in the vault.** `jt`, `jt-exec-ops`,
`jt-research-brief` and `jt-sprint` read `~/Documents/pkm/.ai/state/*` and the
vault's notes; extracting them would leave a plugin that only works in one
checkout and split the content away from the repo that owns it.
