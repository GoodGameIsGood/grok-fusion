# Implementation Track

Use for explicit code changes. Default answer track remains readonly.

Single-batch Standard/Heavy edits use the one-shot sequence below. MVP uses the autonomous wave loop.

Acceptance for every mutating path uses [multi-pass-verification.md](multi-pass-verification.md). That contract **replaces** the legacy `2×gf-reviewer + gf-auditor` done-gate. Do not stack both.

When the task pack is `debugging`, also follow [debugging-playbook.md](debugging-playbook.md): no edits until a Repair Card with `confidence: high` exists; attach the card to the contract; require `baseline_test_snapshot`; after the fix run characterization + blast-radius suite before multi-pass.

## One-shot sequence

0. If planning is mandatory and no accepted plan exists, build one per [planning-contract.md](planning-contract.md) and obtain plan quality gate `PASS` (including multi-pass consensus) before any edit.
0b. If pack is `debugging`: complete playbook steps through Repair Card approval before any edit. `confidence` below `debugging.min_fix_confidence` ⇒ no mutating.
1. Run the selected deliberative pipeline first and produce a file-level implementation contract that cites plan step ids when a plan exists.
2. The contract must list:
   - exact allowed paths (⊆ Repair Card `allowed_paths` when debugging)
   - invariants
   - preconditions
   - repository-native test commands
   - acceptance clauses
   - atomic steps (see multi-pass atomic-step definition)
   - `repair_card` when debugging
   - `baseline_test_snapshot` (required for debugging)
3. Only the parent agent edits files. `gf-worker` stays readonly. Debugging: implement **only** `patch_intent` — no drive-by refactors.
4. Verify every precondition before changing code. Debugging: characterization cmds green first.
5. For each atomic step: implement, run `verify_cmd`, then Phase A `step_recheck` per [multi-pass-verification.md](multi-pass-verification.md). Record each run in `verification_runs` / `events.jsonl`.
6. After all steps: debugging verify ladder (failing case → characterization → blast suite), then Phases B→ verify hard gate → C→D. Do not mark done if `verify_hard_gate` is on and no successful verify exists.
7. Fix only evidence-backed defects within allowed paths, then re-enter from Error Hunt #1. Respect `max_fix_cycles` and `max_consensus_rounds`. Debugging scope changes need a **new** Repair Card.
8. Audit every acceptance clause as `PASS`, `FAIL`, or `UNVERIFIED` via completion_quality.
9. Never say done while any mandatory clause is `FAIL` or `UNVERIFIED`, or while multi-pass `consensus` is not `PASS`.
10. Record multi-pass results on `RunEnvelope.verification.multi_pass` (one-shot) or under `.grok-fusion/runs/<run-id>/multi_pass/` (MVP). Persist `repair_card` on `RunEnvelope.verification.repair_card` or `multi_pass/<id>.json`.

## Implementation contract schema

```yaml
goal:
allowed_paths:
forbidden_paths:
invariants:
preconditions:
test_commands:
acceptance_clauses:
steps:
  - id:
    files: []
    action: ""
    verify_cmd: ""
    acceptance_ids: []
wave_id:
baseline_test_snapshot:
rollback_git_ref:
migration_steps: []
compat_checks: []
repair_card: {}
```

## Wave preamble

Before every MVP wave, re-read `spine.json`, `lessons.json`, and the active wave entry in `dag.json`. Re-state in one short block: goal, invariants, `owns_paths`, `forbidden_paths`, required gates. Long-context drift is not an excuse: the preamble re-grounds every wave. Apply every lesson whose `applies_to` matches the current wave.

## MVP wave loop

For each ready wave in topological order:

