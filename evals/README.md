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
- `fixtures/valid-run/` — valid MVP state fixture for `validate_plugin.py --state`
- `fixtures/invalid-run/` — intentionally invalid state fixture (must fail)

## Status

No benchmark results are recorded in this repository yet. Until adaptive, MVP, and smoke suites pass with recorded evidence, public documentation must not claim universal capability or measured Fable parity.
