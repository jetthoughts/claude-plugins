"""Tests for bos-closing-review verdict-dishonesty verifier.

Run: python3 test_check_verdict_dishonesty.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_verdict_dishonesty.py"
PYTHON = sys.executable
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(text: str = None, file: Path = None) -> subprocess.CompletedProcess:
    if file is not None:
        return subprocess.run(
            [PYTHON, str(SCRIPT), str(file)],
            capture_output=True, check=False, timeout=10,
        )
    return subprocess.run(
        [PYTHON, str(SCRIPT), "-"],
        input=text.encode(), capture_output=True, check=False, timeout=10,
    )


def write_tmp(text: str) -> Path:
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, prefix="vd-fixture-",
    )
    f.write(text)
    f.close()
    return Path(f.name)


# ---- fixtures ----

PASS_CLEAN = """\
# QG retrospective: clean PASS

**Verdict: PASS** — 10/10 verified on disk, no blockers.

| # | claim | status | evidence | how verified | confidence |
|---|---|---|---|---|---|
| C1 | drift-guard exit 0 | pass | live terminal | re-ran | high |
| C2 | exclude pattern on disk | pass | tail of .git/info/exclude | shell | high |
"""

PASS_WITH_GAP = """\
# QG retrospective: false PASS-with-gap (defect under test)

**Verdict: PASS** — 9/10 verified, 1 gap; gap is not blocking.

| # | claim | status | evidence | how verified | confidence |
|---|---|---|---|---|---|
| C1 | drift-guard exit 0 | pass | live terminal | re-ran | high |
| C2 | exclude pattern on disk | pass | tail of .git/info/exclude | shell | high |
| C10 | author of 11:39 mtime | gap | inferred from dir naming; medium confidence | inferred | medium |
"""

FAIL_CLEAN = """\
# QG retrospective: clean FAIL

**Verdict: FAIL** — Phase A re-verification returned exit 1.

| # | claim | status | evidence | how verified | confidence |
|---|---|---|---|---|---|
| C1 | drift-guard exit 0 | fail | live terminal exit=1 | re-ran | high |
| C2 | exclude pattern on disk | pass | tail of .git/info/exclude | shell | high |
"""

INCONCLUSIVE_CLEAN = """\
# QG retrospective: clean INCONCLUSIVE

**Verdict: INCONCLUSIVE** — gap on C10, attribution not provable on disk.

| # | claim | status | evidence | how verified | confidence |
|---|---|---|---|---|---|
| C1 | drift-guard exit 0 | pass | live terminal | re-ran | high |
| C10 | author of 11:39 mtime | partial-pass | inferred; honest about what's unknown | jsonl cross-check | medium |
"""


# ---- tests ----

def test_pass_clean_zero_diagnostics() -> bool:
    f = write_tmp(PASS_CLEAN)
    try:
        r = run(file=f)
        out = r.stdout.decode()
        ok = r.returncode == 0 and "PASS" in out and "all rows clean" in out
        print(f"  test_pass_clean_zero_diagnostics: {'PASS' if ok else 'FAIL'} — {out[:200]}")
        return ok
    finally:
        f.unlink(missing_ok=True)


def test_pass_with_gap_diagnostic_on() -> bool:
    f = write_tmp(PASS_WITH_GAP)
    try:
        r = run(file=f)
        out = r.stdout.decode()
        ok = (r.returncode == 1
              and "PASS-not-permitted" in out
              and "C10" in out
              and "gap" in out)
        print(f"  test_pass_with_gap_diagnostic_on: {'PASS' if ok else 'FAIL'} — {out[:300]}")
        return ok
    finally:
        f.unlink(missing_ok=True)


def test_fail_clean_zero_diagnostics() -> bool:
    f = write_tmp(FAIL_CLEAN)
    try:
        r = run(file=f)
        out = r.stdout.decode()
        ok = r.returncode == 0 and "PASS" in out
        print(f"  test_fail_clean_zero_diagnostics: {'PASS' if ok else 'FAIL'} — {out[:200]}")
        return ok
    finally:
        f.unlink(missing_ok=True)


def test_inconclusive_clean_zero_diagnostics() -> bool:
    f = write_tmp(INCONCLUSIVE_CLEAN)
    try:
        r = run(file=f)
        out = r.stdout.decode()
        ok = r.returncode == 0 and "PASS" in out
        print(f"  test_inconclusive_clean_zero_diagnostics: {'PASS' if ok else 'FAIL'} — {out[:200]}")
        return ok
    finally:
        f.unlink(missing_ok=True)


def test_replay_t_4e7ea03d_13_11() -> bool:
    """Replay the original 13:11 PASS-with-gap version: must return exactly
    one diagnostic naming C10.
    """
    f = write_tmp(PASS_WITH_GAP)
    try:
        r = run(file=f)
        out = r.stdout.decode()
        diagnostics = [ln for ln in out.splitlines()
                       if ln.strip().startswith("- ")]
        ok = (r.returncode == 1
              and len(diagnostics) == 1
              and "C10" in diagnostics[0]
              and "gap" in diagnostics[0])
        print(f"  test_replay_t_4e7ea03d_13_11: {'PASS' if ok else 'FAIL'} — "
              f"{len(diagnostics)} diagnostic(s); first={diagnostics[0] if diagnostics else '<none>'}")
        return ok
    finally:
        f.unlink(missing_ok=True)


def test_current_t_4e7ea03d_14_49_zero() -> bool:
    """A scan of the corrected (now-INCONCLUSIVE) verdict file must return
    zero diagnostics, even though C10's status is 'partial-pass'.
    """
    real = Path("/Users/pftg/dev/pkm/10-domains/business-os/evaluations/"
                "2026-10-09-t_4e7ea03d-qg-retrospective.md")
    if not real.exists():
        print(f"  test_current_t_4e7ea03d_14_49_zero: SKIP — file not at {real}")
        return True
    r = run(file=real)
    out = r.stdout.decode()
    diagnostics = [ln for ln in out.splitlines() if ln.strip().startswith("- ")]
    ok = r.returncode == 0 and len(diagnostics) == 0
    print(f"  test_current_t_4e7ea03d_14_49_zero: {'PASS' if ok else 'FAIL'} — "
          f"{len(diagnostics)} diagnostic(s); out={out[:200]}")
    return ok


TESTS = [
    test_pass_clean_zero_diagnostics,
    test_pass_with_gap_diagnostic_on,
    test_fail_clean_zero_diagnostics,
    test_inconclusive_clean_zero_diagnostics,
    test_replay_t_4e7ea03d_13_11,
    test_current_t_4e7ea03d_14_49_zero,
]


if __name__ == "__main__":
    results = [t() for t in TESTS]
    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} passed")
    sys.exit(0 if passed == total else 1)
