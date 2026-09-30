# Research-lane wiring audit (step 8) and cost leak (step 9)

Why agents skip the ladder: check wiring in this order — most common causes first.

### 8. Research-lane wiring audit (why agents skip the ladder)

When "agents/kimi don't use perplexica/LDR/searxng" is the symptom, check wiring in this order — most common causes first:

1. **Hermes web backend bypass**: `grep -A3 '^web:' /Users/pftg/.hermes/config.yaml`. If `search_backend: exa`, Hermes' built-in web tool goes straight to the metered paid API and never touches searxng. That is a config-policy conflict with the searxng-first ladder — flag as `high`.
2. **MCP wiring**: confirm `searxng` and `perplexica` entries exist under `mcp_servers:` in the same config and are not `enabled: false`.
3. **Skill presence**: `ls ~/.hermes/skills | grep -i 'research\|lanes'` — the `local-deep-research` skill lives only in `~/.agents/skills` (kimi scope); Hermes profiles need a Hermes-side skill or SOUL line to reach LDR.
4. **SOUL ladder line**: researcher SOUL references the ladder; verify other research-touching profiles (growth-operator, delivery-manager) name it too, or they will default to the built-in web tool.
5. **Kimi side**: `~/.kimi-code/mcp.json` carries searxng/perplexica — if a kimi session skipped them, check whether `[experimental] tool-select` deferred them (loaded on demand only).

## Step 9 — cost leak: metered backends

### 9. Cost leak: metered backends

Any of `web.backend: exa`, `web.search_backend: exa`, or tavily usage beyond its single announced-fallback role is a cost leak under the `j-research` ladder. Cross-check `call_logs` for exa/tavily traffic volume when the backend config disagrees with the ladder.
