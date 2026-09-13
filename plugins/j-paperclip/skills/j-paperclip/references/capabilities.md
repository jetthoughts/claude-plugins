# What Paperclip 2026.831.1 can do for us, and how we use each part

Read 2026-09-11 from the installed build (`/api/openapi.json`), the upstream docs (Context7 `/paperclipai/paperclip`, DeepWiki) and live tests on disposable cards. "Enforced" means the server refuses or redirects; "advisory" means a seat has to honour it. Every route below exists on this build; a route that does not is named in the last section.

## The rule for all of it

Use the native mechanism before writing a rule, and write a rule before writing a script (Paul, 2026-09-11: no ops scripts). Read the object back after every write; several of these normalise silently.

## 1. Execution policy: the completion gate (enforced for the executor)

`executionPolicy` is a field on the issue, set on create or by `PATCH /issues/:id`:

```json
{"executionPolicy":{"mode":"normal","commentRequired":true,"stages":[
  {"type":"review","participants":[{"type":"agent","agentId":"<Verifier>"}]},
  {"type":"approval","participants":[{"type":"user","userId":"<Paul>"}]}]}}
```

What it enforces (measured on JET-512): when the executor sets `status: done`, the runtime keeps the card `in_review`, sets `executionState.currentStageType` and hands it to the current participant. The participant decides with `PATCH /issues/:id {"status":"done","comment":"..."}` (approve) or `{"status":"in_progress","comment":"..."}` (changes requested, card returns to `returnAssignee`). A non-participant agent gets 422. `commentRequired` is always true.

What it does not: a board user with full rights can force `done` past a pending stage, and can `PATCH executionPolicy {"stages":[]}`, which normalises the policy to `null` (a stage with no valid participant is dropped; no stages, no policy). Read `executionPolicy` back after every write. It binds the workflow, not a document revision.

How we use it: every gated card (one that carries a `delegation-contract` document) gets a review stage held by the checker seat and an approval stage held by Paul (outward or phase-1 work) or the Chief of Staff (internal). Probe cards carry one approval stage held by Paul.

## 2. Approvals: a decision record with a free payload (enforced as a record, not as a gate)

`POST /companies/:c/approvals` `{"type":"request_board_approval","requestedByAgentId":null,"payload":{...},"issueIds":[...]}`, then `POST /approvals/:id/approve|reject|request-revision {"decisionNote"}` and `resubmit {"payload"}`. Types: `hire_agent`, `approve_ceo_strategy`, `budget_override_required`, `request_board_approval`. Resolving one wakes the requesting agent with `PAPERCLIP_APPROVAL_ID` and `PAPERCLIP_APPROVAL_STATUS`.

Nothing ties an approval to issue completion or to a document revision (measured: `done` succeeded with only a rejected and a stale approval linked). So we bind the revision ourselves: payload `{"kind":"artifact-acceptance","issueId","documentKey","revisionId","contract","checker","verdict","reason"}`, and whoever decides reads `GET /issues/:id/approvals` and `GET /issues/:id/documents/<key>` and closes only when the approved approval's `payload.revisionId` equals `latestRevisionId`. `DELETE /issues/:id/approvals/:approvalId` is in the spec but answers "API route not found".

## 3. Documents: revisioned artifacts with an optimistic lock (enforced)

`PUT /issues/:id/documents/:key {"title","format":"markdown","body","changeSummary","baseRevisionId"}`; `GET .../documents/:key` (field `body`, `latestRevisionId`, `latestRevisionNumber`, `updatedByAgentId`); `GET .../revisions`. A PUT whose `baseRevisionId` is stale returns 409 `Document was updated by someone else` with `currentRevisionId`; the document is untouched. That is the native "recovery preserves an intervening update". Documents are how a card carries its contract (`delegation-contract`), its artifact, and its evidence; comments are the story, documents are the record.

`GET /companies/:c/issues` returns descriptions cut at 1,200 characters. Read `GET /issues/:id` before quoting or editing one.

## 4. Interactions: typed questions to Paul (enforced resolver policy)

