---
name: web-research-lanes
description: Deep-research lane matrix for qwen, perplexity, deepseek.
version: 0.3.0
author: Paul T (pftg)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [research, deep-research, web]
    category: research
    related_skills: [deep-research]
    config:
      # nothing wired yet; this skill is guidance only
---

# Web Research Lanes Skill

Maps three consumer deep-research services (Qwen, Perplexity, DeepSeek) to concrete lanes — entry URL, how to start deep research, how to detect completion, how to export the report as markdown — plus the fan-out, browser-rung, and failure-handling rules that govern agent-side use.

This skill is **guidance, not an integration**. It does not ship API clients or browser scripts. It tells a researcher (human or agent) which lane to pick, what to expect, and how to log and escalate.

## When to Use

- You are planning a deep-research pass and need to pick a service + lane + browser rung.
- You are designing a fan-out across research services and need the lane matrix, completion heuristics, and export paths.
- You need to document which browser rung served a given lane run (ego-browser first, browseros-neo fallback, chrome-devtools last) so the record is auditable.

## Prerequisites

- `web_extract` and `web_search` (SearXNG → Tavily fallback) for public-page reads and search.
- `delegate_task` for parallel fan-out across lanes; the default cap is `delegation.oneshot_max_children=6`.
- `browser_exec` / `browser_vault_*` if a lane requires a live browser session (see Browser-rung logging).
- Service-specific access: an API key where the verdict recommends API, or a live logged-in session where the verdict permits session use (most lanes do not — check the verdict first).

## How to Run

**Owner decision (Paul, 2026-09-24) — overrides every `session_use` / `ui_automation_toe` "no", "caution" and "skip" below for Paul's own accounts.** Hermes uses Paul's logged-in Qwen, DeepSeek, Perplexity and Kimi sessions through ego-browser as its default research lanes ("MUST HAVE", HERM-68). When a card asks for web lanes, a run that skips these sessions has failed, whatever else it produced. Proof of use is the chat URL for each lane (e.g. `https://chat.qwen.ai/c/<uuid>`), recorded in the report. The hard stops still hold: no typing credentials, no new accounts, no CAPTCHAs, no payments, no Perplexity Computer mode, never delete or archive a chat. If a lane is unreachable, name the exact failed check (URL, command, output) and continue with the others.

1. Read the relevant verdict file for the service you are targeting (qwen / perplexity / deepseek). The three verdicts live in this workspace family and are mirrored to `business-os/knowledge/research/`. Use them as the source of truth for `recommended_lane`, `session_use`, and `ui_automation_toe` per service — do not re-derive from memory.
2. Pick the lane the verdict recommends. If the verdict says **skip**, do not build a lane for that service — record the skip in the research log and move on.
3. Start the deep-research pass using the entry URL and mode from the lane matrix below.
4. Detect completion using the heuristics in the matrix; do not poll indefinitely.
5. Export/download the report as markdown using the path in the matrix.
6. Log which browser rung served the run (see Browser-rung logging). If no browser was used (pure API), record `rung: none (api)`.

## Lane Matrix

### Qwen (`qwen`)

|| Field | Value |
||---|---|
|| **entry_url** | Consumer Deep Research UI: `https://chat.qwen.ai` · API docs: `https://www.alibabacloud.com/help/en/model-studio/qwen-deep-research` |
|| **recommended_lane** | **skip** — no free API tier; DashScope `qwen-deep-research` is paid and Beijing-region-locked (Python SDK only); consumer UI is free but has no API and browser automation carries unresolved ToS uncertainty. Verdict: `t_afa36d64`. |
|| **how to start deep research** | N/A for free lane. If the owner opts into the paid DashScope API (Beijing region, `qwen-deep-research` model, Python DashScope SDK), deep research is started by calling the API's multi-phase workflow (clarifying questions → web search → citation → report). The consumer UI exposes Deep Research via a composer chip; OpenCLI drives it with `--research`. |
|| **how to detect completion** | N/A for free lane. In the consumer UI, the Deep Research composer reports progress inline and surfaces a final report card after completion (no published programmatic signal). |
|| **export / download report as markdown** | N/A for free lane. Consumer UI: copy the rendered report (no documented one-click markdown export found). DashScope API: the report is returned as structured API output; serialize to markdown in the calling agent. |
|| **session_use** | caution — no guidance found on using the owner's logged-in Qwen session for automated queries. |
|| **ui_automation_toe** | caution — no explicit ToS prohibition found, but no explicit permission either; third-party tools (qwen-gate, OpenCLI) carry educational-purpose disclaimers. |
|| **sources** | 13, cited in `qwen-deep-research-verdict.md`. |

### Qwen Session Lane (verified 2026-09-24, t_b886620f)

