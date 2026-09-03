# Paperclip API route map

Generated from the running build's route handlers
(`~/.infra/services/paperclip/data/cli/current/node_modules/@paperclipai/server/dist/routes/*.js`).
Every path below is prefixed with `/api`. Grouped by handler file, so the file name tells you which
domain owns the route. Regenerate after a Paperclip upgrade with the command at the bottom.

## access

```
DELETE /board-api-keys/:keyId
GET /admin/users
GET /admin/users/:userId/company-access
GET /board-api-keys
GET /board-claim/:token
GET /cli-auth/challenges/:id
GET /cli-auth/me
GET /companies/:companyId/invites
GET /companies/:companyId/join-requests
GET /companies/:companyId/members
GET /companies/:companyId/user-directory
GET /invites/:token
GET /invites/:token/logo
GET /invites/:token/onboarding
GET /invites/:token/onboarding.txt
GET /invites/:token/skills/:skillName
GET /invites/:token/skills/index
GET /invites/:token/test-resolution
GET /skills/:skillName
GET /skills/available
GET /skills/index
PATCH /companies/:companyId/members/:memberId
PATCH /companies/:companyId/members/:memberId/permissions
PATCH /companies/:companyId/members/:memberId/role-and-grants
POST /admin/users/:userId/demote-instance-admin
POST /admin/users/:userId/promote-instance-admin
POST /board-api-keys
POST /board-claim/:token/claim
POST /bootstrap/claim
POST /cli-auth/challenges
POST /cli-auth/challenges/:id/approve
POST /cli-auth/challenges/:id/cancel
POST /cli-auth/revoke-current
POST /companies/:companyId/invites
POST /companies/:companyId/join-requests/:requestId/approve
POST /companies/:companyId/join-requests/:requestId/reject
POST /companies/:companyId/members/:memberId/archive
POST /companies/:companyId/openclaw/invite-prompt
POST /invites/:inviteId/revoke
POST /invites/:token/accept
POST /join-requests/:requestId/claim-api-key
PUT /admin/users/:userId/company-access
```

## activity

```
GET /companies/:companyId/activity
GET /companies/:companyId/audit/agent-actions
GET /companies/:companyId/audit/agent-actions.csv
GET /heartbeat-runs/:runId/issues
GET /issues/:id/activity
GET /issues/:id/runs
POST /companies/:companyId/activity
```

## adapters

```
DELETE /adapters/:type
GET /adapters
GET /adapters/:type
GET /adapters/:type/config-schema
GET /adapters/:type/ui-parser.js
PATCH /adapters/:type
PATCH /adapters/:type/override
POST /adapters/:type/reinstall
POST /adapters/:type/reload
POST /adapters/install
```

## agents

```
DELETE /agents/:id
DELETE /agents/:id/instructions-bundle/file
DELETE /agents/:id/keys/:keyId
GET /agents/:id
GET /agents/:id/config-revisions
GET /agents/:id/config-revisions/:revisionId
GET /agents/:id/configuration
GET /agents/:id/instructions-bundle
GET /agents/:id/instructions-bundle/file
GET /agents/:id/keys
GET /agents/:id/runtime-state
GET /agents/:id/skills
GET /agents/:id/task-sessions
GET /agents/me
GET /agents/me/inbox-lite
GET /agents/me/inbox/mine
GET /companies/:companyId/adapters/:type/detect-model
GET /companies/:companyId/adapters/:type/login-sessions/:sessionId
GET /companies/:companyId/adapters/:type/model-profiles
GET /companies/:companyId/adapters/:type/models
GET /companies/:companyId/agent-configurations
GET /companies/:companyId/agents
GET /companies/:companyId/claude-oauth-token-status
GET /companies/:companyId/heartbeat-runs
GET /companies/:companyId/live-runs
GET /companies/:companyId/org
GET /companies/:companyId/org.png
GET /companies/:companyId/org.svg
GET /companies/:companyId/setup-token-login-sessions/:sessionId
GET /companies/:companyId/setup-token-login-sessions/:sessionId/prompt
GET /heartbeat-runs/:runId
GET /heartbeat-runs/:runId/events
GET /heartbeat-runs/:runId/log
GET /heartbeat-runs/:runId/workspace-operations
GET /instance/scheduler-heartbeats
GET /issues/:issueId/active-run
GET /issues/:issueId/live-runs
GET /workspace-operations/:operationId/log
PATCH /agents/:id
PATCH /agents/:id/instructions-bundle
PATCH /agents/:id/instructions-path
PATCH /agents/:id/permissions
POST /agents/:id/approve
POST /agents/:id/claude-login
POST /agents/:id/clear-error
POST /agents/:id/config-revisions/:revisionId/rollback
POST /agents/:id/heartbeat/invoke
POST /agents/:id/keys
POST /agents/:id/pause
POST /agents/:id/resume
POST /agents/:id/runtime-state/reset-session
POST /agents/:id/skills/sync
POST /agents/:id/terminate
POST /agents/:id/wakeup
POST /companies/:companyId/adapters/:type/login-sessions
POST /companies/:companyId/adapters/:type/login-sessions/:sessionId/cancel
POST /companies/:companyId/adapters/:type/test-environment
POST /companies/:companyId/agent-hires
POST /companies/:companyId/agents
POST /companies/:companyId/setup-token-login-sessions
POST /companies/:companyId/setup-token-login-sessions/:sessionId/cancel
POST /companies/:companyId/setup-token-login-sessions/:sessionId/code
POST /companies/:companyId/setup-token-login-sessions/:sessionId/completion
POST /heartbeat-runs/:runId/cancel
POST /heartbeat-runs/:runId/watchdog-decisions
PUT /agents/:id/instructions-bundle/file
```

