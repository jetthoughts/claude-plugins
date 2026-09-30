# JetThoughts Plugins — Install

Upstream: jetthoughts (marketplace.json). This repo distributes our skills.

## Claude Code / Codex / Cursor / Windsurf / Gemini / Antigravity

Bundle (B) + Marketplace (C):
- Each plugin dir has `.claude-plugin/plugin.json`
- Root `plugin.json`: name=jetthoughts, 16 plugins listed
- Marketplace install (the supported path):
  claude plugin marketplace add /Users/pftg/dev/claude-plugins
  claude plugin install <plugin>@jetthoughts
- Marketplace entry: ~/.claude/plugins/marketplaces/jetthoughts/

**One delivery path, deliberately.** `NAMING.md` records why: five homes held 458
entries, two of them unversioned, and three edits to three house skills landed in three
different places. Delivery is therefore the marketplace only. `~/.claude/skills/` is not
a house-skill home, and `~/.config/skillshare/skills/_claude-plugins/` must not hold a
clone of this repo — that copy froze on 2026-09-24 and silently served pre-rename
skills to every session while the live repo moved on. Do not re-introduce symlinks or a
second checkout; verify with `python3 scripts/validate_skills.py` instead.

## Updating (2026-09-13, delivery decision 2026-09-30)

- Marketplace install: plugins are cached copies. Bump `version` in the plugin's `plugin.json`, then `claude plugin marketplace update jetthoughts`; skills are invoked as `plugin:skill`.
- Paperclip seats: `paperclip-skills.json` maps catalog slug to file. Seats cannot see `~/.claude/skills`; the Platform Engineer's instrument sweep re-imports an entry when its file changed. Convention and reasons: NAMING.md § One home, two deliveries.
