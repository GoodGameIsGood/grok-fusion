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
- `results/` — dated eval records (`structural-*.json`, `smoke-ci-*.json`, `mvp-golden-*.json`); not blind Fable benchmarks

## Status

Recorded under [`results/`](results/):

- `structural-2026-07-18.json` — plugin + state-fixture validate
- `smoke-ci-2026-07-18.json` — CI/fixture/file-presence smoke (`kind: smoke-ci`; **not** live Cursor Task/badge smoke)
- `mvp-golden-2026-07-18.json` — `mvp-04` crash-resume **PARTIAL** (fixture/contract evidence; live `Continue run` still pending)

Blind adaptive and full live Cursor smoke suites still lack complete recorded pass evidence. Until those suites pass with recorded evidence, public documentation must not claim universal capability or measured Fable parity.
