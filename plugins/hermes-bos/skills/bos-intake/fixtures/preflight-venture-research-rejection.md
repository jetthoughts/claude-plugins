# Fixture: bos-intake preflight-venture-research rejection (kanban t_41ee06a4 / rock 5.1)

Captures the input that closes the venture-research preflight gap so any
kanban card the orchestrator files with `venture_research: true` MUST carry
`forcing_party`, `forcing_date`, and `pain_fit` (rock 5.1; Paul preference
memory `viking://user/default/memories/preferences/Paul/venture_operating_rules.md`).

## Input

A `kanban_create` call carries a card body whose frontmatter is:

```
---
venture_research: true
forcing_party: EU AI Act enforcement (auditor)
pain_fit: Audit fees payable by the audited entity, not the auditor
---
```

Note the missing `forcing_date`.

## Expected output (intake-side, sub-second)

```
venture research preflight: missing field(s) forcing_date
```

The wording matches `preflight_venture_research.format_rejection` and is one
line so the orchestrator can paste it back to the operator verbatim. The
operator fixes the frontmatter (adds `forcing_date: 2026-08-02`) and re-fans.

## Pass metric 1

After all three fields are present in the frontmatter (or as `Forcing party:`
/ `Date:` / `Pain fit:` body lines), the helper exits 0 with
`OK: venture research preflight passed` and the orchestrator proceeds to
`kanban_create`.

## Reproduction recipe

```sh
PYTHONPATH=/Users/pftg/.hermes/hermes-agent python3.11 \
  /Users/pftg/dev/claude-plugins/plugins/hermes-bos/skills/bos-intake/scripts/test_preflight_venture_research.py
```

Expected: `Ran 8 tests ... OK`.

The replay guard
(`test_bos_intake_skill_md_carries_venture_research_preflight_clause`) reads
`SKILL.md` and fails if the step 5b procedure clause is missing the required
phrases. Without the clause the gate is unenforced and venture research
without forcing party / date / pain-fit slips into ready.

## Timebox / scope

Helper + tests + SKILL.md wiring + fixture. Revert rule:
`git -C ~/dev/claude-plugins revert <commit-sha>` removes the new script +
test + SKILL wiring; the fixture file is removed with the same revert. No
config or runtime changes outside the bos-intake skill.

## Linked artifacts

- Rock: `operations/decisions/2026-10-09-rocks.md` § Rock 5.1.
- Owner memory: `viking://user/default/memories/preferences/Paul/venture_operating_rules.md`.
- Kanban: `kanban://t_41ee06a4`.
- Helper: `plugins/hermes-bos/skills/bos-intake/scripts/preflight_venture_research.py`.
- Test: `plugins/hermes-bos/skills/bos-intake/scripts/test_preflight_venture_research.py`.