## approvals

```
GET /approvals/:id
GET /approvals/:id/comments
GET /approvals/:id/issues
GET /companies/:companyId/approvals
POST /approvals/:id/approve
POST /approvals/:id/comments
POST /approvals/:id/reject
POST /approvals/:id/request-revision
POST /approvals/:id/resubmit
POST /companies/:companyId/approvals
```

## assets

```
GET /assets/:assetId/content
POST /companies/:companyId/assets/images
POST /companies/:companyId/logo
```

## attention

```
GET /companies/:companyId/attention
```

## auth

```
GET /get-session
GET /profile
PATCH /profile
```

## board-chat

```
POST /board/chat/stream
```

## built-in-agents

```
GET /companies/:companyId/built-in-agents
GET /companies/:companyId/built-in-agents/:key/status
POST /companies/:companyId/built-in-agents/:key/provision
POST /companies/:companyId/built-in-agents/:key/reconcile
POST /companies/:companyId/built-in-agents/:key/reset
POST /companies/:companyId/built-in-agents/:key/routines/:routineKey/disable
POST /companies/:companyId/built-in-agents/:key/routines/:routineKey/enable
POST /companies/:companyId/built-in-agents/:key/routines/:routineKey/run
```

## cases

```
DELETE /cases/:id/documents/:key
GET /cases/:id
GET /cases/:id/documents/:key
GET /cases/:id/documents/:key/annotations
GET /cases/:id/documents/:key/annotations/:threadId
GET /cases/:id/documents/:key/revisions
GET /cases/:id/events
GET /companies/:companyId/cases
GET /issues/:issueId/cases
PATCH /cases/:id
PATCH /cases/:id/documents/:key/annotations/:threadId
POST /cases/:id/attachments
POST /cases/:id/documents/:key/annotations
POST /cases/:id/documents/:key/annotations/:threadId/comments
POST /cases/:id/documents/:key/lock
POST /cases/:id/documents/:key/revisions/:revisionId/restore
POST /cases/:id/documents/:key/unlock
POST /cases/:id/links
POST /companies/:companyId/cases
PUT /cases/:id/documents/:key
```

## cloud

```
GET /stacks
```

## companies

```
DELETE /:companyId
GET /
GET /:companyId
GET /:companyId/artifacts
GET /:companyId/export/fidelity
GET /:companyId/feedback-traces
GET /:companyId/timeline
GET /import/jobs/:jobId
GET /issues
GET /stats
PATCH /:companyId
PATCH /:companyId/branding
POST /
POST /:companyId/archive
POST /:companyId/export
POST /:companyId/exports
POST /:companyId/exports/preview
POST /:companyId/imports/apply
POST /:companyId/imports/preview
POST /import/preview
```

## company-skill-policy

```
DELETE /companies/:companyId/skill-policy
GET /companies/:companyId/skill-policy
POST /companies/:companyId/skill-policy/evaluate
PUT /companies/:companyId/skill-policy
```

## company-skills