0. Confirm the wave maps to accepted plan batch/step ids from [planning-contract.md](planning-contract.md); if no accepted plan exists, build and gate it first (plan multi-pass included). If pack is `debugging`, require an approved Repair Card (`confidence: high`) before edits.
1. Validate durable state and discovery coverage for `owns_paths` (and Repair Card `blast_radius_paths` when debugging).
2. Capture baseline tests and a checkpoint under `.grok-fusion/runs/<run-id>/checkpoints/`.
3. Pause for any required G0–G4 safety gate before editing.
4. Parent edits only `owns_paths` (and ⊆ Repair Card `allowed_paths` when debugging).
5. TDD: write or extend a failing test for the wave acceptance first, implement to green, refactor; then run wave-specific unit/integration/build commands that were verified in discovery. Debugging: characterization first per playbook. Treat each plan step or TDD cycle as an atomic step with Phase A recheck.
6. After all steps are green locally, run the full multi-pass gate from [multi-pass-verification.md](multi-pass-verification.md):
   - Ensure `verification_runs` includes successful repo-native commands (verify hard gate); debugging also runs characterization + blast suite
   - Phase B: Error Hunt #1 then #2 (sequential Task batches)
   - merge blockers (union; empty hunt ≠ clearance)
   - Phase C: one `gf-auditor` `completion_quality` (must see verify evidence + Repair Card clauses when present)
   - Before Phase D: run selection from [specialist-roster.md](specialist-roster.md); record `optional_selection`
   - Phase D: core five + ≤3 optional `gf-reviewer` `specialist_panel` in one parallel batch
   - Persist `repair_card` on the multi_pass artifact when debugging
   - consensus per wave math (core ≥4 valid SHIP; optional veto; no `long_term_risk: high` on core)
7. Fix evidence-backed defects for at most `max_fix_cycles` (6). Consensus panel re-entry at most `max_consensus_rounds` (5). Soft `max_task_calls` (40) → user gate, never PASS.
8. Two identical failure fingerprints trigger rollback and a user gate.
9. Mark the wave complete only when every mandatory clause is `PASS` **and** `multi_pass/<wave-id>.json` has `consensus: PASS` and `status: complete`.
10. Write `summaries/<wave-id>.json` and continue to the next unblocked DAG node.
11. If this wave completes an epic, run the epic integration check from `epic-track.md` before starting the next epic (includes product-level multi-pass with 5/5 consensus).
12. Wave retro: append to `lessons.json` at least one lesson (what failed, what to do differently) whenever any edit cycle, multi-pass phase, or auditor found a defect; set `fingerprint`, `tags`, `recurrence_count`, and `inject_hint`. Before Phase B/D of the next wave, inject top recurring lessons into reviewer prompts when `lessons.inject_recurring` is true.

Never claim MVP done until every mandatory product/epic/wave clause is `PASS`, required multi-pass artifacts are `consensus: PASS`, the build/start path works, and the core vertical flow is verified.

## Safety gates

Hybrid autonomy: reversible waves proceed automatically. Pause only for:

- **G0**: approve MVP scope, architecture spine, and local branch/worktree once before first writes
- **G1**: data/schema migration or destructive operation
- **G2**: breaking public API, auth, permissions, or security boundary
- **G3**: deployment, payments, credentials, or external side effect
- **G4**: changing goal, invariants, non-goals, or epic boundaries

Gate prompts must be structured yes/no or constrained choices. Record gate outcomes in `events.jsonl`.

Re-check G0–G4 before every fix edit inside multi-pass loops. Dirty tree, scope expansion beyond `owns_paths`, or invariant changes pause per the multi-pass fail-closed matrix.

## Mandatory quality clauses

Every mutating wave adds these clauses to its acceptance set, scored by `gf-auditor` `completion_quality` as mandatory:

- repository-native lint/typecheck/build commands from discovery pass cleanly
- errors are handled at system boundaries touched by the wave
- no dead code, placeholder stubs, or commented-out blocks introduced
- no secrets or credentials in code or config
- every symbol used by the change is grounded per `grok-harness.md` symbol grounding
- multi-pass consensus is PASS for this wave

## Reviewer prompts

Reviewers and the auditor receive what their multi-pass mode requires:

- original query
- canonical brief
- implementation contract or wave state
- diff and/or plan artifact
- test command outputs
- discovery coverage for owned modules
- mode (`step_recheck` | `error_hunt` | `specialist_panel` | `completion_quality`) and role stance when applicable

They must not edit files and must not invent APIs or paths absent from the contract, diff, plan, or state. Error Hunt #2 must not receive Hunt #1 findings. Panelists must not receive other panelists' verdicts.

## Safety rules

- No parallel writers
- No speculative dependency installation
- No broadening scope beyond allowed or owned paths
- Fail closed if tests cannot be identified and the change is non-trivial
- Local checkpoint commits only; never push
- Fail closed if Task/custom subagents are unavailable mid multi-pass
