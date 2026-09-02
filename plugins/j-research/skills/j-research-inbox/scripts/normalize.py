#!/usr/bin/env python3
"""Normalize research sources into vault Markdown notes.

Subcommands:
  ingest [--dry-run]                       process research/_inbox/<source>/*
  publish --source S --title T [--url U]   read body from stdin, write one note
          [--tags a,b] [--dry-run]

See SKILL.md for the frontmatter contract and directory layout.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SOURCES = ["perplexica", "perplexity", "claude", "gemini", "notebooklm", "local"]


def default_vault():
    return Path(os.environ.get("RESEARCH_VAULT", "~/Documents/pkm")).expanduser()


def slugify(text, max_len=60):
    text = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    text = re.sub(r"-+", "-", text)
    return text[:max_len].strip("-") or "untitled"


def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(text):
    """Best-effort 'key: value' frontmatter parser. Returns (dict, body)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, text
    fm_text = parts[0][3:]
    rest = parts[1].split("\n", 1)
    body = rest[1] if len(rest) > 1 else ""
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, body.lstrip("\n")


def extract_h1(body):
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def humanize(stem):
    return stem.replace("-", " ").replace("_", " ").strip().title() or "Untitled"


# Perplexity notes follow the vault's own convention: evidence/perplexity/<project>/pplx-<id8>-<slug>.md
# plus one bullet in the hub note. Project folder -> the vault project note it belongs to.
PPLX_BELONGS = {
    "jetthoughts-marketing": "[[jt-business-os]]", "business-os": "[[jt-business-os]]",
    "ai-harness-setup": "[[jt-business-os]]", "job-seek-in-berlin": "[[find-an-eng-leading-job]]",
    "investments": "[[build-finance-portfolio]]", "sessions": "[[pkm]]",
}
PPLX_HUB = "evidence/perplexity/perplexity-library.md"


def existing_pplx_ids(vault):
    return {m.group(1) for path in (vault / "evidence" / "perplexity").glob("*/pplx-*.md")
            for m in [re.match(r"pplx-([0-9a-f]{8})-", path.name)] if m}


def write_pplx_note(vault, source_id, title, body, url, date, project, dry_run):
    id8 = source_id[:8]
    if id8 in existing_pplx_ids(vault):
        return "skip", None
    kind = "computer-task" if "/computer/tasks/" in (url or "") else "thread"
    folder = slugify(project or "sessions", 40)
    belongs = PPLX_BELONGS.get(folder, "[[pkm]]")
    label = "Perplexity Computer task" if kind == "computer-task" else "Perplexity thread"
    body = body.strip()
    safe_title = title.replace('"', "'")
    text = "\n".join([
        "---", "type: Research", "state: organized", "provenance: external-research",
        "source: perplexity", f"kind: {kind}", f"url: {url}",
        f'project: "{project or folder.title()}"', f"filed: {date}",
        "Belongs to:", f'  - "{belongs}"', "Related to:", '  - "[[perplexity-library]]"',
        f"content_hash: {sha256_hex(body)}",
        f"citations_preserved: {'true' if re.search(r'https?://', body) else 'false'}",
        "---", "", f"# {label} \u2014 {safe_title}", "",
        f"Captured {date} from {url} as page text: Paul's prompts and Perplexity's answers, unedited.", "",
        body, "",
    ])
    dest = vault / "evidence" / "perplexity" / folder / f"pplx-{id8}-{slugify(title, 50)}.md"
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        hub = vault / PPLX_HUB
        if hub.exists():
            h = hub.read_text(encoding="utf-8")
            heading = "## " + (project or folder.replace("-", " ").title())
            bullet = f"- [[{dest.stem}]] \u2014 {'task' if kind == 'computer-task' else 'thread'}: {safe_title[:90]}\n"
            if heading in h:
                i = h.index(heading); j = h.find("\n## ", i + 1); j = len(h) if j < 0 else j
                h = h[:j].rstrip("\n") + "\n" + bullet + h[j:]
            else:
                h = h.rstrip("\n") + f"\n\n{heading}\n\n" + bullet
            hub.write_text(h, encoding="utf-8")
    return "ok", dest


def existing_hashes(vault):
    hashes = set()
    for path in vault.glob("research-*.md"):
        try:
            fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        h = fm.get("content_hash")
        if h:
            hashes.add(h)
    return hashes


def build_note(source, source_id, title, body, url=None, date=None, tags=None):
    tags = tags or []
    body = body.strip()
    content_hash = sha256_hex(body)
    citations_preserved = bool(re.search(r"https?://", body))
    imported = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date = date or datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        "type: Research",
        f"source: {source}",
        f"source_id: {source_id}",
        f"date: {date}",
    ]
    if url:
        lines.append(f"url: {url}")
    lines.append("tags: [" + ", ".join(tags) + "]")
    lines.append(f"content_hash: {content_hash}")
    lines.append(f"citations_preserved: {'true' if citations_preserved else 'false'}")
    lines.append(f"imported: {imported}")
    lines.append("---")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(body)
    lines.append("")
    return "\n".join(lines), content_hash


