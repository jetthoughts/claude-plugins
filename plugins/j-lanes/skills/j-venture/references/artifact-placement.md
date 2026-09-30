# Artifact placement

## The placement test

| If… | It goes | Because |
| --- | --- | --- |
| Paul should read it, act on it, or find it again in six months | **a vault note**, typed per PORTENT | Tolaria indexes it, boards surface it, `vault-health` checks its dates |
| Raw research about the world — evidence tables, quotes, source dumps | **`evidence/`** in the vault, Markdown, `type: Research`, stored whole and unfiltered | Tolaria indexes it; it is the citation the notes point to |
| Only agents read it — superseded reasoning, scratch analysis, the system deliberating about itself | **`.ai/`** at the repo root | dot-prefixed, so Tolaria never indexes it |
| It is a session transcript or run log | `.ai/sessions/` | byproduct, not knowledge |
| It is task or run state | the Paperclip card | the board is the queue |
| It is a large binary, PDF or contract | Google Drive under `Documents/` | the vault stays text |

Worked example (2026-08-29): the competitor teardown's raw 8-firm table stays in `evidence/`; its conclusion — the entry wedge — belongs in `who-we-serve-and-what-we-offer`, which is the note that owns positioning.

## Evidence item fields

Every externally derived evidence item carries these fields:

```json
{
  "evidence_id": "unique-id",
  "venture_id": "venture-id",
  "claim": "The specific claim this evidence supports",
  "source_url": "https://...",
  "source_type": "review | forum | job-post | competitor | interview | community | website",
  "captured_quote": "Exact relevant text",
  "captured_at": "ISO-8601 timestamp",
  "buyer_segment": "Who this concerns",
  "signal_type": "pain | urgency | budget | workaround | competitor-gap | reachability",
  "forcing_party": "Who compels the spend, or null",
  "forcing_date": "ISO-8601 date, or null",
  "confidence": "low | medium | high",
  "limitations": "What this does not prove"
}
```
