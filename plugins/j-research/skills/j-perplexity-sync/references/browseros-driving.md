# Driving BrowserOS neo from scripts (verified 2026-09-17)

Companion detail for `j-perplexity-sync`'s acquire step. When its MCP tools are not exposed as
native tools, drive the browseros-neo MCP server (`http://127.0.0.1:9010/mcp`, streamable HTTP)
over JSON-RPC with a persistent session. Hard-won quirks, each cost a failed run:

- **App first, server second.** Port 9010 answers `406` on plain GET when the MCP server is
  up; `000` means the app is not running. Launch with `open -a "BrowserOS neo"`, wait,
  then re-probe. The MCP endpoint URL lives in `~/.claude.json` under `mcpServers.browseros-neo`.
- **One persistent MCP session for the whole run.** Each new `initialize` gets its own
  `mcp-session-id`, and pages opened in one session are **not owned by the next** — a later
  script sees `page N is not owned by this agent`. Keep one HTTP session and reuse it.
- **SSE responses are an event stream.** Parse every `data:` line and take the last event
  carrying `result`/`error`; the first line is a comment-like keepalive (`data: ` empty).
- **`evaluate` takes `func`, not `code` or `expression`.** The value is the function's return
  value. An IIFE passed as `code` returns `undefined`. Async work is fine: return a promise.
  Valid fields: `page`, `code`, `func`, `timeout`, `maxChars`.
- **Never `JSON.stringify` React fiber objects** — circular refs throw. To extract data from
  library rows, walk `__reactFiber$` parents and probe shallow string props (`row`, `href`,
  `to`, `threadId`) plus a depth-capped `props.children` walk.
- **Library anchors are React portals: `a[href]` matches exist but are NOT inside `main`,**
  so `row.querySelectorAll('a[href*=…]')` finds nothing. Collect anchors document-wide and
  dedupe by uuid; the hub's watermark makes the extra ids harmless. Regex over hrefs beats
  fiber walking anyway — 29 hrefs with uuids, zero fiber-based hits.
- **`read` has no `maxChars`; valid fields are `page`, `format`, `selector`, …** Pages over
  the tool's cap are saved to `~/.browseros/tool-output/read-*.md` (path in the response);
  smaller ones come back inline.
- **Cold browser needs ~9s per thread page, not 5.5s.** A shorter sleep returns a ~164-char
  shell; retry once after a longer sleep before marking `skipped`.
- **`UNTRUSTED_PAGE_CONTENT` wrappers must be stripped line-wise, never with a
  `.*?` span regex.** The opening marker is the response's first line and the closing one the
  last, so a span-regex with `re.S` deletes the entire body (a sync silently produced 13
  empty captures this way). Drop the two marker lines, keep everything between.
- **`tabs` valid fields include `action`, `url`, `page`; `wait` takes `page`, `for`, `value`,
  `timeout` (`for: "selector"`).** Name the session first (`name_session`) so the run groups
  under a searchable label in the cockpit.