```
DELETE /companies/:companyId/skill-test-run-templates/:templateId
DELETE /companies/:companyId/skills/:skillId
DELETE /companies/:companyId/skills/:skillId/comments/:commentId
DELETE /companies/:companyId/skills/:skillId/files
DELETE /companies/:companyId/skills/:skillId/star
DELETE /companies/:companyId/skills/:skillId/test-inputs/:inputId
DELETE /companies/:companyId/skills/:skillId/test-runs/:runId
GET /companies/:companyId/skill-test-run-templates
GET /companies/:companyId/skills
GET /companies/:companyId/skills/:skillId
GET /companies/:companyId/skills/:skillId/comments
GET /companies/:companyId/skills/:skillId/files
GET /companies/:companyId/skills/:skillId/fork-precheck
GET /companies/:companyId/skills/:skillId/test-inputs
GET /companies/:companyId/skills/:skillId/test-runs
GET /companies/:companyId/skills/:skillId/test-runs/:runId
GET /companies/:companyId/skills/:skillId/update-status
GET /companies/:companyId/skills/:skillId/versions
GET /companies/:companyId/skills/:skillId/versions/:versionId
GET /companies/:companyId/skills/categories
GET /skills/catalog
GET /skills/catalog/:catalogId
GET /skills/catalog/:catalogId/files
PATCH /companies/:companyId/skill-test-run-templates/:templateId
PATCH /companies/:companyId/skills/:skillId
PATCH /companies/:companyId/skills/:skillId/comments/:commentId
PATCH /companies/:companyId/skills/:skillId/files
PATCH /companies/:companyId/skills/:skillId/test-inputs/:inputId
POST /companies/:companyId/skill-test-run-templates
POST /companies/:companyId/skills
POST /companies/:companyId/skills/:skillId/audit
POST /companies/:companyId/skills/:skillId/comments
POST /companies/:companyId/skills/:skillId/fork
POST /companies/:companyId/skills/:skillId/install-update
POST /companies/:companyId/skills/:skillId/rename
POST /companies/:companyId/skills/:skillId/reset
POST /companies/:companyId/skills/:skillId/star
POST /companies/:companyId/skills/:skillId/test-inputs
POST /companies/:companyId/skills/:skillId/test-runs
POST /companies/:companyId/skills/:skillId/test-runs/:runId/cancel
POST /companies/:companyId/skills/:skillId/versions
POST /companies/:companyId/skills/browse-project
POST /companies/:companyId/skills/import
POST /companies/:companyId/skills/install-catalog
POST /companies/:companyId/skills/scan-projects
```

## costs

```
GET /companies/:companyId/budgets/overview
GET /companies/:companyId/costs/by-agent
GET /companies/:companyId/costs/by-agent-model
GET /companies/:companyId/costs/by-biller
GET /companies/:companyId/costs/by-project
GET /companies/:companyId/costs/by-provider
GET /companies/:companyId/costs/finance-by-biller
GET /companies/:companyId/costs/finance-by-kind
GET /companies/:companyId/costs/finance-events
GET /companies/:companyId/costs/finance-summary
GET /companies/:companyId/costs/quota-windows
GET /companies/:companyId/costs/summary
GET /companies/:companyId/costs/window-spend
GET /issues/:id/cost-summary
PATCH /agents/:agentId/budgets
PATCH /companies/:companyId/budgets
POST /companies/:companyId/budget-incidents/:incidentId/resolve
POST /companies/:companyId/budgets/policies
POST /companies/:companyId/cost-events
POST /companies/:companyId/finance-events
```

## dashboard

```
GET /companies/:companyId/dashboard
GET /companies/:companyId/recovery-observability
```

## decision-queues

```
DELETE /companies/:companyId/decision-queues/:key/items/:sourceKind/:sourceId
GET /companies/:companyId/decision-queue-seed-rules
GET /companies/:companyId/decision-queues
GET /companies/:companyId/decision-queues/:key/items
GET /companies/:companyId/decision-triage/:sourceKind/:sourceId
PATCH /companies/:companyId/decision-queues/:key
PATCH /companies/:companyId/decision-retention/:sourceKind/:sourceId
POST /companies/:companyId/decision-queues
POST /companies/:companyId/decision-queues/:key/items
POST /companies/:companyId/decision-retention/:sourceKind/:sourceId/archive
POST /companies/:companyId/decision-retention/:sourceKind/:sourceId/revive
PUT /companies/:companyId/decision-triage/:sourceKind/:sourceId
```

## decision-training

```
DELETE /decision-training/:id
GET /companies/:companyId/decision-training
GET /companies/:companyId/decision-training/export.jsonl
GET /decision-training/:id
PATCH /decision-training/:id
POST /companies/:companyId/decision-training
POST /companies/:companyId/decision-training/preview
```

