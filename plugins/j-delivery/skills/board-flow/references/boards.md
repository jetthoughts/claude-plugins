# Board tools — mapping the six lists

Keep the six lists in the team's head even where the tool has fewer statuses. Map, do not drop.

| List | Paperclip issue | Linear | GitHub Projects (Status field) | markdown kanban (`kanban-markdown` skill) | Session TODO list |
|---|---|---|---|---|---|
| Backlog | `backlog` | Backlog | Backlog | `status: backlog` | pending, unordered |
| Ready | `todo` (ordered; top = next) | Todo | Ready | `status: ready` | pending, top of list |
| In Progress | `in_progress`, assignee set | In Progress | In Progress | `status: in-progress` | in_progress (one at a time) |
| Code Review | `in_review` if present, else `in_progress` + comment `Review: <agent>` | In Review | In Review | `status: review` | — (spawn the verifier) |
| Verify | Paperclip **approval request** (pending → approved / rejected / revision_requested) | Todo for QA + label `verify`, or a state named Verify | Verify (add the option) | `status: verify` | — |
| Done | `done` after the human merges/approves | Done | Done | `status: done` | completed |

Notes per tool:

- **Paperclip**: status names seen in the CLI: `todo`, `in_progress`, `done`; check `paperclipai issue update --help`
  for the full set on your version. Blocking is real: `blockedByIssueIds` (API only; `PATCH /api/issues/{id}`)
  and `GET /api/issues/{id}/diagnostics/blockers`. Priority `high` = the High label. Assignment wakes the agent
  when `wakeOnAssignment` is on, so moving a card to In Progress with an assignee **is** the pull. The card's
  comment thread is the status surface (`issue comments` / the issue page).
- **Linear**: use the `linear` skill; states are per team — read them once (`list_issue_statuses`) and map.
  Priority 1 (Urgent) or 2 (High) = the High label. Ordering inside a state is the manual sort.
- **GitHub Projects**: the Status single-select field; add `Ready` and `Verify` options if missing. Card order
  inside a column is the manual sort; label `high` = the High label.
- **markdown kanban**: one `.md` per card with `status:` frontmatter; order by a `priority:` or `order:` field.
- **Session TODO list**: the same rules apply inside one agent: one `in_progress` item, finish before starting,
  a blocked item keeps its place with the blocker named.
