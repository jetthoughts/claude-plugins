# Search & Research Tools Inventory

Complete inventory of available MCP tools and services for web search and research.

> **Canonical copy.** This is the canonical search/research tool inventory and it is read at
> runtime by the `j-research` skill (front door). The OKF bundle concept at
> [`../../../.okf/RESEARCH_TOOLS.md`](../../../.okf/RESEARCH_TOOLS.md) is a governed **pointer** to
> this file, not a second copy — do not re-expand it. When the tool stack changes, edit this file and
> refresh the bundle's `verified:` date.

## Quick Reference

| Tool | MCP Server | Speed | Cost | Best For |
|---|---|---|---|---|
| LDR | ldr | Slow (150-500s) | Free | Local, academic sources |
| Wigolo | wigolo | Fast (<15s) | Free | Local-first, caching |
| Exa | exa | Fast (<10s) | Paid tier | Semantic search, high recall |
| Tavily | tavily | Fast (<30s) | Paid tier | Comprehensive, crawling |
| You.com | you-com | Fast (<1min) | Paid | Current events, knowledge |
| Perplexica | perplexica | Medium (30-120s) | Free | Academic + forums |
| Brave | brave-search-mcp | Fast (<5s) | Paid tier | Privacy-first, quality |
| OmniRoute | omniroute | Very fast (~8s) | Free tier | Manual routing, fast synthesis |
| NotebookLM | notebooklm-mcp | Medium (30-180s) | Free | Corpus-grounded questions, studio artifacts |
| j-inbox | Skill | Fast (batch) | Free | Research import processing |

## Consumer Deep Research Services

| Service | Recommended Lane | Cost | Best For |
|---|---|---|---|
| Qwen | Session lane (via consumer-lanes reference card) | Free | Owner's logged-in session, web automation |
| Kimi | Session lane | Free | Chinese AI, session persistence |
| Perplexity | API lane (Pro) | $20/mo | High-quality research with citations |
| DeepSeek | API lane (5M free) | Free tier | OpenAI-compatible, reasoning models |

## Detailed Tool Descriptions

### LDR (Local Deep Research)

**MCP Server:** `ldr`

**Tools:**
- `quick_research` - Fast research summary (1-5 min), web search + analysis + synthesis
- `detailed_research` - Comprehensive analysis (5-15 min), structured findings + metadata
- `generate_report` - Full markdown report (10-30 min), comprehensive sections + citations
- `analyze_documents` - RAG search on local document collections
- `search` - One-shot specialist pull (seconds), no LLM synthesis

**Specialist Engines (for `search` only):**
- `searxng` - General web search
- `arxiv` - Preprint papers (HTTP 406 errors; use openalex instead)
- `openalex` - Academic/ML papers with citations, DOI, OA link (also indexes arXiv)
- `wikipedia` - General knowledge (can be throttled 429)
- `pubmed` - Biomedical literature with study type filtering
- `stackexchange` - Code errors, how-to with accepted answers
- `semantic_scholar` - Academic papers (returns 429 without API key)

**Parameters:**
- `query` (required)
- `search_engine` - For specialist engines
- `strategy` - Research strategy (source-based, rapid, iterative, etc.)
- `iterations` - Number of search iterations (1-10)
- `questions_per_iteration` - Questions per iteration (1-5)

**Use when:**
- Work must stay local (no API keys, no external services)
- Need specialist academic/biomedical sources
- Question is well within 4B model's synthesis ability
- Budget 200-500s per query is acceptable

**Not for:**
- Quick single-fact lookups
- Speed-critical queries
- When stronger synthesis is needed

---

### Wigolo (Local-first Web Intelligence)

**MCP Server:** `wigolo`

