# Changelog

## 0.4.0 - 2026-09-24

Assemble and validate one project's harness; ECC is the parts library.

- `setup` is the buy-first recipe: ask, research (blind brief, ≥3 NEW findings), pick (installed > the library registry, where ECC is one of many and ≥ 2 are compared per need > official > supported), copy picked pieces into `.claude/`, one entry point per goal, trial with `claude plugin eval init` plus `--ablation with-without`.
- Retired the 0.3.0 generator (`scripts/assemble_harness.py`) and the `harness` skill; backups are in (backup deleted 2026-09-24 per Paul: git only).
- Fixed: the kanban `reviewer=` claim (the field does not exist), the "nothing written into the target repo" contradiction (it is now: scratch copy until the trial passes and Paul approves), and the ECC `harness-audit` gate (it counts files; it is not a quality check).
- Run by the overseer session (Paul: "this is your responsibility"), not by Hermes.

## 0.2.0 - 2026-09-09

Breaking simplification to an instruction-only workflow.

- Keep one explicit setup skill; fold review and verification into the same conversation.
- Reuse an available skill-creator through its discovered name; do not bundle a duplicate.
- Remove all four agents, the separate verify skill, Python updater and tests, example plan,
  old scanner/proposal references and Python-specific CI.
- Replace updater instructions with optional, owner-approved native edits of project-owned files.
- Keep discovery, targeted clarification, existing-first recommendations, privacy boundaries,
  exact-change approval, verification honesty and prioritized todos.

The former updater commands, bundles, automatic backups and mechanical checks no longer exist.
Existing user-created bundles or project configuration are not removed or migrated automatically.
Use a clean plugin reload/update and the setup workflow; old verify/updater instructions no longer
apply. The historical test results below are not evidence for this instruction-only version.

## 0.1.0 - 2026-09-09

Initial candidate for an owner-supervised disposable trial.

- Explicit `setup` skill and callable `verify` helper.
- Read-only context auditor, public researcher, skill creator and control reviewer.
- Standard-library metadata scanner and restricted stage/check/diff/apply/rollback utility.
- Strict created-skill/agent frontmatter, drift checks and symlink/hardlink rejection.
- Unit and independent regression tests with scoped Linux/macOS CI.

No hooks, MCP servers, provider changes or autonomous installation are included.
Actual Claude model workflows and tool denials still require live acceptance tests.
