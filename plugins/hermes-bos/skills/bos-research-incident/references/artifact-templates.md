# bos-research-incident — artifact layouts and body templates

```
viking://user/default/incidents/YYYY-MM-DD/<incident_id>/rca.md       (created later in step 2)
viking://user/default/incidents/YYYY-MM-DD/<incident_id>/candidates.md (created later in step 3)
viking://user/default/incidents/YYYY-MM-DD/<incident_id>/vote.md       (created later in step 4)
viking://user/default/incidents/YYYY-MM-DD/<incident_id>/experiment.md (created later in step 5)
viking://user/default/incidents/YYYY-MM-DD/<incident_id>/resolution.md (created later in step 8)
```

```
## Original query
<the failed question>

## Failed output
<path + run id + 1-line summary>

## Missing / wrong
<user's words verbatim, or the auto-trigger>

## Root cause
Which agent failed, which tools it used, why it missed X:
- no deep read (snippet-only)
- outdated filter (time_range not set)
- duplicate collapse (3 different URLs all returned the same press release)
- wrong decomposition (asked the wrong sub-question)
- off-ladder tool substitution (used a tier 3 source instead of tier 1)
- wrong tool substitution (used Wigolo when Tavily was needed for Reddit via include_domains, etc.)

## Tools demoted
- <tool> — false_negative += 1 (with the missing item named)
```

```
## Candidates from Variant A (Discovery)
| candidate | URL | date | evidence | confidence |
|---|---|---|---|---|

## Candidates from Variant B (Freshness)
...

## Candidates from Variant C (Novelty)
...
```

```
| candidate | evidence | recency | relevance | novelty | weighted total |
|---|---|---|---|---|---|
| <A1> | 4 | 5 | 5 | 5 | 17 |
...
```

```
## Original query
<the question>

## What was fixed
<the gap that the variants caught>

## Voting winner
<candidate + total score>

## Verified
<experiment verdict + proof>

## Freshness
<last re-check date + result>

## Action taken
- updated research_notes/{topic}/<slug>.md with corrected version
- appended user_corrections/{topic}: <X>
- updated tool_scores/global: <tool1> demoted (+1 false_negative), <tool2> promoted (+1 true_positive)
- removed gap from known_gaps/{topic}: <X>
```