**Tools:**
- `search` - Web search with ML reranking, cache, audit trails
- `fetch` - Single URL fetch with clean markdown, JS rendering, auth support
- `research` - Multi-step research with structured briefs, gap analysis
- `find_similar` - Semantic discovery via embeddings + keyword + live web
- `crawl` - Multi-page crawl with sitemap/BFS/DFS strategies
- `extract` - Structured data extraction (tables, JSON-LD, metadata)
- `diff` - Compare page versions, change detection
- `cache` - Search local cache, check for changes
- `watch` - Monitor pages for changes over time

**Key Parameters:**
- `query` - String or array of query variants
- `search_depth` - ultra-fast (cache-only), fast, balanced (default), deep
- `category` - general, news, code, docs, papers, images
- `include_domains`/`exclude_domains` - Scope results
- `time_range` - day, week, month, year
- `format` - answer, stream_answer (with LLM synthesis)
- `force_refresh` - Bypass cache for fresh content

**Features:**
- Local-first with persistent cache (cache hits <1s)
- Transparent audit trails with engine telemetry
- ML reranking with explainable evidence scoring
- Multi-query support with deduplication
- Site-specific extractors (Reddit, YouTube, Amazon)

**Use when:**
- Local-first search with caching across sessions
- Transparent audit trails and explainable scoring
- Need research workflow with structured briefs
- Question decomposition and parallel search
- Scoping to specific domains or time ranges

---

### Exa AI

**MCP Server:** `exa`

**Tools:**
- `web_search_exa` - Semantic search with embedding-based index
- `web_fetch_exa` - Clean markdown extraction from URLs

**Key Parameters:**
- `query` (required) - Natural language description of ideal page
- `objective` (required) - Goal for search, which documents should rank first
- `numResults` - Number of results (default 10)
- `category:people` / `category:company` - Focused searches

**Features:**
- Embedding-based index with 20x better recall claimed
- Matches intent rather than keyword overlap
- Best for complex, multi-hop queries
- Clean content extraction

**Use when:**
- Semantic search with high recall needed
- Complex multi-hop queries where intent matching matters
- Clean content extraction from web pages
- Question benefits from embedding-based vs keyword search

**Cost:** Free tier with daily quota, paid per call beyond

---

### Tavily

**MCP Server:** `tavily`

**Tools:**
- `tavily_search` - Web search with multiple depth levels
- `tavily_extract` - Content extraction from URLs
- `tavily_crawl` - Website crawling with depth/breadth control
- `tavily_map` - URL discovery without content extraction

**Key Parameters:**
- `query` (required)
- `search_depth` - basic, advanced, fast, ultra-fast
- `topic` - general (default)
- `time_range` - day, week, month, year
- `include_raw_content` - Full page content
- `include_domains`/`exclude_domains` - Scope results
- `max_results` - 5-20 (default 5)

**Features:**
- Multiple depth levels for thoroughness vs speed
- Content extraction with markdown/text formats
- Site crawling with configurable depth/breadth
- Advanced extraction for LinkedIn, protected sites, tables
- Exact match support for quoted phrases

**Use when:**
- Comprehensive search with multiple depth levels
- Content extraction from multiple URLs
- Site crawling and documentation extraction
- Need control over search parameters (domains, time ranges, exact match)
- Structured content extraction

**Cost:** Free tier available, paid per call beyond quota. Advanced search uses 2 credits per request.

---

### You.com

**MCP Server:** `you-com`

**Tools:**
- `you-search` - Web search with licensed knowledge results

**Key Parameters:**
- `query` (required) - Short natural-language phrase
- `count` - Max results per section (default 30, max 100)
- `freshness` - day, week, month, year, or date range
- `extraction` - highlights (default), none, full_page
- `knowledge` - core (includes licensed knowledge results)
- `exclude_domains` - Up to 500 domains to exclude

**Features:**
- Licensed knowledge results alongside web/news
- Inline filters work automatically (site:, lang:, loc:)
- Full-page extraction with cache/fetch/blend options
- Current events and facts about people/companies
- Verification of claims

**Use when:**
- Current events, news, recent facts
- Facts about people, companies, organizations
- Finding primary sources and verifying claims
- Need licensed knowledge results
- Recency matters (freshness parameter)

