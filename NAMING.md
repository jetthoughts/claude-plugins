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
`wigolo-*` skill set inside `j-wigolo`, which names a vendor tool rather than ours.

## Every plugin gets the prefix, no exceptions (Paul, 2026-09-24)

The "house-specific" carve-out above no longer applies at the plugin-name level: `unfix`,
`deliberate`, `harness-setup`, `cognee`, `wigolo`, and `personal` were renamed to
`j-unfix`, `j-deliberate`, `j-harness-setup`, `j-cognee`, `j-wigolo`, `j-personal` — including
the ones naming an external methodology or vendor product. The term-of-art exception still
applies one level down, to skill names inside a plugin (`wigolo-*`, `j-research:j-deep-research`).

## One home, two deliveries (Paul, 2026-09-13; delivery corrected 2026-09-30)

Measured that day: `~/.claude/skills` held 458 entries in five homes, two of them unversioned, and three edits to three house skills landed in three different places. So:

- **This repo is the only home for a house skill.** A skill is a folder inside its domain plugin. `~/.claude/skills` is **not** a house-skill home; skillshare holds third-party packs only; a project keeps a skill in its own `.claude/skills` only when the skill reads that project's files.
- **A change is a commit here.** Never edit a copy elsewhere — not a symlink target, a Paperclip catalog copy, or a plugin cache. Bump `version` in `plugin.json` when a skill's behaviour changes.
- **Sources travel with the skill.** A skill that rests on a method carries a `## Sources` section: URL, retrieval date, an excerpt under 30 words per load-bearing claim; local adaptations marked ours; a claim without a source is UNSUPPORTED.
- **Delivery to Claude Code sessions** is the marketplace in `.claude-plugin/marketplace.json`: `claude plugin marketplace add <path or git URL>`, then `claude plugin install <plugin>@jetthoughts`. Installed plugins are cached copies. A behaviour change bumps `plugin.json` **and** then needs `claude plugin update <plugin>@jetthoughts` — `claude plugin marketplace update` refreshes marketplace metadata only and will *not* touch installed copies (measured 2026-09-30; the older note here said otherwise). Installed skills are invoked as `plugin:skill`; the bare name does **not** work, and that is intended. Live development uses `claude --plugin-dir <plugin>` for one session. See INSTALL.md.
- **Delivery to Paperclip seats** is `paperclip-skills.json`: slug to file. Seats launch with `--setting-sources=project,local`, so nothing in `~/.claude/skills` reaches them; the catalog copy is the only path, and it is re-imported when the file changes.

### What the symlink model actually cost (2026-09-30)

The line above used to read "`~/.claude/skills/<name>` is a symlink into this checkout on Paul's machine and nothing more", and `README.md` documented `ln -s` as the way to add a skill. That recipe produced, measurably:

- **22 self-referential symlinks committed to git** with absolute `/Users/pftg` paths — 6 already broken by the plugin rename, and non-portable to any other machine.
- A symlink-following glob that saw **592** `SKILL.md` files where `find` saw 99, and a `du -L` that did not terminate.
- A plugin cache whose entries had **empty targets**, which made `harness-setup`, `j-research` and `j-ideation` report **"failed to load"**.
- A **stale clone of this repo** at `~/.config/skillshare/skills/_claude-plugins`, frozen on 2026-09-24, reached by 78 mangled symlinks and serving pre-rename skills to every session while the live repo moved on.

Skill delivery is now the marketplace **only**, with no second checkout and no symlinks, because a second path is what let the first one go stale unnoticed. `scripts/validate_skills.py` fails the build on any committed symlink, so this cannot return quietly. Full account: `SKILLS_REVIEW.md`.

### A package change needs a version bump *and* an update

Measured 2026-09-30, because the two commands are easy to conflate:

| Command | What it does |
|---|---|
| `claude plugin marketplace update jetthoughts` | refreshes marketplace **metadata**; does not touch installed copies |
| `claude plugin update <plugin>@jetthoughts` | refreshes the installed **copy** — and only if `version` changed |

Bumping without updating changes nothing; updating without bumping reports "already at the latest version" and rebuilds nothing. Both, in that order.
