# Grok Fusion

Adaptive same-model deliberation for Grok in Cursor.

The plugin auto-loads routing guidance for every Grok parent request and selects a compute tier before acting: **Quick**, **Standard**, **Heavy**, or **MVP**. Explicit `/grok-fusion` remains available. It is designed to compete with solo Fable on architecture and other expensive deliberation tasks. It does not claim measured Fable parity or universal capability until adaptive, MVP, and smoke evaluation evidence exists.

## What it is

- A Cursor plugin with skill, agents, and an always-on auto rule
- Deterministic tier routing plus task-specific packs
- Same-model orchestration through readonly `gf-worker`, `gf-reviewer`, and `gf-auditor` subagents via the Cursor Task tool
- Answer/Quick/Standard/Heavy tracks that stay artifact-free
- MVP track with durable resumable state under `.grok-fusion/runs/<run-id>/`

## What it is not

- Not a native IDE fan-out button
- Not a multi-provider Fusion panel
- Not a silent Heavy pipeline for every ordinary reply
- Not a proven Fable replacement on long-horizon agentic coding

## Install

```bash
git clone git@github.com:GoodGameIsGood/grok-fusion.git ~/.cursor/plugins/local/grok-fusion
```

Or HTTPS:

```bash
git clone https://github.com/GoodGameIsGood/grok-fusion.git ~/.cursor/plugins/local/grok-fusion
```

Then:

1. Enable third-party / local plugins if your Cursor settings require it.
2. Reload the Cursor window.
3. Select the strongest available non-Fast Grok model.
4. Confirm the auto rule is active and `/grok-fusion` is visible.
5. Confirm agents `gf-worker`, `gf-reviewer`, and `gf-auditor` are visible.
6. On a Standard/Heavy probe, confirm subagent model badges also show Grok.

### Update

```bash
git -C ~/.cursor/plugins/local/grok-fusion pull --ff-only
```

### Uninstall

```bash
rm -rf ~/.cursor/plugins/local/grok-fusion
```

### Other install paths

- Team Marketplace: import the repository URL in Cursor dashboard plugins
- Project fallback: copy all of the following into the project:
  - `skills/grok-fusion/` → `.cursor/skills/grok-fusion/`
  - `agents/gf-worker.md`, `agents/gf-reviewer.md`, `agents/gf-auditor.md` → `.cursor/agents/`
  - `rules/grok-fusion-auto.mdc` → `.cursor/rules/grok-fusion-auto.mdc`

## Usage

Automatic: any Grok parent request should load Fusion routing and choose a tier before work starts.

Explicit:

```text
/grok-fusion Design a durable outbox for our existing Node + Postgres order service.
```

```text
/grok-fusion Fix the flaky test in tests/queue.spec.ts.
```

```text
/grok-fusion Build an MVP waitlist app with signup and admin export.
```

Force a deeper tier by saying so explicitly, for example “use Heavy Fusion” or “treat this as an MVP with durable waves.”

Every response includes a compact footer: `Fusion tier: Quick|Standard|Heavy|MVP`.

## Tiers and cost

| Tier | When | Approximate calls | Output shape |
|---|---|---|---|
| Quick | Clear, local, reversible, single-step/single-file | 1–2 | Direct answer |
| Standard | Moderate ambiguity, ordinary debug/research, a few files | 7–8 | Verdict, evidence, risks |
| Heavy | Architecture, security, migration, high-stakes | ~24 | Full seven-section report |
| MVP | Multi-wave product build needing resume | Heavy once for spine, then adaptive per wave | Product plan + wave reports + durable state |

Quality is prioritized over token cost. Quick exists so simple work is not forced through the Heavy pipeline. Large brownfield refactors use the `refactoring-migration` pack (Heavy for one batch; MVP when the work spans multiple waves).

## MVP state, resume, and safety gates

MVP runs persist JSON under `.grok-fusion/runs/<run-id>/`:

- `run.json`, `spine.json`, `prfaq.json`, `lessons.json`, `discovery.json`, `dag.json`, `acceptance.json`, `events.jsonl`
- `summaries/` and `checkpoints/`

`spine.json` persists the architecture spine and ADR; it changes only through gate G4.

Before the spine pass, write a PR/FAQ (working backwards, EARS criteria, riskiest assumption test). Wave 1 after discovery is a walking skeleton. After waves, `lessons.json` records retros; the final epic ends with a user-zero walkthrough of the documented quickstart.

