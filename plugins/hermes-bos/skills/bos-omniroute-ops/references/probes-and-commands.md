# bos-omniroute-ops — probe queries and commands

All OmniRoute reads use the read-only DB handle `sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro"`. Never write.

```bash
# What OmniRoute serves (client view)
curl -s http://192.168.178.66:20128/v1/models -H "Authorization: Bearer $OMNIROUTE_FREE_KEY"

# What Hermes expects
grep -A5 '^model:' /Users/pftg/.hermes/config.yaml
```

## Step 2 — provider connection health

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT provider, name, is_active, last_error, last_error_at FROM provider_connections ORDER BY is_active, provider;"
```

## Step 3 — error-rate scan

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT date(timestamp) d, status, COUNT(*) FROM call_logs WHERE timestamp > datetime('now','-7 days') GROUP BY d, status ORDER BY d DESC, COUNT(*) DESC LIMIT 30;"
```

## Step 4 — cost / paid-lane audit

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT provider, account, SUM(tokens_in), SUM(tokens_out), COUNT(*) FROM call_logs WHERE timestamp > datetime('now','-7 days') AND provider NOT IN ('lm-studio') GROUP BY provider, account ORDER BY COUNT(*) DESC LIMIT 20;"
```

## Step 5 — combo strategy check

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT name, sort_order FROM combos ORDER BY sort_order;"
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT data FROM combos WHERE name='cos-thinking';"
```

## Step 5b — reweight scan (trailing 48h)

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" \
  "SELECT provider, COUNT(*) calls,
     ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),2) share_pct,
     ROUND(100.0*SUM(CASE WHEN status BETWEEN 200 AND 299 THEN 1 ELSE 0 END)/COUNT(*),1) success_pct
   FROM call_logs
   WHERE timestamp > datetime('now','-2 days')
     AND combo_name IN ('free-coding','free-thinking','free-cheap','cos-thinking','agents-all','cos-default','cos-small')
     AND provider NOT IN ('cos-thinking','free-cheap','free-coding','free-thinking','subs-thinking','subs-coding','subs-cheap','bos-main','agents-all','cos-default','cos-small','auto')
     AND provider NOT LIKE 'combo/%'
   GROUP BY provider ORDER BY calls DESC;"
```

## Step 6 — circuit breakers

```bash
sqlite3 "file:/Users/pftg/.omniroute/storage.sqlite?mode=ro" "SELECT * FROM domain_circuit_breakers;"
```

## Step 7 — research-lane service health

```bash
curl -s "http://127.0.0.1:8081/search?q=hello&format=json" | python3 -c "import json,sys; print('searxng results:', len(json.load(sys.stdin).get('results',[])))"
curl -s -o /dev/null -w "perplexica providers: %{http_code}\n" http://127.0.0.1:3000/api/providers
~/.local/bin/ldr-mcp --help >/dev/null 2>&1 && echo "ldr: runnable" || echo "ldr: broken"
```

## Output — kanban hotfix task

```bash
hermes kanban create "<title>" --triage --assignee quality-guardian --created-by owner --body-file - <<'EOF'
<body: finding, evidence, proposed owner action, verification step>
EOF
```
