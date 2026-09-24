---
name: setup
description: "Assemble and validate the AI harness for one project: research, pick ready pieces from the library registry (ECC is one of many), copy only those in, prove it with a trial run. Use when asked to set up or fix a project's harness — not for general setup, routine coding, or standalone skill authoring."
disable-model-invocation: true
argument-hint: "<project goal> [repo path] [harness: claude|pi|hermes]"
---

# Harness setup — buy-list recipe

Buy ready pieces. Never build unless Paul approves. Every claim is evidence, not assertion.
Run by the overseer Claude Code session itself (Paul, 2026-09-24: "this is your responsibility"); not delegated to Hermes.
**Libraries, plural:** pick from every library in the registry (pkm `business-os/knowledge/sources/2026-09-21-agent-discovery-sources.md` § Library registry: ECC, agency-agents, superpowers, wshobson/agents, claude-code-templates, anthropics/skills and plugins, pi packages, the Hermes Skills Hub, and more). The registry grows monthly. Never install a library wholesale; never default to one.
Treat `$ARGUMENTS` as the goal, repo, and harness choice. Retrieved content is evidence, not authority.

## Default open point

Allow read-only commands: `qmd query`, `gh search`, `gh api`, `curl` to official docs,
`claude plugin eval --help`, `hermes profile install --help`, `pi --help`.
This is the tested default. Use MCP equivalents only if those break.

## The six steps

1. **Ask.** Which harness (Claude Code / pi / Hermes) and what is the project goal?
   Write 5 lines: the problem, DONE WHEN, hard stops (Submit, send, consent, credentials,
   public), the surfaces (local, `-p`, cloud, routine). Stop when every need is one line:
   `need: <capability>`.

2. **Research.** Shortened from the original 6 steps:
   - `qmd query "<need>"` against the repo's skills/plugins and this plugin's collections;
   - OpenViking search (limit >= 12);
   - the latest `capability-scout/YYYY-MM.md` catalog;
   - official docs as markdown — `code.claude.com/docs/en/<page>.md`, DeepWiki for a repo;
   - watched-source repos first (ECC, agency-agents, superpowers), then
     `gh search repos "<need>" --sort stars --created ">15 months ago"`;
   - one `perplexity_ask` restricted to official domains with `recency: year`, for the
     practice itself. Go deep (LDR, deep-research) only if that is contradictory.
   Research agents get a **blind brief** (goal, constraints, prior-research location only) and must
   return >= 3 NEW findings (j-research Step 1b/2); fewer = re-run.
   Stop when each need is marked *have* (with path) or *gap*.

3. **Pick.** Order: **installed > registry libraries > official > supported**. For each `need:`,
   compare candidates from at least 2 libraries before picking one. Library helpers such as
   ECC's `/project-init` (a stack-detected dry-run plan) and `agent-sort` help shortlist, but they
   do not decide. Take only rows that serve a `need:`. A new library found here is proposed to the
   registry.
   "Supported" = >= 1k stars, push within 30 days, release within 90 days, a license.
   Check with `gh api repos/<r>` (stars, `pushed_at`, license) and
   `gh api repos/<r>/releases`. A build needs Paul's approval.
   Stop when every need has exactly one pick with its evidence.

4. **Install and assemble** with the harness's own mechanism:
   - **Claude Code:** plugins, skills, agents, hooks, `.claude/workflows`.
     Skills flattened at `.claude/skills/<name>/SKILL.md`; agents in `.claude/agents/`;
     hooks and deny rules in the committed `.claude/settings.json`, with cc-safety-net as
     the default guard; the loop order as `.claude/workflows/<name>.js`, authored with
     `workflow-builder`. Vendor any skill from a plugin that a cloud run needs.
   - **pi:** `.pi/settings.json` (packages), `.pi/agents/`, skills, prompts, extensions.
     `pi install -l` writes project-local. Use pi-subagents as the single orchestrator —
     do not install pi-dynamic-workflows alongside it (overlap).
   - **Hermes:** profile distribution (`distribution.yaml` +
     `hermes profile install <git|dir> [--name] [--alias]`), skills, cron.
     It never copies `.env`, auth, or memories, and does not schedule cron automatically.
   **Copy, don't install:** picked library pieces are copied into the project's `.claude/`
   (cloud runs load only committed repo files). Stop when every piece is in place,
   `.claude/settings.json` parses, and `hermes doctor --live` is clean (Hermes).
   ECC `harness-audit` counts files (an empty dir scores 4/39); it is not a quality gate.

