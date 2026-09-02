# Changelog — j-ideation

## 0.1.0 — 2026-09-02

Moved from `~/.infra/.claude/{skills,agents}` (commit 7c58c07 there) into this marketplace
so it installs globally and carries the `j-` prefix. Skill and agent names gained the prefix;
`/independent-ideation` is now `/j-independent-ideation`. The decision policy travels with the
router skill (`skills/j-independent-ideation/DECISION-POLICY.md`) and the validator runner is
`skills/j-independent-ideation/scripts/validate.sh`.

Install path assumed by the skills: `~/.claude/skills/j-*` (this repo's symlink convention, see
the root README). Installing only through `claude plugin install` puts the files under
`~/.claude/plugins/`; the `~/.claude/skills/...` paths in the agents then need symlinks too.
