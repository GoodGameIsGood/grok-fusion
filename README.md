# Grok Fusion

> **One Grok. Council-grade judgment.** Adaptive deliberation in Cursor — from quick fixes to architecture and resumable MVPs.

**A Cursor plugin that turns one Grok into a careful council:** independent framing, live evidence checks, competing proposals, judges, self-critique, and verification — then adaptive compute so simple edits stay fast and large builds stay resumable.

Use it when you want stronger architecture judgment, fewer hallucinations, and a safer path from idea → MVP → working product.

---

## Who this is for

- Developers and founders using **Grok inside Cursor**
- People who need better answers on architecture, debugging, research, and multi-step builds
- Anyone who wants an MVP/agent workflow that can pause, resume, and refuse to call itself “done” without proof

## What you get

| Capability | In practice |
|---|---|
| Adaptive tiers | Quick / Standard / Heavy / MVP — picks depth from the task |
| Same-model council | Multiple Grok subagents (`gf-worker`, `gf-reviewer`, `gf-auditor`) via Cursor Task |
| Fresh facts | External versions/APIs checked live and dated — not guessed from memory |
| Self-critique | Devil’s-advocate pass before the answer; empty “LGTM” reviews are rejected |
| Multi-pass QA | Core 5 specialists every round, plus on-demand specialists (20+) with recheck/improve/advise (≤3 optional per round, veto allowed) until consensus PASS |
| Professional plans | EARS criteria, atomic ≤5-file batches, verify commands, plan quality + multi-pass — no extra prompting needed |
| MVP mode | PR/FAQ → spine → discovery → wave DAG → TDD waves → multi-pass → resume + safety gates |
| Fail closed | If Task/subagents or Grok inheritance fail, it says **Fusion did not run** — it will not pretend |

Every reply ends with: `Fusion tier: Quick|Standard|Heavy|MVP`.

### Project config

Per-project quality lives in `.grok-fusion/config.json` (see `project-config.md`). Defaults are `balanced` (adaptive tiers). This repository ships `quality_profile: max` so every request uses MVP + full Heavy spine. Other projects can use `balanced` or `fast` without editing the plugin.

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

---

## Install (2 minutes)

Anyone with Cursor can use either path. **Option A** installs once for all projects. **Option B** copies files into one project only (ZIP download works — Git is optional).

### Option A — local plugin (recommended)

```bash
git clone https://github.com/GoodGameIsGood/grok-fusion.git ~/.cursor/plugins/local/grok-fusion
```

SSH:

```bash
git clone git@github.com:GoodGameIsGood/grok-fusion.git ~/.cursor/plugins/local/grok-fusion
```

Then in Cursor:

1. Enable **third-party / local plugins** if your settings require it
2. **Reload** the window
3. Select the **strongest non-Fast Grok** model you have
4. Confirm `/grok-fusion` appears and agents `gf-worker`, `gf-reviewer`, `gf-auditor` are visible

**Update (Option A):**

```bash
git -C ~/.cursor/plugins/local/grok-fusion pull --ff-only
```

**Uninstall (Option A):**

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
| `agents/gf-worker.md` | `.cursor/agents/gf-worker.md` |
| `agents/gf-reviewer.md` | `.cursor/agents/gf-reviewer.md` |
| `agents/gf-auditor.md` | `.cursor/agents/gf-auditor.md` |
| `rules/grok-fusion-auto.mdc` | `.cursor/rules/grok-fusion-auto.mdc` |

4. Reload Cursor and select a strong non-Fast Grok model.

**Update (Option B):** download or pull the latest repo, then overwrite the same five paths in the project and reload.

**Uninstall (Option B):** delete those copied paths from the project’s `.cursor/` folders and reload. This does **not** use `~/.cursor/plugins/...`.

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

### Plans (no special prompting needed)

Ask for a plan, roadmap, or “how to implement X”. Fusion loads the professional planning contract automatically: goal-backward DoD, EARS acceptance criteria, atomic batches (≤5 files), verify commands, plan quality gate, multi-pass error hunts, and specialist consensus. Edits do not start until the gate is `PASS`.

Force depth when you want it:

- “use Quick Fusion”
- “use Heavy Fusion” / “deep analysis”
- “treat this as an MVP with durable waves”

---

## Tiers (what happens to your request)

| Tier | Typical tasks | Approx. calls | You get |
|---|---|---|---|
| **Quick** | Rename, one-file fix, short explanation | 1–2 | Direct answer + light verify |
| **Standard** | Ordinary debug, research, 2–8 files | 7–8 | Verdict, evidence, risks |
| **Heavy** | Architecture, security, migration, high stakes | ~24 | Full seven-section report |
| **MVP** | Product / multi-wave / resumable build | Heavy spine + per-wave work | Plan, waves, durable state |

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

**Done** means: every mandatory product/epic/wave clause is `PASS`, build/start works, core loop is verified, no open blockers.

---

## Model requirements

- Prefer the **strongest non-Fast Grok** in Cursor  
- Avoid Fast / Code Fast for Fusion runs  
- Subagents use `model: inherit` — their badges must show **Grok**  
- If Task tools are missing or badges fall back to another model: Fusion fails closed  
- On some plans without Max Mode (or under team policy), inheritance can break — fix policy or enable Max Mode  

Live verification of external facts (versions, APIs, pricing) is intentional and is **not** skipped to save tokens.

---

## Privacy

- Quick / Standard / Heavy do **not** write run artifacts into your project by default  
- **MVP** writes under `.grok-fusion/runs/`; keep `config.json` tracked and exclude runs (see `.gitignore` pattern in this repo)  
- Workers are readonly; only the parent agent edits files when you asked for implementation  

### Resume and budgets

- Say **`Continue run <run_id>`** to resume a blocked or interrupted MVP run  
- Raise soft caps in `.grok-fusion/config.json` under `budgets` (`max_task_calls_per_wave`, `max_task_calls_per_epic`) when a large epic exhausts the default budget — never mark PASS on exhaust  

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill / auto rule missing | Confirm install path, enable local plugins, reload |
| Agents missing | Copy all three agents + the auto rule, not only the skill |
| “Fusion did not run” | Check Task/subagents and Grok badges; Max Mode / team model policy |
| Everything feels Heavy | Narrow the ask, or say “use Quick/Standard” |
| MVP won’t resume | Say `Continue run <id>`; check `.grok-fusion/runs/<id>/`; restore from checkpoint |
| Always MVP / too slow | Set `.grok-fusion/config.json` `quality_profile` to `balanced` or `fast` |
| Budget blocked mid-epic | Raise `budgets.max_task_calls_per_*` in config, then `Continue run <id>` |
| Unexpected file edits | Ask for analysis only unless you want implementation |
| Stuck on a gate | Approve, change scope, or abort — G0–G4 are intentional |

Manual smoke checklist: [`evals/smoke-runbook.md`](evals/smoke-runbook.md).

---

## For contributors / CI

```bash
python3 -m py_compile scripts/validate_plugin.py
python3 scripts/validate_plugin.py
python3 scripts/validate_plugin.py --state evals/fixtures/valid-run
```

Invalid fixture must fail. CI: [`.github/workflows/validate.yml`](.github/workflows/validate.yml).

Evaluation contracts live under [`evals/`](evals/). Blind benchmark *results* are not checked in yet — this README does not claim measured parity with other models.

---

## License

MIT © [GoodGameIsGood](https://github.com/GoodGameIsGood). See [LICENSE](LICENSE).
