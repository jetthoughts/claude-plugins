"""Tests for bos-comm-check verifier. Run with: python3 test_check_reply.py"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("/Users/pftg/dev/claude-plugins/plugins/hermes-bos/skills/bos-comm-check/scripts/check_reply.py")
PYTHON = sys.executable


def run(reply: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(SCRIPT)],
        input=reply.encode(),
        capture_output=True,
        check=False,
        timeout=10,
    )


def test_short_pass() -> bool:
    r = run("Run `echo hi`.")
    ok = r.returncode == 0 and "PASS" in r.stdout.decode()
    print(f"  test_short_pass: {'PASS' if ok else 'FAIL'} — {(r.stdout + r.stderr).decode()[:200]}")
    return ok


def test_too_long_fails() -> bool:
    body = "x\n" * 12
    r = run(body)
    out = r.stdout.decode()
    ok = r.returncode == 1 and "line count" in out.lower()
    print(f"  test_too_long_fails: {'PASS' if ok else 'FAIL'} — {out[:200]}")
    return ok


def test_first_line_blocklist_fails() -> bool:
    r = run("Sure! I'll handle that.")
    out = r.stdout.decode()
    ok = r.returncode == 1 and "first line" in out.lower()
    print(f"  test_first_line_blocklist_fails: {'PASS' if ok else 'FAIL'} — {out[:200]}")
    return ok


def test_body_blocklist_fails() -> bool:
    r = run("Run `x`.\n\nPlease note that y.")
    out = r.stdout.decode()
    ok = r.returncode == 1 and "please note" in out.lower()
    print(f"  test_body_blocklist_fails: {'PASS' if ok else 'FAIL'} — {out[:200]}")
    return ok


def test_lead_action_warning() -> bool:
    r = run("The current state is unclear.")
    out = r.stdout.decode()
    ok = r.returncode == 0 and "warning" in out.lower()
    print(f"  test_lead_action_warning: {'PASS' if ok else 'FAIL'} — {out[:200]}")
    return ok


def test_tldr_restate_fails() -> bool:
    last = Path.home() / ".hermes/profiles/kanban-orchestrator/cache/scratch/bos-comm-check/last_tldr.txt"
    last.parent.mkdir(parents=True, exist_ok=True)
    last.write_text("incident resolved by filing comms check skill")
    try:
        reply = "Run `x`.\n\nTLDR: incident resolved by filing comms check skill today."
        r = run(reply)
        out = r.stdout.decode()
        ok = r.returncode == 1 and "tldr" in out.lower()
        print(f"  test_tldr_restate_fails: {'PASS' if ok else 'FAIL'} — {out[:200]}")
        return ok
    finally:
        last.unlink(missing_ok=True)


TESTS = [
    test_short_pass,
    test_too_long_fails,
    test_first_line_blocklist_fails,
    test_body_blocklist_fails,
    test_lead_action_warning,
    test_tldr_restate_fails,
]


if __name__ == "__main__":
    results = [t() for t in TESTS]
    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} passed")
    sys.exit(0 if passed == total else 1)