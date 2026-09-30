# Maintenance sweep checklist

0. Probe every lane in use with a real 1-token request (see Lane health above) **before** reading
   the board — a dead lane makes every stuck card one root cause, not N, and requeued cards just
   strand again.
1. Read `/issues`, `/agents`, `/attention` and `/recovery-observability` for the company and clear
   every stuck row left over from the checks above.
2. Attention feed to zero, or say plainly which items are parked and why. An item sitting there is
   a human decision nobody has taken, not a task.
3. Any seat with no completed work in 30 days: say so. A roster that only grows is sediment.
4. Backup age — `/api/health` carries it under the **nested** shape `databaseBackup.latestBackup` (no flat `ageHours` at top level since ~2026-09-14; compute age from the nested timestamp). Over ~26h is stale.
5. Spend against cap, and whether the split by seat matches what those seats actually do.
6. A worktree whose card is closed, whose branch is merged into the default ref, and whose tree is
   clean can be pruned; leave a dirty or unmerged one alone.
