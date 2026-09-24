---
name: innovate
description: Run a no-code innovation project (research, choose, configure a tool) with four-eyes and safe changes, per contract §10
---

Act as the delivery manager under the `contract` skill (invoke it now). This is no-code work, so
§10 applies on top of the loop: risk tiers, snapshot, dry-run, apply exactly, read back. The
consuming repo's CLAUDE.md/AGENTS.md override the contract on any conflict.

IDEA: $ARGUMENTS

Search memory and the vault for prior work first; if the answer already exists, say so and stop.
Otherwise run the loop one unit at a time (WIP=1).

Hand back: the decision record, what was configured, DONE WHEN output re-run
by the checker, snapshot and rollback paths, the checker's verdicts, and what
you left undone and why.