**Cost:** Paid per call, requires `YDC_API_KEY`

---

### Perplexica

**MCP Server:** `perplexica`

**Tools:**
- `search` - AI-powered search with multiple source types

**Key Parameters:**
- `query` (required)
- `sources` - Array: web, academic, discussions (can combine)
- `chat_model` - Model configuration (default: LM Studio gemma-4-e4b)
- `embedding_model` - Embedding model (default: MiniLM-L6-v2)
- `optimization_mode` - speed, balanced, quality
- `history` - Conversation history for context
- `system_instructions` - Custom system prompts

**Features:**
- Multiple source types in one query
- Academic search (scholarly articles)
- Discussion search (forums like Reddit)
- Local models by default
- Configurable optimization modes

**Use when:**
- Need academic sources combined with web search
- Forum discussions (Reddit) for user sentiment
- Want to combine multiple source types
- Local model execution preferred
- Configurable optimization for speed vs quality

**Cost:** Free, runs on local LM Studio residency

---

### Brave Search

**MCP Server:** Requires setup (brave-search-mcp, @mrfentmen/brave-mcp)

**Tools:**
- Web search via MCP server (varies by implementation)

**Features:**
- Independent, privacy-first search index
- Built without relying on Google or Bing
- World-class quality (on par with or better than incumbents in blinded testing)
- Comprehensive coverage: web, news, images, videos
- Real-time freshness with daily index updates
- Unbiased, high-quality results

**Use when:**
- Need independent, privacy-first search
- Want unbiased results without Google/Bing reliance
- World-class quality search results
- Comprehensive coverage across content types
- RAG and AI agent grounding

**Cost:** Free tier available, paid per call beyond quota. Requires `BRAVE_API_KEY`.

**Setup:** Install MCP server (e.g., `npm install -g brave-search-mcp` or `@mrfentmen/brave-mcp`)

---

### OmniRoute

**MCP Server:** `omniroute`

**Tools:**
- `omniroute_web_search` - Web search through routed models
- `omniroute_route_request` - Model routing and synthesis

**Key Parameters:**
- `model` - Provider-prefixed (gemini/gemini-3.1-flash-lite, cc/claude-opus-5)
- `role` - analysis for synthesis
- Combo-based routing with quota management

**Features:**
- Very fast (~8s total for evidence + synthesis)
- Model routing through combos
- Manual process (you write queries, paste evidence)
- Free with free-tier models
- Premium lanes available

**Use when:**
- Need maximum speed
- LDR's local model loses the thread
- Stronger routed model worth the cost
- Manual control over search queries acceptable
- Loop needs to be fast

**Cost:** Free with free-tier models, varies by combo. Check `omniroute_check_quota` before promising.

**Note:** Manual, not autonomous — you write search queries and paste evidence into synthesis yourself.

---

### NotebookLM MCP

**MCP Server:** `notebooklm-mcp`

**Tools:**
- `refresh_auth` - Reload auth tokens or run headless re-authentication
- `save_auth_tokens` - Save NotebookLM cookies (fallback method)
- `batch` - Batch operations across multiple notebooks (query, add_source, create, delete, studio)
- `notebook_query` - Ask AI about existing sources in notebook (NOT for finding new sources)
- `notebook_query_start` - Start notebook query asynchronously for source-heavy notebooks
- `notebook_query_status` - Poll status of async notebook query
- `research_start` - Start deep research with web search (find new sources, Drive search)
- `research_status` - Poll status of async deep research
- `source_add` - Add source URL to notebook
- `source_list` - List sources in notebook
- `source_list_notebooks` - List all notebooks
- `label` - Manage source labels (auto, list, reorganize, create, rename, move_source, delete)
- `studio_create` - Create studio artifact (audio, video, report, infographic, slides)
- `studio_status` - Poll studio artifact generation status
- `download_artifact` - Download completed studio artifact
- `download_all_artifacts` - Download all completed artifacts for a notebook
- `note` - Manage notes in notebooks (create, list, update, delete)
- `chat_configure` - Configure notebook chat settings

