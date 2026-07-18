# Implementation Track

Use for explicit code changes. Default answer track remains readonly.

Single-batch Standard/Heavy edits use the one-shot sequence below. MVP uses the autonomous wave loop.

## One-shot sequence

0. If planning is mandatory and no accepted plan exists, build one per [planning-contract.md](planning-contract.md) and obtain plan quality gate `PASS` before any edit.
1. Run the selected deliberative pipeline first and produce a file-level implementation contract that cites plan step ids when a plan exists.
2. The contract must list:
   - exact allowed paths
   - invariants
   - preconditions
   - repository-native test commands
   - acceptance clauses
3. Only the parent agent edits files. `gf-worker` stays readonly.
4. Verify every precondition before changing code.
5. Run repository-native tests, typecheck, or lint. Do not invent commands.
6. Invoke `gf-reviewer` twice in one parallel Task batch:
   - correctness, contracts, and edge cases
   - architecture, requirements, and scope drift
7. Fix only evidence-backed defects, then rerun verification.
8. Audit every acceptance clause as `PASS`, `FAIL`, or `UNVERIFIED`.
9. Never say done while any mandatory clause is `FAIL` or `UNVERIFIED`.

## Implementation contract schema

```yaml
goal:
allowed_paths:
forbidden_paths:
invariants:
preconditions:
test_commands:
acceptance_clauses:
wave_id:
baseline_test_snapshot:
rollback_git_ref:
migration_steps: []
compat_checks: []
```

## Wave preamble

Before every MVP wave, re-read `spine.json`, `lessons.json`, and the active wave entry in `dag.json`. Re-state in one short block: goal, invariants, `owns_paths`, `forbidden_paths`, required gates. Long-context drift is not an excuse: the preamble re-grounds every wave. Apply every lesson whose `applies_to` matches the current wave.

## MVP wave loop

For each ready wave in topological order:

0. Confirm the wave maps to accepted plan batch/step ids from [planning-contract.md](planning-contract.md); if no accepted plan exists, build and gate it first.
1. Validate durable state and discovery coverage for `owns_paths`.
2. Capture baseline tests and a checkpoint under `.grok-fusion/runs/<run-id>/checkpoints/`.
3. Pause for any required G0–G4 safety gate before editing.
4. Parent edits only `owns_paths`.
5. TDD: write or extend a failing test for the wave acceptance first, implement to green, refactor; then run wave-specific unit/integration/build commands that were verified in discovery.
6. Launch in one Task batch:
   - `gf-reviewer` correctness
   - `gf-reviewer` scope/architecture
   - `gf-auditor` acceptance
7. Fix evidence-backed defects for at most three edit cycles.
8. Two identical failure fingerprints trigger rollback and a user gate.
9. Mark the wave complete only when every mandatory clause is `PASS`.
10. Write `summaries/<wave-id>.json` and continue to the next unblocked DAG node.
11. If this wave completes an epic, run the epic integration check from `epic-track.md` before starting the next epic.
12. Wave retro: append to `lessons.json` at least one lesson (what failed, what to do differently) whenever any edit cycle, reviewer, or auditor found a defect; propagate recurring lessons into the next wave prompts.

Never claim MVP done until every mandatory product/epic/wave clause is `PASS`, the build/start path works, and the core vertical flow is verified.

## Safety gates

Hybrid autonomy: reversible waves proceed automatically. Pause only for:

- **G0**: approve MVP scope, architecture spine, and local branch/worktree once before first writes
- **G1**: data/schema migration or destructive operation
- **G2**: breaking public API, auth, permissions, or security boundary
- **G3**: deployment, payments, credentials, or external side effect
- **G4**: changing goal, invariants, non-goals, or epic boundaries

Gate prompts must be structured yes/no or constrained choices. Record gate outcomes in `events.jsonl`.

## Mandatory quality clauses

Every mutating wave adds these clauses to its acceptance set, scored by `gf-auditor` as mandatory:

- repository-native lint/typecheck/build commands from discovery pass cleanly
- errors are handled at system boundaries touched by the wave
- no dead code, placeholder stubs, or commented-out blocks introduced
- no secrets or credentials in code or config
- every symbol used by the change is grounded per `grok-harness.md` symbol grounding

## Reviewer prompts

Reviewers and the auditor receive:

- original query
- canonical brief
- implementation contract or wave state
- diff
- test command outputs
- discovery coverage for owned modules

They must not edit files and must not invent APIs or paths absent from the contract, diff, or state.

## Safety rules

- No parallel writers
- No speculative dependency installation
- No broadening scope beyond allowed or owned paths
- Fail closed if tests cannot be identified and the change is non-trivial
- Local checkpoint commits only; never push