When git is available, G0 scope approval authorizes a dedicated local branch or worktree and local checkpoint commits. Never push. Prefer adding `.grok-fusion/` to `.git/info/exclude` over changing a tracked `.gitignore`.

Hybrid gates:

- **G0**: approve MVP scope, architecture spine, and local branch/worktree before writes
- **G1**: data/schema migration or destructive operation
- **G2**: breaking public API, auth, permissions, or security boundary
- **G3**: deployment, payments, credentials, or external side effect
- **G4**: changing goal, invariants, non-goals, or epic boundaries

All other reversible waves proceed autonomously. Interrupted waves stay `blocked`, never partially `PASS`. Resume reloads checkpoint + wave summaries without rerunning Heavy unless the spine changed.

When an epic completes, Fusion runs an epic integration check: the full verified test/build set from discovery plus a spine-conformance audit before the next epic.

MVP is done only when every mandatory product/epic/wave clause is `PASS`, the build/start path works, the core vertical flow is verified, and no unresolved blockers remain.

## Model requirements

- Prefer the strongest non-Fast Grok available in Cursor.
- Avoid Fast and Code Fast variants for Fusion runs.
- Custom agents use `model: inherit`.
- Standard/Heavy/MVP run a one-call model/tool probe and fail closed when the badge is not Grok.
- External facts (library versions, API shapes, pricing, best practices) are verified with live search during the run and dated with `retrieved_at`. Verification and research calls are never skipped to save tokens.
- On some legacy Cursor plans without Max Mode, or under team policy, subagents may fall back to another model. If badges are not Grok, Fusion is not running as designed and should fail closed.

## Privacy

- Scouts read only the context needed for the query.
- Quick/Standard/Heavy answer tracks do not write persistent run artifacts into the user project.
- MVP is the only tier that persists durable state under `.grok-fusion/`.
- The orchestrator keeps a compact in-memory `RunEnvelope` for all tiers.

## Pipeline (Heavy)

1. P0 runtime preflight and model probe
2. P1 independent framing x3
3. P2 evidence scouts x2
4. P3 isolated candidates (task-pack lenses)
5. P4 absolute judges + position-swapped selection
6. P5 minority sentinel
7. P6 falsify then revise
8. P7 verification and final answer

If Task tools, quorum, schema repair, or model inheritance fail, the skill reports that Fusion did not run. It never silently returns a solo answer as Fusion.

## Benchmark and smoke status

The repository includes:

- 30-case Heavy blind contract under `evals/cases.yaml`
- adaptive routing cases in `evals/adaptive-cases.json`
- MVP long-horizon cases in `evals/mvp-cases.json`
- Cursor smoke checks in `evals/smoke-runbook.md`
- state fixtures under `evals/fixtures/`

Release thresholds are defined in `evals/runbook.md` and `evals/smoke-runbook.md`. No benchmark results are checked in yet, so documentation must not claim measured Fable parity, superiority, or universal capability.

## Validation

```bash
python3 -m py_compile scripts/validate_plugin.py
python3 scripts/validate_plugin.py
python3 scripts/validate_plugin.py --state evals/fixtures/valid-run
```

Invalid fixture must fail:

```bash
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-run; test $? -ne 0
```

CI runs the same checks via `.github/workflows/validate.yml`.

Success output:

```text
OK: grok-fusion plugin structure and contracts are valid
```

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Skill or auto rule missing | Plugin path, third-party plugins disabled, or reload skipped | Confirm install paths and reload |
| Agents missing | Project fallback copied skill only | Also copy `gf-worker`, `gf-reviewer`, `gf-auditor`, and the auto rule |
| Fusion did not run | Task/subagents unavailable, quorum failed, or non-Grok badge | Retry once; check Max Mode / team model policy |
| Every task feels Heavy | Router override or ambiguous prompt | Ask for Quick/Standard explicitly or narrow the request |
| MVP cannot resume | Missing or inconsistent `.grok-fusion/runs/<id>/` | Validate with `--state` and restore from checkpoint |
| Unexpected file edits | Implementation intent inferred on answer track | Use analysis wording unless edits are explicit |
| Gate pause | G0–G4 risk trigger | Approve, adjust scope, or abort intentionally |

## License

MIT. See [LICENSE](LICENSE).
