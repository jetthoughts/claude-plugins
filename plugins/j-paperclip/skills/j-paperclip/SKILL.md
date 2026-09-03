---
name: j-paperclip
description: How to operate the self-hosted Paperclip control plane from a session — reach the loopback API, list companies and agents, read and change an agent's model, adapter config and managed instruction bundle, create issues and wake an agent, check budgets and costs, and read run logs. Use whenever the user says Paperclip, the board on :3100, JET-<n> or JETA-<n>, agent company, Chief of Staff, Builder, Reviewer, Strategist, org chart, wake the agent, agent budget, agent instructions, AGENTS.md for an agent, desiredSkills, or asks why an agent did or did not do something. Also use before editing anything under ~/.infra/services/paperclip/data, and when a Paperclip API call returns "API route not found".
---

# Paperclip control plane

Paperclip runs the agent company: org chart, issues, budgets, heartbeats, approvals. The agents
it starts are real `claude` CLI processes. Board *process* rules live in the `board-flow` skill;
this skill is only about driving the machine. The board flow is the same six lists.

## Where it runs

| Thing | Value |
|---|---|
| URL | `http://127.0.0.1:3100` — loopback only, `local_trusted`, no login |
| Service | LaunchAgent `dev.pftg.paperclip` |
| Start / repair | `~/.infra/services/paperclip/bin/start` (installs the plist, waits for health) |
| Data | `~/.infra/services/paperclip/data` (embedded Postgres on 54329, run logs, company files) |
| Health | `curl -s localhost:3100/api/health \| jq .status` → `"ok"` |

There is no auth, so plain `curl` is the whole client. Do not add one.

## The one route trap

**Everything is under `/api`, and agents, issues and skills are scoped by company.**
`GET /api/agents` returns `{"error":"API route not found"}` — that is a wrong path, not a
broken server. Start from companies and walk down:

```bash
curl -s localhost:3100/api/companies | jq -r '.[] | "\(.id)  \(.name)"'
curl -s localhost:3100/api/companies/$C/agents | jq -r '.[] | "\(.id)  \(.name)  \(.adapterConfig.model)"'
```

Per-resource routes are flat once you have an id: `/api/agents/:id`, `/api/issues/:id`.

## Cheat sheet

| Job | Call |
|---|---|
| Companies | `GET /api/companies` |
| Agents in a company | `GET /api/companies/:companyId/agents` |
| One agent | `GET /api/agents/:id` · `GET /api/agents/:id/configuration` |
| Change an agent | `PATCH /api/agents/:id` |
| Managed instructions | `GET|PUT|DELETE /api/agents/:id/instructions-bundle/file` (PUT body `{path, content}`) |
| What skills an agent sees | `GET /api/agents/:id/skills` |
| Wake an agent | `POST /api/agents/:id/wakeup` — body optional; `source` defaults to `on_demand`, add `"forceFreshSession": true` to drop the resumed session |
| Issues | `GET /api/companies/:companyId/issues` · `POST` same path to create · `PATCH /api/issues/:id` |
| Comment | `GET|POST /api/issues/:id/comments` |
| Why is it stuck | `GET /api/issues/:id/diagnostics/blockers` · `/wakes` · `/recovery-actions` |
| Money | `GET /api/companies/:companyId/budgets/overview` · `/costs/summary` · `/costs/by-agent-model` |
| Budget limits | `PATCH /api/companies/:companyId/budgets` · `PATCH /api/agents/:agentId/budgets` |
| Company skill catalog | `GET|POST /api/companies/:companyId/skills` |

Fuller route map: [references/api.md](references/api.md). Amounts are **cents**.

## Changing an agent

Behaviour lives in two places and nowhere else: `adapterConfig` (what process starts) and the
managed instruction bundle (what it is told). Nothing else you edit will change what an agent does.

`PATCH /api/agents/:id` **replaces `adapterConfig` wholesale**. Read, modify one key, write back:

```bash
curl -s localhost:3100/api/agents/$A | jq '.adapterConfig
  | .model = "claude-opus-5"' > /tmp/cfg.json
jq -n --slurpfile c /tmp/cfg.json '{adapterConfig: $c[0]}' \
  | curl -s -X PATCH localhost:3100/api/agents/$A -H 'Content-Type: application/json' --data @-
```

Config changes are versioned: `GET /api/agents/:id/config-revisions` lists them, so a bad PATCH is
recoverable. Keys that matter: `model` (`claude-opus-5`, `claude-sonnet-5`; empty string means the CLI default),
`cwd` (the git worktree the agent works in), `maxTurnsPerRun` (the real cost dial),
`engine: "cli"`, `paperclipSkillSync.desiredSkills`.

The instruction bundle is a managed `AGENTS.md` per agent, appended to the agent's system prompt at
spawn. Rewrite it with `PUT .../instructions-bundle/file` and `{"path":"AGENTS.md","content":"..."}`,
then read it back and assert the old line is gone. A wakeup after the write is the only proof it took.

## Skills and MCP servers: they are already there

The `claude_local` adapter spawns the real CLI without `--setting-sources`, and passes
`--strict-mcp-config` **only when the company manages MCP servers of its own**. With none managed,
every agent inherits the full global skill set and every user-scope MCP server — measured at 882
skills and 43 servers in a live run.

So: **never import global skills into a company's catalog.** It creates same-name duplicates that
compete with the originals. `desiredSkills` is for Paperclip catalog skills only
(`paperclipai/...`). To make an agent *prefer* a tool, write the routing rule into its instruction
bundle — that is the only lever that works, because the tools are already in the process.

`tokensave` and `tolaria` announce but never resolve tools inside agent runs. Do not write
instructions that depend on them.

## Reading what happened

```
~/.infra/services/paperclip/data/instances/default/data/run-logs/<companyId>/<agentId>/<runId>.ndjson
```

One JSON object per line, the agent's whole turn stream. `GET /api/issues/:id/comments` is the
summary the agent chose to publish; the ndjson is what it actually did. Prefer the comments,
fall back to the log when the two disagree.

## Traps

- **The jt-lab guard hook scans command text, not the request target.** A `curl` whose *body*
  contains a URI or hostname is denied as "mutating HTTP request to a non-loopback host". Write the
  payload to a scratch file and post `--data @file`. This is the normal way to comment, not a
  workaround for a real block.
- **A wakeup on a busy agent is skipped, not queued.** The response says so. Check
  `GET /api/agents/:id/runtime-state` before concluding the change did not land.
- **Budget is per company and per agent, in cents.** An agent that stops mid-plan is usually out of
  budget or turns, not broken.
- **Restarting**: `launchctl kickstart -k gui/$(id -u)/dev.pftg.paperclip`, or run
  `~/.infra/services/paperclip/bin/start` which reinstalls the plist and waits for health. Never
  edit the plist in `~/Library/LaunchAgents` — it is generated from the repo template.
