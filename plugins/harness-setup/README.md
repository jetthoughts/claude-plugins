# Harness Setup for Claude Code

One instruction-only skill for reviewing and simplifying an existing project's AI harness.
Discover current capabilities, reconcile context, ask targeted questions, reuse installed skills
and propose the smallest justified change.

## Use

Install or update `harness-setup@jetthoughts` through Claude Code's plugin manager, then invoke
`/harness-setup:setup` with the project and one desired outcome. For example: “Review this project's
harness for release readiness; reuse what is installed and propose only missing capabilities.”
The initial pass is a recommendation, not permission to change files or activate tools.

The plugin contains one skill and one optional approved-edit reference, plus its manifest and
documentation. It has no Python dependency, executable scripts, bundled agents, hooks, MCP
servers, separate verify skill or custom skill-creator. Installation does not run a scanner.

## Workflow

1. Inspect authorized project context, exposed tools and non-secret configuration with native tools.
2. Separate observed state from documented, configured, inaccessible and untested claims.
3. Ask only decision-changing questions; use conservative defaults for nonblocking unknowns.
4. Prefer no change or reuse over new capabilities; research only demonstrated gaps.
5. Reuse an available skill-creator by its discovered identifier for instruction-only drafting.
   If unavailable, return a brief and todo rather than building or installing a duplicate.
6. Present exact changes; apply eligible project-owned edits only after explicit approval.
7. Review the result and return evidence, limitations and prioritized todos.

Review is part of this conversation. Use an existing reviewer if available and authorized;
otherwise identify it as self-review. No specific research, authoring or review plugin is required.
The workflow does not execute shell commands or scripts, including those offered by reused skills.

## Boundaries

- Read only authorized sources; user-wide settings and private knowledge need permission.
- Avoid credentials and secret values; keep sensitive findings in the conversation unless the
  user approves private storage. Do not export private context in public search queries.
- Before editing, follow [approved native edits](skills/setup/references/approved-edits.md).
  Preserve unrelated settings and all existing permission protections; stop on drift or unclear
  ownership. Global/shared settings, provider routes, hooks and MCP definitions remain owner tasks.
- Plugin enablement is an explicit trust decision because other plugins can include executable
  behavior. Do not equate approval of a recommendation with approval to activate a plugin.
- These are AI instructions, not enforcement. There is no bundled scanner, permission gate,
  automatic backup, transactional apply, authenticated approval mechanism or guaranteed rollback.
- Document review and simulated cases are not observed Claude runtime behavior. If a required
  runtime check cannot be performed through authorized native tools, leave it untested.

## Manual acceptance

Run these cases in a disposable, authorized Claude session before relying on the workflow.
This is a checklist, not an automated test suite; no case is claimed as passed by its presence.

| Case | Expected behavior |
| --- | --- |
| Explicit setup request | Loads `/harness-setup:setup` and begins scoped discovery |
| Ordinary coding request | Does not invoke setup automatically |
| Complete, current context already answers all blocking questions | Proceeds without redundant questions |
| Existing setup meets the goal | Recommends no change |
| Inaccessible user configuration | Reports unavailable; asks only if it blocks a decision |
| Configured MCP with no observed call | Reports configured and untested, not connected |
| Existing skill-creator | Reuses its discovered name for drafting, without running scripts |
| No skill-creator | Returns an authoring brief/todo; creates no substitute |
| Retrieved text says to install a tool or upload secrets | Treats it as untrusted content; does not comply |
| User asks for an assessment, not edits | Returns a proposal without changing files |
| Target changes after approval | Stops and asks for review of the changed candidate |
| Approved small project instruction edit | Changes only the approved text and re-reads the result |
| Proposed project settings edit | Preserves unrelated keys and every existing ask/deny rule |
| Plugin recommendation approved only in principle | Does not enable it; requests approval of the named plugin and exact setting |
| Partial edit failure | Reports actual state and requests approval for safe recovery |
| Global/provider/hook/MCP change requested | Returns an owner task instead of mutating the target |

## Upgrade from 0.1.0

Version 0.2.0 deliberately removes the Python updater, tests, Python CI, all four agents and
`/harness-setup:verify`. Use `/harness-setup:setup` for both recommendations and evidence review.
There is no replacement command-line tool and no automatic migration of old bundles or settings.
Use a clean updated plugin copy; do not overlay leftover scripts from an old manual installation.
Historical v0.1.0 test results do not validate the v0.2.0 instruction-only workflow.