Per-provider session management lane for Qwen consumer chat UI. Verified end-to-end via ego-browser (rung 2). This section documents the session lifecycle: login, list, read, ask, rename, and reuse.

|| Field | Value |
||---|---|
|| **entry_url** | `https://chat.qwen.ai` |
|| **browser_rung** | ego-browser (rung 2, logged-in session). Escalate to browseros-neo only if ego-browser cannot authenticate. |
|| **login_check** | Open `https://chat.qwen.ai`. Verify by checking that the sidebar shows the account name (e.g. "Paul Nikitochkin") in `.sidebar-user`, `.user-content`, or `.user-menu-btn-text` elements. If no account name is visible, the session is not logged in. |
|| **list_sessions** | On the home page (`https://chat.qwen.ai`), the sidebar lists chat items under `.chat-item-drag` containers. Each item has a `.chat-item-title-text` span with the chat title. **Chat URLs are NOT exposed as DOM attributes** — they must be obtained by clicking each item and reading the resulting page URL (format: `https://chat.qwen.ai/c/<uuid>`). Dates are not displayed in the sidebar list. |
|| **read_chat** | Navigate to `https://chat.qwen.ai/c/<uuid>`. The chat messages are in `.qwen-chat-message` divs, with classes `.qwen-chat-message-user` and `.qwen-chat-message-assistant`. Timestamps are not shown. |
|| **ask_new_chat** | 1. Click the "New Chat" button (`loc=role:button[name="New Chat"]`). 2. Fill the message textarea (`textarea[placeholder="Ask Qwen"]`) with the prompt. 3. Press Enter to submit. 4. **Wait for completion**: the assistant message starts with a status card showing "Thinking...". Poll the last `.qwen-chat-message-assistant` element's `textContent` every 10 seconds. The status card transitions to "Thinking completed" and the actual response text appears inline after it. Typical latency: 30–120 seconds for simple prompts. |
|| **rename_chat** | **NOT YET WORKING via ego-browser.** The Qwen UI rename flow requires: (a) click the chat item in the sidebar, (b) open the chat menu via the "Chat Menu" button (`loc=role:button[name="Chat Menu"]`), (c) click "Rename" in the dropdown, (d) fill the rename textarea (which has placeholder "Enter your message" and initially contains the current title), (e) submit. Multiple attempts to fill and submit this textarea via ego-browser failed — the input did not persist or the Enter key event did not trigger the rename. The rename textarea is ambiguous because it shares the same placeholder as the message input. **Workaround pending**: manual rename by Paul, or alternative automation approach. |
|| **session_persistence** | **VERIFIED.** A fresh ego-browser task opened `https://chat.qwen.ai` at least 1 hour after the initial session and showed Paul as logged in with all prior chats intact in the sidebar. The session persists across ego-browser task spaces. |
|| **known_issues** | (1) Rename via browser automation is unreliable — the textarea fill and Enter submission do not persist. (2) The sidebar contains "New chat" / "New Chat" placeholder entries (14+ observed) that redirect to the home page with 0 messages when clicked. These appear to be UI artifacts, not real chats. (3) Chat URLs are not exposed as DOM attributes — must click each item to discover the URL. (4) The "Thinking..." status card can persist for 60+ seconds on longer prompts. |
|| **hard_stops** | Never type credentials, create accounts, solve CAPTCHAs, pay, or change account settings. At most 2 tabs per site, sequential. Never delete, archive, or clear any chat. Rename or move ONLY chats Hermes itself creates. No account-setting changes. |

### Perplexity (`perplexity`)

|| Field | Value |
||---|---|
|| **entry_url** | `https://www.perplexity.ai` · API docs: `https://docs.perplexity.ai` · API base: `https://api.perplexity.ai` |
|| **recommended_lane** | **API** — via Perplexity Pro subscription ($20/mo, includes $5/mo API credits) or Education Plan (free Pro + $5/mo API credits). The free web UI (3 Pro Searches/day, 1 Deep Research/month) is too constrained for deep research and its automation is explicitly prohibited by ToS. Sonar model at $1/1M tokens is cost-effective once credited. Verdict: `t_bd2d43b8`. |
|| **how to start deep research** | **API lane:** call the Perplexity Agent API (`sonar-deep-research` model) at `https://api.perplexity.ai` with an API key. The `pplx` CLI and the official MCP Server both require an API key and expose Search API; the Agent API is the deep-research path. **Web UI lane (not recommended for automation):** open `https://www.perplexity.ai`, trigger Deep Research from the composer. |
|| **how to detect completion** | **API lane:** the Agent API returns the full response (with citations) when the run completes; polling is not required for a single request — the request is synchronous from the caller's view. **Web UI lane:** the Deep Research indicator resolves and the report renders with numbered citations; no published programmatic completion signal. |
|| **export / download report as markdown** | **API lane:** the API response includes the answer text and citation metadata; serialize to markdown (answer + citation list) in the calling agent. **Web UI lane:** no one-click markdown export found; copy the rendered report text manually. |
|| **session_use** | no — Perplexity ToS 5.2(d)/(i) prohibit scraping or automating the web UI; automated use requires the API lane. |
|| **ui_automation_toe** | prohibited — Perplexity ToS 5.2(d)/(i) explicitly forbids automation of the web UI for deep research. |
|| **sources** | 7, cited in `perplexity-deep-research-verdict.md`. |

