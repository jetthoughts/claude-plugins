---
name: bos-comm-check
description: 'Pre-send self-check for chat replies against the SOUL comm protocol. Use before sending any reply to Paul from the kanban-orchestrator seat.'
version: 0.1.0
author: pftg
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Business OS, kanban, comms, quality-gate]
    related_skills: [bos-quality-gate, bos-incident-response]
---

# bos-comm-check Skill

Pre-send guardrail for chat replies to Paul from any seat where the SOUL § "Card and reply shape" protocol is in force (kanban-orchestrator, and any seat that adopts the same protocol by reference).

The protocol says: ≤10 lines, lead with the next action, no recap, no preamble, no "let me know" / "happy to help" / "by the way", no restated TLDR. The hard part is execution: the protocol is on disk, but drift is the defect (see kanban task t_cbc58f3b, 2026-10-06).

This skill gives a deterministic pre-send check so future sessions do not rely on memory alone.

## When to invoke

- Before sending any chat reply to Paul from a seat that follows the protocol (currently kanban-orchestrator).
- Optionally: before posting any kanban card comment that will be read by Paul.

## How to invoke

Run the verifier with the proposed reply text on stdin:

```bash
python3 ~/.hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check/check_reply.py <<'EOF'
<proposed reply>
EOF
```

Exit code 0 = reply passes. Exit code 1 = reply fails; stdout lists each violation with line numbers.

A reference copy lives at `references/knock.py` for agents whose `cache/scratch` path differs.

## Checks performed

1. **Line count.** Total non-empty lines must be ≤ 10. (Chat reply cap.)
2. **First line.** Must not start with "Great ", "Let me", "I'll", "Sure!", "Looking at", "To answer", "Please note", or any phrase from the blocklist.
3. **Blocklist scan.** Body must not contain any of: `please note that`, `in summary`, `let me know`, `happy to`, `hope this helps`, `by the way`, `feel free to`, `happy to clarify`.
4. **TLDR restate.** If the reply contains a `TLDR:` heading, it must not be a near-verbatim duplicate of the previous reply's TLDR. The verifier reads `~/.hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check/last_tldr.txt` and flags if the Levenshtein ratio is ≥ 0.85.
5. **Lead with action.** First non-empty line should be a verb-led instruction (matches `^(run|edit|open|read|paste|file|check|verify|approve|reject|extend|pick|comment|reply|stop|done|next|use|load)\b`), a path (starts with `~` or `/`), or a code-fenced command block. Otherwise a warning (non-blocking).

## Setting up (one-time, on first install)

```bash
mkdir -p ~/.hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check
cp ~/dev/claude-plugins/plugins/hermes-bos/skills/bos-comm-check/scripts/check_reply.py \
   ~/.hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check/check_reply.py
```

Enable on the profile: remove `bos-comm-check` from `skills.disabled` in
`~/.hermes/profiles/kanban-orchestrator/config.yaml`. (Use direct file edit with sha
verification — `hermes config set` cannot handle YAML list items.)

## Hard constraint

Do NOT add a hermes-agent self-check via the central gateway (would touch prompt caching). The skill is profile-scoped and runs only when invoked.

## Source of truth

- SOUL protocol: `kanban-orchestrator/SOUL.md` § "Card and reply shape (operator override 2026-10-06)".
- Incident: kanban task t_cbc58f3b, 2026-10-06.
- Authority: Paul direct chat 22:55–22:57 CEST 2026-10-06.