## decisions

```
GET /companies/:companyId/decisions
GET /companies/:companyId/decisions/stats
GET /decisions/:id
POST /companies/:companyId/decision-archive-proposals
POST /companies/:companyId/decision-bundles
POST /companies/:companyId/decisions
POST /decisions/:id/cancel
POST /decisions/:id/decide
POST /decisions/:id/dismiss
```

## environments

```
DELETE /environments/:environmentId/custom-image-template
DELETE /environments/:id
GET /companies/:companyId/environments
GET /companies/:companyId/environments/capabilities
GET /environment-custom-image-setup-sessions/:sessionId
GET /environment-leases/:leaseId
GET /environments/:environmentId/custom-image-template
GET /environments/:id
GET /environments/:id/delete-blast-radius
GET /environments/:id/leases
GET /environments/:id/secret-refs
PATCH /environments/:id
POST /companies/:companyId/environments
POST /companies/:companyId/environments/probe-config
POST /environment-custom-image-setup-sessions/:sessionId/cancel
POST /environment-custom-image-setup-sessions/:sessionId/finish
POST /environment-custom-image-setup-sessions/:sessionId/terminal-session-token
POST /environments/:environmentId/custom-image-setup-sessions
POST /environments/:environmentId/custom-image-template/relink
POST /environments/:environmentId/custom-image-template/rollback
POST /environments/:id/probe
```

## execution-workspaces

```
GET /companies/:companyId/execution-workspaces
GET /companies/:companyId/workspace-overview
GET /execution-workspaces/:id
GET /execution-workspaces/:id/close-readiness
GET /execution-workspaces/:id/workspace-operations
PATCH /execution-workspaces/:id
POST /execution-workspaces/:id/login-handoff
POST /execution-workspaces/:id/reconcile-branch
POST /execution-workspaces/:id/runtime-commands/:action
POST /execution-workspaces/:id/runtime-services/:action
```

## file-resources

```
GET /issues/:issueId/file-resources/content
GET /issues/:issueId/file-resources/list
GET /issues/:issueId/file-resources/resolve
POST /issues/:issueId/file-resources/availability
```

## folders

```
DELETE /companies/:companyId/folders/:folderId
GET /companies/:companyId/folders
PATCH /companies/:companyId/folders/:folderId
POST /companies/:companyId/folders
POST /companies/:companyId/folders/:folderId/move
POST /companies/:companyId/folders/ensure-my
POST /companies/:companyId/folders/items/move
```

## goals

```
DELETE /goals/:id
GET /companies/:companyId/goals
GET /goals/:id
PATCH /goals/:id
POST /companies/:companyId/goals
```

## health

```
GET /
POST /dev-server/restart
```

## inbox-agent-policy

```
GET /companies/:companyId/users/:userId/inbox-agent-policy
GET /companies/:companyId/users/me/inbox-agent-policy
PUT /companies/:companyId/users/:userId/inbox-agent-policy
PUT /companies/:companyId/users/me/inbox-agent-policy
```

## inbox-dismissals

```
DELETE /companies/:companyId/inbox-dismissals/:itemKey
GET /companies/:companyId/inbox-dismissals
POST /companies/:companyId/inbox-dismissals
```

## instance-database-backups

```
POST /instance/database-backups
```

## instance-settings

```
GET /instance/settings
GET /instance/settings/experimental
GET /instance/settings/general
PATCH /instance/settings
PATCH /instance/settings/experimental
PATCH /instance/settings/general
POST /instance/settings/experimental/issue-graph-liveness-auto-recovery/preview
POST /instance/settings/experimental/issue-graph-liveness-auto-recovery/run
```

## issue-tree-control

```
GET /issues/:id/tree-control/state
GET /issues/:id/tree-holds
GET /issues/:id/tree-holds/:holdId
POST /issues/:id/tree-control/preview
POST /issues/:id/tree-holds
POST /issues/:id/tree-holds/:holdId/release
```

## issues

