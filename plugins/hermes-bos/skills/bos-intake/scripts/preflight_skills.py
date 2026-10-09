#!/usr/bin/env python3
"""Preflight: validate every `skills=` entry against the live catalog, returning
the unresolved identifiers in the exact wording ``agent.skill_commands.
format_missing_skills`` uses at worker preload time.

Why: a malformed ``kanban create --skills <id>`` payload currently passes
filing, then crashes the dispatched worker 60-90s later with a single
``Unknown skill(s): ...`` line. This hook lets the intake reject the card
sub-second at filing time with the same wording, so the operator can fix the
identifier before it costs a worker cycle. R11-compliant: no hermes-agent edit.

Usage:

    from preflight_skills import missing, format_rejection

    bad = missing(["hermes-bos/skills/bos-intake"])  # under soul-curator
    if bad:
        raise ValueError(format_rejection(bad))

Profiles: pass ``env={"HERMES_HOME": "<profile-home>"}`` to validate against
a specific profile's external_dirs; otherwise the live process env wins.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable, List, Optional


# Runtime spelling workers print — mirror verbatim (skill_commands.py:278).
UNKNOWN_PREFIX = "Unknown skill(s): "


def _import_skill_loader():
    """Import the same loader the gateway uses for autoskills. Falls back to a
    dummy loader when hermes-agent isn't on PYTHONPATH (the helper is callable
    from any context that sets PYTHONPATH=/Users/pftg/.hermes/hermes-agent)."""
    try:
        from agent.skill_commands import _load_skill_payload, format_missing_skills  # type: ignore
        return _load_skill_payload, format_missing_skills
    except Exception as exc:  # pragma: no cover — environment guard
        _load_skill_payload = None  # type: ignore
        format_missing_skills = None  # type: ignore

        def _stub_missing(_ids: List[str]) -> str:
            return UNKNOWN_PREFIX + ", ".join(_ids)

        return None, _stub_missing


def missing(skills: Optional[Iterable[str]], env: Optional[dict] = None) -> List[str]:
    """Return the subset of *skills* that did NOT resolve against the profile's
    catalog. Empty input → empty output. Profile resolution: set
    ``HERMES_HOME=<profile-home>`` (which skill_utils' ``get_config_path``
    follows) before importing agent.*."""
    if not skills:
        return []
    if env is not None:
        for k, v in env.items():
            os.environ[k] = v
    loader, _ = _import_skill_loader()
    if loader is None:
        # hermes-agent not importable — return everything as missing; the
        # caller (a hook inside an intake procedure) decides policy.
        return [str(s).strip() for s in skills if str(s).strip()]
    out: List[str] = []
    for raw in skills:
        identifier = (str(raw) if raw is not None else "").strip()
        if not identifier:
            continue
        loaded = loader(identifier)
        if loaded is None:
            out.append(identifier)
    return out


def format_rejection(missing_ids: Iterable[str]) -> str:
    """Mirror the runtime wording so the rejection the operator sees at filing
    matches the wording the worker would have printed. One line, CLI-friendly.
    """
    if isinstance(missing_ids, (list, tuple, set)):
        ids = [str(x).strip() for x in missing_ids if str(x).strip()]
    else:
        ids = [s.strip() for s in str(missing_ids).split(",") if s.strip()]
    if not ids:
        return ""
    _, fmt = _import_skill_loader()
    if fmt is not None:
        try:
            line = fmt(ids)
            if line:
                return line
        except Exception:  # pragma: no cover — defensive
            pass
    return UNKNOWN_PREFIX + ", ".join(ids)


if __name__ == "__main__":  # pragma: no cover — manual smoke probe
    argv = sys.argv[1:] or ["hermes-bos/skills/bos-intake"]
    bad = missing(argv)
    if not bad:
        print("OK: all skills resolve")
        sys.exit(0)
    print(format_rejection(bad))
    sys.exit(2)
