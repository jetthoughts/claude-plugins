#!/usr/bin/env bash
# Run every applicable validator against one decision workspace.
# Usage: ~/.claude/skills/j-independent-ideation/scripts/validate.sh <workspace-dir>
set -euo pipefail
[ $# -eq 1 ] || { sed -n '2,3p' "$0"; exit 2; }
DIR=$1
[ -d "$DIR" ] || { echo "not a directory: $DIR" >&2; exit 2; }
S=$(cd "$(dirname "$0")/../.." && pwd -P)   # the skills directory this skill lives in
rc=0
step() { echo "== $1"; shift; "$@" || rc=1; }

step "evidence"  python3 "$S/j-running-independent-research/scripts/validate_evidence.py" "$DIR"
[ -d "$DIR/09-council" ] && step "council" python3 "$S/j-convening-the-council/scripts/aggregate_council.py" "$DIR/09-council"
[ -f "$DIR/10-experiment-portfolio.md" ] && step "portfolio" python3 "$S/j-designing-experiments/scripts/score_portfolio.py" "$DIR/10-experiment-portfolio.md"
[ -f "$DIR/11-decision-record.md" ] && step "decision" python3 "$S/j-making-the-call/scripts/validate_decision.py" "$DIR/11-decision-record.md" --ledger "$DIR/03-evidence-ledger.jsonl"
echo "== result: $([ $rc -eq 0 ] && echo PASS || echo FAIL)"
exit $rc
