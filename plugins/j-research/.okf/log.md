# Change Log

## 2026-09-30

**Bundle reduced to a pointer**
- Moved the canonical inventory out of the bundle to the `j-research` skill:
  `skills/j-research/references/tools-inventory.md` (was `plugins/j-research/RESEARCH_TOOLS.md`,
  now deleted; a repo-root draft copy had been removed earlier the same day)
- Reduced this bundle's `RESEARCH_TOOLS.md` to a governed pointer with its provenance intact —
  one canonical copy, no drift
- Retired the `web-research-lanes` skill; its content became
  `skills/j-research/references/consumer-lanes.md` and is referenced from the `j-research` front door

## 2026-09-29

**Bundle creation**
- Created OKF bundle for research tools inventory
- Added index.md with bundle structure and quick access
- Added RESEARCH_TOOLS.md with complete inventory:
  - 8 MCP tools (LDR, Wigolo, Exa, Tavily, You.com, Perplexica, Brave, OmniRoute)
  - 4 consumer AI services (Kimi, Qwen, Perplexity, DeepSeek)
  - Tool selection guides by speed, source type, cost, and use case
  - Cross-tool considerations (manual/autonomous, local/external, cache/fresh, ToS)
  - Browser rung priority for session-based services
- Integrated content from web-research-lanes skill (Kimi session procedures)
- Integrated content from j-deep-research skill (LDR specialist engines)
- Sources: MCP server list, web-research-lanes skill, j-deep-research skill