```
DELETE /attachments/:attachmentId
DELETE /issues/:id
DELETE /issues/:id/approvals/:approvalId
DELETE /issues/:id/comments/:commentId
DELETE /issues/:id/documents/:key
DELETE /issues/:id/inbox-archive
DELETE /issues/:id/read
DELETE /issues/:id/watchdog
DELETE /labels/:labelId
DELETE /work-products/:id
GET /attachments/:attachmentId/content
GET /companies/:companyId/issues
GET /companies/:companyId/issues/count
GET /companies/:companyId/labels
GET /companies/:companyId/search
GET /companies/:companyId/search/extract
GET /feedback-traces/:traceId
GET /feedback-traces/:traceId/bundle
GET /issues
GET /issues/:id
GET /issues/:id/accepted-plan-decompositions
GET /issues/:id/approvals
GET /issues/:id/attachments
GET /issues/:id/comments
GET /issues/:id/comments/:commentId
GET /issues/:id/diagnostics/blockers
GET /issues/:id/diagnostics/subtree
GET /issues/:id/diagnostics/wakes
GET /issues/:id/documents
GET /issues/:id/documents/:key
GET /issues/:id/documents/:key/annotations
GET /issues/:id/documents/:key/annotations/:threadId
GET /issues/:id/documents/:key/revisions
GET /issues/:id/external-object-summary
GET /issues/:id/external-objects
GET /issues/:id/feedback-traces
GET /issues/:id/feedback-votes
GET /issues/:id/heartbeat-context
GET /issues/:id/interactions
GET /issues/:id/recovery-actions
GET /issues/:id/watchdog
GET /issues/:id/work-products
PATCH /issues/:id
PATCH /issues/:id/documents/:key/annotations/:threadId
PATCH /work-products/:id
POST /companies/:companyId/issues
POST /companies/:companyId/issues/:issueId/attachments
POST /companies/:companyId/issues/external-object-summaries
POST /companies/:companyId/labels
POST /issues/:id/accepted-plan-decompositions
POST /issues/:id/admin/force-release
POST /issues/:id/approvals
POST /issues/:id/checkout
POST /issues/:id/children
POST /issues/:id/comments
POST /issues/:id/documents/:key/annotations
POST /issues/:id/documents/:key/annotations/:threadId/comments
POST /issues/:id/documents/:key/lock
POST /issues/:id/documents/:key/revisions/:revisionId/restore
POST /issues/:id/documents/:key/unlock
POST /issues/:id/external-objects/refresh
POST /issues/:id/feedback-votes
POST /issues/:id/inbox-archive
POST /issues/:id/interactions
POST /issues/:id/interactions/:interactionId/accept
POST /issues/:id/interactions/:interactionId/cancel
POST /issues/:id/interactions/:interactionId/reject
POST /issues/:id/interactions/:interactionId/respond
POST /issues/:id/interactions/:interactionId/verdicts
POST /issues/:id/interactions/:interactionId/withdraw
POST /issues/:id/low-trust/promotions
POST /issues/:id/monitor/check-now
POST /issues/:id/read
POST /issues/:id/recovery-actions/resolve
POST /issues/:id/release
POST /issues/:id/scheduled-retry/retry-now
POST /issues/:id/stalled-review-decision
POST /issues/:id/work-products
POST /issues/:id/work-products/:workProductId/review-document
PUT /issues/:id/documents/:key
PUT /issues/:id/watchdog
```

## llms

```
GET /llms/agent-configuration.txt
GET /llms/agent-configuration/:adapterType.txt
GET /llms/agent-icons.txt
```

## onboarding-seed

```
POST /companies/:companyId/onboarding-seed
```

## openapi

```
GET /openapi.json
```

## pipelines

```
DELETE /cases/:caseId/issue-links/:linkId
DELETE /pipelines/:pipelineId/stages/:stageId
GET /cases/:caseId
GET /cases/:caseId/automation/retry-plan
GET /cases/:caseId/children
GET /cases/:caseId/children/tree
GET /cases/:caseId/context-pack
GET /cases/:caseId/documents/:key
GET /cases/:caseId/documents/:key/revisions
GET /cases/:caseId/events
GET /cases/:caseId/issue-links
GET /cases/:caseId/outputs
GET /cases/:caseId/rollup
GET /companies/:companyId/case-events
GET /companies/:companyId/pipelines
GET /companies/:companyId/pipelines-attention
GET /companies/:companyId/review-cases
GET /pipelines/:pipelineId
GET /pipelines/:pipelineId/cases
GET /pipelines/:pipelineId/documents/:key
GET /pipelines/:pipelineId/documents/:key/revisions
GET /pipelines/:pipelineId/health
GET /pipelines/:pipelineId/intake-form
PATCH /cases/:caseId
PATCH /pipelines/:pipelineId
PATCH /pipelines/:pipelineId/stages/:stageId
PATCH /pipelines/:pipelineId/stages/:stageId/automation-env
POST /cases/:caseId/acknowledge-drift
POST /cases/:caseId/automation/current-stage/rerun
POST /cases/:caseId/automation/retry
POST /cases/:caseId/automations/:automationId/retry
POST /cases/:caseId/breakdown
POST /cases/:caseId/claim
POST /cases/:caseId/documents/:key/revisions/:revisionId/restore
POST /cases/:caseId/issue-links
POST /cases/:caseId/open-conversation
POST /cases/:caseId/release
POST /cases/:caseId/resolve-suggestion
POST /cases/:caseId/review
POST /cases/:caseId/suggest-transition
POST /cases/:caseId/transition
POST /companies/:companyId/pipelines
POST /companies/:companyId/review-cases/bulk
POST /pipelines/:pipelineId/cases
POST /pipelines/:pipelineId/cases/batch
POST /pipelines/:pipelineId/documents/:key/revisions/:revisionId/restore
POST /pipelines/:pipelineId/stages
PUT /cases/:caseId/blockers
PUT /cases/:caseId/documents/:key
PUT /pipelines/:pipelineId/documents/:key
PUT /pipelines/:pipelineId/transitions
```

