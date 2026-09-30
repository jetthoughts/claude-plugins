# Self-detected incident loop — swarm method (step 2)

Agent-LDJ as a kanban swarm. The normative bullets that follow it stay in SKILL.md.

**2. Investigate and discuss: agent-LDJ as a kanban swarm** (LDJ eval 2026-09-22 "ADAPT"; blind
writing beats debate, arXiv 2508.17536 and Diversity Collapse ACL 2026; agent dot-votes failed 0/3
in `Topics/management-methodologies.md`, so scores and a named decider replace the vote). The
orchestrator runs:
`hermes kanban swarm "<incident goal>" --worker researcher:"Blind A: what the runs actually did":five-whys --worker researcher:"Blind B: cause hypotheses from the tools and UI":five-whys,ego-browser --worker quality-guardian:"Blind C: cause hypotheses from skills, config and the card":five-whys --verifier quality-guardian --synthesizer kanban-orchestrator --tenant HERM --idempotency-key <incident key>-swarm`
