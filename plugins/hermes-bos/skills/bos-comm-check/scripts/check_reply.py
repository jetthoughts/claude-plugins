#!/usr/bin/env python3
"""
bos-comm-check pre-send verifier.

Reads a proposed reply from stdin, runs the comm protocol against it, and exits
0 (pass) or 1 (fail) with a per-violation report on stdout.

Checks:
1. Line count <= 10 (non-empty lines).
2. First line blocklist (no "Great ", "Let me", etc.).
3. Body blocklist (no "please note that", "in summary", "let me know", ...).
4. TLDR restate detector vs ~/.hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check/last_tldr.txt.
5. Lead-with-action: first non-empty line should be verb-led, a path, or a code-fenced command.
"""
import re
import os
import sys
from pathlib import Path

LAST_TLDR_PATH = Path.home() / ".hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check/last_tldr.txt"

FIRST_LINE_PHRASES = [
    "Great ", "Let me ", "I'll ", "Sure!", "Looking at ",
    "To answer ", "Please note ", "Sure,", "Of course,",
]

BODY_PHRASES = [
    "please note that", "in summary", "let me know", "happy to",
    "hope this helps", "by the way", "feel free to",
]

LEAD_VERBS = (
    "run|edit|open|read|paste|file|check|verify|approve|reject|extend|pick|"
    "comment|reply|stop|done|next|use|load|restart|rebuild|recheck|revert|"
    "apply|set|add|remove|merge|rebase|stage|push|pull|fetch|build|test|"
    "deploy|install|uninstall|update|upgrade|downgrade|reset|clear|flush|"
    "save|delete|move|copy|rename|create|destroy|kill|spawn|spawned|claim|"
    "complete|block|unblock"
)


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            ins = cur[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + (ca != cb)
            cur[j] = min(ins, dele, sub)
        prev = cur
    return prev[-1]


def similarity_ratio(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    return 1.0 - levenshtein(a, b) / max(len(a), len(b))


def main() -> int:
    reply = sys.stdin.read()
    lines = reply.splitlines()
    nonempty = [ln for ln in lines if ln.strip()]
    violations = []
    warnings = []

    # 1. Line count
    if len(nonempty) > 10:
        violations.append(f"line count: {len(nonempty)} > 10")

    # 2. First line blocklist
    first = nonempty[0] if nonempty else ""
    for phrase in FIRST_LINE_PHRASES:
        if first.lower().startswith(phrase.lower()):
            violations.append(f"first line starts with banned phrase: {phrase!r}")
            break

    # 3. Body blocklist
    body_lc = reply.lower()
    for phrase in BODY_PHRASES:
        if phrase in body_lc:
            violations.append(f"body contains banned phrase: {phrase!r}")

    # 4. TLDR restate
    tldr_match = re.search(r"(?im)^\s*TLDR\s*:\s*(.+)$", reply)
    if tldr_match and LAST_TLDR_PATH.exists():
        current_tldr = tldr_match.group(1).strip()
        last_tldr = LAST_TLDR_PATH.read_text().strip()
        if last_tldr:
            ratio = similarity_ratio(current_tldr.lower(), last_tldr.lower())
            if ratio >= 0.85:
                violations.append(
                    f"TLDR restate: similarity {ratio:.2f} >= 0.85 vs prior reply"
                )
    # write current TLDR for next invocation
    if tldr_match:
        try:
            LAST_TLDR_PATH.parent.mkdir(parents=True, exist_ok=True)
            LAST_TLDR_PATH.write_text(tldr_match.group(1).strip())
        except OSError as e:
            warnings.append(f"could not persist TLDR for next check: {e}")

    # 5. Lead with action (warning only)
    if not first.strip().startswith(("```", "~", "./", "/")):
        if not re.match(rf"^(?:{LEAD_VERBS})\b", first, re.IGNORECASE):
            warnings.append(
                f"first line does not lead with action verb or path: {first[:60]!r}"
            )

    # Report
    if violations:
        print("FAIL: chat reply violates the SOUL comm protocol", file=sys.stdout)
        for v in violations:
            print(f"  - {v}", file=sys.stdout)
        for w in warnings:
            print(f"  ~ warning: {w}", file=sys.stdout)
        return 1

    print("PASS: chat reply conforms to the SOUL comm protocol", file=sys.stdout)
    for w in warnings:
        print(f"  ~ warning: {w}", file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())