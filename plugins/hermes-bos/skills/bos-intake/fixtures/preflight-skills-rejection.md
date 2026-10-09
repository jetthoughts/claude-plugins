# Fixture: bos-intake preflight-skills rejection (composite experiment t_ca1713f3)

Captures the input that closes the `Unknown skill(s)` worker-boot crash
class for *all* profiles (card t_bacc26a7 lineage; closing review
`t_df9dbe0a`).

## Input

A `kanban_create` (or chat-level prompt) carries:

```
skills=["hermes-bos/skills/bos-intake"]
```

Profile under test: any that lacks the `skills:` block in its `config.yaml`
(pre-fix soul-curator and growth-operator; same shape as the verified
baseline).

## Expected output (intake-side, sub-second)

```
Unknown skill(s): hermes-bos/skills/bos-intake
```

The wording matches `agent.skill_commands.format_missing_skills`
(`hermes-agent/agent/skill_commands.py:278`) — same surface the worker
would emit 60-90 s later at boot. Operator can fix the identifier and retry.

## Pass metric 1 (config leg)

After the `skills:` block is restored to the profile's `config.yaml`,
`get_external_skills_dirs()` for the profile returns the same 5 paths as
`kanban-orchestrator`:

```
[
    PosixPath('/Users/pftg/.hermes/skills'),
    PosixPath('/Users/pftg/dev/claude-plugins/plugins'),
    PosixPath('/Users/pftg/.openclaw/skills'),
    PosixPath('/Users/pftg/.config/opencode/skills/j-deep-research'),
    PosixPath('/Users/pftg/.config/skillshare/skills'),
]
```

And the same `skills=` payload is still flagged as unresolvable by the
preflight (the namespaced path-form is not catalog-resolvable through
`_load_skill_payload` regardless of the config's `skills:` block — that is
a runtime identifier-form problem, out of scope for this fixture). What the
restored config DOES change: under profiles that previously had an empty
`external_dirs` set (soul-curator, growth-operator), the helper now sees
the plugins root and can resolve properly-named identifiers like
`bos-intake` instead of failing the entire profile's catalog.

Note that the prevention contract for this hook is the "unknown
identifier" path: `preflight_skills.missing([...])` returns the entries
that fail to resolve under the live profile, with the same
`Unknown skill(s): <id>` wording the worker would print at boot. A
malformed payload is rejected at filing instead of crashing the worker
60-90s later.

## Reproduction recipe

```sh
PYTHONPATH=/Users/pftg/.hermes/hermes-agent /opt/homebrew/bin/python3.14 \
  /Users/pftg/dev/claude-plugins/plugins/hermes-bos/skills/bos-intake/scripts/test_preflight_skills.py
```

Expected: `Ran 3 tests ... OK`.

## Timebox / scope

One composite change (config + script + SKILL wiring + fixture). Revert
rule: `git revert <commit-sha>` from `~/dev/claude-plugins` removes the new
script + fixture + SKILL wiring; the config edits in `~/.hermes` revert with
a sibling `git revert` against the daemon-orchestrator checkout (the
operator handles that follow-up; this card does not touch `~/.hermes`).