**Key Parameters:**
- `notebook_id` - Notebook UUID (required for most operations)
- `query` - Question to ask (for notebook_query, research_start)
- `source_url` - URL to add as source
- `timeout` - Wall-clock query budget in seconds (default: 120s, source-heavy may need 180+)
- `conversation_id` - For follow-up questions
- `artifact_type` - audio, video, report, infographic, slides (for studio_create)

**Features:**
- Corpus-grounded questions on existing sources
- Deep research with web search and Drive integration
- Async operations for long-running tasks
- Studio artifact generation (audio, video, reports)
- Source management and labeling
- Batch operations across multiple notebooks
- Chat configuration (goal, response length, custom prompts)

**Use when:**
- Question about sources already loaded into a NotebookLM notebook
- Need deep research with web search on a corpus
- Generating studio artifacts (audio summaries, video explainers)
- Managing NotebookLM notebooks programmatically
- Batch operations across multiple notebooks
- Research import processing via j-inbox

**Not for:**
- Finding new sources (use research_start for that)
- General web search without corpus context (use Wigolo, Exa, etc.)

**Cost:** Free (requires Google account, NotebookLM service)

**Setup:** Run `nlm login` for automated authentication, or use `save_auth_tokens` as fallback

---

### j-inbox (Research Import Processing)

**Skill:** `j-inbox`

**Purpose:** Save or publish research to Tolaria vault, and import research exports from various sources

**Supported Sources:**
- Claude data export (conversations.json)
- Perplexity Markdown exports
- Perplexity Markdown exports
- Gemini Markdown exports
- NotebookLM Markdown exports
- Hand-dropped Markdown/txt notes

**Directory Layout (in vault):**
```
research/_inbox/{perplexica,perplexity,claude,gemini,notebooklm,local}/   # drop exports here
research/_inbox/_done/<source>/                                          # processed inputs
research/quarantine/                                                     # failed inputs
research-<source>-<slug>.md                                              # output notes
```

**Commands:**
```bash
python3 scripts/normalize.py ingest [--dry-run] [--vault PATH]
python3 scripts/normalize.py publish --source <s> --title <t> [--url <u>] [--tags a,b] < body.txt
```

**Frontmatter Contract:**
```yaml
type: Research
source: local
source_id: <input frontmatter source_id, or filename/conversation uuid>
date: <ISO date>
url: <if known>
tags: [a, b]
content_hash: <sha256 of the normalized body>
citations_preserved: true|false
imported: <ISO timestamp>
```

**Use when:**
- "Save/publish this research to my vault"
- "Import my Claude/Perplexity/NotebookLM export"
- "Process the research inbox"
- Agent has finished research result to record

**Features:**
- Idempotent processing
- Splits Claude conversations.json into one note per conversation
- Handles Markdown/txt with optional frontmatter
- Quarantines failed inputs with reason files
- Git-tracked vault as canonical source of truth

**Not for:**
- Direct web search (use other research tools)
- Real-time research (this is post-processing)

---

## Consumer Deep Research Services

### consumer-lanes (Consumer AI Research reference card)

**Reference card:** `skills/j-research/references/consumer-lanes.md` (moved out of the skill catalog
when the `web-research-lanes` skill was retired; it is a browser-session manual, not a ladder rung).

**Purpose:** Maps consumer deep-research services (Qwen, Kimi, Perplexity, DeepSeek) to concrete lanes with entry URLs, browser automation procedures, completion detection, and export methods.

**Services Covered:**
- **Qwen** - Session lane via ego-browser (logged-in session), paid DashScope API (Beijing-region locked)
- **Kimi** - Session lane (verified end-to-end, 62+ minute session persistence)
- **Perplexity** - API lane (Pro subscription, $20/mo with $5/mo API credits)
- **DeepSeek** - API lane (5M free tokens, OpenAI-compatible)