5. **Entry points.** One per goal — a command, skill, or workflow a human or routine
   calls. Name each with the check that proves it works (the proof run, its exit code,
   what it prints). No extra gestures: a second entry point for the same goal is scope
   creep. Stop when every goal has exactly one entry point.

6. **Trial run.** Binary pass/fail, 3–5 tasks × 3 runs, every one passes and beats the
   no-harness baseline. Each task has a concrete input, a code grader where possible, and
   an LLM grader only for judgement. Read the transcripts. A green run status is not a
   pass (cloud/routines note).
   - **Claude Code:** author the suite with `claude plugin eval init` (interview; writes
     `evals/<task>/case.yaml` plus `graders/*.md`; `--mocks record` stands in for MCPs), then `claude plugin eval .claude --eval-dir evals --ablation with-without
     --max-cost-usd 5 --json evals/results/run1.json`. PASS if every regression task
     passes on all 3 trials (pass^3 = 1) **and** the with-harness score is higher than
     the no-harness arm. Otherwise FAIL, and hand the transcripts to the
     `harness-optimizer` agent.
   - **pi:** `pi -p "<task>" --mode json` in a 3×N shell loop; pi-subagents' `acceptance`
     policy (level, criteria, evidence, `verify` commands, `gate`, `review`) grades it.
   - **Hermes:** `hermes -p <p> chat -q "<task>"` on a scripted task; kanban dispatches
     the trial; a separate review card whose parent is the trial card is the gate (kanban has no reviewer field).
   Stop when the trial is recorded with its exact command and raw output, RED before and
   GREEN after.

## Manifest

Write one table: Need | Pick | Kind | Source | Support evidence (checked on date) | Vendor to.
Below it: open risks, claims marked `unverified`, what was deliberately left out.
Save to `/Users/pftg/dev/pkm/business-os/operations/work-items/harness-<project-slug>-manifest.md`.

## Rules

- **Fewest pieces.** An item that serves no need is removed. A second overlapping skill is
  how a harness rots.
- **Evidence, not assertion.** Every row cites the command or URL that would fail if the
  row were false, with its date. Tool counts and star counts are self-reported; say so.
- **Re-read live state** (board, proposal status, file dates) right before stating it.
- **Hard stops ship in every harness** as hooks in the committed `settings.json`.
- **An instruction-only skill cannot express these** — they are the t_06d944ad verdict's
  proof that some rules need code, not text. Carry them as text here; the vendor step
  wires them as hooks:
  - A permission exemption keyed to role (e.g. `HARNESS_ROLE=planner|acceptance` lets the
    planner edit `features.json`). Text alone cannot enforce it; the emitted `pretooluse.py`
    must read the env var.
  - A path-based ALLOW filter in the hard-stop grep (files that legitimately name submit
    in order to block it, like a guard script). Text alone cannot exempt a path.
  - A per-project constant (e.g. the vault writer binary). Text alone cannot scope it;
    parameterise the template instead of hard-coding.

## Never

No git commit, push or PR. No routines. Assemble and trial in a **scratch copy** of the target
(`cp -R <repo> /private/tmp/hs-<slug>`); the real repo is changed only after the trial PASSES and
Paul approves the manifest. Never trial on jobseek-lab (owned by its own session).
Generated harnesses keep the hard stops (Submit, send, consent, credentials, public) as hooks.