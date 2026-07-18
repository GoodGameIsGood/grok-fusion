# Multi-Pass Verification

Mandatory quality gate for planning artifacts and mutating work. Replaces the legacy implementation `2×gf-reviewer + gf-auditor` acceptance stack. Readonly answer-track (no edits) does not run this pipeline; use `verification-gate.md` devil's advocate only.

Parent edits only. Reviewers and auditors stay readonly via Task. Never simulate subagents inline. `fusion_depth=1`.

## When required

| Track | Required? |
|---|---|
| Planning (`professional-planning`, CreatePlan) | Yes — plan artifact only |
| One-shot mutating (implementation track) | Yes — full |
| MVP waves | Yes — full |
| Epic / product final | Yes — full; stricter consensus |
| Docs-only mutating (`writing-explanation` with file edits) | Yes — adapted panel roles |
| Readonly Quick/Standard/Heavy answers | No |

## Pipeline

```text
per-step recheck → Error Hunt #1 → Error Hunt #2 → merge blockers
  → verify_hard_gate (mutating) → completion_quality (gf-auditor)
  → specialist panel (≥5) → consensus
  → done_evidence + must-not-break walkthrough → Phase E final confirmation
  → closure: CONFIRMED
```

On any evidence-backed blocker or consensus FAIL: parent fixes within `owns_paths` / allowed paths, then re-enter from Error Hunt #1 (never hunt-once after a fix).

Do not nest a specialist panel inside per-step recheck.

When project config `closure.require_final_confirmation` is true (default for this repo), user-facing done requires `closure: CONFIRMED` after Phase E — panel PASS alone is not enough.

## Verify hard gate

When project config `multi_pass.verify_hard_gate` is true (default for `balanced`/`max` mutating), parent must record real command runs before Phase C/D consensus can be `PASS`:

```json
"verification_runs": [
  {"cmd": "", "exit_code": 0, "summary": "", "at": ""}
]
```

Rules:

- At least one mutating verify run with `exit_code: 0` is required for wave/one-shot `status: complete` (unless every step used justified `verify_cmd: n/a` and auditor accepts that justification).
- Any `exit_code != 0` ⇒ consensus FAIL; fix and re-run verify before re-entering hunts.
- Parent appends the same runs to `events.jsonl` (`type: verify`).
- Plans may use checklist verify commands as dry evidence; code-mutating waves require executed commands.

## Atomic step

1. If an accepted plan exists: one plan `steps[].id`.
2. Else (one-shot contract): one acceptance-clause bundle that touches ≤1 primary file group, or one TDD cycle (failing test → implement → green) recorded as a step in the implementation contract.
3. Per-step recheck is required even for single-step one-shots.
4. If `verify_cmd: n/a`: step_recheck must still list concrete static checks. A rubber-stamp `PASS` without checks is invalid → FAIL.

## Phase A — Per-step recheck

1. Parent runs `verify_cmd` (repo-native) or records a justified `n/a`.
2. Launch one `gf-reviewer` Task with `mode=step_recheck` scoped to that step’s diff and `acceptance_ids` only.
3. Step is complete only on `PASS`. Otherwise fix and retry; retries count toward `max_fix_cycles` and `max_step_recheck_retries`.

### step_recheck output

```yaml
mode: step_recheck
step_id: ""
status: PASS|FAIL
defects: []
checks_performed: []
```

## Phase B — Double error hunt

1. `gf-reviewer` `mode=error_hunt` pass #1 — bugs, regressions, silent failures. For plans: adversarial holes (ungrounded paths, missing verify, non-atomic steps). For **debugging** pack: also attack wrong-cause fixes, breakage of `must_not_break`, and scope beyond the Repair Card `patch_intent` / `allowed_paths`. Fold devil’s-advocate pressure into pass #1 (or one dedicated `gf-worker` falsifier immediately before the panel — not a sixth pass after the panel).
2. Independent `gf-reviewer` `mode=error_hunt` pass #2 — **must not receive #1 findings** (anti-anchoring).
3. Parent merges findings.

### Merge rule (mandatory)

