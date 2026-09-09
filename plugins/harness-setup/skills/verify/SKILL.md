---
name: verify
description: "Verify a staged Claude Code harness proposal with positive and negative control evidence. Use after project harness setup or configuration changes, not to claim autonomy from instructions or static checks alone."
disable-model-invocation: false
argument-hint: "[candidate bundle or recommendation path]"
---

# Verify a harness proposal

This read-only verification workflow may be invoked by the setup skill or explicitly by the user.
It does not authorize applying changes.

1. Resolve the fixed candidate and digest. Read its recommendation and exact diff; identify
   unsupported changes, permissions and environment assumptions. Do not mutate the candidate
   while reviewing it. Use the bundled updater's `check` for a staged bundle.
2. Run trusted bundled local tests and native plugin validation if shell execution is authorized.
   The plugin root contains `tests/`; do not execute newly discovered project or upstream scripts
   merely because their names contain “test”. Record command, exit code, version and timestamp.
3. Read [runtime-checks.md](references/runtime-checks.md) and evaluate each relevant control.
   A hand-fed event for any proposed external hook tests its function, not native registration.
   A matching file proves configuration, not tool connectivity or authorization.
4. Request `harness-setup:control-reviewer` from the main conversation for an independent review.
   Bundled subagents have no Agent tool; if already in one, return this request to the parent.
   Keep all model-dependent or inaccessible tests `not_run`, never inferred passing.
5. Return a concise go/no-go decision for the next bounded shadow run, the matrix of evidence,
   failures and untested controls, and at most three immediate fixes. Owner-operated installation,
   apply and live testing remain separate steps; passing this skill never authorizes them.

Completion: every claimed control has a scoped status and reproducible evidence; no fixture-only
control is described as runtime-enforced. Never promise spend caps, release blocking or unattended
autonomy unless the relevant external boundary was actually exercised.
