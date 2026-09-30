# Orchestration by size

The contract holds at every scale.

4. **ORCHESTRATE by size** — the contract holds at every scale:
   - *trivial edit*: inline; a verifier agent still reviews before commit.
   - *one unit*: author agent + distinct verifier (§5).
   - *a feature*: commits proceed one at a time on the sprint branch, each
     independently reviewed; the sprint ships as ONE PR, size-capped per the
     repo's rules (JT default: ~500 changed lines of CODE; docs/logs exempt;
     oversized sprints split into sequential PRs, merge N before N+1).
   - *swarm scale*: NOT the default. With 3+ independent same-shaped units,
     PROPOSE it in the triage verdict; it activates only on explicit request,
     workers isolated in worktrees.