- Union of all evidence-backed blockers from #1 and #2.
- `#2 empty ≠ clearance` if #1 has blockers (and the reverse).
- Speculative / non-evidence items → `dissent`, not auto-blockers.
- Severity arbitration: any `BLOCK`-class finding wins over a nit.
- After **any** fix: re-run **both** hunts.

### error_hunt output

```yaml
mode: error_hunt
pass: 1|2
blockers: []
dissent: []
checks_performed: []
```

## Phase C — Completion quality

Exactly one `gf-auditor` Task with `mode=completion_quality`.

- Scores plan step ids / EARS / wave+product clauses / mandatory quality clauses.
- Does **not** cast specialist `SHIP` votes.
- Any mandatory clause `FAIL` or `UNVERIFIED` → fix → return to Phase B.

Uses the auditor clause_scores schema plus:

```yaml
mode: completion_quality
audit_result: PASS|FAIL
```

## Phase D — Specialist panel

Launch the **core five** `gf-reviewer` Tasks with `mode=specialist_panel` plus up to **three** optional roles from [specialist-roster.md](specialist-roster.md), all in **one** parallel Task batch (max 8). Do not put specialist modes on `gf-auditor`.

Parent runs the selection algorithm in `specialist-roster.md` before this phase and records chosen optional roles+scenarios.

### Code / product roles (core)

| Role id | Focus |
|---|---|
| `correctness_engineer` | bugs, edges, tests |
| `systems_architect` | boundaries, cohesion, long-term evolution |
| `security_reliability` | threats, failure modes, misuse |
| `product_acceptance` | EARS/DoD, user-zero path |
| `ops_maintainability` | rollback, ops debt, observability |

### Optional roles

Select ≤3 from the optional roster in `specialist-roster.md` using pack suggestions and risk triggers (G1/G2/G3, path patterns). Default `scenario: recheck`. For pack `debugging`, prefer `test_strategist`, `concurrency`, and `observability` (pinned by `select_optional_specialists.py` unless G1/G2 forces higher-severity roles).

### Docs-only mutating roles

Remap core to: `accuracy`, `structure_clarity`, `audience_fit`, `completeness`, `maintainability_of_docs`. Same schemas and consensus math. Optional: prefer `docs_accuracy` and related docs roles (still max 3 optional).

### specialist_panel output

```yaml
mode: specialist_panel
role: ""
scenario: recheck|improve|advise
verdict: SHIP|REWORK|BLOCK
blockers: []
improvements: []
advice: []
long_term_risk: high|medium|low
confidence: high|medium|low
checks_performed: []
```

`SHIP` requires nonempty `checks_performed`.

## Anti-LGTM

- `SHIP` with empty or missing `checks_performed` → invalid vote; one repair prompt; still invalid → drop the vote.
- Valid `SHIP` count uses only repaired-valid cards.
- Empty `REWORK` without checks → invalid.
- Prefer `REWORK`/`BLOCK` with concrete blockers.

## Same-model bias mitigation

Roles are **stance diversity**, not model diversity. Same Grok inherit is expected.

- Panelists never see each other’s verdicts before parent aggregation.
- Require pairwise-distinct `checks_performed` themes. If ≥3 valid `SHIP` cards share near-identical check lists → invalidate the panel round as correlated; launch one adversarial `gf-worker` falsifier, then re-panel.
- Multi-pass consensus alone cannot claim `confidence: high` on mutating code waves without repo-native test evidence.

## Consensus math

Core votes live in `panel`. Optional votes live in `optional_panel`.

### Wave / one-shot / plan

`consensus: PASS` iff all hold:

- ≥4 **valid** core `SHIP` (optional `SHIP` does not count toward this)
- zero core `BLOCK`
- zero core `REWORK` with nonempty blockers
- no core panelist with `long_term_risk: high`
- at least 4 valid **core** votes after anti-LGTM (else fail the round)
- zero optional `BLOCK`
- zero optional `REWORK` with nonempty blockers
- optional `SHIP` with empty `checks_performed` → invalid (anti-LGTM); drop that vote

Else: fix → Phase B → C → D.

