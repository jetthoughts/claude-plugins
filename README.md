# JetThoughts Claude Code plugins

Marketplace repo. Install:

```bash
claude plugin marketplace add /Users/pftg/dev/claude-plugins
claude plugin install j-delivery@jetthoughts
claude plugin install j-unfix@jetthoughts
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

## j-unfix

Jurgen Appelo's unFIX pattern library for organisation design - Bases, the
seven Crew types, Forums, Captains, Chiefs, Chairs, and the sixteen Role
Attributes - written from unfix.com rather than from a remembered summary.
Includes a section on applying it to an AI-agent organisation that separates
what transfers from what degenerates, because Chiefs are defined by
recruitment and compensation and agents have neither.

Use it for org structure, team topology, decision rights, reteaming, or
naming the seats in an agent org.

## j-harness-setup

Project harness setup: discover current capabilities, reconcile context, ask targeted
questions, reuse installed skills and review changes before editing. Instruction-only —
no scripts, no generator, no MCP servers. Reuse an available skill-creator instead of
installing a duplicate.

```bash
claude plugin install j-harness-setup@jetthoughts --scope project
```

Invoke `/j-harness-setup:setup` with one project outcome. Installation is optional:
use a reviewed checkout with `claude --plugin-dir /absolute/path/to/plugins/j-harness-setup`
for a temporary trial. See [setup and safety boundaries](plugins/j-harness-setup/README.md).

This plugin currently ships **three** skills: `setup`, plus `omniroute-manager` and
`browseros-neo`, which are machine-environment skills that belong in their own plugin.
See `SKILLS_REVIEW.md` (T2.4) — the plugin README carries the same caveat.

## Adding a skill to this repo

Create the directory and the file — **never a symlink**:

```bash
mkdir -p plugins/<plugin>/skills/<skill>
$EDITOR plugins/<plugin>/skills/<skill>/SKILL.md
```

Then add or bump `plugins/<plugin>/.claude-plugin/plugin.json`, and make sure the plugin
is listed in `.claude-plugin/marketplace.json` and the root `plugin.json`.

**Do not symlink a skill into `~/.claude/skills`.** That was the documented recipe until
2026-09-30 and it produced 22 self-referential symlinks committed to git, a skill
discovered 592 times instead of 99 by anything that followed links, and a plugin cache
whose entries had *empty targets* — which is why several plugins reported
`failed to load`. Delivery is the marketplace only; `NAMING.md` and `INSTALL.md` carry
the reasoning.

Before committing:

```bash
python3 scripts/validate_skills.py     # 0 errors required
```

The same check runs in CI (`.github/workflows/validate-skills.yml`). Install it locally
with `bash scripts/install-hooks.sh`. All of the defects in `SKILLS_REVIEW.md` were
mechanically detectable, so this is what keeps them from coming back.

**Vault-coupled skills stay in the vault.** `jt`, `jt-exec-ops`,
`jt-research-brief` and `jt-sprint` read `~/dev/pkm/.ai/state/*` and the
vault's notes; extracting them would leave a plugin that only works in one
checkout and split the content away from the repo that owns it.