## plugin-ui-static

```
GET /_plugins/:pluginId/ui/*filePath
```

## plugins

```
DELETE /plugins/:pluginId
GET /plugins
GET /plugins/:pluginId
GET /plugins/:pluginId/bridge/stream/:channel
GET /plugins/:pluginId/companies/:companyId/local-folders
GET /plugins/:pluginId/companies/:companyId/local-folders/:folderKey/status
GET /plugins/:pluginId/config
GET /plugins/:pluginId/dashboard
GET /plugins/:pluginId/health
GET /plugins/:pluginId/jobs
GET /plugins/:pluginId/jobs/:jobId/runs
GET /plugins/:pluginId/logs
GET /plugins/examples
GET /plugins/tools
GET /plugins/ui-contributions
POST /plugins/:pluginId/actions/:key
POST /plugins/:pluginId/bridge/action
POST /plugins/:pluginId/bridge/data
POST /plugins/:pluginId/companies/:companyId/local-folders/:folderKey/validate
POST /plugins/:pluginId/config
POST /plugins/:pluginId/config/test
POST /plugins/:pluginId/data/:key
POST /plugins/:pluginId/disable
POST /plugins/:pluginId/enable
POST /plugins/:pluginId/jobs/:jobId/trigger
POST /plugins/:pluginId/upgrade
POST /plugins/:pluginId/webhooks/:endpointKey
POST /plugins/install
POST /plugins/tools/execute
PUT /plugins/:pluginId/companies/:companyId/local-folders/:folderKey
```

## projects

```
DELETE /projects/:id
DELETE /projects/:id/workspaces/:workspaceId
GET /companies/:companyId/projects
GET /projects/:id
GET /projects/:id/external-object-summary
GET /projects/:id/workspaces
PATCH /projects/:id
PATCH /projects/:id/workspaces/:workspaceId
POST /companies/:companyId/projects
POST /projects/:id/workspaces
POST /projects/:id/workspaces/:workspaceId/runtime-commands/:action
POST /projects/:id/workspaces/:workspaceId/runtime-services/:action
```

## resource-memberships

```
GET /companies/:companyId/resource-memberships/me
PUT /companies/:companyId/resource-memberships/me/agents/:agentId
PUT /companies/:companyId/resource-memberships/me/documents/:documentId
PUT /companies/:companyId/resource-memberships/me/projects/:projectId
```

## routines

```
DELETE /routine-triggers/:id
GET /companies/:companyId/routines
GET /routines/:id
GET /routines/:id/description/annotations
GET /routines/:id/description/annotations/:threadId
GET /routines/:id/revisions
GET /routines/:id/runs
PATCH /routine-triggers/:id
PATCH /routines/:id
PATCH /routines/:id/description/annotations/:threadId
POST /companies/:companyId/routines
POST /routine-triggers/:id/rotate-secret
POST /routine-triggers/public/:publicId/fire
POST /routines/:id/description/annotations
POST /routines/:id/description/annotations/:threadId/comments
POST /routines/:id/revisions/:revisionId/restore
POST /routines/:id/run
POST /routines/:id/triggers
```

## secrets

