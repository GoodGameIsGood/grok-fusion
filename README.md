# Grok Fusion

[![CI](https://github.com/GoodGameIsGood/grok-fusion/actions/workflows/validate.yml/badge.svg)](https://github.com/GoodGameIsGood/grok-fusion/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.2-blue.svg)](.cursor-plugin/plugin.json)

> **One Grok. Council-grade judgment.** Adaptive deliberation in Cursor and Grok Build — from quick fixes to architecture, AppSec review, and resumable MVPs.

A plugin that turns one Grok into a careful council: independent framing, live evidence (repo + web researchers), competing proposals with dual-provocation challenges, judges, self-critique, and verification — with adaptive depth so simple edits stay fast and large builds stay resumable. **v0.4.2** ships the same tree for **Cursor** (`.cursor-plugin/`) and **Grok Build** (`.grok-plugin/`), plus a visible warning when the subagents / agents plaque is off.

**Product receipt (what ships / what is not claimed)**

- Ships: adaptive tiers, same-model Task council (`gf-worker` / on Grok Build `grok-fusion:gf-*`), fail-closed honesty, multi-pass QA with closure gates, professional planning & debugging, AppSec craft (`grok-security` + pack `appsec-review`), resumable MVP waves (when mutating), web/UI design siblings, dual-host manifests
- Verified packaging on Grok Build CLI `0.2.103`: `grok plugin validate` / `install --trust` / `inspect` load skills + qualified agents (see `evals/results/smoke-grok-build-2026-07-18.json`, claim `PACKAGING` / status `PARTIAL`)
- Does **not** claim: measured parity with other models, Cursor Marketplace one-click install, **FULL** or **HOST_SMOKE_PASS** Grok↔Cursor behavioral parity until live E2/E3 smoke is recorded `PASS` and SD8 Cursor baseline is satisfied, coverage of every design or security medium, exploit/PoC authorship, or that every MVP-labeled reply writes durable run state
- Does **not** claim: plugin `rules` `alwaysApply` auto-fires on Grok Build without recorded G1 smoke (use `AGENTS.md` / Option C snippet for PARTIAL auto)

## Contents

- [Setup and update](#setup-and-update) (Option A Cursor · Option B project copy · **Option C Grok Build**)
- [Strengths](#strengths)
- [How to use it](#how-to-use-it)
- [Tiers (what happens to your request)](#tiers-what-happens-to-your-request)
- [Building an MVP with Fusion](#building-an-mvp-with-fusion)
- [Model requirements](#model-requirements)
- [Privacy](#privacy)
- [Troubleshooting](#troubleshooting)
- [For contributors / CI](#for-contributors--ci)
- [License](#license)

---

## Setup and update

Anyone with Cursor or **Grok Build** and a strong non-Fast **Grok** model can install (Task/subagents required — see [Model requirements](#model-requirements)). **Option A** installs once for all Cursor projects. **Option B** copies files into one Cursor project (ZIP works — Git is optional). **Option C** installs on Grok Build from the same repo.

### Option A — local plugin (recommended)

```bash
mkdir -p ~/.cursor/plugins/local
git clone https://github.com/GoodGameIsGood/grok-fusion.git ~/.cursor/plugins/local/grok-fusion
```

SSH:

```bash
mkdir -p ~/.cursor/plugins/local
git clone git@github.com:GoodGameIsGood/grok-fusion.git ~/.cursor/plugins/local/grok-fusion
```

Then in Cursor:

1. Enable **third-party / local plugins** if your settings require it
2. **Reload** the window
3. Select the **strongest non-Fast Grok** model you have
4. Confirm `/grok-fusion` appears and agents `gf-worker`, `gf-reviewer`, `gf-auditor`, `gf-researcher-repo`, `gf-researcher-web` are visible
5. Optionally confirm `/grok-design`, `/grok-web-ui`, and `/grok-security` appear (craft siblings)

#### Update (Option A)

```bash
git -C ~/.cursor/plugins/local/grok-fusion pull --ff-only
```

Reload Cursor after updating.

#### Uninstall (Option A)

```bash
rm -rf ~/.cursor/plugins/local/grok-fusion
```

Then reload Cursor.

### Option B — project-only copy

Use this when you cannot (or do not want to) install a global plugin. Works from a `git clone` **or** a [ZIP download](https://github.com/GoodGameIsGood/grok-fusion/archive/refs/heads/main.zip).

1. Open the downloaded repo folder.
2. In your project, create folders if needed: `.cursor/skills/`, `.cursor/agents/`, `.cursor/rules/`.
3. Copy:

| From the repo | Into your project |
|---|---|
| `skills/grok-fusion/` | `.cursor/skills/grok-fusion/` |
| `skills/grok-design/` | `.cursor/skills/grok-design/` |
| `skills/grok-web-ui/` | `.cursor/skills/grok-web-ui/` |
| `skills/grok-security/` | `.cursor/skills/grok-security/` |
| `agents/gf-worker.md` | `.cursor/agents/gf-worker.md` |
| `agents/gf-reviewer.md` | `.cursor/agents/gf-reviewer.md` |
| `agents/gf-auditor.md` | `.cursor/agents/gf-auditor.md` |
| `agents/gf-researcher-repo.md` | `.cursor/agents/gf-researcher-repo.md` |
| `agents/gf-researcher-web.md` | `.cursor/agents/gf-researcher-web.md` |
| `rules/grok-fusion-auto.mdc` | `.cursor/rules/grok-fusion-auto.mdc` |

4. Reload Cursor and select a strong non-Fast Grok model.

#### Update (Option B)

Download or pull the latest repo, overwrite the same paths in the project, then reload.

#### Uninstall (Option B)

Delete those copied paths from the project’s `.cursor/` folders and reload. This does **not** use `~/.cursor/plugins/...`.

**Note:** Additive craft skills (`grok-design`, `grok-web-ui`, `grok-security`) live under `skills/` for plugin discovery. They are **not** dual-tree HARD-mirrored like `grok-fusion`; Option B must copy them explicitly. v0.4.x ships AppSec craft (`grok-security` + pack `appsec-review`) alongside web/UI design craft — not every security or design medium.

### Option C — Grok Build (same repo)

Requires [Grok Build](https://docs.x.ai/build/overview) with subagents enabled. Manifest: [`.grok-plugin/plugin.json`](.grok-plugin/plugin.json) (skills/agents/rules share the repo root with Cursor).

```bash
# From a local clone (recommended while developing)
grok plugin validate .
grok plugin install . --trust

# One-off session without install
grok --plugin-dir /path/to/grok-fusion

# From GitHub (after cloning or once published)
grok plugin install GoodGameIsGood/grok-fusion --trust
```

Enable subagents in `~/.grok/config.toml`:

```toml
[subagents]
enabled = true
```

Если плашка Subagents / agents **выключена**, при старте сессии и при каждом промпте hook покажет предупреждение, а агент обязан вывести баннер «агенты ВЫКЛЮЧЕНЫ» и `Fusion did not run` (см. `runtime-contract.md`).
Then:

1. Start a Grok Build session on a strong non-Fast Grok model
2. Run `grok inspect` — confirm skills `grok-fusion` (+ craft skills) and agents **`grok-fusion:gf-worker`**, `grok-fusion:gf-reviewer`, `grok-fusion:gf-auditor`, `grok-fusion:gf-researcher-repo`, `grok-fusion:gf-researcher-web`
3. Spawn those **qualified** agent IDs (not only bare `gf-*`) when running the council
4. Complete the live checklist in [`evals/smoke-runbook-grok.md`](evals/smoke-runbook-grok.md) (E2/E3 need an authenticated session)
5. **Auto-route (G1):** this repo’s [`AGENTS.md`](AGENTS.md) is loaded by Grok Build as project instructions. For other projects, if plugin rules do not auto-apply, add:

```markdown
# Grok Fusion (Option C)
Before answering or editing: load skill grok-fusion /grok-fusion; read .grok-fusion/config.json
(or defaults balanced); follow runtime-contract host matrix; spawn grok-fusion:gf-* agents;
Task probe for Standard/Heavy/MVP; fail closed if subagents unavailable;
footer Fusion tier: matching actual work.
```

**Claim level today:** **`PACKAGING`** (install/inspect verified). Not `HOST_SMOKE_PASS` / `FULL` until E2+E3 live smoke is `PASS` and SD8 Cursor baseline is set. Marketplace draft: [`docs/marketplace-pr-draft.md`](docs/marketplace-pr-draft.md) (**DO-NOT-SUBMIT** until then).

### Project config

Per-project quality lives in `.grok-fusion/config.json` (see `project-config.md` in the skill). Defaults for consumers are `balanced` (adaptive tiers). This repository ships `quality_profile: max` so every request uses MVP + full Heavy spine. Other projects can use `balanced` or `fast` without editing the plugin.

Example `max`:

```json
{
  "schema_version": 1,
  "quality_profile": "max",
  "tier_policy": "force_mvp"
}
```

Example `balanced`:

```json
{
  "schema_version": 1,
  "quality_profile": "balanced",
  "tier_policy": "adaptive"
}
```

| Profile | Behavior |
|---|---|
| `balanced` | Adaptive Quick / Standard / Heavy / MVP (plugin default) |
| `fast` | Prefer Quick/Standard; escalate only on clear triggers |
| `max` | Every request → MVP + full Heavy spine (this repo) |

---

## Strengths

Built for developers and founders using **Grok in Cursor or Grok Build** who want stronger architecture judgment, evidence-backed answers, and a safer path from idea → MVP → working product.

| Strength | In practice | How to notice |
|---|---|---|
| Adaptive tiers | Quick / Standard / Heavy / MVP — depth matches the task | Footer: `Fusion tier: …` |
| Same-model council | Parallel Grok subagents via host Task tool (Cursor Task / Grok `task`) | Cursor: `gf-*`; Grok Build: `grok-fusion:gf-*` |
| Dual-provocation | Lens 8 forces assumption_attack + lateral_analogy challenges (no extra Task) | `provocation-contract.md`; Quick skips dedicated provocation Tasks |
| Fail closed | No silent solo answer when Task/inheritance fails | Reply says **Fusion did not run** |
| Fresh facts | External versions/APIs checked live and dated when claimed | Dated sources on external facts — not memory guesses |
| Self-critique + multi-pass QA | Devil’s-advocate pass; core specialists + optional roles until consensus | Empty “LGTM” rejected; `closure: CONFIRMED` before done |
| Professional planning & debugging | EARS plans gate edits; debug uses Repair Card + characterization | Plans `PASS` before edits; high-confidence fixes only |
| Resumable MVP builds | PR/FAQ → spine → discovery → wave DAG → TDD waves → resume | Mutating runs under `.grok-fusion/runs/`; G0–G4 safety gates |
| Web/UI design craft | Sibling skills `grok-design` + `grok-web-ui` + pack `visual-ui` | Canon/tokens-first; web/UI scope — not every design medium |
| AppSec craft | Sibling skill `grok-security` + pack `appsec-review` | OWASP/ASVS Finding Cards; Remediation Card only on explicit fix |

One-shot closure keeps `done_evidence` + walkthrough + blind hunt in the same request so follow-up «перепроверь» is not required.

---

## How to use it

### Automatic (default)

Ask Grok normally. The auto rule loads Fusion routing and chooses a tier before work starts.

### Explicit

```text
/grok-fusion Design a durable outbox for our Node + Postgres order service.
```

```text
/grok-fusion Fix the flaky test in tests/queue.spec.ts.
```

```text
/grok-fusion Build an MVP waitlist app with signup and admin export.
```

```text
/grok-fusion Audit authz on the order API — OWASP/ASVS Finding Cards only, no PoC.
```

AppSec-primary prompts use pack `appsec-review` and skill `grok-security`. Audit emits Finding Cards (no edits). Explicit “fix / harden / close the vuln” requires a Remediation Card before any mutation.

### Plans (no special prompting needed)

Ask for a plan, roadmap, or “how to implement X”. Fusion loads the professional planning contract: goal-backward DoD, EARS acceptance criteria, atomic batches (≤5 files), verify commands, plan quality gate, multi-pass error hunts, and specialist consensus. Edits do not start until the gate is `PASS`.

Force depth when you want it (under `balanced` / `fast`):

- “use Quick Fusion”
- “use Heavy Fusion” / “deep analysis”
- “treat this as an MVP with durable waves”

Under `quality_profile: max` / `tier_policy: force_mvp` (including this repository), in-chat Quick/Standard/Heavy does **not** demote — change `.grok-fusion/config.json` instead.

---

## Tiers (what happens to your request)

| Tier | Typical tasks | Approx. calls | You get |
|---|---|---|---|
| **Quick** | Rename, one-file fix, short explanation | 1–2 | Direct answer + light verify |
| **Standard** | Ordinary research, explain-only debug, 2–8 files | 7–8 | Verdict, evidence, risks |
| **Heavy** | Architecture, security, migration, high stakes | ~24 answer-track (mutating + multi-pass is higher) | Full seven-section report |
| **MVP** | Product / multi-wave / resumable build | Heavy spine + per-wave work | Plan, waves; durable state on mutating paths |

Quality over speed. Quick exists so a typo fix is not forced through a 24-call pipeline.

Large brownfield refactors use the `refactoring-migration` pack (Heavy for one batch; MVP if multi-wave).

---

## Building an MVP with Fusion

When the tier is **MVP**, Fusion does not “vibe code” forever. It runs a startup-oriented path:

1. **PR/FAQ** (working backwards) — customer, problem, benefit, riskiest assumptions, EARS acceptance criteria  
2. **Heavy spine** — one coherent architecture locked in `spine.json`  
3. **Discovery** — map only the modules you will touch; no inventing unread APIs  
4. **Wave DAG** — vertical slice first (walking skeleton), then features  
5. **TDD waves** — failing test → implement → green → review → audit  
6. **Lessons + resume** — state under `.grok-fusion/runs/<run-id>/`; interrupted waves stay blocked, never half-“PASS”  
7. **User-zero walkthrough** — final epic checks the quickstart as a first-time user  

### Safety gates (pauses for approval)

| Gate | When |
|---|---|
| G0 | Scope, spine, local branch/worktree before first writes |
| G1 | Schema migration / destructive data ops |
| G2 | Breaking public API, auth, permissions, security boundary |
| G3 | Deploy, payments, credentials, external side effects |
| G4 | Changing goal, invariants, non-goals, or epic boundaries |

Everything else that is reversible proceeds autonomously. Checkpoint commits stay **local** — Fusion never pushes for you.

**Done** means: every mandatory product/epic/wave clause is `PASS`, multi-pass consensus `PASS`, `closure: CONFIRMED` when the closure gate is on, build/start works, core loop is verified, no open blockers.

---

## Model requirements

- Prefer the **strongest non-Fast Grok** (Cursor or Grok Build)  
- Avoid Fast / Code Fast for Fusion runs  
- Subagents use `model: inherit` — Cursor: badges must show **Grok**; Grok Build: operator-visible Grok model (+ pin when available); `model_family_self_report` is weak only  
- If host Task tools are missing (`Task` / `task` / `spawn_subagent`) or model authority is non-Grok: Fusion fails closed  
- On some Cursor plans without Max Mode (or under team policy), inheritance can break — fix policy or enable Max Mode  
- Grok Build: set `[subagents] enabled = true` (see Option C)  

Live verification of external facts (versions, APIs, pricing) is intentional and is **not** skipped to save tokens.

---

## Privacy

- Quick / Standard / Heavy do **not** write run artifacts into your project by default  
- **Mutating MVP** paths write under `.grok-fusion/runs/`; keep `config.json` tracked and exclude runs (see `.gitignore` pattern in this repo). Answer-only MVP under `max` still runs the Heavy spine but does not invent run folders without mutation  
- Workers are readonly; only the parent agent edits files when you asked for implementation  

### Resume and budgets

- Say **`Continue run <run_id>`** to resume a blocked or interrupted MVP run  
- When blocked (including budget exhaust), the MVP footer should include `run_id`, `blocked_reason`, remaining task calls vs caps, and that exact Continue utterance  
- Raise soft caps in `.grok-fusion/config.json` under `budgets` (`max_task_calls_per_wave`, `max_task_calls_per_epic`) when a large epic exhausts the default budget — never mark PASS on exhaust  

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill / auto rule missing | Confirm install path, enable local plugins, reload; on Grok Build see Option C AGENTS snippet |
| Agents missing | Copy all five agents + the auto rule, not only the skill; on Grok try `grok-fusion:gf-*` |
| Grok Build Fusion did not run / баннер про агентов | Включите `[subagents] enabled = true` (плашка Subagents); см. баннер в ответе и `hooks/hooks.json` |
| “Fusion did not run” | Check Task/subagents and Grok badges; Max Mode / team model policy |
| Everything feels Heavy | On `balanced`/`fast`: narrow the ask or say “use Quick/Standard”. On `max`: change `quality_profile` in config |
| MVP won’t resume | Say `Continue run <id>`; check `.grok-fusion/runs/<id>/`; restore from checkpoint |
| Always MVP / too slow | Set `.grok-fusion/config.json` `quality_profile` to `balanced` or `fast` (required under this repo’s `max`) |
| Budget blocked mid-epic | Raise `budgets.max_task_calls_per_*` in config, then `Continue run <id>` |
| Unexpected file edits | Ask for analysis only unless you want implementation |
| Stuck on a gate | Approve, change scope, or abort — G0–G4 are intentional |

Manual smoke checklist: [`evals/smoke-runbook.md`](evals/smoke-runbook.md) (Cursor) · [`evals/smoke-runbook-grok.md`](evals/smoke-runbook-grok.md) (Grok Build).

---

## For contributors / CI

```bash
python3 -m py_compile scripts/validate_plugin.py
python3 scripts/validate_plugin.py
python3 scripts/validate_plugin.py --state evals/fixtures/valid-run
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-run            # must fail
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-legacy-fields # must fail
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-blocked-missing-reason # must fail
python3 scripts/validate_plugin.py --state evals/fixtures/invalid-false-done    # must fail
# Optional (requires Grok Build CLI): 
#   grok plugin validate .
#   grok plugin install . --trust && grok inspect
```

Invalid fixtures must fail. CI: [`.github/workflows/validate.yml`](.github/workflows/validate.yml).

Evaluation contracts live under [`evals/`](evals/). Structural / smoke / mvp-golden records may exist under [`evals/results/`](evals/results/); blind Fable-parity benchmarks and full live `Continue run` Cursor sessions are not claimed — this README does not claim measured parity with other models. Grok Build install/inspect packaging evidence: `evals/results/smoke-grok-build-2026-07-18.json` (`PARTIAL` / `PACKAGING`).

---

## License

MIT © [GoodGameIsGood](https://github.com/GoodGameIsGood). See [LICENSE](LICENSE).