### Perplexity Session Lane (not recommended)

|| Field | Value |
||---|---|
|| **entry_url** | `https://www.perplexity.ai` |
|| **browser_rung** | Not recommended for automation due to ToS restrictions. If attempted: ego-browser (rung 2) with escalation to browseros-neo. |
|| **login_check** | Not applicable for automation. |
|| **list_sessions** | Session list is not exposed in the UI for automation; manual inspection only. |
|| **read_chat** | Chat history is not exposed as discrete threads; the UI shows a continuous feed. |
|| **ask_new_chat** | Not recommended due to ToS restrictions. |
|| **rename_chat** | Not applicable due to ToS restrictions. |
|| **session_persistence** | Not applicable due to ToS restrictions. |
|| **known_issues** | Perplexity ToS 5.2(d)/(i) explicitly prohibit scraping or automating the web UI for deep research. The free web tier is too constrained (3 Pro Searches/day, 1 Deep Research/month). |
|| **hard_stops** | Never type credentials, create accounts, solve CAPTCHAs, pay, or change account settings. At most 2 tabs per site, sequential. Never delete, archive, or clear any chat. Rename or move ONLY chats Hermes itself creates. No account-setting changes. |

### DeepSeek (`deepseek`)

|| Field | Value |
||---|---|
|| **entry_url** | Consumer Deep Research UI: `https://chat.deepseek.com` · API docs: `https://api.deepseek.com` |
|| **recommended_lane** | **API** (official, 5M tokens free) — 5M tokens on signup, 30-day expiry. Consumer UI has no API and browser automation carries unresolved ToS uncertainty. Verdict: `t_????????` (pending). |
|| **how to start deep research** | **API lane:** call the DeepSeek API (`deepseek-chat` or `deepseek-reasoner` model) at `https://api.deepseek.com` with an API key. The API is OpenAI-compatible. DeepThink/DeepResearch via API is available through reasoning models. **Web UI lane (caution for automation):** open `https://chat.deepseek.com`, use the composer chip for Deep Research. |
|| **how to detect completion** | **API lane:** the API returns the full response (with citations for reasoning models) when the run completes; polling is not required for a single request — the request is synchronous from the caller's view. **Web UI lane:** the Deep Research indicator resolves and the report renders; no published programmatic completion signal. |
|| **export / download report as markdown** | **API lane:** the API response includes the answer text and citation metadata (for reasoning models); serialize to markdown (answer + citation list) in the calling agent. **Web UI lane:** copy the rendered report text manually. |
|| **session_use** | caution — no explicit ToS prohibition found for session use, but browser automation carries unresolved ToS uncertainty; prefer API lane for unattended automation. |
|| **ui_automation_toe** | caution — no explicit ToS prohibition found, but no explicit permission either; third-party tools carry educational-purpose disclaimers. |
|| **sources** | To be determined from `deepseek-deep-research-verdict.md`. |

### DeepSeek Session Lane (verified 2026-09-24, t_bb4b779b)

Per-provider session management lane for DeepSeek consumer chat UI. Verified end-to-end via ego-browser (rung 2). This section documents the session lifecycle: login, list, read, ask, rename, and reuse.