**Key Features:**
- Entry URLs for consumer UI and API docs
- Browser rung priority (ego-browser → browseros-neo → chrome-devtools)
- Session management procedures (login check, list sessions, read chat, ask new chat, rename chat)
- Completion detection heuristics
- Export/download as markdown procedures
- ToS considerations and hard stops
- Session persistence verification

**Browser Rung Priority:**
1. **ego-browser** (rung 2) - Default for logged-in sessions
2. **browseros-neo** - Escalate if ego-browser cannot authenticate
3. **chrome-devtools** - Last resort fallback

**Use when:**
- Paul specifically wants a consumer AI service thread (e.g., to capture into evidence/)
- Using owner's logged-in sessions via ego-browser
- Need session-based research with persistence
- Following the consumer-lanes reference card for a specific service

**Not for:**
- General web search (use Wigolo, Exa, etc.)
- API-only research (use direct API calls)
- When consumer service is not appropriate for the task

**Cost:** Free for session lanes (consumer UI), paid for API tiers

**Sources:** Verdict files for each service (qwen-deep-research-verdict.md, perplexity-deep-research-verdict.md, etc.)

---

### Kimi (Session Lane)

**Entry URL:** `https://www.kimi.ai/`

**Recommended Lane:** Session lane (verified 2026-09-24)

**Cost:** Free

**How to Start Deep Research:**
- Open `https://www.kimi.ai/`
- Click "New chat"
- Type prompt, press Enter
- Uses `div.chat-editor-content` contenteditable editor

**How to Detect Completion:**
- Assistant message appears after "Thinking complete" text
- Poll `.chat-detail-main` or `.chat-detail-content` for response text
- Typical latency: <1 second for simple prompts

**Export/Download Report as Markdown:**
- Read chat container's `innerText` and serialize to markdown
- No native export button found

**Session Use:** Yes — verified end-to-end
- Session persists across ego-browser task spaces (62+ minutes verified)
- Paul's session persists with all chats intact

**UI Automation Toe:** No explicit ToS prohibition found
- Session use is the intended path for this provider

**Browser Rung:** ego-browser (rung 2, logged-in session)
- Escalate to browseros-neo only if ego-browser cannot authenticate

**Hard Stops:**
- Never type credentials, create accounts, solve CAPTCHAs, pay, or change account settings
- At most 2 tabs per site, sequential
- Never delete, archive, or clear any chat
- Rename or move ONLY chats Hermes itself creates
- No account-setting changes

**Known Issues:**
- First Enter in fresh tab may open new tab instead of sending
- "More" button must be found by locating chat anchor first
- Chat dates shown as relative text ("Friday") under "This month" grouping

---

### Qwen (Skip)

**Entry URL:** Consumer: `https://chat.qwen.ai` · API: `https://www.alibabacloud.com/help/en/model-studio/qwen-deep-research`

**Recommended Lane:** Skip — no free API tier
- DashScope `qwen-deep-research` is paid and Beijing-region-locked (Python SDK only)
- Consumer UI is free but has no API and browser automation carries unresolved ToS uncertainty

**Cost:** Paid (DashScope API)

**Session Use:** Caution — no guidance found on using logged-in session for automated queries

**UI Automation Toe:** Caution — no explicit ToS prohibition found, but no explicit permission either

**Sources:** 13 sources cited in `qwen-deep-research-verdict.md`

---

### Perplexity (API Lane)

**Entry URL:** `https://www.perplexity.ai` · API: `https://api.perplexity.ai` · Docs: `https://docs.perplexity.ai`

**Recommended Lane:** API (recommended)
- Perplexity Pro subscription ($20/mo, includes $5/mo API credits)
- Education Plan (free Pro + $5/mo API credits)
- Free web UI too constrained (3 Pro Searches/day, 1 Deep Research/month)
- Web UI automation explicitly prohibited by ToS

**Cost:** $20/mo Pro + API credits, or Education Plan

