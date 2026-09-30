---
name: five-whys
description: Five Whys (5 Whys, Toyota Production System) — drill a symptom to a systemic root cause by asking why repeatedly, with evidence or UNSUPPORTED named at every step. Use for "why did this happen again", recurring incidents, postmortems, and any decision that keeps coming back. Not for framing the problem, ranking options, or deciding what to do — frame with framing first, and make the call with decision-panel or deliberate.
argument-hint: Optional issue or symptom description
---

# Five Whys Analysis

Iteratively ask "why" to move from surface symptoms to fundamental causes. Identifies systemic issues rather than quick fixes.

**The framing step is not this skill's job.** The problem statement, the decision sentence, and what "solved" measures come from `framing` — run it first, or confirm a frame already exists, and do not restate it here. Five Whys starts from a symptom that has already been framed.

**Usage**: `/why [issue_description]`

**Variables**: ISSUE (problem or symptom to analyze; default: prompt for input) · DEPTH (number of "why" iterations; default: 5, adjust as needed).

## Steps

1. Take the problem statement from the frame.
2. Ask "Why did this happen?" and document the answer.
3. For that answer, ask "Why?" again.
4. Continue until reaching root cause (usually 5 iterations).
5. Validate by working backwards: root cause → symptom.
6. Explore branches if multiple causes emerge.
7. Propose solutions addressing root causes, not symptoms.

## Examples

### Example 1: Production Bug

```
Problem: Users see 500 error on checkout
Why 1: Payment service throws exception
Why 2: Request timeout after 30 seconds
Why 3: Database query takes 45 seconds
Why 4: Missing index on transactions table
Why 5: Index creation wasn't in migration scripts
Root Cause: Migration review process doesn't check query performance

Solution: Add query performance checks to migration PR template
```

### Example 2: CI/CD Pipeline Failures

```
Problem: E2E tests fail intermittently
Why 1: Race condition in async test setup
Why 2: Test doesn't wait for database seed completion
Why 3: Seed function doesn't return promise
Why 4: TypeScript didn't catch missing return type
Why 5: strict mode not enabled in test config
Root Cause: Inconsistent TypeScript config between src and tests

Solution: Unify TypeScript config, enable strict mode everywhere
```

### Example 3: Multi-Branch Analysis

```
Problem: Feature deployment takes 2 hours

Branch A (Build):
Why 1: Docker build takes 90 minutes
Why 2: No layer caching
Why 3: Dependencies reinstalled every time
Why 4: Cache invalidated by timestamp in Dockerfile
Root Cause A: Dockerfile uses current timestamp for versioning

Branch B (Tests):
Why 1: Test suite takes 30 minutes
Why 2: Integration tests run sequentially
Why 3: Test runner config has maxWorkers: 1
Why 4: Previous developer disabled parallelism due to flaky tests
Root Cause B: Flaky tests masked by disabling parallelism

Solutions:
A) Remove timestamp from Dockerfile, use git SHA
B) Fix flaky tests, re-enable parallel test execution
```

## Notes

- Don't stop at symptoms; keep digging for systemic issues
- Multiple root causes may exist - explore different branches
- Consider both technical and process-related causes
- The magic isn't in exactly 5 whys - stop when you reach the true root cause
- Stop when you hit systemic/process issues, not just technical details
- If "human error" appears, keep digging: why was error possible?
- Root cause usually involves: missing validation, missing docs, unclear process, or missing automation
- Test solutions: implement → verify symptom resolved → monitor for recurrence

## Evidence rule (ours, not the source's)

A why is a claim. Each step names the evidence behind it (a log line, a measurement, a reproducible check) or is marked UNSUPPORTED, and an UNSUPPORTED why is never presented as the root cause. Correlation is the usual trap: two things that changed together are one observation, not a cause. When the chain reaches an UNSUPPORTED step, the output is the test that would settle it, not a conclusion.

## Sources

Lean Enterprise Institute, "5 Whys" (https://www.lean.org/lexicon-terms/5-whys/, retrieved 2026-09-13): "5 Whys is the practice of asking why repeatedly whenever a problem is encountered in order to get beyond the obvious symptoms to discover the root cause." Originator: Taiichi Ohno, *Toyota Production System* (1988), quoted there; the book itself was not fetched.
