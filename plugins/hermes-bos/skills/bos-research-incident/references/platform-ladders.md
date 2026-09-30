# bos-research-incident — platform-aware ladders

Same ladder `j-research` owns; the platform lane gets no order of its own.


| Platform | Rung 1 — `searxng_web_search` | Rung 2 — `tavily_search`, announced | Rung 3 — `agent-reach`, off-ladder |
|---|---|---|---|
| Reddit | `site:reddit.com` (+ `time_range`) | `include_domains: ["reddit.com"]`, `search_depth: advanced`, `time_range: month` | Reddit backend — login-walled threads, full comment text |
| Twitter / X | `site:x.com OR site:twitter.com` | `include_domains: ["twitter.com", "x.com"]` (alternate: `omniroute_x_search`) | X backend — thread text behind a login |
| YouTube (transcript) | `site:youtube.com` for the page | `tavily_extract` on `youtube.com/watch?v=…` (description + first comments) | YouTube backend — the actual transcript |
| GitHub | `site:github.com` (+ `web_extract` for README/issues) | `include_domains: ["github.com"]` | GitHub backend — issue/PR trees |
| LinkedIn (public posts) | `site:linkedin.com` | `include_domains: ["linkedin.com"]` | LinkedIn backend |
| Bilibili / XiaoHongShu | `site:bilibili.com` / `site:xiaohongshu.com` | the platform domain in `include_domains` | platform backends |
| RSS feeds | feed item URLs via `searxng_web_search` | feed item URLs via `tavily_search` | RSS backend — full history |
