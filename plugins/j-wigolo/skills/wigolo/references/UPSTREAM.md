# Upstream provenance — KnockOutEZ/wigolo

This skill is a **fork of vendored upstream**, not an original JetThoughts skill.

| Field | Value |
|---|---|
| Upstream | https://github.com/KnockOutEZ/wigolo |
| Upstream author | KnockOutEZ |
| Fork point (version) | `0.1.43-beta.2` |
| License | AGPL-3.0-only (inherited; see the upstream repo) |
| Vendored into this repo | originally as an 11-skill pack under `plugins/j-wigolo/skills/` |
| Repackaged | `wigolo` front door + `references/<tool>.md`; the 10 sibling `wigolo-*` skills were removed |

## What was repackaged, and what was not

Upstream ships one skill directory per tool (`wigolo-search`, `wigolo-fetch`, `wigolo-crawl`,
`wigolo-cache`, `wigolo-extract`, `wigolo-diff`, `wigolo-watch`, `wigolo-research`,
`wigolo-agent`, `wigolo-find-similar`) plus the `wigolo` front door. Every one of those had the
same shape — frontmatter, `# wigolo <tool>`, a Quick Reference JSON block, a Parameters table,
one See Also — and the front door's Tool Selection table already routed between them.

This repo collapsed that pack into a single `wigolo` skill whose body carries the front door and
the routing table, with each tool's detail moved verbatim into `references/<tool>.md`. Tool
parameters, output shapes, anti-patterns and "when not to use" notes are upstream's text; only the
packaging and the relative links changed. `metadata.author`, `metadata.version`, `metadata.homepage`
and the `license` field in `SKILL.md` still carry upstream's values.

## Sync step for a future upstream revision

1. Fetch upstream at the new tag, e.g.
   `git clone --depth 1 --branch <tag> https://github.com/KnockOutEZ/wigolo`.
2. Diff upstream's `wigolo-<tool>/SKILL.md` body against `references/<tool>.md` here. Expect link
   churn only; any body change is a real semantic change.
3. Diff upstream's `wigolo/SKILL.md` (description, Tool Selection table, Key Rules, Search backend)
   against this skill's body, keeping this repo's routing paragraph ("Wigolo is not the research
   router…") in place — that paragraph is local policy, not upstream.
4. Update `metadata.version` and this file's "Fork point (version)" row.
