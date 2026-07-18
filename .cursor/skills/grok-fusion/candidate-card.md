# Candidate Card

Canonical schema for every P3 proposer output. Judges score these cards. Style and identity must be normalized away before selection.

## Hard limits

- Maximum 900 words
- YAML-shaped fields only
- No raw chain-of-thought
- No role self-identification
- No confidence rhetoric such as "I am certain" or "obviously"

## Required fields

```yaml
thesis:
verified_facts:
assumptions:
unknowns:
proposed_design:
rejected_alternative:
quality_scenarios:
failure_modes:
validation_or_falsification:
symbol_grounding:
```

When the lens is `dual-provocation`, also require:

```yaml
provocation_challenges:
  - kind: assumption_attack  # or lateral_analogy
    question: ""
    decision_delta: ""
    operator_id: INVERT  # optional: INVERT | NAIVE_CUT | PREMORTEM_SEED
```

## Field rules

- `thesis`: one coherent claim answering the user query
- `verified_facts`: only VERIFIED evidence records or file-backed facts
- `assumptions`: every non-verified premise used by the thesis
- `unknowns`: missing facts that could change the recommendation
- `proposed_design`: the concrete recommendation or architecture
- `rejected_alternative`: at least one serious alternative and why it loses
- `quality_scenarios`: for architecture tasks, ATAM-lite scenarios; otherwise concrete success checks
- `failure_modes`: at least one specific way the proposal can fail
- `validation_or_falsification`: a test, measurement, counterexample, or experiment that could prove the proposal wrong
- `symbol_grounding`: list of `{symbol, evidence_id}` for every referenced API/path/command; use the literal value `SPECULATIVE` instead of an evidence_id when unverified
- `provocation_challenges`: required only for lens `dual-provocation`; MUST include ≥1 `assumption_attack` and ≥1 `lateral_analogy`, each with nonempty `decision_delta` (see [provocation-contract.md](provocation-contract.md)); total words across items ≤180; do not use role-name keys

## Normalization before judging

Parent must strip or ignore:

- role names and lens labels
- stylistic padding
- duplicated verbosity
- self-assigned confidence percentages

Keep `provocation_challenges` content for judges (kinds and decision deltas); strip only identity labels, not the challenge substance.

All cards must be presented to judges in the same field order.