**How to Start Deep Research (API Lane):**
- Call Perplexity Agent API (`sonar-deep-research` model) at `https://api.perplexity.ai`
- Requires API key
- `pplx` CLI and official MCP Server require API key

**How to Detect Completion (API Lane):**
- Agent API returns full response with citations when run completes
- No polling required for single request
- Request is synchronous from caller's view

**Export/Download Report as Markdown (API Lane):**
- API response includes answer text and citation metadata
- Serialize to markdown (answer + citation list) in calling agent

**Session Use:** No — Perplexity ToS 5.2(d)/(i) prohibit scraping or automating web UI
- Automated use requires API lane

**UI Automation Toe:** Prohibited — Perplexity ToS 5.2(d)/(i) explicitly forbids automation of web UI for deep research

**Sources:** 7 sources cited in `perplexity-deep-research-verdict.md`

**Hard Stops:**
- Never type credentials, create accounts, solve CAPTCHAs, pay, or change account settings
- At most 2 tabs per site, sequential
- Never delete, archive, or clear any chat
- Rename or move ONLY chats Hermes itself creates
- No account-setting changes

---

### DeepSeek (API Lane)

**Entry URL:** Consumer: `https://chat.deepseek.com` · API: `https://api.deepseek.com`

**Recommended Lane:** API (official, 5M tokens free)
- 5M tokens on signup, 30-day expiry
- Consumer UI has no API and browser automation carries unresolved ToS uncertainty

**Cost:** Free tier (5M tokens), then paid

**How to Start Deep Research (API Lane):**
- Call DeepSeek API (`deepseek-chat` or `deepseek-reasoner` model) at `https://api.deepseek.com`
- Requires API key
- API is OpenAI-compatible
- DeepThink/DeepResearch available through reasoning models

**How to Detect Completion (API Lane):**
- API returns full response (with citations for reasoning models) when run completes
- No polling required for single request
- Request is synchronous from caller's view

**Export/Download Report as Markdown (API Lane):**
- API response includes answer text and citation metadata
- Serialize to markdown in calling agent

**Session Use:** Consumer UI carries unresolved ToS uncertainty
- API lane recommended for automation

**UI Automation Toe:** Consumer UI automation carries unresolved ToS uncertainty
- API lane recommended for automation

**Sources:** Verdict pending (t_????????)

---

## Tool Selection Guide

### By Speed Requirement

| Speed | Tools |
|---|---|
| Ultra-fast (<5s) | Brave, Wigolo cache, OmniRoute |
| Fast (<15s) | Exa, Tavily basic, Wigolo web |
| Medium (<2min) | Perplexica, Wigolo research, Kimi session |
| Slow (>2min) | LDR |

### By Source Type

| Source Type | Tools |
|---|---|
| Academic papers | LDR (openalex), Perplexica (academic) |
| Biomedical literature | LDR (pubmed) |
| Forum discussions | Perplexica (discussions), agent-reach |
| Current events/news | You.com, Tavily (time_range), Wigolo (category:news) |
| Code/technical | Wigolo (category:code), LDR (stackexchange) |
| Platform-specific content | agent-reach (Twitter/X, Reddit, YouTube, GitHub, LinkedIn) |
| Library documentation | Context7, DeepWiki |
| Local documents | LDR (analyze_documents), NotebookLM MCP |
| Consumer AI research | Kimi (session), Perplexity (API), DeepSeek (API), Qwen (session via the consumer-lanes reference card) |
| Research import processing | j-inbox (Claude/Perplexity/Gemini/NotebookLM exports) |

### By Cost Preference

| Cost | Tools |
|---|---|
| Free (local) | LDR, Perplexica, Wigolo, Kimi (session) |
| Free tier available | Exa, Tavily, Brave, DeepSeek (5M tokens) |
| Paid per call | You.com, Exa (beyond tier), Tavily (beyond tier), Brave (beyond tier), Perplexity (Pro) |

