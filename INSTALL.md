# JetThoughts Plugins — Install

Upstream: jetthoughts (marketplace.json). This repo distributes our skills.

## Claude Code / Codex / Cursor / Windsurf / Gemini / Antigravity

Bundle (B) + Marketplace (C):
- Each plugin dir has `.claude-plugin/plugin.json`
- Root `plugin.json`: name=jetthoughts, 11 plugins listed
- Symlink install (works in any harness using ~/.claude):
  for p in plugins/*/skills/*; do ln -sf $(pwd)/$p ~/.claude/skills/$(basename $p); done
  for a in plugins/*/agents/*.md; do ln -sf $(pwd)/$a ~/.claude/agents/$(basename $a .md); done
- Marketplace entry: ~/.claude/plugins/marketplaces/jetthoughts/

## Updating (2026-09-13)

- Symlink install: `git pull` is the update; the links point into the checkout, so edits are live in the next session.
- Marketplace install: plugins are cached copies. Bump `version` in the plugin's `plugin.json`, then `claude plugin marketplace update jetthoughts`; skills are invoked as `plugin:skill`.
- Paperclip seats: `paperclip-skills.json` maps catalog slug to file. Seats cannot see `~/.claude/skills`; the Platform Engineer's instrument sweep re-imports an entry when its file changed. Convention and reasons: NAMING.md § One home, two deliveries.
