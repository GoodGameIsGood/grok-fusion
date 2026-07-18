# Grok Fusion

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
| MVP mode | PR/FAQ → spine → discovery → wave DAG → TDD waves → resume + safety gates |
| Fail closed | If Task/subagents or Grok inheritance fail, it says **Fusion did not run** — it will not pretend |

Every reply ends with: `Fusion tier: Quick|Standard|Heavy|MVP`.

---

## Install (2 minutes)

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

### Option B — project-only copy

Copy into the project:

- `skills/grok-fusion/` → `.cursor/skills/grok-fusion/`
- `agents/gf-worker.md`, `agents/gf-reviewer.md`, `agents/gf-auditor.md` → `.cursor/agents/`
- `rules/grok-fusion-auto.mdc` → `.cursor/rules/`

### Update / uninstall

```bash
git -C ~/.cursor/plugins/local/grok-fusion pull --ff-only
rm -rf ~/.cursor/plugins/local/grok-fusion
```

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
- **MVP only** writes under `.grok-fusion/` (add that path to `.git/info/exclude` when possible)  
- Workers are readonly; only the parent agent edits files when you asked for implementation  

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill / auto rule missing | Confirm install path, enable local plugins, reload |
| Agents missing | Copy all three agents + the auto rule, not only the skill |
| “Fusion did not run” | Check Task/subagents and Grok badges; Max Mode / team model policy |
| Everything feels Heavy | Narrow the ask, or say “use Quick/Standard” |
| MVP won’t resume | Check `.grok-fusion/runs/<id>/`; restore from checkpoint |
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
