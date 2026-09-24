# Harness Setup

One instruction-only skill that **assembles and validates the AI harness for one project**:
Claude Code, pi or Hermes. It works by research, then picking ready pieces, then copying in only
what the goal needs, then a trial run that passes or fails. It contains no scripts and no
generator. The generator from 0.3.0 (`assemble_harness.py`) was retired on 2026-09-24 and is kept
in (backup deleted 2026-09-24 per Paul: git only).

Run by the overseer Claude Code session (Paul, 2026-09-24: "this is your responsibility"). Invoke
it as `/harness-setup:setup <project goal> [repo path] [harness]`.

## How it works

1. **Ask:** name the harness, the project goal, what done means and the hard stops; write one
   `need:` line per capability.
2. **Research:** what is installed, the monthly capability catalog, the official docs, the
   watched sources, then GitHub. Research agents get a blind brief and must return ≥ 3 NEW
   findings.
3. **Pick:** installed first, then the **library registry**: ECC, agency-agents, superpowers,
   wshobson/agents, claude-code-templates, anthropics/skills and plugins, pi packages, the Hermes
   Skills Hub and more. It is kept in pkm `business-os/knowledge/sources/2026-09-21-agent-discovery-sources.md`
   and grows monthly. At least 2 libraries are compared per need, and none is the default or
   installed wholesale.
4. **Assemble** in a scratch copy. Picked pieces are **copied** into the project's `.claude/`,
   because cloud sessions and routines load only committed repo files and repo plugins do not
   load there. Hard stops ship as hooks in the committed `settings.json`.
5. **Entry points:** one per goal, each with the check that proves it works.
6. **Trial run:** `claude plugin eval init` writes the suite, and
   `claude plugin eval … --ablation with-without` runs it. PASS = every task passes 3 of 3 runs
   and the harness beats the no-harness baseline. pi and Hermes use their own scripted runs.

The real repo is changed only after the trial passes and Paul approves the manifest.

## Evidence

- `business-os/knowledge/research/2026-09-24-harness-buy-list.md`
- `business-os/knowledge/research/2026-09-24-ruflo-alternatives.md` (ruflo vs ECC vs our own set)
- `business-os/knowledge/research/2026-09-24-claude-code-per-project-harness.md`: what loads where.
