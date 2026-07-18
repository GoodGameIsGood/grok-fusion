# Falsify and Revise

Defines Heavy/MVP P6. Falsification comes before revision. No free-form debate.

## Inputs

- original query
- canonical brief
- evidence pack
- selected spine
- minority sentinel output

## Falsifier

Launch one isolated `gf-worker` Task call.

### Falsifier output schema

```yaml
must_fix: []
should_fix: []
accepted_risk: []
counterexamples: []
falsification_tests: []
fatal_flaw: false
fatal_flaw_summary:
```

Rules:

- Attack the spine only.
- Prefer concrete counterexamples and tests over rhetoric.
- Maximum 600 words.
- Do not propose a replacement design unless `fatal_flaw` is true.

## Revision editor

After the falsifier returns, launch one isolated `gf-worker` Task call.

### Revision output schema

```yaml
spine_id:
changes_made: []
must_fix_resolved: []
should_fix_resolved: []
accepted_risk_remaining: []
compatible_insights_added: []
unresolved: []
revised_spine:
```

Rules:

- Change only demonstrated defects and compatible blind spots.
- One revision maximum.
- If `fatal_flaw` is true and unfixable without replacing the spine, select the next Top-3 card and rerun only P6.
- Do not average incompatible alternatives into the revised spine.
- Maximum 900 words for `revised_spine`.

## Stop conditions

- Exactly one falsifier call and at most one revision call per spine attempt
- At most one spine replacement after an unfixable fatal flaw
- Then continue to verification
