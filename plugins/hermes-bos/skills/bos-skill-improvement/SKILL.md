---
name: bos-skill-improvement
description: Propose a skill fix from an observed failure.
version: 0.1.0
author: pftg
platforms: [macos]
---

# bos-skill-improvement Skill

Turn one observed skill failure into a durable improvement: a reproduction
fixture in `evaluations/fixtures/`, a minimal patch to the responsible
local skill, and a before/after run note in `evaluations/runs/`. Only
agent-created skills under `~/.hermes/skills/` may be patched; bundled or
hub-installed skills are recorded as proposals for the owner instead.
Writes files only; commits nothing.

- Business OS root: `/Users/pftg/dev/pkm/business-os`
- Fixtures directory: `/Users/pftg/dev/pkm/business-os/evaluations/fixtures/`
- Run notes directory: `/Users/pftg/dev/pkm/business-os/evaluations/runs/`
- Editable skills: `/Users/pftg/.hermes/skills/` (agent-created only)

## Use when

Use after a skill produced a wrong, incomplete, or policy-violating result
and the failure is attributable to the skill's instructions (not to a
model improvising well beyond them). Not for new-skill requests — this
skill changes existing behavior, narrowly.

## Inputs

- The observed failure: what was asked, what the skill did, what should
  have happened (as verbatim as available)
- The responsible skill name, or "none exists" if the failure is a gap
- The seat that observed the failure

## Procedure

1. Capture the failure verbatim — input, actual output, expected output,
   and the policy or work-item rule it violated. A failure without
   verbatim evidence is not actionable; collect it first.
2. Read the responsible skill's `SKILL.md` with `read_file` and the
   authoring standards at `~/.hermes/hermes-agent/skills/AGENTS.md`. If
   the skill is bundled (`hermes-agent/skills/`) or hub-installed, do not
   patch it — write the proposal into the run note (step 6) with the
   recommended wording and stop there.
3. Write the fixture with `patch` at
   `evaluations/fixtures/FIX-<NNN>-<slug>.md`, taking the next unused
   three-digit number (confirm with `search_files target='files'`).
   Fixture frontmatter states `id`, `title`, `expected_risk_class`, and
   `expected`, so the fixture fails against the old skill and passes
   against the fixed one.
4. Patch the skill minimally — the smallest instruction change that would
   have prevented the failure. Keep the authoring standards intact:
   `description` ≤ 60 chars ending with a period, native Hermes tool names
   in backticks, canonical section order. One failure, one patch; do not
   rewrite the skill.
5. Re-test against the fixture: apply the patched procedure to the fixture
   input and confirm it now produces the `expected` result. If it does
   not, revise the patch once; on a second failure the fix is wrong —
   restore the skill to its prior content and record the attempt as
   `reverted`.
6. Write the before/after note with `patch` at
   `evaluations/runs/IMP-<YYYYMMDD>-<skill>-FIX-<NNN>.md`: before
   behavior, the patch (path plus summary), after behavior, evidence
   (fixture path, failing and passing observations), and — for bundled or
   hub skills — the proposal text awaiting the owner.

Run note format:

```markdown
---
improvement: IMP-<YYYYMMDD>-<skill>-FIX-<NNN>
date: <YYYY-MM-DD>
skill: <path under ~/.hermes/skills/>
fixture: FIX-<NNN>
seat: <profile>
result: <patched|proposal-only|reverted>
---

# Improvement note — <skill> / FIX-<NNN>

## Failure observed
<verbatim input, actual vs expected, policy violated>

## Change
<what was patched and why it is minimal>

## Before / after
<behavior against the fixture, before and after>

## Evidence
<paths to fixture, skill, observations>

## Proposal for owner (bundled/hub skills only)
<recommended wording; nothing patched>
```

## Output

Return the fixture path, the patched skill path (or `proposal-only` with
the reason), the run-note path, and the before/after verdict.

## Failure modes

- Do not patch bundled (`hermes-agent/skills/`) or hub-installed skills —
  proposals only.
- Do not fix more than the observed failure; scope creep here erodes the
  skill under test.
- Do not edit a skill while a gate verdict on it is pending — record the
  proposal and let the verdict land first.
- Do not put secrets, transcripts with personal data, or key material into
  fixtures or run notes; reference env var names only.
- Do not commit, push, or rewrite Git history — in either repository; the
  owner commits.
- Do not mark `result: patched` without a passing re-run against the
  fixture; an unverified patch is recorded as `reverted` or
  `proposal-only`.

## Verification

- The fixture file exists with complete frontmatter and reproduces the
  failure against the pre-patch skill instructions.
- The skill diff is minimal: one behavioral change, and the authoring
  standards still hold (description length, section order, tool naming).
- Re-running the patched skill's own `## Verification` against the fixture
  passes.
- The run note exists, cites fixture and skill by path, and its `result`
  matches what was actually done.
