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
