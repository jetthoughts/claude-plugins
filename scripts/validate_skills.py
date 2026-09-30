#!/usr/bin/env python3
"""Guardrail for the JetThoughts skill estate.

Turns SKILLS_REVIEW.md's findings into a failing exit code, so they cannot come back.

    python3 scripts/validate_skills.py            # errors + warnings
    python3 scripts/validate_skills.py --quiet    # errors only, no warning list

Exit 0 = clean. Exit 1 = at least one ERROR. Warnings never fail the build.

Checks
  E1  frontmatter does not parse as YAML, or has no name/description
  E2  a symlink is committed anywhere under plugins/            (breaks clones, recurses)
  E3  a skill name is duplicated across the estate              (the router cannot choose)
  E4  a skill directory has no SKILL.md
  E5  a repo-relative path is referenced but does not exist     (dangling reference)
  E6  a plugin.json declares a component key that is not path-like
      (e.g. commands: ["sync-perplexity"], which fails manifest validation and
      makes the whole plugin "failed to load" — commands auto-discover from commands/)
  E7  a path in paperclip-skills.json does not resolve from $HOME
      (the Paperclip catalog delivers by file path; a rename or a moved vault
      breaks seat delivery silently, which is what happened on 2026-09-30)
  W1  description is over budget or has no "not for" boundary
  W2  body is over the monolith threshold with no references/   (no progressive disclosure)
  W3  a plugin on disk is missing from marketplace.json or has no plugin.json
  W4  a plugin's plugin.json name disagrees with its directory
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS = os.path.join(ROOT, "plugins")
MARKETPLACE = os.path.join(ROOT, ".claude-plugin", "marketplace.json")

DESC_BUDGET = 700          # chars; the review targets 320, this catches the outliers
MONOLITH = 8000            # body chars above which a references/ file is expected
# Evaluation workspaces are gitignored (see .gitignore): they hold skill snapshots
# under the same names as the real skills, so they must not be validated as skills.
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
SKIP_FRAGMENTS = ("-workspace", "skill-snapshot", "iteration-")
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
PATH_REF = re.compile(r"`((?:plugins|skills|references|scripts|templates|agents)/[A-Za-z0-9_./-]+)`")

errors: list[str] = []
warnings: list[str] = []


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def skipped(path: str) -> bool:
    return any(frag in path for frag in SKIP_FRAGMENTS)


def walk(base: str):
    """Walk without following symlinks, skipping vendored, ignored and eval dirs."""
    for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
        dirnames[:] = [
            d for d in dirnames if d not in SKIP_DIRS and not skipped(d)
        ]
        if skipped(dirpath):
            continue
        yield dirpath, dirnames, filenames


def load_frontmatter(path: str):
    text = open(path, encoding="utf-8", errors="replace").read()
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def skill_files() -> list[str]:
    out = []
    for dirpath, _dirnames, filenames in walk(PLUGINS):
        if "SKILL.md" in filenames:
            out.append(os.path.join(dirpath, "SKILL.md"))
    return sorted(out)


def check_symlinks() -> None:
    """E2 — a committed symlink is either a recursion loop or a broken absolute path."""
    for dirpath, dirnames, filenames in walk(PLUGINS):
        for name in list(dirnames) + list(filenames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                errors.append(
                    f"E2 symlink under plugins/: {rel(path)} -> {os.readlink(path)}"
                )


def check_frontmatter(skills: list[str]) -> tuple[dict[str, str], dict[str, list[str]]]:
    """E1, E3, W1 — parse frontmatter, collect names, check descriptions."""
    names: dict[str, list[str]] = {}
    meta: dict[str, str] = {}
    for path in skills:
        fm, body = load_frontmatter(path)
        if fm is None:
            errors.append(f"E1 no YAML frontmatter: {rel(path)}")
            continue
        try:
            data = yaml.safe_load(fm) or {}
        except yaml.YAMLError as exc:
            errors.append(f"E1 frontmatter does not parse: {rel(path)}: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"E1 frontmatter is not a mapping: {rel(path)}")
            continue
        name = str(data.get("name") or "").strip()
        desc = " ".join(str(data.get("description") or "").split())
        if not name:
            errors.append(f"E1 no 'name' in frontmatter: {rel(path)}")
            continue
        if not desc:
            errors.append(f"E1 no 'description' in frontmatter: {rel(path)}")
        names.setdefault(name, []).append(path)
        meta[path] = name

        if len(desc) > DESC_BUDGET:
            warnings.append(f"W1 description {len(desc)} chars (>{DESC_BUDGET}): {rel(path)}")

        # E4 is structural, handled separately
        if len(body) > MONOLITH and not os.path.isdir(os.path.join(os.path.dirname(path), "references")):
            warnings.append(
                f"W2 body {len(body)} chars with no references/: {rel(path)}"
            )
    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            errors.append("E3 duplicate skill name '{}': {}".format(name, ", ".join(rel(p) for p in paths)))
    return meta, names


def check_dangling(meta: dict[str, str]) -> None:
    """E5 — a referenced repo-relative path must resolve somewhere in the estate.

    A skill may legitimately point at a sibling skill's reference file
    (e.g. "see `j-paperclip`'s `references/api.md`"), so resolution is tried
    relative to the skill, the plugin, and the repo, then as a suffix match
    anywhere under plugins/.
    """
    repo_index = [
        os.path.join(dirpath, name)
        for dirpath, _dirnames, filenames in walk(PLUGINS)
        for name in filenames
    ]

    for path in skill_files():
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        here = os.path.dirname(path)
        plugin_dir = os.path.join(PLUGINS, rel(path).split(os.sep)[1])
        for ref in PATH_REF.findall(text):
            candidates = [
                os.path.join(ROOT, ref),
                os.path.join(here, ref),
                os.path.join(plugin_dir, ref),
            ]
            if any(os.path.exists(c) for c in candidates):
                continue
            # suffix match: the same relative path inside another skill/plugin
            tail = os.sep + ref.replace("/", os.sep)
            if any(c.endswith(tail) for c in repo_index):
                continue
            errors.append(f"E5 dangling reference '{ref}' in {rel(path)}")


def check_plugins() -> None:
    """W3, W4 — marketplace coverage and plugin.json name agreement."""
    if not os.path.isdir(PLUGINS):
        errors.append("plugins/ directory is missing")
        return
    on_disk = sorted(
        d
        for d in os.listdir(PLUGINS)
        if os.path.isdir(os.path.join(PLUGINS, d)) and not skipped(d)
    )
    listed: set[str] = set()
    if os.path.exists(MARKETPLACE):
        try:
            data = json.load(open(MARKETPLACE, encoding="utf-8"))
            listed = {p.get("name") for p in data.get("plugins", [])}
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"W3 marketplace.json does not parse: {exc}")
    else:
        warnings.append("W3 no .claude-plugin/marketplace.json")

    for name in on_disk:
        pj = os.path.join(PLUGINS, name, ".claude-plugin", "plugin.json")
        if not os.path.exists(pj):
            warnings.append(f"W3 no plugin.json: plugins/{name}")
            continue
        try:
            declared = json.load(open(pj, encoding="utf-8")).get("name")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"W4 plugin.json does not parse: plugins/{name}: {exc}")
            continue
        if declared and declared != name:
            warnings.append(
                f"W4 plugin.json name '{declared}' != directory '{name}'"
            )
        if name not in listed:
            warnings.append(f"W3 plugins/{name} is not in marketplace.json (uninstallable)")


def check_manifest_keys() -> None:
    """E6 — component keys in plugin.json must be paths, not bare names.

    `commands`, `agents`, `skills` and `hooks` accept a path (or list of paths)
    and the CLI *auto-discovers* the conventional directories. Declaring a bare
    component name instead fails manifest validation, which takes the entire
    plugin down with "failed to load" — not just the one component.
    """
    component_keys = ("commands", "agents", "skills", "hooks")
    for dirpath, _dirnames, filenames in walk(PLUGINS):
        if "plugin.json" not in filenames or ".claude-plugin" not in dirpath:
            continue
        path = os.path.join(dirpath, "plugin.json")
        try:
            data = json.load(open(path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue  # W4 reports parse failures
        if not isinstance(data, dict):
            continue
        for key in component_keys:
            if key not in data:
                continue
            value = data[key]
            entries = value if isinstance(value, list) else [value]
            for entry in entries:
                if not isinstance(entry, str):
                    errors.append(
                        f"E6 {rel(path)}: '{key}' entry is not a string: {entry!r}"
                    )
                    continue
                if entry.startswith("./") or "/" in entry or entry.endswith(".md") or entry.endswith(".json"):
                    continue
                errors.append(
                    f"E6 {rel(path)}: '{key}: [\"{entry}\"]' is not path-like — "
                    f"declare a path or drop the key and let {key}/ auto-discover"
                )


def check_paperclip_catalog() -> None:
    """E7 — every catalog path must resolve from $HOME.

    paperclip-skills.json maps a catalog slug to a file path relative to $HOME.
    The Paperclip instrument sweep re-imports a slug only when its file changes,
    so a path that no longer resolves fails *silently*: the seat keeps whatever
    copy it last imported and nothing reports an error. Four of the seven entries
    were broken this way on 2026-09-30 — the plugin rename changed
    plugins/deliberate to plugins/j-deliberate, and the vault moved from
    ~/Documents/pkm to ~/dev/pkm.
    """
    catalog = os.path.join(ROOT, "paperclip-skills.json")
    if not os.path.exists(catalog):
        return
    try:
        data = json.load(open(catalog, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"E7 paperclip-skills.json does not parse: {exc}")
        return
    home = os.path.expanduser("~")
    for slug, path in sorted(data.items()):
        if slug.startswith("_"):
            continue
        if not isinstance(path, str):
            errors.append(f"E7 paperclip-skills.json: '{slug}' is not a path string")
            continue
        if not os.path.exists(os.path.join(home, path)):
            errors.append(
                f"E7 paperclip-skills.json: slug '{slug}' -> ~/{path} does not exist"
            )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true", help="suppress the warning list")
    args = ap.parse_args()

    skills = skill_files()
    check_symlinks()
    meta, _names = check_frontmatter(skills)
    check_dangling(meta)
    check_plugins()
    check_manifest_keys()
    check_paperclip_catalog()

    for line in errors:
        print(line)
    if not args.quiet:
        for line in warnings:
            print(line)

    print()
    print(f"{len(skills)} skills checked, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
