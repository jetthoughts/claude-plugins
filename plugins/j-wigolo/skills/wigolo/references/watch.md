# wigolo watch

Track a page over time. Register a watch job on a URL (or many), then check it to see whether the content changed since the last snapshot. Optionally deliver a webhook when a change fires.

**Lazy execution model** — there is no background daemon. A job's check runs when you call `action: "check"`, or opportunistically when another tool runs and the job is overdue. Set realistic `interval_seconds` (minimum 60).

## Quick Reference

```json
// Create a single-URL watch (checks no more than once every 6 hours)
{ "action": "create", "url": "https://nodejs.org/en/blog", "interval_seconds": 21600 }

// Batch create across several URLs
{ "action": "create", "urls": ["https://a.example.com", "https://b.example.com"], "interval_seconds": 3600 }

// Scope the diff to a subtree
{ "action": "create", "url": "https://example.com/pricing", "interval_seconds": 86400, "selector": "#pricing-table" }

// Deliver a webhook on change (SSRF-guarded)
{ "action": "create", "url": "https://example.com/status", "interval_seconds": 300, "notification": "https://hooks.example.com/wigolo" }

// List all jobs
{ "action": "list" }

// Check one job now
{ "action": "check", "job_id": "job_abc123" }

// Pause / resume / delete
{ "action": "pause", "job_id": "job_abc123" }
{ "action": "resume", "job_id": "job_abc123" }
{ "action": "delete", "job_id": "job_abc123" }
```

## Parameters

| Parameter | Type | Default | When to use |
|-----------|------|---------|-------------|
| `action` | string | required | "create", "list", "check", "pause", "resume", "delete" |
| `url` | string | none | Single-URL create. Mutually exclusive with `urls` |
| `urls` | string[] | none | Batch create. Response carries `jobs[]` only |
| `interval_seconds` | number | none | Required for create. Minimum check interval (min 60) |
| `selector` | string | none | Create-only CSS selector to scope the diff to a subtree |
| `notification` | string | "inline" | "inline" (return on next check) or a webhook URL |
| `job_id` | string | none | Required for check, pause, resume, delete |

Single-URL create returns `job` (singular) plus `jobs: [job]` (legacy). Batch create returns `jobs[]` only.

## How It Works

1. **create** — registers the job and takes a baseline snapshot of the page (or the `selector` subtree).
2. **check** — re-fetches, diffs against the last snapshot, and reports changed/unchanged. On change it advances the snapshot and, if a webhook is configured, delivers it.
3. **list / pause / resume / delete** — manage the job set.

Webhook delivery is SSRF-guarded: the server validates the destination before posting, so a job cannot be pointed at internal or loopback addresses.

## Anti-Patterns

- DON'T set `interval_seconds` below 60 — the minimum is enforced.
- DON'T expect checks to fire on their own — this is a lazy model; call `check` (or rely on overdue opportunistic runs).
- DON'T pass both `url` and `urls` — they are mutually exclusive.

## When NOT to use `watch`

- **One-off comparison of two versions** — use `diff` instead.
- **Bulk change detection across the whole cache on demand** — use `cache` with `check_changes: true`.

## See Also

- [diff](diff.md) — one-shot version comparison
- [cache](cache.md) — on-demand bulk change detection
- [fetch](fetch.md) — the fetch each check runs under the hood
