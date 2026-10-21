---
name: bos-hermes-drift-guard
description: Block dispatch when the hermes-agent clone has uncommitted or untracked custom code.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-hermes-drift-guard Skill

Pre-flight gate that fails closed when the Hermes Agent clone
(`~/.hermes/hermes-agent`) has drifted from upstream — i.e. carries modified
tracked files or untracked custom scripts that were not part of the Nous
Research distribution. The clone is treated as read-only here; any drift is a
violation of "no custom code without PO approval" and blocks dispatch until the
owner resolves it.

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Hermes Agent clone: `~/.hermes/hermes-agent` (override with `HERMES_AGENT`)
- Guard script: `scripts/drift-guard.sh` (same directory as this SKILL.md)
- Verdicts and incidents: `business-os/operations/incidents/` (per
  `bos-incident-response`)
- Phases: pre-dispatch (default, fails closed) and post-run audit
  (`--post-run`, emits a machine-readable outcome row, never blocks)
- Wiring: `operations/incidents/INC-20261003/README.md`
- On-call: `bos-incident-response` recipe R14 (post-run drift)

## Hard reject: no clone edits

**Any wiring that requires editing `hermes_cli/` is a reject, full stop.**

The guard exists precisely to keep that tree read-only. Wiring it by writing
into the tree would close the gate by destroying the door. Both phases invoke
a script that lives **outside** the clone, in
`~/dev/claude-plugins/plugins/hermes-bos/skills/bos-hermes-drift-guard/scripts/`.
The pre-dispatch step is procedural (overseer runs the script, checks the exit
code, blocks on 1) — not a code change to the dispatcher. If the only path to
wire the guard requires touching the clone, the wiring is wrong and must be
redesigned, not the clone touched.

## Use when

Any seat is about to dispatch a worker, spawn a sub-agent, or run a kanban
dispatch cycle in this workspace. Also run on developer sessions before any
`git` operation touching the clone, and as a CI check for the fleet.

Not for: editing the clone (the guard detects that, it does not permit it),
or auditing third-party external skills (`skills.external_dirs` — those are
upstream, not drift).

## Procedure

1. Resolve the clone path: `$HERMES_AGENT` if set, else
   `~/.hermes/hermes-agent`. If the directory does not exist, exit 0 (guard
   is a no-op where the clone is absent).
2. Run `scripts/drift-guard.sh <clone-path>`. It exits 0 on a clean tree and
   1 on drift, printing the offending paths.
3. On exit 1: do NOT dispatch. Record the drift on the current work item as a
   blocker, and if no incident card exists, file one under `bos-incident-response`
   (Class 1 — unauthorized code in a read-only clone). Escalate to the owner.
   Do not attempt to revert or stash without the owner's decision.
4. On exit 0: proceed with dispatch.

### Post-run audit (`drift-guard.sh --post-run <clone>`)

Run after a worker completes, before its outcome is marked done. The script
exits 0 always — a worker that already ran cannot be un-run — but emits a
machine-readable outcome row on stdout:

```
{"phase":"post-run","clean":true,"drift":[]}
```

or, on drift:

```
{"phase":"post-run","clean":false,"drift":"<porcelain lines, | -separated>"}
```

The dispatcher appends that row to the worker's outcome record. Drift found
post-run is a **finding**, not a block: it goes on the worker's record, and if
the same drift appears on a second worker it enters the incident loop
(`bos-incident-response` T1 — same goal failed on 2+ attempts).

## Drift definition (what counts)

Any of the following in `git -C <clone> status --porcelain`:

- `M` or `D` on a tracked file (a modification or deletion vs upstream HEAD),
- `??` on an untracked file under `hermes_cli/`, or
- `??` on an untracked `.py` / `.sh` / `.js` file at the clone root.

External skills under `skills.external_dirs` are outside the clone and are not
drift by this definition; they are governed by their own upstream.

## Failure modes

- Do not silence the guard to let a card through. A blocked card is a result,
  not a failure of the guard.
- Do not auto-revert. Reverting destroys evidence of what was changed and what
  the PO approved or did not; the owner decides revert vs. keep.
- If the guard itself errors (clone missing, git unavailable), fail closed:
  report the error and block dispatch rather than assume clean.

- Post-run drift is not a retry trigger. Re-running the same worker does not
  undo the drift; the owner resolves the tree first.

## Verification

- `bash scripts/drift-guard.sh` exits 0 against a pristine clone and 1 against
  a clone with any `M`/`??` entry under `hermes_cli/` or a root-level script.
- `bash scripts/drift-guard.sh --post-run` exits 0 always and emits a JSON row;
  `clean:false` when drift is present, `clean:true` otherwise.
- The guard makes no changes to the clone; `git status` before and after are
  identical.