---
name: bos-quality-gate
description: Gate artifacts against done definition, policy, evidence.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-quality-gate Skill

Apply the Operations Controller gate: evaluate one artifact against the
Business OS definition of done, approval classes, and factual support, and
return a pass/fail verdict plus a reproducible defect list. Read-only with
respect to the artifact — the gate never edits what it grades, takes no
external action, and commits nothing (the owner reviews and commits).

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Gate verdicts are written under `evaluations/` and `operations/reviews/`
  (the Operations Controller's `WRITE_INTERNAL` scope per the authority matrix).

## Use when

Use when an artifact (work item, decision record, evidence pack, deliverable)
is submitted for review, when a run reaches the `VERIFY` state, or when a
human asks whether an item meets the definition of done. Not for editing,
rework, or execution — only for judging.

## Inputs

- Artifact: file path under the Business OS root, or a work-item ID
- Author seat (Hermes profile or human) that produced the artifact
- Intended `approval` class of the work (what the artifact claims to enable)

## Procedure

1. Read the governing files with `read_file`: the Business OS root
   `AGENTS.md`, `constitution/definition-of-done.md`,
   `constitution/authority-matrix.md`, `constitution/risk-policy.md`, and
   `constitution/escalation-policy.md`.
2. Resolve the artifact and its owning work item. Enforce author ≠ verifier:
   if the running seat authored the artifact, stop — a different seat must
   apply the gate (authority matrix rule 1).
3. Run deterministic checks: frontmatter schema complete, ID format and
   uniqueness, canonical location per the root `AGENTS.md`, status vocabulary
   valid, and every `evidence` link resolves (`read_file` for paths,
   `search_files target='files'` for repo-relative references).
4. Score the artifact against each of the six definition-of-done criteria:
   artifact landed, evidence linked, deterministic checks pass, independent
   review, state recorded, owner-visible summary.
5. Check factual support: every material claim has a source path or URL in
   the work item's `evidence` field; unsupported material claims and
   contradictions between sources are defects.
6. Check authority: the artifact's implied actions must not exceed its
   recorded `approval` class. Any implied `EXTERNAL` or `IRREVERSIBLE` action
   without the owner's explicit per-instance yes is a blocker (deny-on-silence:
   a draft or silence is never consent). Secrets or key material in files are
   an immediate blocker.
6b. Check test-first and goal match: the result shows the check failing before the work
   (RED) and passing after it (GREEN), with both outputs pasted. The check proves the
   requester's ORIGINAL goal (quoted in the root or its source, e.g. the Plane item), not a
   narrowed rewrite. A missing RED or GREEN, or a goal mismatch, is a blocker.
7. Verdict: `FAIL` if any blocker exists, otherwise `PASS`. Record the
   verdict and defect list under `evaluations/` or `operations/reviews/` and
   reference it from the work item's `status` (`verify` on pass input,
   `escalated` with a `why` line on fail input per the escalation policy).

Defect format (each defect must be independently re-checkable):

```markdown
- id: DEF-<NNN>
  severity: <blocker|note>
  location: <path:line or path>
  criterion: <definition-of-done item # or policy name>
  finding: <what is wrong>
  evidence: <quote or observed value>
```

## Output

Return the verdict (`PASS`/`FAIL`), the criteria table, the defect list in
the format above, the approval-class determination, and rollback advice.
Rollback advice states the smallest safe reversal for the artifact's changes
(e.g., "revert to previous file revision; no external side effects exist") —
the gate itself changes nothing but its own verdict file.

## Failure modes

- Do not modify the artifact; the gate that grades is not the hand that fixes.
- Do not approve work produced by the same seat running the gate.
- Do not perform external actions or contact anyone; verdicts land in files.
- Do not guess on missing authority — fail closed and escalate instead.
- If `constitution/definition-of-done.md` or the authority matrix is missing,
  the run fails closed: verdict `FAIL`, first defect records the missing
  governance file, and the work item is set to `escalated`.

## Verification

- Re-running the deterministic checks reproduces the identical defect list.
- Every defect cites a location and the criterion it violates.
- Verdict is consistent with the rule: `PASS` iff zero blockers.
- The artifact's bytes are unchanged — `read_file` before and after match
  except for the gate's own verdict file.