def write_note(vault, source, source_id, title, body, url, date, tags, dry_run, known_hashes):
    note_text, content_hash = build_note(source, source_id, title, body, url, date, tags)
    if content_hash in known_hashes:
        return "skip", None
    dest = vault / f"research-{source}-{slugify(title or source_id)}.md"
    if not dry_run:
        dest.write_text(note_text, encoding="utf-8")
    known_hashes.add(content_hash)
    return "ok", dest


def quarantine(vault, src_path, reason, dry_run, content=""):
    qdir = vault / "research" / "quarantine"
    if dry_run:
        return
    qdir.mkdir(parents=True, exist_ok=True)
    if src_path is not None:
        dest = qdir / src_path.name
        src_path.replace(dest)
    else:
        ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        dest = qdir / f"publish-{ts}.txt"
        dest.write_text(content, encoding="utf-8")
    (qdir / f"{dest.name}.reason.txt").write_text(reason + "\n", encoding="utf-8")


def mark_done(vault, source, src_path, dry_run):
    if dry_run:
        return
    done_dir = vault / "research" / "_inbox" / "_done" / source
    done_dir.mkdir(parents=True, exist_ok=True)
    src_path.replace(done_dir / src_path.name)


def process_markdown_file(vault, source, path, known_hashes, dry_run):
    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    body = body.strip()
    if not body:
        raise ValueError("empty body")
    title = fm.get("title") or extract_h1(body) or humanize(path.stem)
    source_id = fm.get("source_id") or path.stem
    date = fm.get("date") or datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
    if fm.get("source", source) == "perplexity":
        return write_pplx_note(vault, source_id, title, body, fm.get("url"), date, fm.get("project"), dry_run)
    status, dest = write_note(
        vault, fm.get("source", source), source_id, title, body,
        fm.get("url"), date, [], dry_run, known_hashes,
    )
    return status, dest


def process_claude_export(vault, source, path, known_hashes, dry_run):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("conversations.json must be a JSON array")
    results = []
    for convo in data:
        name = convo.get("name") or "untitled-conversation"
        lines = []
        for msg in convo.get("chat_messages") or []:
            text = (msg.get("text") or "").strip()
            if text:
                lines.append(f"**{msg.get('sender', 'unknown')}:** {text}\n")
        body = "\n".join(lines).strip()
        if not body:
            results.append(("skip", None))
            continue
        date = (convo.get("created_at") or "")[:10] or None
        source_id = convo.get("uuid") or name
        status, dest = write_note(
            vault, source, source_id, name, body, None, date, [], dry_run, known_hashes,
        )
        results.append((status, dest))
    return results


def ingest(vault, dry_run=False):
    known_hashes = existing_hashes(vault)
    results = []
    quarantined = False
    inbox_root = vault / "research" / "_inbox"
    for source in SOURCES:
        src_dir = inbox_root / source
        if not src_dir.is_dir():
            continue
        for path in sorted(src_dir.iterdir()):
            if path.is_dir() or path.name.startswith("."):
                continue
            try:
                if source == "claude" and path.suffix == ".json":
                    for status, dest in process_claude_export(vault, source, path, known_hashes, dry_run):
                        results.append((status, dest or path))
                else:
                    status, dest = process_markdown_file(vault, source, path, known_hashes, dry_run)
                    results.append((status, dest or path))
                mark_done(vault, source, path, dry_run)
            except Exception as exc:  # noqa: BLE001 - any per-file failure is quarantined
                quarantine(vault, path, str(exc), dry_run)
                results.append(("quarantine", path))
                quarantined = True
    for status, path in results:
        print(f"{status}\t{path}")
    return 1 if quarantined else 0


def publish(vault, source, title, url, tags, dry_run=False):
    body = sys.stdin.read().strip()
    known_hashes = existing_hashes(vault)
    if not body:
        quarantine(vault, None, "empty body from stdin", dry_run)
        print(f"quarantine\t<stdin:{source}:{title}>")
        return 1
    status, dest = write_note(vault, source, title, title, body, url, None, tags, dry_run, known_hashes)
    print(f"{status}\t{dest or f'<stdin:{source}:{title}>'}")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(prog="normalize.py")
    parser.add_argument("--vault", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("--dry-run", action="store_true")

    p_publish = sub.add_parser("publish")
    p_publish.add_argument("--source", required=True)
    p_publish.add_argument("--title", required=True)
    p_publish.add_argument("--url")
    p_publish.add_argument("--tags", default="")
    p_publish.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    vault = args.vault or default_vault()

    if args.command == "ingest":
        return ingest(vault, dry_run=args.dry_run)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    return publish(vault, args.source, args.title, args.url, tags, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
