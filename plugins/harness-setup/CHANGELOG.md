# Changelog

## 0.1.0 - 2026-09-09

Initial candidate for an owner-supervised disposable trial.

- Explicit `setup` skill and callable `verify` helper.
- Read-only context auditor, public researcher, skill creator and control reviewer.
- Standard-library metadata scanner and restricted stage/check/diff/apply/rollback utility.
- Strict created-skill/agent frontmatter, drift checks and symlink/hardlink rejection.
- Unit and independent regression tests with scoped Linux/macOS CI.

No hooks, MCP servers, provider changes or autonomous installation are included.
Actual Claude model workflows and tool denials still require live acceptance tests.
