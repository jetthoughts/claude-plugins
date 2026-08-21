# JetThoughts Claude Code plugins

Marketplace repo. Install:

```bash
claude plugin marketplace add jetthoughts/claude-plugins
claude plugin install jt-delivery@jetthoughts
```

## jt-delivery

The autonomous delivery contract (4-eyes, evidence standard, WIP=1) as a
load-on-demand skill, the `/deliver` kickoff command, the async-first SOP,
and the core author/verifier agent roster. The consuming repo's own
instructions (CLAUDE.md / AGENTS.md) override the plugin on every conflict -
the plugin is the default, never the authority.

Canonical origin: `jetthoughts/jetthoughts.github.io` ADR-0005; that repo
keeps its project-specific appendices (tool snapshot, domain map, gates).

Versioning: semver git tags; consumers upgrade deliberately via
`claude plugin update`. CHANGELOG per plugin.