`REWORK` with empty blockers counts as non-SHIP for core (blocks epic 5/5). For wave 4/5, one empty-blocker core `REWORK` is allowed only if the other four core votes are valid `SHIP` and no `long_term_risk: high`.

### Epic / product final

Require **5/5 valid core SHIP**, zero core `BLOCK`, zero core `REWORK` with nonempty blockers, no core `long_term_risk: high`, plus zero optional `BLOCK` / zero optional `REWORK` with nonempty blockers.

## Done evidence pack

After Phase D `consensus: PASS` (and before Phase E), parent builds `done_evidence`. Missing required fields ⇒ cannot enter Phase E.

```yaml
done_evidence:
  request_restatement: ""
  acceptance_ids: []
  verification_runs: []
  must_not_break: []
  repair_card_id: ""
  open_dissent: []
  unknowns: []
```

Rules:

- `acceptance_ids`: every mandatory clause must be PASS
- `verification_runs`: when verify hard gate is on, at least one `exit_code: 0`
- `must_not_break`: ≥1 primary happy path + ≥2 adjacent scenarios with cmd/result (or justified static check)
- `repair_card_id`: required when debugging Repair Card was used
- `open_dissent` / `unknowns`: non-blocking only; blocking items ⇒ not ready for Phase E
- Persist on `multi_pass/*.json` and on answer-track `RunEnvelope.verification.done_evidence`

## Must-not-break walkthrough

Before Phase E on mutating paths: execute or explicitly verify the `must_not_break` scenarios from the Repair Card, plan EARS, or spine. Fail closed if a walkthrough cmd fails. Record results inside `done_evidence.must_not_break`.

## Phase E — Final Confirmation

When `closure.require_final_confirmation` is true, after D PASS + complete `done_evidence` + walkthrough:

1. Re-run `verify_cmd` (mutating) and append to `verification_runs`.
2. Launch **one blind** `gf-reviewer` Task with `mode=error_hunt` and prompt tag `final_confirmation`. Do **not** pass prior panel SHIP cards or parent rationale — only diff, contract, observation, and `done_evidence`.
3. Required output:

```yaml
mode: final_confirmation
verdict: CONFIRMED|FOUND_ISSUES
falsify_attempt: ""
checks_performed: []
blockers: []
```

4. `FOUND_ISSUES`, empty `checks_performed`, or empty `falsify_attempt` → invalid; fix → re-enter Phase B (counts toward `max_fix_cycles`). At most `max_final_confirmation_rounds` (default 2).
5. `CONFIRMED` + verify green + no blockers → set `closure: CONFIRMED` on the artifact; only then user-facing done.

### Anti-empty-perfect

When `closure.forbid_empty_perfect` is true, forbidden user-facing claims without `closure: CONFIRMED` and nonempty checks: «всё идеально», «перепроверка не нужна», «багов нет». Allowed: report `closure: CONFIRMED`, summarize checks, and list residual `open_dissent` / `unknowns`.

If the user later says «перепроверь себя» after CONFIRMED: re-run Phase E only (cheap path). If still CONFIRMED, report checks — do not invent issues.

### Scope lock

Phase E does not expand product scope. New desires → new request, new Repair Card, or G4.

## Budget SoT

Authoritative numbers live here and in `long-horizon-contract.md` (must match). Runtime mirrors the Task shapes only.

| Budget | Value |
|---|---|
| `max_fix_cycles` per wave/one-shot | 6 (or `budgets.max_fix_cycles`) |
| `max_consensus_rounds` per wave/one-shot | 5 (or `budgets.max_consensus_rounds`) |
| `max_plan_multi_pass_rounds` | 2 |
| `max_step_recheck_retries` per step | 2 |
| `max_task_calls` soft ceiling per wave | 40 (or `budgets.max_task_calls_per_wave`) |
| `max_task_calls` soft ceiling per epic | 200 (or `budgets.max_task_calls_per_epic`) |
| `max_final_confirmation_rounds` | 2 (or `closure.max_final_confirmation_rounds`) |
| Identical failure fingerprint | 2 (then rollback + user gate) |

