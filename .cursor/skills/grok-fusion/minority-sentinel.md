# Minority Sentinel

Formal overturn path against a correlated same-model majority.

Cite [provocation-contract.md](provocation-contract.md) when weighing minority claims that attack framing or load-bearing assumptions: prefer evidence-backed `decision_delta` style challenges over novelty rhetoric. Do not re-run the full operator bank; do not overturn for novelty alone.

## When to run

After Top-3 and provisional spine selection, launch one isolated `gf-worker` call as the `minority sentinel`.

## Inputs

- original query
- canonical brief
- evidence pack
- Top-3 candidate cards
- provisional spine id

Do not tell the sentinel the absolute scores or judge identities.

## Required output

```yaml
strongest_minority_claim:
  claim:
  evidence:
  why_majority_missed_it:
predicted_spine_failure:
  failure:
  severity: must_fix | should_fix | accepted_risk
falsification_test:
overturn_recommendation: keep_spine | replace_spine
replacement_candidate_id:
rationale:
```

## Overturn rule

Replace the spine only when at least one is true:

1. new evidence the spine ignored and that changes the decision
2. a checkable fatal flaw with a concrete falsification test

Do not overturn for rhetoric, confidence tone, novelty, or length.

## Dissent preservation

Whether or not overturn happens, preserve:

- the strongest minority claim
- unresolved contradictions among Top-3
- accepted risks that remain after sentinel review

These must appear in the final user answer under panel dissent.
