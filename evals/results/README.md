# Eval results

Dated JSON under this directory records measured evidence for Grok Fusion.

| Pattern | Meaning |
|---|---|
| `structural-*.json` | Plugin + state-fixture validate matrix |
| `smoke-ci-*.json` | CI/fixture/file-presence smoke (not live Cursor Task/badge) |
| `smoke-grok-build-TEMPLATE.json` | Schema for live Grok Build smoke (`E1`–`E6` + `cursor_baseline`) |
| `smoke-grok-build-*.json` | Recorded Grok Build smoke (`HOST_SMOKE_PASS` only when `status=PASS`; `PARTIAL`/`PACKAGING` allowed for install-only evidence) |
| `mvp-golden-*.json` | Golden MVP case evidence (`PASS` or honest `PARTIAL` + `live_pending`) |
| `harness-ab-*.json` | Exploratory solo-vs-Fusion A/B lift (`claim_level=exploratory`; not release) |
| `harness-ab-*.raw.json` | Raw arm answers (deep-merge by case id; solos then fusions) |
| `harness-ab-*.judges.json` | Position-swapped LLM judge cards for harness-ab |

These do **not** authorize universal-capability or Fable-parity claims. `harness-ab-*` is explicitly exploratory and non-release. Live Cursor smoke rows (Task spawn, model inherit badge, interactive `Continue run`) remain open until recorded separately. Live Grok Build smoke is recorded only via `smoke-grok-build-*.json` (see `evals/smoke-runbook-grok.md`); TEMPLATE alone is not PASS. Never treat harness-ab means as `evals/benchmark-results.json` / runbook Evidence.

### Claim ladder (Grok Build)

| Level | Requires |
|---|---|
| `PACKAGING` | `.grok-plugin/` + dual `validate_plugin` green + README Option C |
| `HOST_SMOKE_PASS` | `smoke-grok-build-*.json` with `status=PASS` (E1–E6) |
| `FULL` | `HOST_SMOKE_PASS` **and** `cursor_baseline.status=PASS` (or explicit user waiver) **and** G1–G4 |

If `cursor_baseline.status=live_pending`, max public claim is `PARTIAL` (`FULL` forbidden).
