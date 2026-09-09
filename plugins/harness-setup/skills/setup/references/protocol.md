# Reconciliation, proposal and approval protocol

## Clarification gate

Inspect first; do not ask for facts already established by current evidence. Maintain:

| Unknown | Source searched | Decision affected | Default | Blocking? |
| --- | --- | --- | --- | --- |
| Example: production release authority | Project brief, latest decision | May release be enabled? | No release | Yes for release, no for audit |

Ask only questions changing outcome, target root, authority, access, data boundary, paid
services/provider, review capacity or success/stop conditions. Say what was discovered before
asking about missing tools. Limit the first batch to four questions.

Default: one active outcome, local drafts, no external actions, no purchases, no new recurring
work, no production access, no provider changes, no global configuration edits. These are
workflow defaults, not machine-enforced limits.

## One decision packet

Treat recommendations and plans as sensitive. Use an operator-approved private directory outside
the checkout, or verify that the consuming repository excludes `.harness-setup/` from Git before
writing under `.harness-setup/candidates/<case>/`. The installed plugin's `.gitignore` does not
protect another repository. Do not silently edit ignore rules or include private artifacts in commits.

Write a single `recommendation.md` in that approved location, containing:

1. Outcome and acceptance check.
2. Current-system inventory, source dates, conflicts and unverified items.
3. Existing roles/capabilities to reuse and the smallest justified additions.
4. Clarifications, conservative assumptions and authority boundaries.
5. Exact proposed file changes with rationale and tool/skill provenance.
6. Enforcement matrix: carrier, trigger, state, rejecting mechanism, positive test, negative
   test, run evidence, expiry/version, status and bypass boundary.
7. Now/Next/Later, maximum three items each, each with owner, dependency and completion check.
8. One owner decision and rollback conditions.

Do not create live board tickets, agents or schedules. Keep later ideas as intent, not a backlog
of speculative subtasks. Paperclip remains the user's coordination layer where already adopted.

Use separate evidence labels:
`proposed`, `configured`, `static_pass`, `fixture_pass`, `runtime_pass`, `not_run`, `failed`.
Never collapse fixture tests into runtime_pass. Evidence for a test must bind the candidate digest,
Claude version, tool name, actual input/output, timestamp and relevant settings scope.

## Narrow updater boundary

The bundled updater only stages:
- A managed block in `CLAUDE.md`, preserving unrelated text.
- Project `enabledPlugins` and additional `permissions.ask`/`permissions.deny` entries.
- New agent Markdown or skill `SKILL.md`/reference Markdown.

New skills must be explicit-only and new agents must use the updater's read-only tool subset.
The CLI rejects complex or unknown native frontmatter, including hooks/model/permissionMode/MCP
configuration; it is not a general-purpose skill installer. Use the documented safe subset.

It does not configure MCP, install plugins, modify global/local overrides, delete old skills,
change models/providers, add hooks, execute tests from the project, or activate Paperclip.
Those changes require explicit manual follow-up with their own risk review and runtime proof.
Enabling a plugin can activate its code/hooks: review its source/version and trust before approval.

Generate a plan only after reading the bundled CLI `--help` and
[plan.json](../../../examples/plan.json).
Run stage/check/diff, not apply. A no-change result is valid; do not invent changes to fill a plan.

## Action boundary

The owner reviews the exact diff, provenance and current test evidence. Ask for approval of that
specific digest, not a general “set it up” authorization. The operator runs apply in their own
terminal. Re-check current state immediately before application; drift invalidates the proposal.
Restart/reload as required by the installed Claude version, then run the runtime acceptance cases.

The digest is an integrity token, not proof of human identity. Local scripts cannot prevent an
agent with the same operating-system privileges from directly editing settings or invoking apply.
For a hard separation, use an external approver and filesystem/container/managed-policy controls.
This plugin does not supply those controls.

If live tests fail, stop the affected capability. The operator can roll back only when the changed
files still match the applied candidate; otherwise preserve intervening edits and review a new diff.
Record observed outcomes, human interventions and escaped defects after the first bounded task.
Do not grant general autonomy merely because setup tests passed.
