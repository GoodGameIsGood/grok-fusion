# Planning Contract

Professional, executable planning for Grok Fusion. When planning is mandatory, follow this contract without waiting for extra user instructions.

## When planning is mandatory

Planning is required when any is true:

- the user asks for a plan, roadmap, spec, CreatePlan, or how to implement something (`plan`, `план`, `roadmap`, `спека`, `как реализовать`)
- mutation would touch more than one file or more than one wave
- MVP work before the epic/wave DAG is written
- Cursor Plan mode or any pre-implementation design of work

Do not start edits until the plan quality gate is `PASS`.

## Plan shape

Emit this structure (YAML or equivalent markdown sections). All fields are required.

```yaml
goal: ""  # one sentence
non_goals: []
assumptions: []  # each with VERIFIED|INFERRED|SPECULATIVE|INSUFFICIENT
unknowns: []
success_definition: []  # goal-backward must-haves
ears_criteria:
  - id: ""
    text: ""  # WHEN <trigger> THE SYSTEM SHALL <response> or Given-When-Then
constraints:
  forbidden_paths: []
  invariants: []
  budgets: []
evidence_needed: []  # reads/searches before steps; apply freshness-contract.md
batches:
  - id: ""
    files: []  # max 5 paths
    steps:
      - id: ""
        files: []
        action: ""
        verify_cmd: ""  # repo-native command, or "n/a" plus reason
        acceptance_ids: []
        done_evidence: ""
risks_and_rollback: []
stop_conditions: []
```

Rules:

- Build `success_definition` first (goal-backward), then derive batches that make those must-haves true.
- Every batch has at most 5 files.
- Every step has a verify command or an explicit `n/a` reason.
- Paths and symbols must be grounded per `grok-harness.md` symbol grounding and `freshness-contract.md`.
- Spec → Plan → Tasks → Implement. Never jump from intent to code.

## Anti-patterns (reject)

Reject and revise any plan that contains:

- vague verbs only (“improve”, “refactor”, “polish”, «улучшить», «отрефакторить») without concrete files and verify
- steps without `verify_cmd` or without EARS linkage
- a batch with more than 5 files
- missing `non_goals` or missing `ears_criteria`
- open-ended leftovers (“and then everything else”)
- prose-only plans with no atomic steps

## Plan quality gate

Launch one `gf-worker` or `gf-auditor` Task that scores the draft plan only. Required checklist:

- atomic steps (one outcome each)
- verifiability (`verify_cmd` or justified n/a)
- path grounding (no invented paths)
- every batch ≤ 5 files
- `ears_criteria` present and testable
- no silent assumptions (all listed)

Output:

```yaml
plan_quality: PASS|FAIL
failures: []
repair_hints: []
```

On `FAIL`: one revision only. On a second `FAIL`: fail closed or ask at most two clarifying questions. Do not implement.

## Devil's advocate on plans

Before accepting a plan, run one adversarial pass whose only goal is to prove the plan fails in implementation. Return the strongest evidence-backed objection and one cheaper alternative path. A checkable flaw triggers revision; an unresolved objection is reported as dissent with lowered confidence. Never suppress it.

## Handoff

After `plan_quality: PASS`, the plan is the source of truth for `implementation-track.md` and the epic/wave DAG. Do not change goal, non-goals, invariants, or batch boundaries mid-flight without an explicit user gate equivalent to G4. Wave and edit batches must cite plan step ids.
