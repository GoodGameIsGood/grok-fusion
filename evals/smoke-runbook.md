# Cursor smoke runbook

Manual checks after installing the plugin. Do not claim universality until these pass.

## Install

1. Install to `~/.cursor/plugins/local/grok-fusion` or copy:
   - `skills/grok-fusion/`
   - `skills/grok-design/`
   - `skills/grok-web-ui/`
   - `skills/grok-security/`
   - `agents/gf-worker.md`
   - `agents/gf-reviewer.md`
   - `agents/gf-auditor.md`
   - `agents/gf-researcher-repo.md`
   - `agents/gf-researcher-web.md`
   - `rules/grok-fusion-auto.mdc`
2. Enable third-party plugins if required by Cursor settings.
3. Reload the window.
4. Select the strongest non-Fast Grok model.

## Checks

| Check | Pass criteria |
|---|---|
| Skill visible | `/grok-fusion` appears and auto rule loads |
| Design skills visible | `/grok-design` and `/grok-web-ui` appear (Option A plugin or Option B copy) |
| AppSec skill visible | `/grok-security` appears (Option A plugin or Option B copy of `skills/grok-security/`) |
| Agents visible | `gf-worker`, `gf-reviewer`, `gf-auditor`, `gf-researcher-repo`, `gf-researcher-web` are available |
| Task spawning | Standard/Heavy runs create real Task subagents, not inline simulation; after reload, spawn trivial Tasks for `gf-researcher-repo` and `gf-researcher-web` (fail closed if unresolved — E7) |
| Model inherit | Subagent badges match parent Grok |
| Fail closed | Disabling Task or forcing non-Grok fallback yields “Fusion did not run” |
| Quick routing | Single-file rename stays Quick and finishes with low call count |
| Standard routing | Ordinary research / explain-only debug uses Standard footer |
| Heavy routing | Architecture/security prompts and mutating debug use Heavy (or MVP under `max`) |
| MVP resume | Creating an MVP run writes `.grok-fusion/runs/<id>/` and can resume |
| Safety gates | Migration/breaking changes pause at G1/G2 |
| Freshness | External library/version claims carry retrieved_at from live lookups |
| Self-critique | Final answers include resolved or reported devil's advocate objection |
| Dual-provocation | When lens `dual-provocation` runs, cards include both `assumption_attack` and `lateral_analogy`; Quick has no dedicated provocation Task |
| Multi-pass consensus | Mutating/plan runs show per-step recheck, double error hunt, completion quality, and ≥5 specialist votes with consensus PASS before done |
| Optional specialists | Migration or public-API waves fire ≤3 optional roles (e.g. `data_migration`, `api_compat`) recorded in `optional_panel` |
| Project config | Missing config → balanced adaptive tiers; with `quality_profile: max` → MVP footer every turn |
| Footer telemetry | When enabled, footer includes `profile=` and `tasks=` / `multi_pass=` / `verify=` |
| Verify hard gate | Mutating done claims include successful `verification_runs` (exit_code 0) |
| Continue run | `Continue run <run_id>` resumes durable state and lessons |
| Professional debugging | Mutating debug shows Repair Card + characterization before edits; no drive-by refactors |
| AppSec craft | AppSec-primary prompts use pack `appsec-review` + Finding Cards; remediate needs Remediation Card; no PoC |
| One-shot closure | Mutating done shows `done_evidence`, Phase E blind confirmation, and `closure: CONFIRMED` before user-facing done |

## Commands

```bash
python3 -m py_compile scripts/validate_plugin.py
python3 scripts/validate_plugin.py
python3 scripts/validate_plugin.py --state evals/fixtures/valid-run
```

Invalid fixtures must fail (substring checks in CI):

```bash
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-run; test $? -ne 0
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-legacy-fields; test $? -ne 0
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-blocked-missing-reason; test $? -ne 0
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-false-done; test $? -ne 0
```

Structural results (not blind benchmarks) may be recorded under `evals/results/structural-*.json`.

Grok Build live/packaging smoke: see [smoke-runbook-grok.md](smoke-runbook-grok.md).
