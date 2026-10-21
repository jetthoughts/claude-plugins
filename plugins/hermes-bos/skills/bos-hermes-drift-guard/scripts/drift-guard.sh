#!/usr/bin/env bash
# drift-guard.sh — drift gate for the Hermes Agent clone.
#
# Two phases, one script:
#
#   pre-dispatch (default, no flag):
#     Exit 0 = clean, proceed. Exit 1 = drift detected, BLOCK dispatch.
#     This is the gate. It fails closed.
#
#   post-run (--post-run):
#     Re-probe after a worker completes. Exit 0 always (the worker already
#     ran — you cannot un-run it) but emit a machine-readable outcome row on
#     stdout: {"phase":"post-run","clean":true|false,"drift":[...]}.
#     The caller appends that row to the worker's outcome. Drift found
#     post-run is a finding, not a block — it goes on the worker's record and
#     into the incident loop if it recurs.
#
# Usage: drift-guard.sh [--post-run] [clone-path]
#   clone-path defaults to $HERMES_AGENT or ~/.hermes/hermes-agent.
#
# The guard makes no changes to the clone. Safe to run anywhere, including
# from a kanban pre-dispatch lint or a post-run worker audit.

set -u

POST_RUN=false
if [ "${1:-}" = "--post-run" ]; then
  POST_RUN=true
  shift
fi

CLONE="${1:-${HERMES_AGENT:-$HOME/.hermes/hermes-agent}}"

if [ ! -d "$CLONE" ]; then
  if $POST_RUN; then
    echo '{"phase":"post-run","clean":true,"drift":[],"note":"clone absent"}'
  else
    echo "drift-guard: clone path not found: $CLONE (no-op, treating as clean)" >&2
  fi
  exit 0
fi

if ! command -v git >/dev/null 2>&1; then
  echo "drift-guard: git not available; failing closed" >&2
  exit 1
fi

cd "$CLONE" || { echo "drift-guard: cannot enter $CLONE; failing closed" >&2; exit 1; }

# Drift = any non-empty porcelain line. git status --porcelain emits nothing
# on a clean tree, so any output is a modification, deletion, rename,
# conflict, or untracked file — custom code touched the read-only clone.
DRIFT=$(git status --porcelain 2>/dev/null | grep -E '.' || true)

if [ -n "$DRIFT" ]; then
  if $POST_RUN; then
    # Machine-readable row for the worker outcome. Escape newlines so the
    # JSON stays one line.
    JSON_DRIFT=$(printf '%s' "$DRIFT" | sed 's/"/\\"/g' | tr '\n' '|')
    echo "{\"phase\":\"post-run\",\"clean\":false,\"drift\":\"$JSON_DRIFT\"}"
    exit 0
  fi
  echo "drift-guard: DRIFT DETECTED in $CLONE" >&2
  echo "$DRIFT" | sed 's/^/  /' >&2
  echo "drift-guard: dispatch blocked. Resolve drift or obtain PO approval." >&2
  exit 1
fi

if $POST_RUN; then
  echo '{"phase":"post-run","clean":true,"drift":[]}'
else
  echo "drift-guard: clean ($CLONE)"
fi
exit 0