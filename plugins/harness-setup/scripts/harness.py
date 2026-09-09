#!/usr/bin/env python3
"""Conservative, offline harness discovery and reviewed file transactions.

Python 3.10+, macOS/Linux, standard library only. No project commands are run.
An approval digest is an integrity/concurrency token, NOT human authentication.
Run apply/rollback yourself outside the agent in a trusted OS boundary.
Cooperating writers are serialized. Hostile writers and crash recovery are out
of scope: replacement is atomic per file, not across the whole transaction.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import contextlib
import datetime as dt
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile


SCHEMA = 1
MAX_FILE = 1024 * 1024
MAX_PLAN = 4 * MAX_FILE
MAX_BUNDLE = 16 * MAX_FILE
MAX_CHANGES = 32
MAX_ENTRIES = 512
MAX_NODES = 2000
MAX_RECORDS = 512
BEGIN = "<!-- harness-setup:begin -->"
END = "<!-- harness-setup:end -->"
IDENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}(?:@[A-Za-z0-9][A-Za-z0-9._-]{0,63})?\Z")
SLUG = r"[a-z0-9][a-z0-9-]{0,63}"
CREATE_PATH = re.compile(
    rf"(?:\.claude/agents/{SLUG}\.md|\.claude/skills/{SLUG}/"
    rf"(?:SKILL\.md|references/{SLUG}\.md))\Z"
)
STACK_FILES = {
    "package.json", "pyproject.toml", "requirements.txt", "Pipfile",
    "Cargo.toml", "go.mod", "Gemfile", "pom.xml", "build.gradle",
    "build.gradle.kts", "composer.json", "mix.exs", "pubspec.yaml",
    "deno.json", "deno.jsonc", "Package.swift", "CMakeLists.txt",
}
EXCLUDED = {
    ".git", "node_modules", "vendor", ".venv", "venv", "env",
    "__pycache__", "dist", "build", "target", ".next", ".cache",
    "coverage", ".tox", ".mypy_cache", ".pytest_cache", ".turbo",
}
SETTINGS_KEYS = {
    "permissions", "enabledPlugins", "hooks", "env", "model",
    "apiKeyHelper", "forceLoginMethod", "forceLoginOrgUUID",
    "enableAllProjectMcpServers", "enabledMcpjsonServers",
    "disabledMcpjsonServers", "mcpServers", "sandbox",
    "allowManagedPermissionRulesOnly", "allowManagedHooksOnly",
    "allowManagedMcpServersOnly", "disableAllHooks",
    "statusLine", "outputStyle", "language", "autoUpdatesChannel",
    "extraKnownMarketplaces", "alwaysThinkingEnabled",
}
ROUTE_ENV = (
    "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)


class HarnessError(Exception):
    """A deliberately content-free, safe-to-display validation failure."""


def require(condition, message):
    if not condition:
        raise HarnessError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def constant(_):
        raise HarnessError("non-finite JSON number")

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=constant)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise HarnessError("malformed UTF-8 JSON") from exc


def exact_keys(value, keys, label):
    require(type(value) is dict and set(value) == set(keys),
            f"invalid {label} schema")


def safe_path(value):
    """Reject symlinks before resolve(), including every existing ancestor."""
    path = Path(value).expanduser()
    require(".." not in path.parts, "parent traversal is forbidden")
    path = Path(os.path.abspath(path))
    for part in reversed((path, *path.parents)):
        try:
            mode = part.lstat().st_mode
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(mode), "symlink path is forbidden")
        if part != path:
            require(stat.S_ISDIR(mode), "non-directory path ancestor")
    return path


def project_path(value):
    path = safe_path(value)
    require(path.is_dir(), "project must be an existing directory")
    require(path == path.resolve(), "project must resolve to the same path")
    return path


def bounded_read(path, limit=MAX_FILE, require_single_link=False):
    path = safe_path(path)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "expected a regular file")
    require(not require_single_link or before.st_nlink == 1,
            "hardlinked mutable target is forbidden")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | os.O_NONBLOCK
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as handle:
        st = os.fstat(handle.fileno())
        require(stat.S_ISREG(st.st_mode), "expected a regular file")
        require(not require_single_link or st.st_nlink == 1,
                "hardlinked mutable target is forbidden")
        require(st.st_size <= limit, "file exceeds size limit")
        data = handle.read(limit + 1)
        require(len(data) <= limit, "file exceeds size limit")
        require(not require_single_link or
                (os.fstat(handle.fileno()).st_nlink == 1 and path.lstat().st_nlink == 1),
                "hardlinked mutable target is forbidden")
        return data, stat.S_IMODE(st.st_mode)


def text(data):
    try:
        result = data.decode("utf-8")
    except UnicodeError as exc:
        raise HarnessError("target is not UTF-8") from exc
    require("\x00" not in result, "NUL in target text")
    return result


def snapshot(path):
    path = safe_path(path)
    if not path.exists():
        return {"exists": False, "sha256": None, "content_b64": None, "mode": None}
    data, mode = bounded_read(path, require_single_link=True)
    text(data)
    require(mode <= 0o777, "special file modes are unsupported")
    return {"exists": True, "sha256": sha(data),
            "content_b64": base64.b64encode(data).decode("ascii"), "mode": mode}


def decode_image(image, baseline=False):
    exact_keys(image, ("exists", "sha256", "content_b64", "mode") if baseline
               else ("sha256", "content_b64", "mode"), "file image")
    if baseline:
        require(type(image["exists"]) is bool, "invalid existence flag")
        if not image["exists"]:
            require(all(image[k] is None for k in ("sha256", "content_b64", "mode")),
                    "invalid absent baseline")
            return None
    require(type(image["content_b64"]) is str and
            len(image["content_b64"]) <= (MAX_FILE + 2) // 3 * 4,
            "invalid image size")
    require(type(image["mode"]) is int and 0 <= image["mode"] <= 0o777,
            "invalid image mode")
    try:
        data = base64.b64decode(image["content_b64"], validate=True)
    except (ValueError, binascii.Error) as exc:
        raise HarnessError("invalid base64 image") from exc
    require(len(data) <= MAX_FILE and sha(data) == image["sha256"],
            "image hash mismatch")
    require(base64.b64encode(data).decode("ascii") == image["content_b64"],
            "noncanonical image encoding")
    text(data)
    return data


def valid_target(path, operation):
    require(type(path) is str and path and "\\" not in path and
            not PurePosixPath(path).is_absolute() and
            all(p not in ("", ".", "..") for p in path.split("/")),
            "invalid relative target path")
    allowed = ((operation == "json_merge" and path == ".claude/settings.json") or
               (operation == "managed_block" and path == "CLAUDE.md") or
               (operation == "create" and CREATE_PATH.fullmatch(path)))
    require(bool(allowed), "unsupported operation or target path")


def recursive_merge(original, patch):
    result = dict(original)
    for key, value in patch.items():
        if type(value) is dict and type(result.get(key)) is dict:
            result[key] = recursive_merge(result[key], value)
        else:
            result[key] = value
    return result


def settings_patch(original, patch):
    require(type(original) is dict, "settings must be a JSON object")
    require(type(patch) is dict and patch and
            set(patch) <= {"enabledPlugins", "permissions"},
            "settings patch permits only enabledPlugins and permissions.ask/deny")
    if "enabledPlugins" in patch:
        plugins = patch["enabledPlugins"]
        require(type(plugins) is dict and 0 < len(plugins) <= 128,
                "enabledPlugins must be a nonempty bounded object")
        require(all(IDENT.fullmatch(k) and type(v) is bool
                    for k, v in plugins.items()), "invalid plugin identifier or boolean")
        require(type(original.get("enabledPlugins", {})) is dict,
                "existing enabledPlugins is malformed")
    if "permissions" in patch:
        permissions = patch["permissions"]
        require(type(permissions) is dict and permissions and
                set(permissions) <= {"ask", "deny"},
                "only permissions.ask and permissions.deny may be patched")
        old = original.get("permissions", {})
        require(type(old) is dict, "existing permissions are malformed")
        for key, rules in permissions.items():
            require(type(rules) is list and len(rules) <= 256 and
                    all(type(rule) is str and rule.strip() and len(rule) <= 512 and
                        not any(ord(c) < 32 or ord(c) == 127 for c in rule)
                        for rule in rules), "invalid permission rules")
            before = old.get(key, [])
            require(type(before) is list and all(type(r) is str for r in before),
                    "existing permission rules are malformed")
            require(set(before) <= set(rules),
                    "replacement must retain every existing ask/deny rule")
    return recursive_merge(original, patch)


def managed_block(original, value):
    require(type(value) is str and value.strip() and "\x00" not in value and
            BEGIN not in value and END not in value, "invalid managed block value")
    block = (BEGIN + "\n" + value.rstrip("\r\n") + "\n" + END).encode("utf-8")
    start, end = BEGIN.encode(), END.encode()
    require(original.count(start) == original.count(end) and
            original.count(start) <= 1, "broken or repeated owned markers")
    if start not in original:
        return original + (b"\n" if original and not original.endswith(b"\n") else b"") + block + b"\n"
    left, right = original.index(start), original.index(end)
    require(left < right, "reversed owned markers")
    for pos, marker in ((left, start), (right, end)):
        require(pos == 0 or original[pos - 1:pos] == b"\n",
                "owned marker must occupy its own line")
        require(original[pos + len(marker):].startswith((b"\n", b"\r\n")) or
                pos + len(marker) == len(original),
                "owned marker must occupy its own line")
    return original[:left] + block + original[right + len(end):]


def validate_created_markdown(path, value):
    """A strict native frontmatter subset, not a behavioral sandbox for prose."""
    if "/references/" in path:
        return
    skill = path.endswith("/SKILL.md")
    expected_name = PurePosixPath(path).parent.name if skill else PurePosixPath(path).stem
    allowed = ({"name", "description", "disable-model-invocation", "argument-hint"}
               if skill else {"name", "description", "tools"})
    required = allowed - {"argument-hint"} if skill else allowed
    end = value.find("\n---\n", 3)
    require(value.startswith("---\n") and 3 < end <= 4096 and
            value[end + 5:].strip(), "create requires strict frontmatter and a prose body")
    fields = {}
    for line in value[4:end].split("\n"):
        match = re.fullmatch(r"([a-z][a-z-]*): ([^\r\n\t]+)", line)
        require(match is not None, "unsupported frontmatter syntax")
        key, raw = match.groups()
        require(key in allowed and key not in fields and len(raw) <= 2048,
                "unknown, duplicate, or oversized frontmatter field")
        fields[key] = raw
    require(required <= set(fields), "required frontmatter fields are missing")
    require(fields["name"] == expected_name, "frontmatter name must match target name")
    for key in ("description", "argument-hint"):
        if key in fields:
            raw = fields[key]
            require(raw.startswith('"') and raw.endswith('"'),
                    "frontmatter descriptions/hints must be JSON-quoted strings")
            parsed = strict_json(raw.encode("utf-8"))
            require(type(parsed) is str and 0 < len(parsed.strip()) <= 512 and
                    not any(ord(c) < 32 or ord(c) == 127 for c in parsed),
                    "invalid frontmatter description or hint")
    if skill:
        require(fields["disable-model-invocation"] == "true",
                "created skills must disable model invocation")
    else:
        tools = [tool.strip() for tool in fields["tools"].split(",")]
        require(tools and len(tools) == len(set(tools)) and
                set(tools) <= {"Read", "Glob", "Grep", "WebSearch", "WebFetch"},
                "created agents require a nonempty read-only tool list")


def postimage(path, operation, value, baseline):
    valid_target(path, operation)
    before = decode_image(baseline, baseline=True)
    if operation == "json_merge":
        merged = settings_patch(strict_json(before) if before is not None else {}, value)
        after = (json.dumps(merged, sort_keys=True, indent=2, ensure_ascii=True,
                            allow_nan=False) + "\n").encode("utf-8")
    elif operation == "managed_block":
        after = managed_block(before or b"", value)
    else:
        require(before is None, "create refuses an existing target")
        require(type(value) is str and value.strip(), "create requires nonempty text")
        validate_created_markdown(path, value)
        after = value.encode("utf-8")
    require(len(after) <= MAX_FILE, "postimage exceeds size limit")
    text(after)
    return {"sha256": sha(after), "content_b64": base64.b64encode(after).decode("ascii"),
            "mode": baseline["mode"] if baseline["exists"] else 0o600}


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def stamp(value):
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_stamp(value):
    require(type(value) is str, "invalid timestamp")
    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError as exc:
        raise HarnessError("invalid timestamp") from exc
    require(stamp(parsed) == value, "noncanonical timestamp")
    return parsed


def candidate_digest(manifest):
    return sha(canonical({k: v for k, v in manifest.items() if k != "digest"}))


def exclusive_write(path, data, mode=0o600):
    path = safe_path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), mode)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def atomic_write(path, data, mode=0o600):
    path = safe_path(path)
    require(path.parent.is_dir(), "target parent is missing")
    fd, temp = tempfile.mkstemp(prefix=".harness-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            os.fchmod(handle.fileno(), mode)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        safe_path(path)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def stage(project, plan, out):
    root = project_path(project)
    plan_path = safe_path(plan)
    bundle = safe_path(out)
    require(bundle != root and root not in bundle.parents,
            "bundle must be outside the project")
    require(not bundle.exists() and bundle.parent.is_dir(),
            "bundle must be new with an existing parent directory")
    specification = strict_json(bounded_read(plan_path, MAX_PLAN)[0])
    exact_keys(specification, ("schema_version", "rationale", "changes"), "plan")
    require(type(specification["schema_version"]) is int and
            specification["schema_version"] == SCHEMA, "unsupported plan schema")
    require(type(specification["rationale"]) is str and
            0 < len(specification["rationale"].strip()) <= 4096,
            "a nonempty bounded rationale is required")
    changes = specification["changes"]
    require(type(changes) is list and 0 < len(changes) <= MAX_CHANGES,
            "a nonempty bounded change list is required")
    entries, seen = [], set()
    for change in changes:
        exact_keys(change, ("path", "operation", "value"), "change")
        valid_target(change["path"], change["operation"])
        require(change["path"] not in seen, "duplicate target path")
        seen.add(change["path"])
        baseline = snapshot(root / change["path"])
        after = postimage(change["path"], change["operation"], change["value"], baseline)
        entries.append({**change, "baseline": baseline, "postimage": after})
    created = now()
    manifest = {
        "schema_version": SCHEMA, "project": str(root),
        "created_at": stamp(created), "expires_at": stamp(created + dt.timedelta(hours=24)),
        "rationale": specification["rationale"], "changes": entries,
    }
    manifest["digest"] = candidate_digest(manifest)
    encoded = canonical(manifest) + b"\n"
    require(len(encoded) <= MAX_BUNDLE, "bundle exceeds size limit")
    os.mkdir(bundle, 0o700)
    exclusive_write(bundle / "manifest.json", encoded)
    return {"status": "staged", "bundle": str(bundle), "digest": manifest["digest"],
            "expires_at": manifest["expires_at"], "changes": len(entries),
            "project_files_changed": False}


def load_bundle(bundle, project=None, allow_expired=False):
    directory = safe_path(bundle)
    require(directory.is_dir(), "bundle directory is missing")
    manifest = strict_json(bounded_read(directory / "manifest.json", MAX_BUNDLE)[0])
    exact_keys(manifest, ("schema_version", "project", "created_at", "expires_at",
                          "rationale", "changes", "digest"), "manifest")
    require(type(manifest["schema_version"]) is int and
            manifest["schema_version"] == SCHEMA, "unsupported bundle schema")
    require(type(manifest["digest"]) is str and
            re.fullmatch(r"[a-f0-9]{64}", manifest["digest"]) and
            manifest["digest"] == candidate_digest(manifest), "manifest digest mismatch")
    require(type(manifest["project"]) is str and
            Path(manifest["project"]).is_absolute(), "invalid bound project")
    root = project_path(manifest["project"])
    require(str(root) == manifest["project"], "project path is not canonical")
    require(root != directory and root not in directory.parents,
            "bundle must be outside the project")
    if project is not None:
        require(project_path(project) == root, "bundle is bound to a different project")
    created, expires = parse_stamp(manifest["created_at"]), parse_stamp(manifest["expires_at"])
    require(expires - created == dt.timedelta(hours=24), "invalid bundle lifetime")
    require(created <= now(), "bundle creation time is in the future")
    if not allow_expired:
        require(now() < expires, "bundle expired; stage a new proposal")
    require(type(manifest["rationale"]) is str and
            0 < len(manifest["rationale"].strip()) <= 4096, "invalid rationale")
    require(type(manifest["changes"]) is list and
            0 < len(manifest["changes"]) <= MAX_CHANGES, "invalid change list")
    seen = set()
    for change in manifest["changes"]:
        exact_keys(change, ("path", "operation", "value", "baseline", "postimage"),
                   "bundle change")
        valid_target(change["path"], change["operation"])
        require(change["path"] not in seen, "duplicate target path")
        seen.add(change["path"])
        safe_path(root / change["path"])
        decode_image(change["baseline"], baseline=True)
        decode_image(change["postimage"])
        expected = postimage(change["path"], change["operation"], change["value"],
                             change["baseline"])
        require(expected == change["postimage"], "postimage does not match approved operation")
    return directory, root, manifest


def matches(root, change, applied):
    live = snapshot(root / change["path"])
    expected = {"exists": True, **change["postimage"]} if applied else change["baseline"]
    require(live == expected, f"file drift: {change['path']}")


RECEIPT_STATES = {
    "applying", "applied", "apply_failed", "apply_reverted",
    "rolling_back", "rolled_back", "rollback_failed",
}


def read_receipt(bundle, manifest, required=False):
    path = safe_path(bundle / "receipt.json")
    if not path.exists():
        require(not required, "no application receipt")
        return None
    value = strict_json(bounded_read(path)[0])
    exact_keys(value, ("schema_version", "digest", "state", "pending", "updated_at",
                       "errors"), "receipt")
    require(type(value["schema_version"]) is int and value["schema_version"] == SCHEMA
            and value["digest"] == manifest["digest"], "receipt binding mismatch")
    require(type(value["state"]) is str and value["state"] in RECEIPT_STATES,
            "invalid receipt state")
    paths = [change["path"] for change in manifest["changes"]]
    pending = value["pending"]
    require(type(pending) is list and all(type(p) is str and p in paths for p in pending)
            and len(set(pending)) == len(pending), "invalid receipt paths")
    require(type(value["errors"]) is list and len(value["errors"]) <= MAX_CHANGES + 1 and
            all(type(e) is str and len(e) <= 256 for e in value["errors"]),
            "invalid receipt errors")
    parse_stamp(value["updated_at"])
    if value["state"] == "applied":
        require(pending == paths, "incomplete applied receipt")
    if value["state"] in {"rolled_back", "apply_reverted"}:
        require(not pending, "inconsistent reverted receipt")
    return value


def write_receipt(bundle, manifest, state, pending, errors=None):
    value = {"schema_version": SCHEMA, "digest": manifest["digest"], "state": state,
             "pending": list(pending), "updated_at": stamp(now()), "errors": errors or []}
    atomic_write(bundle / "receipt.json", canonical(value) + b"\n")


def check(bundle, project=None):
    directory, root, manifest = load_bundle(bundle, project)
    receipt = read_receipt(directory, manifest)
    require(receipt is None, "bundle already attempted; inspect its receipt or roll back")
    for change in manifest["changes"]:
        matches(root, change, False)
    return {"status": "ready", "digest": manifest["digest"], "project": str(root),
            "changes": len(manifest["changes"]), "expires_at": manifest["expires_at"],
            "effective_runtime": "unverified"}


def diff(bundle, project=None):
    _, _, manifest = load_bundle(bundle, project, allow_expired=True)
    result = []
    for change in manifest["changes"]:
        before = decode_image(change["baseline"], baseline=True)
        after = decode_image(change["postimage"])
        lines = difflib.unified_diff(
            text(before or b"").splitlines(keepends=True), text(after).splitlines(keepends=True),
            fromfile="a/" + change["path"] if before is not None else "/dev/null",
            tofile="b/" + change["path"], lineterm="\n")
        for line in lines:
            result.append(line)
            if not line.endswith("\n"):
                result.append("\n\\ No newline at end of file\n")
    return "".join(result)


@contextlib.contextmanager
def writer_lock(root):
    # Per-user, per-project locks outside the project. Never delete lock files:
    # unlinking a locked inode could allow a second cooperating writer through.
    # macOS commonly spells its trusted temporary base through /var -> /private/var.
    # Resolve only that OS-selected base, never a project, bundle, or lock child.
    temporary_base = Path(tempfile.gettempdir()).resolve()
    directory = safe_path(temporary_base / f"harness-setup-{os.getuid()}-locks")
    try:
        os.mkdir(directory, 0o700)
    except FileExistsError:
        pass
    st = directory.lstat()
    require(stat.S_ISDIR(st.st_mode) and st.st_uid == os.getuid() and
            stat.S_IMODE(st.st_mode) == 0o700, "unsafe writer lock directory")
    lock = safe_path(directory / (sha(str(root).encode("utf-8")) + ".lock"))
    fd = os.open(lock, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        st = os.fstat(fd)
        require(stat.S_ISREG(st.st_mode) and st.st_uid == os.getuid() and
                stat.S_IMODE(st.st_mode) == 0o600 and st.st_nlink == 1,
                "unsafe writer lock")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise HarnessError("another harness writer holds the project lock") from exc
        yield
    finally:
        os.close(fd)


def ensure_parents(root, path):
    for relative in reversed(path.relative_to(root).parents):
        directory = safe_path(root / relative)
        if not directory.exists():
            os.mkdir(directory, 0o700)
        require(directory.is_dir(), "target parent is not a directory")


def restore(root, change):
    path = safe_path(root / change["path"])
    baseline = change["baseline"]
    if baseline["exists"]:
        atomic_write(path, decode_image(baseline, baseline=True), baseline["mode"])
    else:
        os.unlink(path)


def verify_backups(bundle, manifest):
    for index, change in enumerate(manifest["changes"]):
        if change["baseline"]["exists"]:
            data, _ = bounded_read(bundle / "backups" / f"{index:04d}.bin")
            require(data == decode_image(change["baseline"], baseline=True),
                    "backup integrity mismatch")


def approve(manifest, approval):
    require(type(approval) is str and approval == manifest["digest"],
            "approval must equal the exact manifest digest")


def apply(bundle, approval, project=None):
    directory, root, manifest = load_bundle(bundle, project)
    approve(manifest, approval)
    with writer_lock(root):
        directory, root, manifest = load_bundle(bundle, project)
        approve(manifest, approval)
        require(read_receipt(directory, manifest) is None,
                "bundle already attempted; stage a new proposal")
        for change in manifest["changes"]:
            matches(root, change, False)
        backup_dir = safe_path(directory / "backups")
        require(not backup_dir.exists(), "unexpected backup directory; restage")
        os.mkdir(backup_dir, 0o700)
        for index, change in enumerate(manifest["changes"]):
            if change["baseline"]["exists"]:
                exclusive_write(backup_dir / f"{index:04d}.bin",
                                decode_image(change["baseline"], baseline=True))
        pending = []
        write_receipt(directory, manifest, "applying", pending)
        try:
            for change in manifest["changes"]:
                matches(root, change, False)
                target = safe_path(root / change["path"])
                ensure_parents(root, target)
                atomic_write(target, decode_image(change["postimage"]), change["postimage"]["mode"])
                pending.append(change["path"])
                write_receipt(directory, manifest, "applying", pending)
            write_receipt(directory, manifest, "applied", pending)
        except (OSError, HarnessError) as exc:
            errors = ["application failed"]
            for change in reversed(manifest["changes"]):
                if change["path"] in pending:
                    try:
                        matches(root, change, True)
                        restore(root, change)
                        pending.remove(change["path"])
                    except (OSError, HarnessError):
                        errors.append("compensation failed: " + change["path"])
            try:
                write_receipt(directory, manifest, "apply_failed" if pending else "apply_reverted",
                              pending, errors)
            except (OSError, HarnessError):
                raise HarnessError("apply failed; receipt update also failed; manual recovery required") from exc
            raise HarnessError("apply failed; " + ("partial changes remain; inspect receipt" if pending
                                                  else "completed writes were reverted")) from exc
    return {"status": "applied", "digest": manifest["digest"], "changes": len(pending),
            "effective_runtime": "unverified"}


def rollback(bundle, approval, project=None):
    # Expiry prevents new application, not recovery of an already applied bundle.
    directory, root, manifest = load_bundle(bundle, project, allow_expired=True)
    approve(manifest, approval)
    with writer_lock(root):
        directory, root, manifest = load_bundle(bundle, project, allow_expired=True)
        approve(manifest, approval)
        receipt = read_receipt(directory, manifest, required=True)
        require(receipt["state"] in {"applied", "apply_failed", "rollback_failed"},
                "receipt is not rollback-ready; interrupted states need manual recovery")
        pending = list(receipt["pending"])
        require(pending, "no remaining applied changes")
        verify_backups(directory, manifest)
        for change in manifest["changes"]:
            matches(root, change, change["path"] in pending)
        count = len(pending)
        write_receipt(directory, manifest, "rolling_back", pending)
        try:
            for change in reversed(manifest["changes"]):
                if change["path"] in pending:
                    matches(root, change, True)
                    restore(root, change)
                    pending.remove(change["path"])
                    write_receipt(directory, manifest, "rolling_back", pending)
            write_receipt(directory, manifest, "rolled_back", [])
        except (OSError, HarnessError) as exc:
            try:
                write_receipt(directory, manifest, "rollback_failed", pending, ["rollback failed"])
            except (OSError, HarnessError):
                raise HarnessError("rollback failed; receipt update also failed; manual recovery required") from exc
            raise HarnessError("rollback incomplete; remaining paths recorded in receipt") from exc
    return {"status": "rolled_back", "digest": manifest["digest"], "changes": count}


def settings_summary(value):
    require(type(value) is dict, "configuration is not an object")
    summary = {
        "known_key_names": sorted(set(value) & SETTINGS_KEYS),
        "other_key_count": len(set(value) - SETTINGS_KEYS),
    }
    permissions = value.get("permissions", {})
    if type(permissions) is dict:
        summary["permission_counts"] = {
            key: len(permissions[key]) if type(permissions.get(key)) is list else None
            for key in ("allow", "ask", "deny")
        }
    else:
        summary["permissions_status"] = "malformed"
    enabled = value.get("enabledPlugins", {})
    if type(enabled) is dict:
        summary["enabled_plugins"] = {
            key: val for key, val in sorted(enabled.items())[:128]
            if IDENT.fullmatch(key) and type(val) is bool
        }
        summary["plugins_omitted"] = len(enabled) - len(summary["enabled_plugins"])
    else:
        summary["plugins_status"] = "malformed"
    return summary


def metadata(path, label, kind="file"):
    result = {"path": label, "kind": kind}
    try:
        safe_path(path)
        if not path.exists():
            return {**result, "status": "missing"}
        st = path.lstat()
        if stat.S_ISDIR(st.st_mode):
            return {**result, "status": "directory"}
        if not stat.S_ISREG(st.st_mode):
            return {**result, "status": "not_regular"}
        result["size_bytes"] = st.st_size
        if st.st_size > MAX_FILE:
            return {**result, "status": "too_large"}
        data, _ = bounded_read(path)
        result.update(status="present", sha256=sha(data))
        if kind in {"settings", "mcp", "plugin", "plugin_index", "marketplace_index", "user_config"}:
            try:
                value = strict_json(data)
                require(type(value) is dict, "configuration is not an object")
                if kind == "settings":
                    result["summary"] = settings_summary(value)
                elif kind == "mcp":
                    servers = value.get("mcpServers", {})
                    require(type(servers) is dict, "invalid MCP server map")
                    result["summary"] = {"server_count": len(servers), "connection": "unverified"}
                elif kind == "plugin":
                    result["summary"] = {
                        key: value[key] for key in ("name", "version")
                        if type(value.get(key)) is str and IDENT.fullmatch(value[key])
                    }
                elif kind == "plugin_index":
                    plugins = value.get("plugins", {})
                    require(type(plugins) is dict, "invalid plugin index")
                    names = [key for key in sorted(plugins)[:128] if IDENT.fullmatch(key)]
                    result["summary"] = {"plugin_ids": names, "entry_count": len(plugins),
                                         "omitted": len(plugins) - len(names)}
                elif kind == "marketplace_index":
                    result["summary"] = {"entry_count": len(value)}
                else:
                    result["summary"] = {"key_count": len(value), "effective_runtime": "unverified"}
            except HarnessError:
                result["status"] = "malformed"
    except HarnessError:
        result["status"] = "symlink" if any(p.is_symlink() for p in (path, *path.parents)) else "unreadable"
    except (OSError, ValueError):
        result["status"] = "unreadable"
    return result


def directory_entries(directory):
    """Bound enumeration; truncated directories are explicitly incomplete."""
    try:
        safe_path(directory)
        with os.scandir(directory) as entries:
            found = []
            for index, entry in enumerate(entries):
                if index == MAX_ENTRIES:
                    return sorted(found), "truncated"
                found.append(entry.name)
        return sorted(found), "complete"
    except HarnessError:
        return [], "symlink"
    except FileNotFoundError:
        return [], "missing"
    except OSError:
        return [], "unreadable"


def scan(project, include_user=False, max_depth=3):
    root = project_path(project)
    require(type(max_depth) is int and 0 <= max_depth <= 6, "max depth must be 0..6")
    report = {
        "schema_version": SCHEMA, "project": str(root),
        "scope": {
            "include_user": include_user, "max_depth": max_depth,
            "max_file_bytes": MAX_FILE, "max_directory_entries": MAX_ENTRIES,
            "max_nodes": MAX_NODES, "max_records_per_collection": MAX_RECORDS,
            "global_managed_state": "incomplete", "effective_settings": "unverified",
            "runtime_readiness": "unverified", "commands_executed": False,
            "mcp_policy": "live changes require separate human CLI approval",
        },
        "runtime": {
            "route_environment_names_present": [key for key in ROUTE_ENV if key in os.environ],
            "shell_aliases_wrappers": "unverified", "effective_provider_route": "unverified",
            "native_cli_version": "not_probed", "required_human_evidence": "real Claude Code /status",
        },
        "instructions": [], "configuration": [], "stack_manifests": [],
        "skills": [], "agents": [], "plugin_metadata": [], "coverage": [],
    }
    ancestors = [root, *root.parents]
    for parent in ancestors[:32]:
        for name in ("CLAUDE.md", "AGENTS.md"):
            report["instructions"].append(metadata(parent / name, str(parent / name), "instruction"))
    if len(ancestors) > 32:
        report["coverage"].append({"path": "ancestors", "status": "truncated"})
    for relative, kind in (
        (".claude/settings.json", "settings"), (".claude/settings.local.json", "settings"),
        (".mcp.json", "mcp"),
    ):
        report["configuration"].append(metadata(root / relative, relative, kind))

    nodes = 0

    def walk(directory, depth):
        nonlocal nodes
        if nodes >= MAX_NODES:
            return
        names, status = directory_entries(directory)
        if status != "complete":
            report["coverage"].append({"path": str(directory.relative_to(root)), "status": status})
        for name in names:
            nodes += 1
            if nodes > MAX_NODES:
                return
            child = directory / name
            relative = str(child.relative_to(root))
            if name in STACK_FILES and len(report["stack_manifests"]) < MAX_RECORDS:
                report["stack_manifests"].append(metadata(child, relative, "stack_manifest"))
            if name in EXCLUDED or name.startswith("."):
                continue
            if child.is_symlink():
                if len(report["coverage"]) < MAX_RECORDS:
                    report["coverage"].append({"path": relative, "status": "symlink"})
                continue
            if depth < max_depth and child.is_dir():
                walk(child, depth + 1)

    walk(root, 0)
    if nodes >= MAX_NODES:
        report["coverage"].append({"path": ".", "status": "node_limit_reached"})

    def installed(base, label):
        for category in ("skills", "agents"):
            directory = base / category
            names, status = directory_entries(directory)
            report["coverage"].append({"path": label + "/" + category, "status": status})
            for name in names:
                if len(report[category]) >= MAX_RECORDS:
                    report["coverage"].append({"path": label + "/" + category, "status": "record_limit_reached"})
                    break
                if category == "agents" and re.fullmatch(SLUG + r"\.md", name):
                    report["agents"].append(metadata(directory / name, label + "/agents/" + name, "agent"))
                elif category == "skills" and re.fullmatch(SLUG, name):
                    report["skills"].append(metadata(directory / name / "SKILL.md",
                                                     label + "/skills/" + name + "/SKILL.md", "skill"))
                    references = directory / name / "references"
                    ref_names, ref_status = directory_entries(references)
                    if ref_status != "missing":
                        report["coverage"].append({"path": label + "/skills/" + name + "/references", "status": ref_status})
                    for ref in ref_names:
                        if re.fullmatch(SLUG + r"\.md", ref) and len(report["skills"]) < MAX_RECORDS:
                            report["skills"].append(metadata(references / ref,
                                label + "/skills/" + name + "/references/" + ref, "skill_reference"))

    def instruction_directory(base, label):
        report["instructions"].append(metadata(base / "CLAUDE.md", label + "/CLAUDE.md", "instruction"))
        names, status = directory_entries(base / "rules")
        report["coverage"].append({"path": label + "/rules", "status": status})
        for name in names:
            if len(report["instructions"]) >= MAX_RECORDS:
                report["coverage"].append({"path": label + "/rules", "status": "record_limit_reached"})
                break
            if re.fullmatch(SLUG + r"\.md", name):
                report["instructions"].append(metadata(base / "rules" / name,
                                                      label + "/rules/" + name, "rule"))

    instruction_directory(root / ".claude", ".claude")
    installed(root / ".claude", ".claude")
    for name in ("plugin.json", "marketplace.json"):
        relative = ".claude-plugin/" + name
        report["plugin_metadata"].append(metadata(root / relative, relative, "plugin" if name == "plugin.json" else "marketplace_index"))
    if report["plugin_metadata"][0]["status"] == "present":
        installed(root, ".")

    custom = os.environ.get("CLAUDE_CONFIG_DIR")
    report["user"] = {
        "included": include_user,
        "claude_config_dir": {"is_set": custom is not None, "value": "not_reported"},
        "configuration": [], "resolution": "incomplete",
    }
    if include_user:
        # Fixed config/index paths only. Never inspect credentials, sessions,
        # transcripts, shell startup files, ~/.infra, or arbitrary home trees.
        bases = [(Path.home() / ".claude", "~/.claude")]
        if custom:
            bases.append((Path(custom).expanduser(), "CLAUDE_CONFIG_DIR"))
        for base, label in bases:
            report["user"]["configuration"].append(metadata(base, label, "config_directory"))
            for relative, kind in (
                ("settings.json", "settings"), ("settings.local.json", "settings"),
                ("CLAUDE.md", "instruction"), ("AGENTS.md", "instruction"),
                (".mcp.json", "mcp"), ("plugins/installed_plugins.json", "plugin_index"),
                ("plugins/known_marketplaces.json", "marketplace_index"),
            ):
                report["user"]["configuration"].append(metadata(base / relative, label + "/" + relative, kind))
            installed(base, label)
            instruction_directory(base, label)
        report["user"]["configuration"].append(metadata(Path.home() / ".claude.json", "~/.claude.json", "user_config"))
    return report


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    scan_parser = sub.add_parser("scan", help="bounded read-only metadata; no CLI execution")
    scan_parser.add_argument("--project", required=True)
    scan_parser.add_argument("--include-user", action="store_true")
    scan_parser.add_argument("--max-depth", type=int, choices=range(7), default=3)
    scan_parser.add_argument("--output", help="write only this new JSON artifact instead of stdout")
    stage_parser = sub.add_parser("stage", help="validate a plan and create a new external bundle")
    stage_parser.add_argument("--project", required=True)
    stage_parser.add_argument("--plan", required=True)
    stage_parser.add_argument("--out", required=True)
    for command in ("check", "diff", "apply", "rollback"):
        command_parser = sub.add_parser(command)
        command_parser.add_argument("--bundle", required=True)
        command_parser.add_argument("--project", help="optional additional project-binding assertion")
        if command in ("apply", "rollback"):
            command_parser.add_argument("--approve", required=True,
                help="exact manifest SHA-256; integrity token, not human authentication")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "scan":
            result = scan(args.project, args.include_user, args.max_depth)
            if args.output:
                exclusive_write(safe_path(args.output), canonical(result) + b"\n")
                return 0
        elif args.command == "stage":
            result = stage(args.project, args.plan, args.out)
        elif args.command == "diff":
            sys.stdout.write(diff(args.bundle, args.project))
            return 0
        elif args.command == "check":
            result = check(args.bundle, args.project)
        elif args.command == "apply":
            result = apply(args.bundle, args.approve, args.project)
        else:
            result = rollback(args.bundle, args.approve, args.project)
        print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True))
        return 0
    except (HarnessError, OSError, ValueError, RecursionError) as exc:
        # OS/parser exception strings can contain untrusted content or paths.
        message = str(exc) if isinstance(exc, HarnessError) else "filesystem or input failure"
        print(json.dumps({"status": "error", "error": message}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
