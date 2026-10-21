---
name: telegram-compression-mimicry
description: Telegram bot [COMPRESSED:summary] echo loop diag and fix.
---

# Telegram bot `[COMPRESSED:…]` echo-loop

## Symptom

The Telegram bot replies with `[COMPRESSED:summary] <one-line paraphrase>` or `[COMPRESSED:aging:fullSummary] <one-line paraphrase>` and stops — no tool calls, no real work. Looks like the bot is running an explicit compression step, but it isn't.

## Root cause

The bot's session for that chat has been running for days/weeks. Earlier turns got wrapped in `[COMPRESSED:…]` markers by:
- Hermes profile `compression:` block (default: `enabled: true, threshold: 0.5, target_ratio: 0.2`), OR
- omniroute gateway `caveman` engine in the `default-caveman` pipeline

Once that prefix appears in the model's own context window, the model learns to **mimic it**. When asked "give me a summary", it writes `[COMPRESSED:summary]<paraphrase>` and stops. This is a **learned degenerate behavior** in a long-lived session, NOT a live compression event.

## How to verify

```sql
-- In the affected profile's state.db (NOT the root /Users/pftg/.hermes/state.db):
SELECT id, role, substr(content, 1, 200), _compressed_summary, compacted
FROM messages
WHERE session_id = '<session-id-of-telegram-chat>'
ORDER BY timestamp DESC LIMIT 10;
```

If the latest assistant messages all start with `[COMPRESSED:…]` AND `_compressed_summary=0` AND `compacted=0`, the model is mimicking, not being compressed.

Also check `compression_fallback_streak` and `compression_overload_streak` on the session row — both should be 0 if the engine is not firing.

## Fix (in order)

1. **Archive the bad session** to force a fresh start on next inbound message:
   ```sql
   -- Edit the profile's state.db (e.g. kanban-orchestrator).
   -- Backup first: cp state.db state.db.bak-reset-<date>
   UPDATE sessions
   SET title = '[archived <date>] telegram-dm <chat_id> - reset',
       ended_at = strftime('%s','now'),
       end_reason = 'compressed_marker_learned_degenerate',
       archived = 1, hidden = 1, auto_archived = 1,
       last_activity_at = strftime('%s','now')
   WHERE id = '<session-id>';
   ```

2. **Prevent recurrence** with both layers:
   - **omniroute gateway**: edit `~/.omniroute/storage.sqlite` `compression_combos.pipeline` for `default-caveman` → `[{"engine":"rtk","intensity":"standard"}]` (drop caveman/aggressive/ultra/omniglyph). Verify the boot migration in `src_0dznf9w._.js` won't re-write it.
   - **Profile config**: in `~/.hermes/profiles/<profile>/config.yaml` set `compression.enabled: false`. All five worker profiles (delivery-manager, kanban-orchestrator, quality-guardian, researcher, stuck-guardian) had identical compression blocks.

## Why prior layers of fix don't help

- `runtime/active_sessions.json` is empty when the gateway is idle — no in-memory cache to invalidate.
- `hermes sessions archive` from the CLI only sees the root `~/.hermes/state.db`; the active Telegram session for chat_id 445093405 lives in the **profile**'s state.db (`~/.hermes/profiles/kanban-orchestrator/state.db`), which the CLI cannot reach.
- The profile's state.db is read fresh per message by the gateway. SQLite update on the row is sufficient — no gateway restart needed.

## Verification

Send any Telegram message after archiving. gateway.log should show a new `session=agent:kanban-orchestrator:telegram:dm:<chat_id>` and the reply should NOT start with `[COMPRESSED:`. If it does, check hooks/ and config.yaml `prompts:`/`message_handlers:` sections for hidden instruction sources.

## Don't confuse with

- Real compression-engine output: that has `_compressed_summary=1` in the messages row.
- Real omniroute 503 cascade (different symptom — `ALL_TARGETS_SKIPPED` in error logs, not `[COMPRESSED:` markers in replies).
