# Harness Setup for Claude Code

Review-first setup for an existing project's AI harness, not a new orchestration platform.
Discover current capabilities, reconcile context, ask targeted questions, reuse existing skills,
draft one missing capability, and prepare an exact configuration diff for operator review.

Status: candidate for an owner-supervised disposable trial. Static and fixture tests do not prove
native model behavior, tool denials, spending limits or production readiness.

## Try without installing

Requires Python 3.10+ on Linux/macOS and a Claude Code installation supporting plugins and
subagents. Local tests need no Python packages or API credentials; model sessions use the
operator's existing Claude authentication and route.

From a reviewed repository checkout:

```sh
PLUGIN="$PWD/plugins/harness-setup"
python3 -B -m unittest discover -s "$PLUGIN/tests" -v
claude plugin validate --strict "$PLUGIN"
python3 "$PLUGIN/scripts/harness.py" scan --project /absolute/target/project
cd /absolute/target/project
claude --plugin-dir "$PLUGIN"
```

Then invoke `/harness-setup:setup` with one outcome. The first pass prepares a recommendation;
it does not apply configuration changes. User-level scanning requires explicit permission and
`--include-user`; the scanner never executes project commands or starts MCP servers.

For a reviewed installation from this marketplace:

```sh
claude plugin marketplace add jetthoughts/claude-plugins
cd /absolute/target/project
claude plugin install harness-setup@jetthoughts --scope project
```

Do not install alongside another copy of this plugin. Test the actual loaded version after
restart or reload; marketplace registration is a separate client configuration change.

## Components

| Component | Purpose |
| --- | --- |
| `/harness-setup:setup` | Explicit discovery, clarification, capability selection and proposal |
| `/harness-setup:verify` | Separate static/fixture evidence from actual runtime evidence |
| `context-auditor` | Local read-only context and capability reconciliation |
| `public-researcher` | Sanitized public research; no local file tools |
| `skill-creator` | Return skill content without write, shell, MCP or delegation tools |
| `control-reviewer` | Challenge the fixed proposal without modifying it |

Existing delivery, research, knowledge-base and control-plane tools are reuse candidates, not
dependencies. Keep the consuming project's approved context, provider route and canonical
configuration; research or author only a demonstrated gap.

## Review a restricted change

Inspect [examples/plan.json](examples/plan.json) for the exact plan shape. Bundles must be new,
private directories outside the target project, with an existing parent.

```sh
python3 "$PLUGIN/scripts/harness.py" stage \
  --project /absolute/project --plan /absolute/reviewed-plan.json \
  --out /absolute/private-review/new-bundle
python3 "$PLUGIN/scripts/harness.py" check --bundle /absolute/private-review/new-bundle
python3 "$PLUGIN/scripts/harness.py" diff --bundle /absolute/private-review/new-bundle
```

Only the operator runs the following after reviewing the exact diff and its SHA-256 digest:

```sh
python3 "$PLUGIN/scripts/harness.py" apply \
  --bundle /absolute/private-review/new-bundle --approve REVIEWED_SHA256
python3 "$PLUGIN/scripts/harness.py" rollback \
  --bundle /absolute/private-review/new-bundle --approve REVIEWED_SHA256
```

| Operation | Supported target |
| --- | --- |
| `managed_block` | Owned marker block in `CLAUDE.md`, preserving unrelated text |
| `json_merge` | `.claude/settings.json`: plugin enablement and ask/deny rules only |
| `create` | New `.claude/agents/<slug>.md`, `.claude/skills/<slug>/SKILL.md`, or its `references/<slug>.md` |

Dictionary keys merge recursively. Ask/deny arrays explicitly replace but must retain every
existing rule; removal is rejected. Created skills require matching `name`, JSON-double-quoted
`description`, `disable-model-invocation: true`, and optionally a quoted `argument-hint`.
Created agents require matching `name`, quoted `description`, and a comma-separated `tools`
subset of `Read, Glob, Grep, WebSearch, WebFetch`. Unknown fields and complex YAML are rejected.

Check/apply reject expired bundles after 24 hours, wrong digests, drift, symlinked paths and
hardlinked mutable targets. Rollback remains available after expiry but refuses intervening
edits. Existing files are never overwritten by `create`.

## Boundaries

- **No general installer:** no MCP configuration, global/local overrides, model/provider fields,
  permission allow-list edits, hook definitions, arbitrary scripts or deletion plans.
- **Plugin trust remains separate:** enabling an existing plugin can activate its own code/hooks.
  Permission-string semantics and untrusted Markdown prose still require review.
- **No OS sandbox:** a digest is integrity, not human authentication; same-privilege processes can
  bypass this utility. Parent-agent policy and human-operated apply are workflow conventions.
- **Bounded recovery:** per-file replacement and compensation for caught failures, not whole-tree
  atomicity, hostile-writer protection or crash-proof recovery. ACLs/xattrs are not preserved;
  rollback can leave empty directories.
- **Sensitive artifacts:** bundles contain complete selected-file before/after text and backups.
  Scan paths and identifiers are also private metadata; do not upload them automatically.
  Keep recommendations/plans in an operator-approved private directory outside the checkout,
  unless the consuming repository's Git exclusion for `.harness-setup/` is verified first.
  This plugin's own `.gitignore` does not protect another repository.

Shared or generated configuration must be updated at its canonical source through a separate
review. This plugin neither grants external-action authority nor enforces organization-wide
spending, release or WIP limits.

## Verification and release gate

Run the suite from a full repository checkout for the marketplace integration check:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s plugins/harness-setup/tests -v
claude plugin validate --strict plugins/harness-setup
claude plugin validate .
claude --plugin-dir "$PWD/plugins/harness-setup" plugin details harness-setup
```

An installed standalone plugin skips only the repository marketplace check. CI covers local
tests on Linux/macOS; it does not authenticate to Claude or run model evaluations.
The existing marketplace can produce version-specific warnings; compare them with the base
branch rather than treating this plugin's strict manifest check as marketplace-wide validation.
Before relying on controls, execute the positive and negative cases in
[runtime-checks.md](skills/verify/references/runtime-checks.md) in a disposable authenticated
project, verify actual child tool availability and unchanged routing, then trial one outcome.
