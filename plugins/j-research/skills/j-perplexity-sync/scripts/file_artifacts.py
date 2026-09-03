#!/usr/bin/env python3
"""File downloaded Perplexity Computer artifacts into the vault + Drive.

usage: file_artifacts.py <stage_dir> <month YYYY-MM> [--dry-run]
text (.md/.txt/no-ext markdown) -> evidence/perplexity/artifacts/pplx-doc-<slug>.md (frontmatter added)
.csv/.py                        -> evidence/perplexity/artifacts/<name>   (kept as files)
.png/.zip/.pdf/.docx            -> ~/Google Drive/My Drive/Documents/2. Resource/Perplexity artifacts/
Every item gets one bullet in evidence/perplexity/perplexity-library.md under "## Computer artifacts".
"""
import hashlib, re, shutil, sys
from pathlib import Path

VAULT = Path.home() / "Documents/pkm"
OUT = VAULT / "evidence/perplexity/artifacts"
DRIVE = Path.home() / "Google Drive/My Drive/Documents/2. Resource/Perplexity artifacts"
HUB = VAULT / "evidence/perplexity/perplexity-library.md"
SKIP = {"GitLab — Who to Follow, Connect, and Get Referred By.md", "LinkedIn Content Plan — 8 Weeks.md"}  # already filed as pplx-*-doc-* notes
BINARY = {".png", ".zip", ".pdf", ".docx", ".xlsx", ".jpg"}
FILES = {".csv", ".py", ".txt", ".json"}
SLUG_OVERRIDE = {"Краткое общение с топ-менеджерами IT": "short-talk-with-it-top-managers"}
GENERIC_STEM = re.compile(r"^(md|claude-code-business-os)( \(\d+\))?$")
GENERIC_HEAD = re.compile(r"^(executive summary|overview|request|background|direct answer|introduction)$", re.I)


def base_name(p):
    return re.sub(r" \(\d+\)$", "", re.sub(r"\.(md|txt|py|csv|png|zip)$", "", p.name))


def slugify(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return re.sub(r"-+", "-", t)[:60].strip("-")


def title_of(path, text):
    stem = base_name(path)
    if not GENERIC_STEM.match(stem):
        return stem[:120]
    m = re.search(r"^#{1,3}\s+(.+?)\s*$", text, re.M)
    t = (m.group(1) if m else stem).strip("# ").strip()
    if GENERIC_HEAD.match(t) and m:
        para = re.search(r"\n\n([^\n#].{20,})", text[m.end():])
        if para:
            t = f"{t}: " + " ".join(re.sub(r"[*_`\[\]]", "", para.group(1)).split()[:9])
    return re.sub(r"\s+", " ", t)[:120]


def main(stage, month, dry):
    OUT.mkdir(parents=True, exist_ok=True)
    if not dry:
        DRIVE.mkdir(parents=True, exist_ok=True)
    bullets = []
    seen = set()
    for p in sorted(Path(stage).iterdir()):
        if not p.is_file() or p.name.startswith(".") or p.name in SKIP:
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h in seen:
            print("dup-content\t", p.name); continue
        seen.add(h)
        ext = p.suffix.lower()
        if p.name.startswith("signal_scan.py"):
            dest = OUT / "signal_scan.py"
            if not dry: shutil.copy2(p, dest)
            bullets.append(f"- `evidence/perplexity/artifacts/signal_scan.py` — file: buying-signal scanner ({month})")
            print("file\t", dest.name); continue
        if ext in BINARY:
            dest = DRIVE / p.name
            if not dry: shutil.copy2(p, dest)
            bullets.append(f"- `{dest.relative_to(Path.home())}` — file ({month})")
            print("drive\t", dest.name); continue
        if ext in FILES:
            dest = OUT / p.name
            if not dry: shutil.copy2(p, dest)
            bullets.append(f"- `evidence/perplexity/artifacts/{p.name}` — file ({month})")
            print("file\t", dest.name); continue
        text = p.read_text(encoding="utf-8", errors="replace")
        title = title_of(p, text)
        slug = SLUG_OVERRIDE.get(title) or slugify(title) or h[:8]
        dest = OUT / f"pplx-doc-{slug}.md"
        n = 2
        while dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() != h and f"content_hash: {h}" not in dest.read_text(encoding="utf-8"):
            dest = OUT / f"pplx-doc-{slug}-{n}.md"; n += 1
        if dest.exists():
            print("exists\t", dest.name); continue
        safe = title.replace('"', "'")
        note = "\n".join([
            "---", "type: Research", "state: organized", "provenance: external-research",
            "source: perplexity", "kind: computer-document", f'title: "{safe}"',
            "url: https://www.perplexity.ai/computer/artifacts", f"created: {month}", "filed: 2026-09-03",
            "Belongs to:", '  - "[[pkm]]"', "Related to:", '  - "[[perplexity-library]]"',
            f"content_hash: {h}", "---", "",
            f"Perplexity Computer artifact `{p.name}`, downloaded 2026-09-03 from perplexity.ai/computer/artifacts, unedited.", "",
            text.rstrip(), ""])
        if not dry: dest.write_text(note, encoding="utf-8")
        bullets.append(f"- [[{dest.stem}]] — document: {safe[:90]} ({month})")
        print("note\t", dest.name)
    if bullets and not dry:
        h = HUB.read_text(encoding="utf-8")
        head = "## Computer artifacts"
        block = "\n".join(bullets) + "\n"
        if head in h:
            i = h.index(head); j = h.find("\n## ", i + 1); j = len(h) if j < 0 else j
            h = h[:j].rstrip("\n") + "\n" + block + h[j:]
        else:
            h = h.rstrip("\n") + f"\n\n{head}\n\nFiles the Computer tasks produced (perplexity.ai/computer/artifacts). Text lives here as `pplx-doc-*` notes; binaries on Google Drive under `Documents/2. Resource/Perplexity artifacts/`.\n\n" + block
        HUB.write_text(h, encoding="utf-8")
    print(f"{len(bullets)} filed")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--dry-run" in sys.argv)
