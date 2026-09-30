# No-code risk tiers

| Risk | Examples | Rule |
|---|---|---|
| low | research, drafts, read-only probes | checker required for the conclusion |
| medium | a reversible write in a sandbox, a disabled integration, single-user config with a snapshot | checker PASS before apply |
| high | paid, external (send, post, share, invite), permissions or credentials, deletes, production-wide or shared config (a file several agents or homes load, SOUL, merged skills), no working rollback | checker PASS **and** the owner approves the exact change just before apply; a changed diff voids the approval |
| never by an agent | granting itself access, disabling audit or approval, approving its own work, deleting the snapshot | human only |
