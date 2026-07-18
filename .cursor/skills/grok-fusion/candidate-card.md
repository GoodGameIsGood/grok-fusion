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

## Normalization before judging

Parent must strip or ignore:

- role names and lens labels
- stylistic padding
- duplicated verbosity
- self-assigned confidence percentages

All cards must be presented to judges in the same field order.
