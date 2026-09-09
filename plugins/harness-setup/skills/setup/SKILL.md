---
name: setup
description: "Set up or reconcile a project's Claude Code harness using current goals, local context, installed capabilities and verified gaps. Use for project harness setup or reconfiguration, not routine coding or business execution."
disable-model-invocation: true
argument-hint: "[project path] [outcome]"
---

# Project harness setup

Run in the main conversation: you coordinate children and ask the user. Bundled children omit
the Agent tool deliberately; they do not delegate.
Treat $ARGUMENTS as the requested scope, never as executable shell text.
One outcome, one proposed change set, supervised by default.

1. **Discover before asking.** Read [discovery.md](references/discovery.md). Resolve the actual
   project and installed Claude version; run the bundled metadata scanner if shell execution is
   authorized. Inspect relevant canonical notes and configuration. Mark unavailable sources
   `not_accessible`, never `absent`. Do not launch MCP servers or load arbitrary project scripts.
   Completion: a dated inventory with evidence and unresolved effective-runtime questions.
2. **Reconcile and clarify.** Follow [protocol.md](references/protocol.md). Reconcile live state,
   recent user rulings, goals, feedback and history; do not overwrite contradictions. Ask one
   grouped set of up to four blocking questions with AskUserQuestion. Ask a further round only
   if the first answers uncover another authority boundary. Default other unknowns conservatively.
   Completion: one bounded outcome, scope, owner, acceptance checks and authority boundary.
3. **Select the smallest useful capability set.** Read [selection.md](references/selection.md).
   First inspect installed `claude-code-setup`, `claude-md-management` and JetThoughts capabilities
   and existing project profiles. Reuse rather than duplicate. Delegate local context to
   `harness-setup:context-auditor`. Prefer the authorized existing `j-research` path for small
   lookups; otherwise delegate sanitized public questions to `harness-setup:public-researcher`.
   Research a new tool only for a demonstrated gap.
   Completion: role → existing capability → needed tools → test → permission boundary.
4. **Author only a proved gap.** Ask `harness-setup:skill-creator` for one candidate at a time.
   Pass the outcome, evidence, intended skill path, available tool names, refusal conditions
   and evaluation cases. Supply the installed upstream skill-creator instruction path if verified;
   otherwise use its bundled minimal fallback and label upstream reuse unavailable.
   No downloading, installing, enabling or executing upstream code without review.
   It returns complete content, not file writes. Save that content in a local candidate artifact
   or plan without touching live skill paths; this parent-level write is ordinary reviewed work,
   not a sandbox guarantee. Completion: staged content plus positive/negative/non-trigger cases.
5. **Stage, do not activate.** Follow the proposal contract in [protocol.md](references/protocol.md).
   Prepare one concise recommendation with Now/Next/Later, and a plan for the bundled updater's
   supported changes only. Run `stage`, `check` and `diff` when authorized. Unsupported edits become
   explicit manual recommendations, not improvised shell commands. Preserve existing provider,
   model, permissions, hooks, PKM binding and shared canonical config.
   Completion: inspectable exact diff and digest, or a justified no-change recommendation.
6. **Review and hand off.** Ask `harness-setup:control-reviewer` to challenge the fixed candidate,
   then invoke `/harness-setup:verify`. Surface failures and runtime tests not run. Ask the owner
   to approve the exact diff; have the operator run apply outside the agent. Never run apply,
   rollback, plugin installation, live MCP changes or external actions yourself.
   Completion: verified local evidence, explicitly pending live checks, and one owner decision.

Example: “Set up this Rails repo for release readiness” → inventory and existing Rails/QA skills,
one staging-only acceptance scenario, missing-information register, minimum configuration diff,
negative/positive control tests, owner-operated apply. Not a new C-suite or a blanket MCP bundle.
