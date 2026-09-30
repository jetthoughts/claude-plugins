# Skills review and simplification proposal

Measured 2026-09-29 against this checkout and the four skill homes on this machine.
Every claim below is a command output, not an impression. Reproduce with the
commands in [§7](#7-how-to-reproduce).

## Verdict

The skill *library* is mostly sound. Three things are not: **the delivery path**
(sessions read a five-day-stale pre-rename clone, not this repo), **22 self-referential
symlinks** that are committed to git with absolute paths, and **two clusters that
overlap by design** (19 skills doing one decision job, 22 doing one research job).

Fixing T0 + T1 is mechanical and high-value. T2 is judgement and needs your call.

---

## 0. Remediation status (2026-09-30)

Phases 0, 1 and 2 are **done and verified**. Phase 3 (cluster consolidation) and Phase 4
(progressive disclosure) are **not started** — see [§4](#4-phased-plan).

| Measure | Before | After |
|---|---|---|
| Tracked symlinks in `plugins/` | 22 | **0** |
| Broken symlinks | 6 | **0** |
| `SKILL.md` seen by a symlink-following glob | 592 | **85** |
| YAML frontmatter failures | 2 | **0** |
| Tracked `.pyc` files | 3 | **0** |
| Shipped duplicate skill names | 2 | **0** |
| Dangling repo-path references | 6 | **0** |
| Plugins with a valid `plugin.json` | 14 of 17 | **16 of 16** |
| Plugins in `marketplace.json` | 12 | **16** |
| Plugins reporting *failed to load* | 3 | **0** |
| Empty-target symlinks in the plugin cache | 30 | **0** |
| Stale pre-rename plugin install records | 89 | **0** |
| Validator errors | — | **0** |

Four things were discovered only by doing the work, and are recorded above as T0.7 and
T1.3: the invalid `commands` manifest key that took `j-research` down, the 30
empty-target symlinks in the plugin cache, the 86 duplicate `jt-delivery` records (one
per pkm worktree), and the fact that my first version of T1.3 was simply wrong.

Two decisions from the review were **reversed by evidence**:

- **T1.3 was wrong.** I reported the marketplace as unregistered and no house plugin as
  installed. Both were false — I had read a truncated `installed_plugins.json`. The
  marketplace was registered and 20+ house records existed under pre-rename names.
- **`j-delivery-workspace` cannot be "installed".** It has **zero tracked files**; it is
  gitignored eval scaffolding holding a snapshot copy of `j-delivery`. It is the one
  directory in `plugins/` that is not a plugin, and it stays out of both manifests.

Delivery now runs through the marketplace only, as decided. Withdrawing the stale clone
*removes* the fallback path, so this only works because the 16 plugins were reinstalled
from the corrected repo — that ordering mattered and is the reason Phase 1 was done
before Phase 3.

---

## 1. Baseline

| Measure | Value |
|---|---|
| Plugin directories on disk | 17 |
| Plugins in `marketplace.json` (installable) | 12 |
| `SKILL.md` under `plugins/` | 86 |
| — in canonical `plugins/*/skills/*/SKILL.md` layout | 82 |
| — distinct skill `name:` values | 81 |
| `SKILL.md` outside `plugins/` (`.claude/skills`, `drafts/`) | 13 |
| Skill descriptions loaded every session | 30,474 chars ≈ **7.6k tokens** |
| Body text (loaded only on invoke) | 502,589 chars ≈ 126k tokens |
| Tracked symlinks / of which broken | 22 / **6** |
| Tracked build artifacts (`*.pyc`) | 3 |
| Git dirty files | 38 |

The description budget is the recurring cost. 7.6k tokens is paid in every session
before any work starts; it is worth defending, but it is not the emergency.

---

## 2. Findings, by damage

### T0 — Broken now (an agent hits these today)

**T0.1 — Invalid YAML frontmatter, including a shipped plugin's front door.**

`deliberate` and `bos-categorize` put an unquoted `: ` inside the `description` plain
scalar. A strict YAML load fails outright:

```
plugins/j-deliberate/skills/deliberate/SKILL.md:2
  mapping values are not allowed here ... line 2, column 71
plugins/hermes-bos/skills/bos-categorize/SKILL.md:2
  mapping values are not allowed here ... line 2, column 150
```

`deliberate` is the front door of `j-deliberate`, a marketplace plugin. Depending on
the loader's leniency, its `name`/`description` are dropped or mangled — so the skill
may not be routable at all. Fix: quote the description, or replace the offending
`decision: gather` / `categories: quick-lookup` colons.

**T0.2 — 22 tracked self-referential symlinks with absolute paths.**

Every one of these points at its own container directory:

```
plugins/j-paperclip/skills/j-paperclip/j-paperclip -> /Users/pftg/dev/claude-plugins/plugins/j-paperclip//skills/j-paperclip
plugins/j-ideation/skills/j-mapping-assumptions/j-mapping-assumptions -> .../skills/j-mapping-assumptions
(+ 20 more, tracked in git)
```

Three consequences:

- **Infinite recursion.** A symlink-following glob sees **592** `SKILL.md` files
  where `find` sees 99. `du -L plugins` does not terminate.
- **Non-portable.** Targets are absolute `/Users/pftg` paths, committed to git. A
  clone on any other machine gets 22 dead links.
- **6 are already broken** — leftovers of the 2026-09-24 rename, still pointing at
  pre-rename paths: `plugins/deliberate/…`, `plugins/unfix/…`, `plugins/harness-setup/…`,
  plus `j-research-triage` and `j-research-inbox` under `j-research/skills/`.

They look like fallout from the README's documented migration (`mv` of a directory
that still contained the `ln -s`). They carry no information: delete all 22.

**T0.3 — Two skills declare the same output path.**

`j-convening-the-council` and `j-evaluating-interfaces` both declare
`09-council/consensus-report.md` as their Output, with different content shapes
(Delphi median report vs UX heat map). Whichever runs second overwrites the first.
Fix: the interface skill must own `09-ux/ux-heatmap.md`.

**T0.4 — A description advertises three skills that do not exist.**

`j-jobseek`'s description routes the user to `j-board-run`, `j-apply-one-job` and
`j-linkedin-engage`. None exist anywhere in the repo, and the skill's own body
(line 14) says so: *"Three routes below are dead"*. The description and the body
contradict each other, and the description is what the router reads. Remove the dead
routes from the description and the `next` row, or restore the skills.

**T0.5 — Dangling references (6).**

| Referenced | By | Reality |
|---|---|---|
| `references/legal_notes.md` | `j-personal/skills/berlin-rental-agreement` | `references/` is an **empty shipped directory** |
| `templates/operating-system.md` | `j-business/skills/eos-lite` | `templates/` holds only `scorecard.md`, `weekly-review.md` |
| `skills/jobs-to-be-done/SKILL.md` | `j-deliberate/skills/problem-statement` | not in repo |
| `skills/proto-persona/SKILL.md` | same | not in repo |
| `skills/positioning-statement/SKILL.md` | same | not in repo |
| `skills/user-story/SKILL.md` | same | not in repo |

`problem-statement` is 9.1k chars of otherwise-generic PM text whose four
dependencies all live in *other* skill libraries. Fold or prune it (see T2.1).

**T0.6 — Conflicting standing instructions about which tool to use.**

This one is not a dead link but an unresolvable contradiction the agent hits on its first
research request: five skills claim routing authority and four ladders disagree on order,
on whether a cost gate applies, and on whether `agent-reach` may run at all. The
canonical policy file flags the clash and declines to resolve it. Full detail in T2.2 —
it is listed here because it is load-bearing *today*, not a cleanup item.

**T0.7 — An invalid manifest key silently killed a whole plugin.**
*(Found 2026-09-30 while fixing T0.2 — it was not in the first version of this review.)*

`plugins/j-research/.claude-plugin/plugin.json` declared:

```json
"commands": ["sync-perplexity"]
```

Component keys take a **path**; commands are auto-discovered from `commands/`. The CLI
rejects the manifest, and the failure is total, not partial:

```
Error: Plugin j-research has an invalid manifest file at
.../plugins/j-research/.claude-plugin/plugin.json.
Validation errors: commands: Invalid input
```

so `claude plugin list` reported `j-research@jetthoughts` as **"failed to load"** and the
plugin's nine skills were unavailable — including at project scope in `pkm`. The command
itself (`commands/sync-perplexity.md`) was always fine; only the declaration was wrong.
`j-delivery` ships two commands and declares no such key, which is the correct pattern.

---

### T1 — Delivery topology: edits are not reaching sessions

This is the largest finding and it is not about skill content at all.

**T1.1 — Sessions read a stale, pre-rename clone, not this repo.**

`~/.config/skillshare/skills/_claude-plugins/` is a **partial git clone of this repo**
(`origin = file:///Users/pftg/dev/claude-plugins`), frozen at **2026-09-24** — before
the plugin rename. It still contains `plugins/deliberate`, `plugins/unfix`,
`plugins/wigolo`, `plugins/cognee`, `plugins/personal`, `plugins/harness-setup`.

`~/.agents/skills` holds **78 symlinks** into that clone, under mangled names:

```
~/.agents/skills/_claude-plugins__plugins__deliberate__skills__deliberate
```

Divergence is measurable:

| Skill | clone | live |
|---|---|---|
| `j-research` | `0358e21ddd` | `311c12ad8f` (**13 changed lines**) |
| `j-paperclip-ops` | `2ded4c8741` | `cdf004f380` (**23 changed lines**) |
| `deliberate` / `j-deliberate` | **absent** | present |

**16 live skills are never delivered by any path**, including
`cross-check-agent-claims`, `bos-research-incident`, `evolve-agent-skills` and
`product-discovery`.

**T1.2 — The one-home rule is stated but not enforced.**

`NAMING.md` says "skillshare holds third-party packs only" and "`~/.claude/skills/<name>`
is a symlink into this checkout". Neither is true today. House skills live in four
places:

| Home | Entries | House-skill copies |
|---|---|---|
| `~/.config/skillshare/skills` | 433 | **79** |
| `~/.agents/skills` | 160 | 3 (+78 mangled links to the clone) |
| `~/.claude/skills` | 90 | 2 |
| repo `plugins/` (canonical) | 86 | 81 |

Across homes: **775 catalog entries for 664 distinct names**, 96 names in more than
one home. That redundancy is what inflates the session catalog and re-creates the
"three edits in three places" failure `NAMING.md` was written to end.

**T1.3 — The installed plugin state is corrupted, and five plugins could not be installed.**
*(Corrected 2026-09-30 — the first version of this finding was wrong: the `jetthoughts`
marketplace **is** registered, at `~/.claude/plugins/cache/jetthoughts`, and house
plugins **are** installed. My earlier check read a truncated `installed_plugins.json`
and concluded otherwise.)*

What is actually true is worse. Every one of the **30 symlinks** in the plugin cache has
an **empty target** (`readlink` returns `""`), which is why `claude plugin list` reports
`harness-setup@jetthoughts`, `j-research@jetthoughts` and `j-ideation@jetthoughts` as
**"failed to load"**. All 30 date from 2026-09-16 to 2026-09-24 — they are a direct
consequence of T0.2: the plugin copy process could not represent the repo's
self-referential symlinks and wrote zero-length links instead. Removing those symlinks
(T0.2) was necessary; the cache still needs rebuilding.

Separately, the installed set is a museum of renamed and duplicated identities:

| Stale record | Status |
|---|---|
| `jt-delivery@jetthoughts` × 30 | disabled |
| `harness-setup@jetthoughts` × 3 | failed to load |
| `cognee@jetthoughts`, `deliberate@jetthoughts`, `unfix@jetthoughts`, `wigolo@jetthoughts` | disabled (pre-rename names) |
| `llm-wiki@jetthoughts` | present in cache, not a plugin in this repo |
| `j-business`, `j-delivery`, `j-lanes` | installed at **both** user and project scope, repeatedly |

And the five plugins that were absent from `marketplace.json`: `hermes-bos` (19 skills),
`hermes-ops`, `search-routing`, `j-linkedin-post`, plus `j-delivery-workspace`, which is
not a plugin at all (zero tracked files; gitignored eval scaffolding).
`hermes-ops` and `search-routing` had **no `plugin.json`**.

**T1.4 — The Paperclip catalog was delivering almost nothing.**
*(Found 2026-09-30 while checking the merges would not break it — not in the first version
of this review.)*

`paperclip-skills.json` maps a catalog slug to a file path, and the instrument sweep
re-imports a slug only when that file changes. A path that stops resolving therefore fails
**silently**: the seat keeps whatever copy it last imported and nothing reports an error.

Six of the seven entries were broken, by two independent drifts:

| Slug | Was | Why it broke |
|---|---|---|
| `ldj`, `lightning-demos`, `five-whys`, `decision-panel` | `plugins/deliberate/…` | the plugin rename to `plugins/j-deliberate` |
| `house-rules` | `Documents/pkm/paperclip-house-rules.md` | vault moved to `~/dev/pkm`, file now in `Notes/` |
| `method-catalogue` | `Documents/pkm/management-methodologies.md` | same, file now in `Topics/` |

Only `practice-research` resolved — because it was already filed under `j-research`. The
seats were running on stale or absent copies of four of their five delivered skills. All
seven now resolve, and validators check E7 fails the build on any future drift.

**T1.5 — The vault path in skill bodies is stale.**
The vault moved from `~/Documents/pkm` to `~/dev/pkm`; `~/Documents/pkm` is now a
three-file stub (`getting-started.md`, `index.md`, `log.md`) with no git. Five files still
reference the old path — `j-triage`, `j-inbox`, `j-perplexity-sync`, `README.md` (all
fixed) — and the risk is the same silent-failure class as T1.4: a skill that reads a stub,
finds nothing, and reports success.

---

### T2 — The skill set itself

**T2.1 — `j-ideation` + `j-deliberate`: 19 skills for one job.**

Both are "gather independent evidence, then decide". `deliberate` runs
FRAME→GATHER→LEDGER→IDEATE→DECIDE inline; `j-independent-ideation` is the same
pipeline as a numbered workspace with validators and a human gate.

What they do **not** share, and a merge must not erase:

- **Authority.** `decision-panel` runs a sealed, binding ballot with a named Decision
  Voter and board approval. `j-convening-the-council` is explicitly *advisory*
  ("Decision-support, never a voting machine"). These are different instruments; merging
  them would silently change who decides.
- **Determinism.** j-ideation ships 4 stdlib validators and per-score `E-nnn` citation
  requirements. `deliberate` *refuses* checkers on principle and verifies by a human
  opening citations.
- **Entry conditions.** `ldj` is 40 minutes, no research, human dot-vote. `deliberate`
  is for questions that are "true". `j-independent-ideation` is for questions that are
  "going".

Proposed: one front door (`deliberate`) plus one artifact contract
(`j-decision-workspace`, from `j-independent-ideation`), folding the thin skills into
their siblings:

- `lightning-demos` ← absorbs `j-scanning-lightning-demos` (which self-describes as
  an add-on to it, and owns only isolation + `E-nnn` citation)
- `framing` ← `j-framing-the-question` + `problem-statement` + `structural-decisions`
  + `five-whys` (decision sentence, metric, reversibility, root cause, shape gate)
- `j-evaluating-interfaces` must own `09-ux/ux-heatmap.md`, not `consensus-report.md`

Kept apart deliberately: `decision-panel`, `ldj`, `deliberate`,
`j-convening-the-council`, `j-making-the-call`.
Net: **19 → about 15**, with no loss of authority or determinism.

**T2.2 — Research: five competing front doors, and four contradictory ladders.**

Five skills claim routing authority over the same requests:

| Claimant | Claim |
|---|---|
| `j-research` | "the front door for **any** open-web research request" |
| `wigolo` | "Use wigolo for **ALL** web operations" (unconditional) |
| `search-routing` | "the tool-level router underneath it" |
| `bos-research` | "searxng — first rung for any web fact; wigolo **off-ladder**" |
| `local-deep-research` | "searxng → tavily; never a silent fallthrough" (outside this repo) |

`search-routing` — the one that claims to be the router — carries
`disable-model-invocation: true`, so it **can never be invoked**, and it is not in
`marketplace.json`. Its twin `setup/SKILL.md` has the identical name and a *different*
routing table (one omits tavily).

Worse, the ladders contradict each other on three axes:

- **Order.** `j-deep-research` gives three alternatives in one file
  (`searxng → perplexica → tavily`, `perplexica → searxng → ldr`,
  `searxng → perplexica → tavily → ldr`), then says "pick the ladder that matches
  the tools actually available" — which delegates the conflict back to the agent.
  `j-research` gives `wigolo → perplexica → keyed/cloud`. `bos-research` gives
  `searxng → tavily` with wigolo explicitly off-ladder.
- **Cost gate.** `j-research`: "**No cost gate** — pick by fit." `bos-research`:
  tavily is "**the single metered fallback** ... do not use a metered tool silently."
- **`agent-reach`.** `j-research` routes platform names to it. `bos-research-incident`
  says "**never run `agent-reach`** if tavily with `include_domains` works first."

The canonical policy file (`~/.infra/.okf/references/research-routing.md`) notices this
and *flags rather than resolves* it: "it conflicts with the global CLAUDE.md instruction
to prefer wigolo for all web ops — flagged, not silently overridden."

Fix: **one front door, `j-research`** — the only skill that enumerates the whole stack
*and* hands off, and the one `search-routing` already names. Demote `wigolo`'s line 4 to
"default fetch/search backend", register-or-delete `search-routing`, and make
`bos-research` cite `j-research`'s table instead of restating a competing ladder.

Then collapse the wrappers: `j-wigolo`'s 11 skills total 45,573 bytes, and the 10
sub-skills are identical in shape — frontmatter, a Quick Reference JSON block, a
parameter table, a See Also. The front door's 10-row table **is already the router**.
Collapse to `skills/wigolo/` plus `references/<tool>.md`, following the existing
non-skill `skills/wigolo/rules/` precedent. That removes 10 ambient descriptions and
the trigger collisions between `wigolo-cache` ("before any web request") and
`wigolo-search` / `wigolo-research` / `j-deep-research`.

**Caveat:** `wigolo` is a vendored upstream fork (`author: KnockOutEZ`,
`v0.1.43-beta.2`, AGPL-3.0-only). Collapsing it creates a divergence that needs a sync
step, so this is a fork decision, not a free refactor.

**T2.3 — Duplicate and misnamed skills.**

- `search-routing` ships **two skills with the identical name and identical description**
  (`skills/search-routing/SKILL.md` and `skills/setup/SKILL.md`), with divergent bodies.
  The router cannot choose between them. Delete one.
- `j-business` has three cluster skills (`j-market`, `j-offer`, `j-publish`) and **no
  front door**, contrary to `NAMING.md`'s "one per plugin". Same for `j-personal`.
- `j-linkedin-post` is a single skill that repeats its plugin name — the exact pattern
  `NAMING.md` bans. It is also not in the marketplace.

**T2.4 — Manifest drift.**

- Root `plugin.json` lists 11 plugins, **5 under pre-rename names** (`cognee`,
  `deliberate`, `harness-setup`, `unfix`, `wigolo`) and omits 11 real directories.
  It disagrees with `marketplace.json`, which is the file that actually installs.
- `j-deliberate/.claude-plugin/plugin.json` describes 5 skills; the plugin ships 7.
- `j-harness-setup` documents itself as "**One** instruction-only skill" (plugin README)
  and "One explicit skill, no bundled agents" (root README). It ships **3**, including
  `omniroute-manager` (22.1k body) and `browseros-neo`. Neither is harness setup. Both
  READMEs are now false.
- `j-delivery-workspace` contains **two** `plugin.json` files, one of which declares
  `"name": "j-delivery"`.

**T2.5 — Two skills disagree on where research notes land.**

`j-inbox` documents output as `research-<source>-<slug>.md` **at vault root**.
`j-perplexity-sync` (12.1k, the plugin's largest) says notes land in
`evidence/perplexity/<project>/pplx-<id8>-<slug>.md`. `j-triage` then selects exactly
`evidence/perplexity/*/pplx-*.md` — so triage can only ever find what
`j-perplexity-sync` writes, never what `j-inbox` documents. Fix: `j-inbox` owns the
layout contract; `j-perplexity-sync` shrinks to acquire → `_inbox` → call `j-inbox`.

Also unreachable: `research-deep` never appears in `j-research`'s menu. It is a third
distinct job (outline runner) sharing a name with `j-deep-research` (LDR synthesis).
Rename it rather than merge it.

---

### T3 — Cost hygiene

**T3.1 — Progressive disclosure is barely used.** 11 skills exceed 8,000 body chars
with no `references/` directory, so the whole body lands in context on invoke:

| Skill | Body |
|---|---|
| `web-research-lanes` | 27,390 |
| `j-paperclip-ops` | 24,526 |
| `j-venture` | 20,367 |
| `bos-incident-response` | 18,159 |
| `bos-research-incident` | 17,311 |
| `bos-omniroute-ops` | 13,688 |
| `contract` | 11,703 |
| `j-perplexity-sync` | 11,589 |
| `j-jobseek` | 9,535 |
| `berlin-rental-agreement` | 9,046 |
| `bos-intake` | 8,363 |

**T3.2 — `web-research-lanes` is the worst cost/value ratio in the estate.** 27,390
chars — the largest body in the repo — behind a **57-character** description, so it is
invisible to routing and expensive when it does load. It is also misfiled: the
description calls it a "deep-research lane matrix for qwen, perplexity, deepseek", but
the body is a consumer **browser-session manual** (Qwen/Kimi/Perplexity/DeepSeek entry
URLs, completion heuristics, ego-browser selectors, chat rename/delete sequences) with no
searxng/tavily ladder in it at all. Nothing in its own plugin references it; its only two
inbound references are mis-pointers that expect a research ladder. Its content is already
restated in `plugins/j-research/RESEARCH_TOOLS.md`. It is reference data, not a skill:
move it to `plugins/j-research/skills/j-research/references/` and drop the standalone
description.

**T3.3 — Committed junk and divergent duplicates.** 3 tracked `.pyc` files under
`__pycache__/`. `RESEARCH_TOOLS.md` exists in **three** places with three different
contents:

| Path | Bytes |
|---|---|
| `RESEARCH_TOOLS.md` (root) | 13,239 |
| `plugins/j-research/RESEARCH_TOOLS.md` | 27,067 |
| `plugins/j-research/.okf/RESEARCH_TOOLS.md` | 21,514 |

Three copies of one tool inventory will drift further. Pick one as canonical — the OKF
bundle is the natural home — and make the others reference it. Also:
`j-deliberate/deliberate-workspace/skill-snapshot{,-prev}/` hold two more 22–25k copies
of `deliberate`; they are gitignored so they never ship, but they are live local
skill-discovery noise.

---

## 3. Proposed target state

1. **One home, verified.** `plugins/` is the only source. No symlinks anywhere in the
   tree; no clone; house skills reach a session through exactly one mechanism.
2. **Every plugin installable or archived.** 17 → either listed in `marketplace.json`
   with a `plugin.json`, or moved to `archive/`. No third state.
3. **No duplicate skill names** anywhere in the estate (a validator enforces this).
4. **Descriptions are triggers.** One sentence of purpose, the phrases a user types, an
   explicit "not for — use X". Budget: ≤ 320 chars, ~6k tokens total.
5. **Bodies are procedures.** Anything over ~8k chars moves detail into `references/`.
6. **Every plugin has a front door**, named after the cluster.

Projected effect: 17 → ~14 plugins shipped, 81 → ~65 distinct skills, catalog
descriptions 30.5k → under 20k chars (≈7.6k → 5k tokens/session), 22 broken or
recursive links removed, one research front door instead of five, and live skills
actually reaching sessions.

---

## 4. Phased plan

Each phase is independently shippable and reversible.

### Phase 0 — Stop the breakage — **DONE** (mechanical, no judgement)

```bash
cd /Users/pftg/dev/claude-plugins

# 0.1 delete the 22 self-referential symlinks (6 are already broken anyway)
find . -path ./.git -prune -o -type l -print | while read -r l; do
  t=$(readlink "$l")
  case "$t" in "$PWD"/*) git rm -q --cached "$l" && rm "$l" && echo "removed $l";; esac
done

# 0.2 quote the two broken descriptions, then prove every frontmatter parses
python3 -c "
import re,glob,yaml,sys
bad=0
for f in glob.glob('plugins/*/skills/*/SKILL.md'):
    t=open(f,encoding='utf-8').read()
    m=re.match(r'^---\n(.*?)\n---\n',t,re.S)
    try: yaml.safe_load(m.group(1))
    except Exception as e: bad+=1; print('FAIL',f,e)
print('frontmatter failures:',bad); sys.exit(1 if bad else 0)"

# 0.3 drop tracked bytecode
git ls-files | grep '\.pyc$' | xargs -r git rm -q --cached
git ls-files | grep '__pycache__' | xargs -r git rm -q --cached
printf '\n__pycache__/\n*.pyc\n' >> .gitignore
```

Also: delete `search-routing/skills/setup/SKILL.md` (same-name duplicate), remove the
empty `berlin-rental-agreement/references/` dir, and fix the `eos-lite` template path.

### Phase 1 — Make delivery true — **DONE**

The plan below was written before the work and was **partly wrong**: the marketplace was
already registered, so step 1 was a no-op. What was actually required, in order:

1. Fix everything in the repo first (Phases 0 and 2), because a cached plugin copy can
   only be refreshed by a **version bump** — `claude plugin marketplace update` refreshes
   marketplace metadata, it does **not** touch installed copies.
2. Bump the version of every plugin whose content changed, then
   `claude plugin update <plugin>@jetthoughts`. Bumping without updating changes nothing;
   updating without bumping reports "already at the latest version" and rebuilds nothing.
3. Install the plugins that only existed under pre-rename names
   (`j-deliberate`, `j-harness-setup`, `j-personal`, `j-cognee`, `j-unfix`, `j-wigolo`)
   and uninstall the stale identities.
4. Remove the stale clone and its 78 symlinks — **do this last**, because it removes the
   only path that was still serving *some* version of these skills:
   ```bash
   find ~/.agents/skills -maxdepth 1 -type l -name '_claude-plugins__*' -delete
   rm -rf ~/.config/skillshare/skills/_claude-plugins
   ```
5. Prune the bookkeeping: orphaned project-scope records, superseded version directories.
   Back up `installed_plugins.json` first — it is live config, not a build artifact.

Verify with `claude plugin list | grep 'failed to load'` (expect nothing) and
`find ~/.claude/plugins/cache/jetthoughts -type l` (expect no empty targets).

Note for anyone repeating this: before step 4 the session skill catalog *still listed*
the house skills from the stale clone; after step 4 they vanish until step 2/3 have
landed. That gap is expected, not a bug — but it means the order cannot be shuffled.

### Phase 2 — Reconcile manifests and prune — **DONE**

- Rewrite root `plugin.json` to match `marketplace.json`, or delete it if
  `marketplace.json` is authoritative (it is).
- For each of `hermes-bos` (19 skills), `hermes-ops`, `search-routing`,
  `j-delivery-workspace`, `j-linkedin-post`: **install or archive**, no third state.
  `hermes-bos` is 19 skills with no `plugin.json`'s siblings — decide whether it is a
  live estate or a superseded one before spending effort inside it.
- Fix `j-deliberate/plugin.json` (describes 5 of 7 skills) and
  `j-harness-setup/README.md` (claims 1 skill, ships 3 — and `omniroute-manager` belongs
  in its own plugin, not in harness setup).
- Remove the second `plugin.json` in `j-delivery-workspace`.
- Reconcile the three `RESEARCH_TOOLS.md` files into one canonical copy (the OKF bundle
  is the natural home) and have the others point at it.

### Phase 3 — Consolidate the two clusters, and settle routing — **DONE**

The merges ran as three disjoint workstreams (decision cluster, research cluster,
progressive disclosure) so they could not fight over the same files. Outcome:

| Cluster | Before | After |
|---|---|---|
| `j-ideation` + `j-deliberate` | 19 skills | **16** |
| `j-wigolo` | 11 skills | **1** skill + 11 references |
| `j-research` | 9 skills | **8** |

**Decision cluster.** `j-scanning-lightning-demos` folded into `lightning-demos`
(its unique content — the five isolated roles, the ≥30% outside-industry check, `E-nnn`
citation, UNKNOWN-on-shortfall — moved across, with the detail in
`references/agent-evidence-contract.md`). A new `framing` merged
`j-framing-the-question` + `problem-statement` + `structural-decisions` into three
parts: decision frame, problem narrative, shape-versus-fix gate. `five-whys` became a
thin alias keeping its root-cause drill. **The four Paperclip slugs survive with exact
names** (`ldj`, `lightning-demos`, `five-whys`, `decision-panel`), as decided.

`j-deliberate` is now 6 skills (`deliberate`, `framing`, `lightning-demos`, `five-whys`,
`decision-panel`, `ldj`), `j-ideation` is 10 (router + 9 stages).

**Routing settled.** One ladder, owned by `j-research`, in order:
`searxng` → `tavily` as the single metered fallback, announced in the answer → built-in
`web_search`/`web_extract` only when both fail, naming the failed rung. `wigolo` and
`perplexica` are **off-ladder roles, not rungs** — which is what `j-wigolo`'s description
now says outright. `j-deep-research`'s three-in-one ladder and its
"pick the ladder that matches the tools available" escape hatch are gone; it now states
there is only one ladder and it belongs to `j-research`.

`search-routing` kept `disable-model-invocation: true` and was instead relabelled
honestly: *"This is not a router and not a second front door."* That was one of the two
options offered, and it is the more truthful of them — the skill was never invocable, so
pretending otherwise would have been worse.

**T0.3 fixed.** `j-convening-the-council` owns `09-council/consensus-report.md`,
`j-evaluating-interfaces` owns `09-ux/ux-heatmap.md` and states it never overwrites the
council's report. Both paths are in the router's artifact contract.

**T2.5 fixed.** `j-inbox` owns the layout contract; `j-perplexity-sync` agrees with it and
with `j-triage`, so triage can now find what sync writes.

**T3.2 done.** `web-research-lanes` (the 27,390-char browser-session manual behind a
57-character description) moved to `references/consumer-lanes.md`.

### Phase 4 — Progressive disclosure and a description budget — **IN PROGRESS**

Descriptions trimmed — catalog cost 31,097 → **29,196 chars** (≈7.8k → 7.3k tokens/session):

| Skill | Description before | after |
|---|---|---|
| `board-flow` | 800 | 377 |
| `j-venture` | 711 | 441 |
| `j-paperclip-ops` | 905 | 438 |
| `j-paperclip` | 705 | 419 |
| `berlin-rental-agreement` | 835 | 380 |

Two remain and belong to the cluster work still running: `j-research` (1,039) and
`lightning-demos` (817).

Still to do:

- `web-research-lanes` → `references/` under the research front door; drop its standalone
  description.
- Collapse the 11 `wigolo-*` skills (45,573 bytes) into `skills/wigolo/` plus
  `references/<tool>.md`, following the existing non-skill `skills/wigolo/rules/`
  precedent. **This is a fork, not a refactor:** wigolo is vendored upstream
  (AGPL-3.0-only, `v0.1.43-beta.2`). Record the upstream revision forked from and add a
  sync step, or the collapse turns a clean vendor copy into an unmergeable local branch.
- Move the other T3.1 monoliths' detail into `references/`.
- Rewrite descriptions to the `NAMING.md` contract: trigger, typed phrases, explicit
  "not for". Several of the strongest skills already do this well — `j-jobseek`,
  `j-perplexity-sync` and `j-offer` are the models to copy.

---

## 5. Guardrail — **BUILT**

The findings above were all mechanically detectable, which means they should not need a
review to catch again. `scripts/validate_skills.py` now fails the build on:

| Check | Severity | Catches |
|---|---|---|
| E1 | error | frontmatter that does not parse as YAML, or has no `name`/`description` |
| E2 | error | any symlink committed under `plugins/` |
| E3 | error | a skill `name` duplicated anywhere in the estate |
| E5 | error | a repo-relative path referenced but absent |
| E6 | error | a `plugin.json` component key that is not path-like (T0.7) |
| W1 | warning | description over the length budget |
| W2 | warning | body over ~8k chars with no `references/` |
| W3 | warning | a plugin missing from `marketplace.json`, or with no `plugin.json` |
| W4 | warning | `plugin.json` `name` disagrees with its directory |

Two things run it, so it does not depend on anyone remembering:

- `.github/workflows/validate-skills.yml` — runs on every push and PR touching `plugins/`.
- `scripts/install-hooks.sh` — a local pre-commit hook, writing into `.git/hooks/`.

The E6 check exists because T0.7 was found by hand while fixing T0.2, not by the review.
Its logic was verified by temporarily reintroducing the invalid key and confirming it
fails, then restoring the fix. Errors block; warnings inform. A warning list that stays
non-empty is the honest state of Phase 3 and 4 work.

---

## 6. What not to change

- **`decision-panel` vs `j-convening-the-council`.** Different authority models
  (binding vs advisory). Merging them changes who decides.
- **`deliberate`'s refusal of automated checkers** vs **j-ideation's validators.**
  Both are defensible; the disagreement is a real design choice, not drift.
- **The `wigolo-*` decision needs your call, not mine.** Collapsing them saves ~1k
  catalog tokens and removes four colliding triggers, but it forks AGPL upstream code.
  If you sync wigolo regularly, keep the 11 and just trim the descriptions; if wigolo is
  effectively vendored-and-frozen, collapse it.
- **`j-research`'s "not for" clauses.** The description is 1,039 chars — over budget —
  but its boundaries are doing real routing work. Trim, do not gut.

---

## 7. How to reproduce

```bash
cd /Users/pftg/dev/claude-plugins

# inventory + frontmatter health
find plugins -name SKILL.md | wc -l
python3 - <<'EOF'
import re,glob,yaml
tot=n=0
for f in glob.glob('plugins/*/skills/*/SKILL.md'):
    t=open(f,encoding='utf-8',errors='replace').read()
    m=re.match(r'^---\n(.*?)\n---\n',t,re.S)
    try: d=' '.join(str(yaml.safe_load(m.group(1)).get('description','')).split())
    except Exception as e: print('YAML FAIL',f); continue
    tot+=len(d); n+=1
print(f'{n} skills, {tot:,} description chars, ~{tot//4:,} tokens/session')
EOF

# symlink loops
find . -path ./.git -prune -o -type l -print | wc -l
find . -path ./.git -prune -o -type l ! -exec test -e {} \; -print   # broken

# delivery divergence
C=~/.config/skillshare/skills/_claude-plugins
(cd $C && git log -1 --format=%ad --date=short)
diff <(cat $C/plugins/j-research/skills/j-research/SKILL.md) \
     <(cat plugins/j-research/skills/j-research/SKILL.md) | wc -l

# catalog duplication across homes
find ~/.claude/skills ~/.agents/skills ~/.config/skillshare/skills -name SKILL.md | wc -l
```

---

## 8. Residual items that need an owner

These are **not** blockers and are outside the repo, so they were reported rather than
changed unilaterally. Each is a real contradiction with the policy you approved, so each
will re-create the T0.6 problem if it is left.

**8.1 — `~/.infra/.okf/references/research-routing.md` says the opposite of the approved policy.**
Its title is *"Research routing — local first, no cost gate"* and its body states: *"the
2026-09-05 'two-rung ladder' and its metered-tool cost gate are gone … there is no 'only
when the others are down' rule left to enforce."* That was a deliberate rewrite on
2026-09-24, but on 2026-09-30 you approved the opposite: **searxng first, tavily as the
announced metered fallback.** The skills now implement your decision and `j-research` owns
the ladder; this file still contradicts it. Whoever owns `~/.infra` should reconcile it —
the drift is recorded explicitly in `bos-research` and `bos-omniroute-ops`.

**8.2 — `~/.claude/CLAUDE.md:356` still says wigolo is for everything.**
`**Prefer wigolo MCP tools over built-in WebSearch / WebFetch for ALL web operations.**`
This is inside a **machine-managed block** (`<!-- wigolo:start v0.2.1 wigolo -->` …
`<!-- wigolo:end -->`), so editing it in place would be overwritten on the next wigolo
update — it needs disabling at the source, not patching. It is the instruction that
`j-wigolo` and the global rules disagreed about; `j-wigolo`'s description now correctly
calls it a backend and not a rung.

**8.3 — `~/.infra/.okf/references/research-tools-inventory.md` is a second inventory.**
It is **not** a duplicate: 72 lines and 4 headings against the repo reference's 742 lines
and 30 headings, structured as *one row per capability* and paired with
`research-routing.md` and the benchmarks. It is a decision matrix; the repo reference is
the manual. They should cross-reference each other rather than merge — but they can now
drift on facts (tool lists, cost models), and nothing checks that.

**8.4 — Four `hermes-bos` SOP bodies remain over 8k with no `references/`.**
`bos-incident-response` (18.2k), `bos-research-incident` (18.0k), `bos-omniroute-ops`
(14.3k), `bos-intake` (8.5k). These are the only remaining validator warnings. Splitting
them is the last unticked Phase 4 item and was left pending your call.