`POST /issues/:id/interactions` with kinds `ask_user_questions`, `request_confirmation`, `request_checkbox_confirmation`, `request_item_verdicts`, `suggest_tasks`; resolved by `.../accept|reject|respond|verdicts|withdraw|cancel`. `resolverPolicy` defaults to board-only except `ask_user_questions` (board or agents); anything with `payload.toolAction` is board-only. `continuationPolicy: wake_assignee` wakes the seat on resolution; `supersedeOnUserComment` expires the ask when the asker comments again (measured: an agent's own follow-up comment expired its own question). A pending interaction is a first-class waiting path for `in_review`.

How we use it: waiting on Paul is `in_review` plus one interaction; an ask in prose is not an ask.

A seat's `ask_user_questions` interaction is answered with `POST /issues/:id/interactions/:interactionId/respond {"answers":[{"questionId":"…","optionIds":["…"]}],"summaryMarkdown":…}` (measured 2026-09-12); a status change to `done` expires every open interaction on the card and removes Paul's reply box. A `request_board_approval` item is what puts Approve/Reject buttons on Paul's Decisions tab; an execution-policy approval stage shows him only a notice. Status cards compile again on the Summarizer (`project_primary`); "Job Seek — filled and filtered rows for Paul's re-review" (2b977154) is the live example: FILLED / FILTERED / OPEN CHECKS with every status word quoted from its source card.

## 5. Blockers, unblock descriptors, recovery (enforced liveness)

`blockedByIssueIds` (array replaces; include existing) and `unblockDescriptor {owner:{agentId|userId}, action}` are the only waiting paths for `blocked`; a blocked card with neither is `needs_attention`. Paperclip opens a `stranded_assigned_issue` recovery action when a card's assignee cannot run (paused seat), and it re-strands the card after every status change until the seat is live or the assignee released. Resolve with `POST /issues/:id/recovery-actions/resolve {"outcome":"restored|blocked|false_positive","sourceIssueStatus":"todo|done|in_review|blocked"}`. `GET /companies/:c/recovery-observability` is the weekly recovery counter (the goal-2 denominator). `GET /companies/:c/attention` is the human's queue.

How we use it: blocked cards go to `todo` with the assignee released before a seat is unpaused (Paul, 2026-09-11), with a "Run with:" comment; re-assign at unpause.

## 6. Monitors: one-shot deferred checks (enforced bounds)

`executionPolicy.monitor {nextCheckAt, notes, serviceName, externalRef, timeoutAt, maxAttempts, recoveryPolicy}` on an `in_progress` or `in_review` card. When due, the assignee is woken with `issue_monitor_due`; the monitor is cleared and must be re-armed; an exhausted monitor cannot be re-armed. This is the native way to wait for an external answer (an ATS mail, a deploy) without a routine.

## 7. Routines: recurring cards (enforced concurrency and catch-up)

`GET /companies/:c/routines`; each has `triggers` (`schedule` with `cronExpression` and `timezone`, `webhook`, `api`), `assigneeAgentId`, `projectId`, `concurrencyPolicy` (`coalesce_if_active` default: a new trigger attaches to the active issue; `skip_if_active`; `always_enqueue`), `catchUpPolicy` (`skip_missed`), and an `activityGatePolicy`. A routine creates an execution issue the seat processes on its heartbeat. `PATCH /routines/:id {"status":"paused"}` stops it; `POST /routines/:id/triggers` and `PATCH /routine-triggers/:id {"enabled"}` edit the schedule.

Trap measured 2026-09-11: `coalesce_if_active` does not cover a `blocked` card, so a routine firing into a paused seat piles up duplicates. Pause the routine when its seat is paused.

## 8. Budgets and cost ledger (enforced caps, wrong numbers)

`GET /companies/:c/budgets/overview`; `POST /companies/:c/budgets/policies {scopeType, scopeId, amount, hardStopEnabled, notifyEnabled, isActive}` upserts per scope; `PATCH /companies/:c/budgets` and `/agents/:id/budgets {budgetMonthlyCents}`. A hard stop pauses the scope. The ledger (`/costs/*`) prices every run through the gateway as Anthropic `metered_api` (JET-505), so its dollars are not evidence; OmniRoute's `call_logs` are. All policies deactivated 2026-09-11 (Paul).

## 9. Skills catalog and skill policy (enforced install, advisory content)

`POST /companies/:c/skills {name, slug, markdown, sharingScope}`; update served text with `PATCH .../skills/:id/files {"path":"SKILL.md","content"}` (PATCH `{markdown}` returns 200 and changes nothing); a seat lists `company/<companyId>/<slug>` in `adapterConfig.paperclipSkillSync.desiredSkills` and installs it on its next fresh run. `claude_local` seats also inherit `~/.claude/skills`. House rules travel this way to every adapter; the vault note is the original, the catalog copy is delivery.

## 10. Instruction bundles (managed text)

`GET /agents/:id/instructions-bundle` (files, metadata) and `GET|PUT /agents/:id/instructions-bundle/file?path=AGENTS.md` (`{"path","content"}`). The bundle loads on a fresh session only (`wakeup {"forceFreshSession":true}`). The canonical text is `jt/seats/<seat>.md` in the vault; the guard denies seats writing either the bundle on disk or the seat file.

## 11. Agents, permissions, hires (enforced permissions)

`GET /agents/:id/configuration` is the honest view (`GET /agents/:id` nulls `reportsTo`, `heartbeat`, `canCreateAgents`); `PATCH /agents/:id {adapterConfig}` (restore `modelProfiles.*.adapterConfig` first or the write fails). An agent token gets `deny_no_grant` on `agents:configure` (measured in a Captain run log). `POST /companies/:c/agent-hires` creates a seat `pending_approval` with `sourceIssueIds`. `pause`/`resume`/`wakeup`/`clear-error` per agent; a wakeup without an assignment has no issue and no workspace. A wakeup that should carry the card is `{"source":"assignment","reason":"issue_assigned","payload":{"issueId":…},"forceFreshSession":true}`. While any run holds the issue (`executionRunId` on the issue), every other seat's wake on it answers `skipped / issue_execution_deferred` and assignment changes fire nothing: cancel the holder first. **`terminate` is irreversible**: a terminated seat cannot be resumed, cleared or set idle (measured 2026-09-11, the Verifier had to be recreated). To stop a run, `POST /heartbeat-runs/:runId/cancel` or `PATCH /issues/:id {"interrupt": true}`, then pause the seat.

The model a claude_local seat rides is `adapterConfig.model`, passed as `ANTHROPIC_MODEL` at ACP startup **only when the seat env lacks that key** (`adapter-utils/dist/acpx-engine/execute.js:1117`). An `env.ANTHROPIC_MODEL` entry therefore silently overrides both the model field and a per-issue `assigneeAdapterOverrides.adapterConfig.model` (measured 2026-09-11: Paperclip logged the override, OmniRoute served the old lane). Removed from every seat that day; never add it back.

## 12. Workspaces and worktrees (enforced coherence)

A card runs only with an execution workspace; one is resolved from the card's project workspace at launch, and a card without a project dies with `workspace_validation_failed` (JET-409 owns the root cause). `adapterConfig.cwd` is deprecated (the UI says so): the run's directory is the card's execution workspace first, the configured `cwd` only when a run has no workspace (a manual wakeup, a project-less card), then the server's own cwd. So `cwd` is a fallback we never want to hit; every card carries a project. `adapterConfig.workspaceStrategy {"type":"git_worktree"}` gives each card its own worktree under `~/.infra/.paperclip/worktrees/`; the branch is cut once and never follows main. `GET /companies/:c/execution-workspaces`, `.../close-readiness`, `reconcile-branch`.

## 13. Tool gateway (exists, unused here)

`GET|POST /companies/:c/tools/policies` (allow, block, require_approval, trust_rule, rate_limit) govern MCP calls made through registered tool connections, with action requests a human approves. It covers MCP only, never Bash, Write or Edit; this company has zero connections and zero policies because seats load MCP servers directly. The jt-lab guard covers the rest.

## 14. Run logs and heartbeat runs (the record)

`GET /companies/:c/heartbeat-runs?limit=N` and `GET /issues/:id/runs` (both in the spec; `GET /agents/:id/runs` answers but is not in the spec); the log is `~/.infra/services/paperclip/data/instances/default/data/run-logs/<company>/<agent>/<run>.ndjson`. Line 2 (`acpx.session`) carries the harness model label and the cwd; the label is not the served model, OmniRoute's `call_logs` are. The run object has no model field.

## 15. Also on this build, not yet used

Decision queues, triage and training (`/companies/:c/decision-*`), stalled-review decisions (`POST /issues/:id/stalled-review-decision {action: approve|request_changes|send_back}`), work products and `review-document`, tree control previews, teams catalog (`/companies/:c/teams/catalog`), company export and import, secret proposals, inbox agent policy, cloud stacks, board chat.

## Not on this build

`/execution-policies` as a route (it is the field above); `DELETE /issues/:id/approvals/:id` (spec only); any approval-to-completion interlock; any revision binding on decisions.
