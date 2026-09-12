# Board tools — mapping the six lists

Keep the six lists in the team's head even where the tool has fewer statuses. Map, do not drop. Linear is not a
column: unlinked 2026-09-04, nothing new goes there, and no `linear` skill or MCP tool resolves in a session.

| List | Paperclip issue | GitHub Projects (Status field) | markdown kanban (`kanban-markdown` skill) | Session TODO list |
|---|---|---|---|---|
| Backlog | `backlog` | Backlog | `status: backlog` | pending, unordered |
| Ready | `todo` (ordered; top = next) | Ready | `status: ready` | pending, top of list |
| In Progress | `in_progress`, assignee set | In Progress | `status: in-progress` | in_progress (one at a time) |
| Code Review | `in_review` + comment `Review: <agent>` | In Review | `status: review` | — (spawn the verifier) |
| Verify | `in_review` + Paperclip **approval request** (pending → approved / rejected / revision_requested) | Verify (add the option) | `status: verify` | — |
| Done | `done` after the human merges/approves | Done | `status: done` | completed |

Notes per tool:

- **Paperclip**: statuses in `/api/openapi.json` (read 2026-09-12): `backlog`, `todo`, `in_progress`, `in_review`,
  `done`, `blocked`, `cancelled`. `blocked` keeps its assignee — releasing it spawns liveness incidents — and means
  another card or agent owes the next move; a card waiting on a human is `in_review`. Blocking is real:
  `blockedByIssueIds` on `PATCH /api/issues/{id}` (the array replaces, include existing) and
  `GET /api/issues/{id}/diagnostics/blockers`. Priority `high` = the High label. Assignment wakes the agent when
  `runtimeConfig.heartbeat.wakeOnAssignment` is on and the status is not `backlog`, so assigning a card **is** the
  pull. The card's comment thread is the status surface; the ops runbook is the `j-paperclip-ops` skill.
- **GitHub Projects**: the Status single-select field; add `Ready` and `Verify` options if missing. Card order
  inside a column is the manual sort; label `high` = the High label.
- **markdown kanban**: one `.md` per card with `status:` frontmatter; order by a `priority:` or `order:` field.
- **Session TODO list**: the same rules apply inside one agent: one `in_progress` item, finish before starting,
  a blocked item keeps its place with the blocker named.
