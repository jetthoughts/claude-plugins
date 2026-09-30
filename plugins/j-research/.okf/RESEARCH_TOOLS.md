---
type: Reference
title: Search & Research Tools Inventory
description: Pointer to the canonical search/research tool inventory, which lives in the j-research skill's references/
tags: [research, search, tools, inventory, mcp, consumer-ai, pointer]
generated:
  by: claude-code/snapshot
  at: 2026-09-29T00:00:00Z
verified:
  - by: human:pftg
    at: 2026-09-29T00:00:00Z
sources:
  - id: mcp-servers
    resource: mcp_list_servers
    title: MCP Server List
    author: system
    usage_count: 1
    usage_window:
      from: 2026-09-29T00:00:00Z
      to: 2026-09-29T00:00:00Z
  - id: tools-inventory
    resource: /Users/pftg/dev/claude-plugins/plugins/j-research/skills/j-research/references/tools-inventory.md
    title: Search & Research Tools Inventory (canonical copy)
    author: pftg
    usage_count: 1
    usage_window:
      from: 2026-09-30T00:00:00Z
      to: 2026-09-30T00:00:00Z
  - id: j-deep-research
    resource: /Users/pftg/dev/claude-plugins/plugins/j-research/skills/j-deep-research/SKILL.md
    title: Deep Research Skill
    author: pftg
    usage_count: 1
    usage_window:
      from: 2026-09-29T00:00:00Z
      to: 2026-09-29T00:00:00Z
---

# Search & Research Tools Inventory — pointer

The inventory is **not** duplicated in this bundle. Its one canonical copy is the skill reference

`plugins/j-research/skills/j-research/references/tools-inventory.md`

which the `j-research` front door reads at runtime. This OKF concept is a governed **pointer**: it
keeps the bundle's provenance and index intact without a second, drift-prone 27 KB copy.

- **Canonical:** `references/tools-inventory.md` in the `j-research` skill — every MCP server,
  consumer service, cost model, speed class and selection guide.
- **This file:** pointer only. Do not re-expand it with the inventory body.
- **Upkeep:** when the tool stack changes, edit the canonical reference and refresh the `verified:`
  date here.

Superseded 2026-09-30 — the bundle body was reduced to this pointer when the canonical copy moved
from the plugin root into the skill's `references/` directory. The retired `web-research-lanes` skill
was replaced by that skill's `references/consumer-lanes.md`.
