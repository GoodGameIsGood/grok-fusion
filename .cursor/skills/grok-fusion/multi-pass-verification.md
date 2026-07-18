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
  → completion_quality (gf-auditor) → specialist panel (≥5) → consensus
```

On any evidence-backed blocker or consensus FAIL: parent fixes within `owns_paths` / allowed paths, then re-enter from Error Hunt #1 (never hunt-once after a fix).

Do not nest a specialist panel inside per-step recheck.

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

1. `gf-reviewer` `mode=error_hunt` pass #1 — bugs, regressions, silent failures. For plans: adversarial holes (ungrounded paths, missing verify, non-atomic steps). Fold devil’s-advocate pressure into pass #1 (or one dedicated `gf-worker` falsifier immediately before the panel — not a sixth pass after the panel).
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

Launch **five** `gf-reviewer` Tasks with `mode=specialist_panel` in **one** parallel Task batch. Do not put specialist modes on `gf-auditor`.

### Code / product roles

| Role id | Focus |
|---|---|
| `correctness_engineer` | bugs, edges, tests |
| `systems_architect` | boundaries, cohesion, long-term evolution |
| `security_reliability` | threats, failure modes, misuse |
| `product_acceptance` | EARS/DoD, user-zero path |
| `ops_maintainability` | rollback, ops debt, observability |

### Docs-only mutating roles

Remap to: `accuracy`, `structure_clarity`, `audience_fit`, `completeness`, `maintainability_of_docs`. Same schemas and consensus math.

### specialist_panel output

```yaml
mode: specialist_panel
role: ""
verdict: SHIP|REWORK|BLOCK
blockers: []
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

### Wave / one-shot / plan

`consensus: PASS` iff all hold:

- ≥4 **valid** `SHIP`
- zero `BLOCK`
- zero `REWORK` with nonempty blockers
- no panelist with `long_term_risk: high`
- at least 4 valid votes after anti-LGTM (else fail the round)

Else: fix → Phase B → C → D.

`REWORK` with empty blockers counts as non-SHIP (blocks epic 5/5). For wave 4/5, one empty-blocker `REWORK` is allowed only if the other four are valid `SHIP` and no `long_term_risk: high`.

### Epic / product final

Require **5/5 valid SHIP**, zero `BLOCK`, zero `REWORK` with nonempty blockers, no `long_term_risk: high`.

## Budget SoT

Authoritative numbers live here and in `long-horizon-contract.md` (must match). Runtime mirrors the Task shapes only.

| Budget | Value |
|---|---|
| `max_fix_cycles` per wave/one-shot | 6 |
| `max_consensus_rounds` per wave/one-shot | 5 |
| `max_plan_multi_pass_rounds` | 2 |
| `max_step_recheck_retries` per step | 2 |
| `max_task_calls` soft ceiling per wave | 40 |
| Identical failure fingerprint | 2 (then rollback + user gate) |

On budget exhaust: status `blocked`, never “almost done”. A structured yes/no user gate may authorize another round.

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

Interrupted multi-pass ⇒ wave/plan `blocked`, not partial PASS. Resume via `recovery-track.md` using `multi_pass/<id>.json`.

## Durable artifact (MVP)

```text
.grok-fusion/runs/<run-id>/multi_pass/<wave-or-plan-or-epic-id>.json
```

```json
{
  "schema_version": 1,
  "id": "",
  "phase": "step_recheck|error_hunt_1|error_hunt_2|completion_quality|panel|done",
  "round": 0,
  "steps": [],
  "error_hunt_1": {},
  "error_hunt_2": {},
  "merged_blockers": [],
  "completion_quality": {},
  "panel": [],
  "consensus": "PASS|FAIL|IN_PROGRESS",
  "status": "in_progress|blocked|complete",
  "task_calls_used": 0
}
```

One-shot mutating (non-MVP): record the same fields on the in-memory `RunEnvelope.verification.multi_pass` object; do not invent on-disk MVP state.

## Done predicates

- Wave/one-shot: `consensus: PASS` and `status: complete` (MVP file or envelope), no open `merged_blockers`, mandatory clauses PASS.
- Plan: plan quality checklist PASS **and** multi-pass `consensus: PASS`.
- Epic/product: local wave multi-pass complete, plus product-level multi-pass with **5/5** consensus PASS.
- MVP product done additionally requires every required `multi_pass/*.json` for completed waves/plan/epic to show `consensus: PASS` and `status: complete`.

## Agent assignment

| Mode | Agent |
|---|---|
| `step_recheck` | `gf-reviewer` |
| `error_hunt` | `gf-reviewer` |
| `specialist_panel` | `gf-reviewer` |
| `completion_quality` | `gf-auditor` |
| Correlated-panel falsifier / optional plan checklist | `gf-worker` |

`gf-worker` never casts `SHIP` votes.
