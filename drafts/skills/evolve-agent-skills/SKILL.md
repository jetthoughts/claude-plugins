---
name: evolve-agent-skills
description: Use when asked to optimize agent profiles, clean memory clutter, or review skill drift. Audits SOUL.md, MEMORY.md, and active skill files for redundancies, staleness, or hardcoded secrets, then proposes structured updates.
version: 0.1.0
author: default
platforms: [macos]
---

# SKILL: evolve-agent-skills

Trigger: "Optimize agent profile", "Clean memory clutter", "Review skill drift"

## Allowed Tools
- filesystem (read/write inside `~/.hermes/`)
- execute_code (for syntax testing)
- web_search (to check updated community standards)

## Procedure Steps

1. Execute `git status` or file checks across `~/.hermes/skills/` to pull target workflow definitions.
2. Read the latest session logs or `findings.md` to identify failed trajectories.
3. Isolate prompt clutter: Extract facts to `MEMORY.md` and multi-step checklists to individual `SKILL.md` files.
4. Execute `python -m evolution.skills.evolve_skill --skill [target]` if GEPA environment is active.
5. Present a clean unified `diff` layout to the user.

## Safety & Boundaries

- DO NOT overwrite `SOUL.md` or active skill files automatically without a binary user confirmation gate.
- Never write API keys or authorization bearer tokens into public-facing markdown documentation.