On budget exhaust: status `blocked`, never “almost done”. Prompt the user with `Continue run <run_id>` after raising caps in `.grok-fusion/config.json` if needed. A structured yes/no user gate may authorize another round.

## Fail-closed and resume matrix

| Event | Action | May mark done? |
|---|---|---|
| Task/subagents unavailable mid multi-pass | Fail closed: Fusion did not run / wave `blocked` | No |
| Incomplete panel batch / missing votes | Invalid round; one repair batch; else `blocked` | No |
| Crash mid round | Persist `multi_pass/*.json` `status=in_progress`; resume from `round`+phase; never invent votes | No until full PASS |
| Dirty tree before fix edit | Ownership rule / user gate; stop | No |
| G0–G4 triggered by a fix | Pause; record gate; continue only after approval; G4 if paths/invariants expand | No while gate open |
| Scope drift in fix cycle | `owns_paths` only; auditor flags drift; new paths → G4 or new wave | No if drift open |
| Soft Task ceiling hit | User gate | No |
| Correlated SHIP panel | Invalidate; adversarial falsifier + re-panel | No until clean panel |
| Fingerprint hit twice | Rollback checkpoint + user gate | No |
| Phase E Task unavailable | Fail closed / `blocked`; never invent CONFIRMED | No |
| Final confirmation FOUND_ISSUES after max rounds | `blocked` or user gate | No |

Interrupted multi-pass ⇒ wave/plan `blocked`, not partial PASS. Resume via `recovery-track.md` using `multi_pass/<id>.json`.

## Durable artifact (MVP)

```text
.grok-fusion/runs/<run-id>/multi_pass/<wave-or-plan-or-epic-id>.json
```

```json
{
  "schema_version": 1,
  "id": "",
  "phase": "step_recheck|error_hunt_1|error_hunt_2|completion_quality|panel|final_confirmation|done",
  "round": 0,
  "steps": [],
  "error_hunt_1": {},
  "error_hunt_2": {},
  "merged_blockers": [],
  "completion_quality": {},
  "verification_runs": [],
  "panel": [],
  "optional_panel": [],
  "optional_selection": {
    "triggers_matched": [],
    "selected": [],
    "dropped_by_cap": []
  },
  "repair_card": {},
  "done_evidence": {},
  "final_confirmation": {},
  "closure": "PENDING|CONFIRMED",
  "consensus": "PASS|FAIL|IN_PROGRESS",
  "status": "in_progress|blocked|complete",
  "task_calls_used": 0
}
```

One-shot mutating (non-MVP): record the same fields on the in-memory `RunEnvelope.verification.multi_pass` object (and `RunEnvelope.verification.repair_card` / `done_evidence` / `closure` when applicable); do not invent on-disk MVP state.

When a Repair Card is present: any evidence that the diff diverges from `patch_intent` or `allowed_paths` ⇒ consensus FAIL (auditor clause `repair_card_followed`).

## Done predicates

- Wave/one-shot: `consensus: PASS`, `closure: CONFIRMED` (when closure gate on), `status: complete`, no open `merged_blockers`, mandatory clauses PASS, verify hard gate satisfied when enabled, `done_evidence` complete.
- Plan: plan quality checklist PASS **and** multi-pass `consensus: PASS` **and** `closure: CONFIRMED` when closure gate on.
- Epic/product: local wave multi-pass complete, plus product-level multi-pass with **5/5** consensus PASS and `closure: CONFIRMED`.
- MVP product done additionally requires every required `multi_pass/*.json` for completed waves/plan/epic to show `consensus: PASS`, `status: complete`, and `closure: CONFIRMED` when the gate is enabled.

## Agent assignment

| Mode | Agent |
|---|---|
| `step_recheck` | `gf-reviewer` |
| `error_hunt` | `gf-reviewer` |
| `specialist_panel` | `gf-reviewer` |
| `final_confirmation` (blind) | `gf-reviewer` |
| `completion_quality` | `gf-auditor` |
| Correlated-panel falsifier / optional plan checklist | `gf-worker` |

`gf-worker` never casts `SHIP` votes.