### By Use Case

| Use Case | Recommended Tool |
|---|---|
| Deep multi-source synthesis | LDR detailed_research, Wigolo research |
| Quick fact lookup | Wigolo search, Exa, Tavily basic |
| Academic research | LDR (openalex), Perplexica (academic) |
| Current events | You.com, Tavily (time_range) |
| Content extraction | Tavily extract, Wigolo fetch, Exa fetch |
| Site crawling | Tavily crawl, Wigolo crawl |
| Semantic search | Exa, Wigolo find_similar |
| Local corpus search | LDR analyze_documents, NotebookLM MCP, j-inbox (import processing) |
| Maximum speed | OmniRoute, Brave, Wigolo cache |
| Privacy-first | Brave |
| Manual control | OmniRoute |
| Consumer AI research | Kimi (session), Perplexity (API), DeepSeek (API) |
| Chinese AI research | Kimi (session) |

## Integration with Skills

### Research Skills Reference

- **j-research** (router) - References this inventory for tool selection logic
- **j-deep-research** - References LDR section when local deep research needed
- **j-perplexica-search** - References Perplexica section for academic/forum sources
- **consumer-lanes** (reference card, `j-research/references/consumer-lanes.md`) - consumer AI services section for session/API lanes; not a ladder rung
- **j-inbox** - May reference tool options for research import
- **j-triage** - May reference tool capabilities for processing research

### Cross-Tool Considerations

**Manual vs Autonomous:**
- Autonomous: LDR, Exa, Tavily, You.com, Perplexica, Wigolo (decide queries and synthesis)
- Manual: OmniRoute (you write queries and paste evidence)
- Session-based: Kimi (requires browser automation via ego-browser)

**Local vs External:**
- Local-only: LDR, Perplexica, Wigolo (no API keys, run on this machine)
- External: Exa, Tavily, You.com, Brave, Perplexity (API), DeepSeek (API) (require API keys, internet access)
- Session-based: Kimi (requires logged-in browser session)

**Cache vs Fresh:**
- Cache-first: Wigolo (persistent cache, instant hits)
- Fresh-only: You.com (force_refresh), Tavily (time_range)
- Hybrid: Exa, LDR (configurable)
- Session-based: Kimi (uses session context)

**ToS Considerations:**
- Strict ToS: Perplexity (web UI automation prohibited)
- Caution: Qwen (unresolved ToS uncertainty), DeepSeek (unresolved ToS uncertainty)
- Permitted: Kimi (session use intended path), Brave (API use permitted)
- Local tools: LDR, Wigolo, Perplexica (no ToS concerns for local execution)

## Browser Rung Priority

For services requiring browser automation (Kimi session lane):

1. **ego-browser** (rung 2) - Default for logged-in sessions
2. **browseros-neo** - Escalate if ego-browser cannot authenticate
3. **chrome-devtools** - Last resort fallback

**Browser-rung logging:** Always record which browser rung served the run in the research log. If no browser was used (pure API), record `rung: none (api)`.

## Maintenance

**When to update this inventory:**
- New MCP tools added to the system
- Tool parameters or capabilities change
- New search/research services become available
- Performance measurements updated
- Pricing or quota models change
- Consumer AI service ToS or access changes
- Session persistence verified/invalidated

**Update process:**
1. Run `mcp_list_servers` to check current servers
2. Run `mcp_list_tools` for each search/research server
3. Update tool descriptions, parameters, and use cases
4. Update consumer AI service lanes if ToS/access changes
5. Update quick reference table
6. Update selection guides if needed
7. Test tool changes with relevant skills

## Related Documentation

- Individual skill files (j-deep-research, j-perplexica-search, etc.) and reference cards (consumer-lanes)
- MCP server documentation
- Local infrastructure setup (~/.infra/bin/)
- LM Studio model status (`lms ps`)
- Verdict files for consumer AI services (qwen-deep-research-verdict.md, perplexity-deep-research-verdict.md, etc.)
