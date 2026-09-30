# ICE vs category — two axes, not a replacement

ICE and the `bos-categorize` category field answer **different questions**.
Keep both; do not conflate them.

- **ICE** (this skill) answers: *how valuable vs. how much work?* It decides
  queue priority. Inputs: impact, effort. Output: a numeric score.
- **`category`** (`bos-categorize`, run at triage promotion) answers: *how
  much research does this deserve before anyone acts?* It decides routing.
  Inputs: work item body, `approval`, `risk_class`, `domain_novelty`. Output:
  `quick-lookup` / `pre-research` / `deep-research` / `workshop`.

A high-ICE item can be a `quick-lookup` (valuable and cheap, already answered
locally). A low-ICE item can be a `deep-research` (not valuable yet, but
irreversible — the rubric forces the floor regardless of ICE). The two are
orthogonal; neither replaces the other. When a work item carries both a score
and a `category`, read them as independent axes.
