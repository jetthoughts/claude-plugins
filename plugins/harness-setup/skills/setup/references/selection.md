# Capability selection

Use this as a set of hypotheses, not an automatic installation registry. A role is an accountable
function; it need not be a persistent agent or a new executive title.

| Outcome | Existing-first capability | Add only when demonstrated missing |
| --- | --- | --- |
| Business decision | Existing strategy/PM skills, approved PKM, public research | One domain skill with a decision-quality test |
| Coding delivery | Stack-specific delivery skills, Git/code search, tests and CI | One stack/QA skill tied to a failing acceptance case |
| Research | Approved local retrieval, existing web research, citation verification | Retrieval improvement after measured misses |
| Delegation | Existing PM/delegation contract and independent review | One bounded delegation skill, not another coordinator |
| Browser QA | Existing authorized browser, local/staging target, reproducible checks | Browser capability only after access and safety review |

Check for `claude-code-setup`, `claude-md-management`, shared plugin repositories and
project-specific profiles. These are discovery leads, not installation requirements or proof
of availability. Preserve upstream names and provenance; never copy a whole marketplace just
to expose one useful capability.

This marketplace, `jetthoughts/claude-plugins`, also provides
`j-delivery`, `j-research`, `j-paperclip`, `deliberate`, `j-ideation` and `unfix`; repository presence
does not prove any are installed in the target root. Check runtime availability and relevant
contracts before proposing another delivery, ideation or control-plane workflow.

Prefer the existing `j-research:j-perplexica-search` for a quick cited lookup when
`mcp__perplexica__search` is actually available and authorized. Follow its own call budget and
preserve configured model defaults. Escalate to deeper research only for an unresolved consequential
question; do not default to a paid deep-research service. The bundled public researcher is a
no-private-context fallback with native web tools, not a replacement for the existing research stack.

## Reuse ladder

1. Use a verified existing native tool/skill.
2. Enable a previously installed capability at project scope after reviewing the exact change.
3. Adapt a small trusted upstream skill in an isolated candidate directory, preserving provenance.
4. Author one missing skill through skill-creator.
5. Recommend new infrastructure only if the preceding options fail a bounded experiment.

Do not install a gateway, vector database, agent framework, tool server or C-level library by
default. Search/ripgrep is a valid baseline; semantic search earns adoption by improving actual
cross-file questions, not by sounding more capable.

## Required recommendation fields

- Blocked outcome and evidence of the gap.
- Current baseline and why it is insufficient.
- Reuse/no-change option plus at most two alternatives.
- One recommendation, exact version/source/license if verified; otherwise unknown.
- Data boundary, authentication owner, costs in the user's chosen budget terms and maintenance.
- Positive and negative acceptance cases; comparison with the baseline.
- Permission change, owner decision, rollback and stop condition.

Keep runtime tools seat-specific. A business reader does not need shell writes; a public
researcher does not need private PKM or client credentials; a skill author does not need
publishing access. Prompts about spending, WIP or escalation are not hard limits.

If a recommendation requires broad existing permissions to be reduced, stage that separately.
The bundled updater deliberately does not remove or rewrite the user's permission policy.