```
DELETE /agents/me/secret-proposals/:id
DELETE /companies/:companyId/me/user-secrets/:secretId
DELETE /companies/:companyId/user-secret-definitions/:definitionId
DELETE /secret-provider-configs/:id
DELETE /secrets/:id
GET /agents/me/secret-proposals
GET /agents/me/secrets
GET /companies/:companyId/me/user-secrets
GET /companies/:companyId/secret-proposals
GET /companies/:companyId/secret-provider-configs
GET /companies/:companyId/secret-providers
GET /companies/:companyId/secret-providers/health
GET /companies/:companyId/secrets
GET /companies/:companyId/secrets/catalog
GET /companies/:companyId/user-secret-definitions
GET /companies/:companyId/user-secret-definitions/:definitionId/coverage
GET /secret-provider-configs/:id
GET /secrets/:id/access-events
GET /secrets/:id/usage
PATCH /companies/:companyId/me/user-secrets/:secretId
PATCH /companies/:companyId/user-secret-definitions/:definitionId
PATCH /secret-provider-configs/:id
PATCH /secrets/:id
POST /agents/me/secret-proposals
POST /agents/me/secrets/:key/value
POST /companies/:companyId/me/user-secrets
POST /companies/:companyId/me/user-secrets/:secretId/rotate
POST /companies/:companyId/secret-proposals/:id/approve
POST /companies/:companyId/secret-proposals/:id/reject
POST /companies/:companyId/secret-provider-configs
POST /companies/:companyId/secret-provider-configs/discovery/preview
POST /companies/:companyId/secrets
POST /companies/:companyId/secrets/remote-import
POST /companies/:companyId/secrets/remote-import/preview
POST /companies/:companyId/user-secret-definitions
POST /secret-provider-configs/:id/default
POST /secret-provider-configs/:id/health
POST /secrets/:id/rotate
```

## sidebar-badges

```
GET /companies/:companyId/sidebar-badges
```

## sidebar-preferences

```
GET /companies/:companyId/sidebar-preferences/me
GET /sidebar-preferences/me
PUT /companies/:companyId/sidebar-preferences/me
PUT /sidebar-preferences/me
```

## smoke-lab

```
GET /companies/:companyId/smoke-lab/oauth/authorize
GET /companies/:companyId/smoke-lab/oauth/userinfo
GET /companies/:companyId/smoke-lab/runs
GET /companies/:companyId/smoke-lab/runs/:runId
GET /companies/:companyId/smoke-lab/services
PATCH /companies/:companyId/smoke-lab/runs/:runId
POST /companies/:companyId/smoke-lab/install-fixtures
POST /companies/:companyId/smoke-lab/oauth/authorize
POST /companies/:companyId/smoke-lab/oauth/revoke
POST /companies/:companyId/smoke-lab/oauth/token
POST /companies/:companyId/smoke-lab/reset
POST /companies/:companyId/smoke-lab/runs
POST /companies/:companyId/smoke-lab/runs/:runId/steps
POST /companies/:companyId/smoke-lab/services/start
POST /companies/:companyId/smoke-lab/services/stop
```

## status-cards

```
DELETE /status-cards/:id
GET /companies/:companyId/status-cards
GET /status-cards/:id
GET /status-cards/:id/dry-run
GET /status-cards/:id/summary-revisions
GET /status-cards/:id/updates
PATCH /status-cards/:id
POST /companies/:companyId/status-cards
POST /status-cards/:id/recompile
POST /status-cards/:id/refresh
PUT /status-cards/:id/query
PUT /status-cards/:id/summary
```

## summary-slots

```
GET /companies/:companyId/summary-slots/:scopeKind/:slotKey
GET /companies/:companyId/summary-slots/:scopeKind/:slotKey/revisions
POST /companies/:companyId/summary-slots/:scopeKind/:slotKey/generate
PUT /companies/:companyId/summary-slots/:scopeKind/:slotKey
```

## teams-catalog

```
GET /companies/:companyId/teams/catalog/installed
GET /teams/catalog
GET /teams/catalog/:catalogId
GET /teams/catalog/:catalogId/files
POST /companies/:companyId/teams/catalog/:catalogId/install
POST /companies/:companyId/teams/catalog/:catalogId/preview
```

## tool-access