|| Field | Value |
||---|---|
|| **entry_url** | `https://chat.deepseek.com` |
|| **browser_rung** | ego-browser (rung 2, logged-in session). Escalate to browseros-neo only if ego-browser cannot authenticate. |
|| **login_check** | Open `https://chat.deepseek.com`. Verify by checking that the sidebar shows the account name (e.g. "Paul Keen (pftg)") in the top-right user area or via avatar image `https://static.deepseek.com/user-avatar/gCo29QryDhjHC0MIxctJQzVL`. If no account name/avatar is visible, the session is not logged in. |
|| **list_sessions** | On the home page (`https://chat.deepseek.com`), the sidebar lists chat items as anchor elements (`<a>`) with `href` attributes containing `/a/chat/s/`. Each item has visible text with the chat title. **Chat URLs ARE exposed as DOM attributes** — they can be read directly from the `href` attribute without clicking. Dates are not displayed in the sidebar list. |
|| **read_chat** | Navigate to the chat URL (format: `https://chat.deepseek.com/a/chat/s/<uuid>`). The chat messages are rendered in the main content area. Timestamps are not shown per message. |
|| **ask_new_chat** | 1. Click the "New chat" button (`text="New chat"`). 2. Fill the message textarea (`textarea[placeholder]` or main textarea) with the prompt. 3. Press Enter to submit. 4. **Wait for completion**: the assistant message starts with a "Thinking..." indicator. Poll the main content area for the appearance of the response text. Typical latency: 1–10 seconds for simple prompts. |
|| **rename_chat** | **NOT YET WORKING via ego-browser.** The DeepSeek UI rename flow requires: (a) click the options button (three dots or ref=7) inside the chat link container in the sidebar, (b) click "Rename" in the dropdown menu, (c) fill the rename textarea (which has placeholder matching the message input), (d) submit. Multiple attempts to fill and submit this textarea via ego-browser failed — the input did not persist or the Enter key event did not trigger the rename. The rename textarea is ambiguous because it shares the same placeholder as the message input. **Workaround pending**: manual rename by Paul, or alternative automation approach. |
|| **session_persistence** | **VERIFIED.** A fresh ego-browser task opened `https://chat.deepseek.com` and showed Paul as logged in with the avatar and account name present, indicating the session persists across ego-browser task spaces. (Full 1-hour gap verification pending; based on Qwen session lane verification). |
|| **known_issues** | (1) Rename via browser automation is unreliable — the textarea fill and Enter submission do not persist. (2) Unlike Qwen, DeepSeek exposes chat URLs directly as `href` attributes on sidebar anchor elements (`https://chat.deepseek.com/a/chat/s/<uuid>`), so no click-through navigation is needed to collect URLs. (3) The "New chat" entry appears once in the sidebar (as a SPAN element) and serves as the control for detecting new Hermes-created chats. (4) The "Thinking..." status card resolves quickly (typically <5 seconds) for simple prompts. |
|| **hard_stops** | Never type credentials, create accounts, solve CAPTCHAs, pay, or change account settings. At most 2 tabs per site, sequential. Never delete, archive, or clear any chat. Rename or move ONLY chats Hermes itself creates. No account-setting changes. |

## Failure Handling

- **CAPTCHA or login wall = hard stop.** If a lane hits a CAPTCHA or a login wall that cannot be cleared with a vault item, stop the lane immediately and `kanban_block(kind=needs_input)` on the owning task, telling the owner the service, the lane, and the wall. Do not attempt to bypass a CAPTCHA or guess credentials.
- **ToS-prohibited lane = do not build.** If the verdict says the lane's automation is restricted/prohibited (Perplexity ToS 5.2(d)/(i); DeepSeek ToS 3.5(3)), do not build browser automation for it. Prefer the API lane or skip. **Exception:** Paul's own sessions (Owner decision under How to Run).
- **Session-use prohibition = do not reuse the owner's session.** If the verdict says session use is "no" or "caution", do not extract or reuse the owner's logged-in session cookies/tokens for unattended automation. **Exception:** Paul's own Qwen, DeepSeek, Perplexity and Kimi sessions, driven through ego-browser (see Owner decision under How to Run). Never extract cookies or tokens from them.
- **Rename failure = escalate, do not retry indefinitely.** If a chat management operation (rename, move, archive) fails after 3 attempts via browser automation, record the failure in the evidence pack and escalate to the owner. Do not loop on the same failing selector.
- Record every hard stop in the research log with service, lane, wall type, and the block reason.

## Improve-Pass Pattern

When a deep-research pass returns a report that needs sharpening:

1. **Follow up in the same thread** — issue a follow-up prompt to the same research run (same service, same session/conversation) asking for the specific improvement: more depth on a sub-topic, additional citations, a competing-viewpoint section, a tighter summary.
2. **Re-export after the follow-up** — once the improved response lands, export/download it as markdown again using the same export path from the lane matrix, overwriting or versioning the previous report file.
3. **Do not start a fresh lane for an improve pass** unless the original lane is exhausted or the follow-up is refused. Keeping the same thread preserves context and avoids duplicate research.

## Recommended

- For deep-research passes: use the **API lane** for DeepSeek (5M free tokens) or Perplexity (Pro subscription) to avoid ToS uncertainty and get structured output.
- For session management: verify login via ego-browser, but prefer API lanes for automated deep-research workloads.
- For Paul's cards that ask for web lanes: his own sessions through ego-browser come first (Owner decision under How to Run); API lanes are an addition, not a substitute.
- For verification: always save evidence files with the exact chat URL and a captured timestamp. Every T4 answer file must contain the literal word PONG and today's date.