# Naming convention

**The plugin is the domain. The skill is the job. The prefix is never repeated.**

`harness-setup:setup` reads as a sentence. `j-research:j-deep-research` stutters, and the stutter is
the tell that the plugin name is doing the skill's work.

| | Rule | Why |
|---|---|---|
| **Plugin** | a domain noun, `j-` prefixed when it is house-specific | groups what installs and versions together |
| **Skill** | the job, as the user would say it — a verb or a short noun phrase | it is what gets typed |
| **Entry skill** | one per plugin, the thing you reach for when you do not know the sub-step | a cluster needs a front door, not a directory |
| **Never** | repeat the plugin name inside the skill name | `plugin:skill` is the address; saying it twice wastes the only characters a reader scans |

**The bare name must stand alone.** A skill is invocable bare as well as as `plugin:skill`, and bare
is what people type. So the name must be unambiguous across the whole installed estate, not just
inside its plugin — check with `qmd query "<name>" -c plugin-skills -c skills -c skills-share`
before claiming one.

**The description is a trigger, never a summary of the workflow.** Measured elsewhere: a description
that summarises the steps makes the agent follow the description and skip the body. Say what the
skill is for and when to reach for it, list the phrases a user would actually type, and name what it
is *not* for with the sibling that owns that instead.

## Two clarifications, from applying it 2026-09-12

**The front door takes the cluster's own name.** A plugin with several skills still needs one you
reach for when you do not know the sub-step, and that one is named after the cluster:
`deliberate:deliberate`, `j-research:j-research`, `j-business:j-market`. It looks like repetition and
is not — it is the address of the front door, and it is what people actually type.

**A term of art beats the anti-stutter rule.** `j-research:j-deep-research` stutters and stays,
because "deep research" is what the user says and renaming it to something tidier would cost more in
discoverability than the stutter costs in readability. The rule exists to stop the plugin name doing
the skill's work — not to ban a word the reader is looking for.

**What was renamed:** `j-research-start` → `j-research` (it was the front door all along),
`j-research-inbox` → `j-inbox`, `j-research-triage` → `j-triage`. Left alone deliberately:
`j-independent-ideation` (53 references for a readability gain), `j-paperclip-ops`, and the
`wigolo-*` set, which is a vendor namespace rather than ours.