```
DELETE /companies/:companyId/tools/policies/:policyId
DELETE /tool-applications/:applicationId
DELETE /tool-connections/:connectionId
DELETE /tool-connections/:connectionId/grants/:grantId
DELETE /tool-profile-entries/:entryId
DELETE /tool-profiles/:profileId
GET /companies/:companyId/tools/action-requests
GET /companies/:companyId/tools/applications
GET /companies/:companyId/tools/apps/attention
GET /companies/:companyId/tools/connections
GET /companies/:companyId/tools/examples
GET /companies/:companyId/tools/gallery
GET /companies/:companyId/tools/policies
GET /companies/:companyId/tools/profiles
GET /companies/:companyId/tools/profiles/effective/agents/:agentId
GET /companies/:companyId/tools/runs/:runId/decisions
GET /companies/:companyId/tools/runtime-health
GET /companies/:companyId/tools/runtime-slots
GET /companies/:companyId/tools/stdio-templates
GET /companies/:companyId/tools/trust-rules
GET /tool-connections/:connectionId
GET /tool-connections/:connectionId/activity
GET /tool-connections/:connectionId/catalog
GET /tool-connections/:connectionId/grants
GET /tool-connections/:connectionId/installs
GET /tool-connections/:connectionId/test-agents
GET /tool-connections/:connectionId/test-calls/:actionRequestId
GET /tool-connections/:connectionId/usage
GET /tool-profiles/:profileId/new-tools
GET /tools/oauth/callback
PATCH /companies/:companyId/tools/policies/:policyId
PATCH /tool-applications/:applicationId
PATCH /tool-connections/:connectionId
PATCH /tool-profile-entries/:entryId
PATCH /tool-profiles/:profileId
POST /agents/me/connections/:connectionId/start-authorization
POST /agents/me/connections/:connectionId/token
POST /companies/:companyId/tools/action-requests/:actionRequestId/trust-rule
POST /companies/:companyId/tools/applications
POST /companies/:companyId/tools/apps/:connectionId/finish
POST /companies/:companyId/tools/apps/connect
POST /companies/:companyId/tools/connections
POST /companies/:companyId/tools/connections/:connectionId/start-authorization
POST /companies/:companyId/tools/examples/:id/install
POST /companies/:companyId/tools/examples/:id/smoke
POST /companies/:companyId/tools/mcp/import-json
POST /companies/:companyId/tools/policies
POST /companies/:companyId/tools/policies/:policyId/duplicate
POST /companies/:companyId/tools/policies/reorder
POST /companies/:companyId/tools/policy/test
POST /companies/:companyId/tools/profiles
POST /companies/:companyId/tools/profiles/:profileId/bind
POST /companies/:companyId/tools/profiles/:profileId/unbind
POST /companies/:companyId/tools/runtime-slots/:id/restart
POST /companies/:companyId/tools/runtime-slots/:id/stop
POST /companies/:companyId/tools/stdio-templates
POST /companies/:companyId/tools/stdio-templates/:templateId/disable
POST /companies/:companyId/tools/trust-rules/:policyId/revoke
POST /tool-connections/:connectionId/catalog/refresh
POST /tool-connections/:connectionId/grants/installations
POST /tool-connections/:connectionId/health-check
POST /tool-connections/:connectionId/reconnect
POST /tool-connections/:connectionId/test-calls
POST /tool-profiles/:profileId/duplicate
POST /tool-profiles/:profileId/entries
POST /tool-profiles/:profileId/new-tools/review
POST /tools/oauth/:connectionId/start
PUT /tool-connections/:connectionId/installs
```

## tool-gateway

```
GET /companies/:companyId/tools/gateways
GET /mcp/gateways/:gatewayPublicId
GET /tool-gateway/audit
GET /tool-gateway/gateways/:gatewayId/mcp
GET /tool-gateway/runtime-slots
GET /tool-gateway/tools
PATCH /tool-gateway/gateways/:gatewayId
POST /companies/:companyId/tools/gateways
POST /mcp/gateways/:gatewayPublicId
POST /tool-gateway/action-requests/:id/approve
POST /tool-gateway/action-requests/:id/decline
POST /tool-gateway/gateway-tokens/:tokenId/revoke
POST /tool-gateway/gateways/:gatewayId/mcp
POST /tool-gateway/gateways/:gatewayId/tokens
POST /tool-gateway/runtime-slots/:slotId/restart
POST /tool-gateway/runtime-slots/:slotId/stop
POST /tool-gateway/sessions
POST /tool-gateway/sessions/:sessionId/revoke
POST /tool-gateway/tools/call
```

## user-profiles

```
GET /companies/:companyId/users/:userSlug/profile
```

## Regenerate

```bash
D=~/.infra/services/paperclip/data/cli/current/node_modules/@paperclipai/server/dist/routes
grep -hoE '\.(get|post|patch|put|delete)\("(/[^"]*)"' $D/*.js \
  | sed -E 's/^\.//; s/\("/ /; s/"$//' | awk '{print toupper($1), $2}' | sort -u
```
