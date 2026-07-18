# Grok Fusion evaluations

This directory defines evaluation contracts for:

- solo Grok
- Grok Fusion (Quick / Standard / Heavy / MVP)
- solo Fable (architecture deliberation comparison only)

## Contents

- `cases.yaml` — exactly 30 Heavy-oriented blind cases across four categories
- `rubric.yaml` — atomic weighted scoring criteria
- `negative-criteria.yaml` — penalties and disqualifiers
- `runbook.md` — blind protocol and release thresholds
- `adaptive-cases.json` — Quick/Standard/Heavy/MVP routing cases
- `mvp-cases.json` — multi-wave, migration, resume, and rollback scenarios
- `smoke-runbook.md` — manual Cursor plugin-load and Task smoke checks
- `design-cases.yaml` — web/UI design skill routing and claim-hygiene cases (≥3)
- `fixtures/valid-run/` — valid MVP state fixture for `validate_plugin.py --state`
- `fixtures/invalid-run/` — intentionally invalid state fixture (must fail)
- `fixtures/invalid-legacy-fields/` — dag still using legacy `outputs`/`tests` (must fail mentioning `produces`)
- `fixtures/invalid-blocked-missing-reason/` — `run.status=blocked` without `blocked_reason` (must fail)
- `fixtures/invalid-false-done/` — multi_pass `complete` without `closure: CONFIRMED` (must fail)
- `results/` — dated structural validate records (`structural-*.json`); not blind benchmarks

## Status

Structural validate results are recorded under [`results/`](results/) (see `structural-2026-07-18.json`). Blind adaptive, MVP, and smoke suites still lack recorded pass evidence. Until those suites pass with recorded evidence, public documentation must not claim universal capability or measured Fable parity.
