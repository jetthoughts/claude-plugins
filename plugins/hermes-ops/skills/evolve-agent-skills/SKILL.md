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
4. **Score and patch.** Read the target skill against the rubric below, score 1–5 per row, and write the diff to the user as a patch. If the repo has the `evolution` Python package installed and configured (**verify first** with `python -c 'import evolution.skills; print("ok")'`), you may alternatively run `python -m evolution.skills.evolve_skill --skill <target>` and report its output instead.
5. Present a clean unified `diff` layout to the user.

## Rubric (score 1–5 per row)

| Row | What to check | 5 when |
|---|---|---|
| Freshness | Does the skill require dates on sources and reject undated snippets? | Yes, explicit, with a recency threshold |
| Novelty | Does the skill require ≥3 NEW findings not in the brief or prior research? | Yes, with a failure path (re-run, not relay) |
| Source diversity | Does the skill require 2+ independent domains per material claim? | Yes, with source-tier vocabulary |
| Tool fit | Does the skill use tools that are actually enabled in the profile's mcp_servers? | Yes, every named tool is verified callable |
| Clutter | Are multi-step checklists extracted from SOUL.md into the skill, and are stale notes pruned? | Yes, procedure lives in the skill, SOUL.md stays identity + stance |
| Verification | Does the skill name an explicit acceptance check (artifact exists, reads back, gate passes)? | Yes, one concrete check per procedure |

Score ≤ 2 on any row → that row is a candidate patch. Score ≤ 2 on three+ rows → propose a rewrite, not a patch.

- DO NOT overwrite `SOUL.md` or active skill files automatically without a binary user confirmation gate.
- Never write API keys or authorization bearer tokens into public-facing markdown documentation.
