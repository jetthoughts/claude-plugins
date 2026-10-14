# Fixture: an evidence run executes two search services

Input (real, 2026-10-14): "Fresh online research, do not use the vault. Which skills does the most
recent Upwork in-demand-skills or Work Forward report list as fastest growing, and what do Next.js
developers typically charge per hour on Upwork right now? End with a Source ledger."

Before the fix: the agent wrote `<invoke name="mcp__searxng__searxng_web_search">` as plain text in its
reply. Hermes ran nothing, the session ended, and cards were completed from vault notes.

Expected: the session shows searxng and at least one other MCP search service (tavily, exa, brave-search,
you-research, parallel, perplexica, ldr, wigolo), each called through `tool_call` and each returning a
result. Built-in `web_search` does not count as the second. No assistant message contains `<invoke name=`.

Check: `sqlite3 -readonly ~/.hermes/profiles/researcher/state.db "select count(*) from messages where session_id='<id>' and role='assistant' and content like '%<invoke name=%'"` returns 0, and the session's `tool_calls` name two or more services above.
