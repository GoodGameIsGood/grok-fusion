# Long Horizon Contract

Durable state for MVP tier only. Quick, Standard, and Heavy remain artifact-free.

## Activation

Use MVP durable state when the adaptive router selects `MVP`.

## Artifact root

```text
.grok-fusion/runs/<run-id>/
  run.json
  spine.json
  prfaq.json
  lessons.json
  discovery.json
  dag.json
  acceptance.json
  events.jsonl
  multi_pass/
  summaries/
  checkpoints/
```

If `.git` exists, prefer excluding `.grok-fusion/runs/` (keep `config.json` tracked). See repository `.gitignore` pattern.

## Persistence rules

- Persist JSON only.
- Parent writes state files; workers remain readonly.
- Never push checkpoint commits.
- G0 approval authorizes a dedicated local branch or worktree for git repos.
- Non-git projects snapshot owned paths under `checkpoints/`.

## Required files

### run.json

```json
{
  "schema_version": 1,
  "run_id": "",
  "workspace_identity": "",
  "tier": "MVP",
  "spine_id": "",
  "status": "active|blocked|complete|aborted",
  "active_wave": "",
  "branch_or_worktree": "",
  "created_at": "",
  "updated_at": ""
}
```

### spine.json

Persisted architecture spine and ADR. Written once after the Heavy spine pass, before wave 1.

```json
{
  "schema_version": 1,
  "spine_id": "",
  "goal": "",
  "invariants": [],
  "non_goals": [],
  "forbidden_paths": [],
  "decisions": [
    {
      "id": "",
      "decision": "",
      "rejected_alternatives": [],
      "consequences": [],
      "revisit_triggers": []
    }
  ],
  "carried_dissent": []
}
```

`spine_id` must equal `run.json.spine_id`.

### prfaq.json

Working-backwards product definition. Written before the Heavy spine pass.

```json
{
  "schema_version": 1,
  "press_release": "",
  "customer": "",
  "problem": "",
  "benefit": "",
  "faq": [{"q": "", "a": ""}],
  "riskiest_assumptions": [{"assumption": "", "test": "", "wave_id": ""}],
  "ears_criteria": [{"id": "", "text": ""}]
}
```

### lessons.json

Reflexion memory. Appended after every wave retro; read in every wave preamble. When project config `lessons.inject_recurring` is true, inject top recurring lessons into Error Hunt and specialist prompts.

```json
{
  "schema_version": 1,
  "lessons": [
    {
      "id": "",
      "wave_id": "",
      "observation": "",
      "rule": "",
      "applies_to": "",
      "fingerprint": "",
      "tags": [],
      "recurrence_count": 1,
      "inject_hint": ""
    }
  ]
}
```

Rules:

- On each defect-driven retro, append or bump `recurrence_count` for matching `fingerprint`.
- Before Phase B/D, inject lessons with highest `recurrence_count` whose `applies_to` matches the wave/epic (or `*`).
- Resume must reload `lessons.json` and keep injecting until the fingerprint is cleared by a successful wave.

### discovery.json

See `discovery-track.md`.

### dag.json

See `epic-track.md`.

### acceptance.json

```json
{
  "schema_version": 1,
  "product_clauses": [],
  "epic_clauses": [],
  "wave_clauses": {}
}
```

Each clause object:

```json
{
  "id": "",
  "text": "",
  "mandatory": true,
  "status": "PASS|FAIL|UNVERIFIED"
}
```

### events.jsonl

Append-only records:

```json
{"ts":"","type":"action|failure|gate|recovery","wave_id":"","detail":{},"fingerprint":""}
```

### summaries/<wave-id>.json

Compact completed-wave state for context compaction. See `recovery-track.md`.

### checkpoints/

Rollback metadata, patches, or path snapshots for the active wave.

### multi_pass/

Per-wave, plan, and epic multi-pass artifacts. Schema and consensus rules: [multi-pass-verification.md](multi-pass-verification.md).

```text
multi_pass/<wave-or-plan-or-epic-id>.json
```

Required fields: `schema_version`, `id`, `phase`, `round`, `merged_blockers`, `panel`, `optional_panel`, `verification_runs`, `consensus`, `status`, `task_calls_used`.

## Spine lock

The spine lives in `spine.json`. These fields are immutable without gate G4:

- goal
- invariants
- non-goals
- forbidden_paths
- epic boundaries

Any G4-approved spine change must rewrite `spine.json` and append a `gate` event to `events.jsonl`.

## Anti-loop budgets

Authoritative multi-pass budgets (must match [multi-pass-verification.md](multi-pass-verification.md)):

- `max_fix_cycles` per wave/one-shot: 6 (override via project config)
- `max_consensus_rounds` per wave/one-shot: 5 (override via project config)
- `max_plan_multi_pass_rounds`: 2
- `max_step_recheck_retries` per step: 2
- `max_task_calls` soft ceiling per wave: 40 (override via `budgets.max_task_calls_per_wave`)
- `max_task_calls` soft ceiling per epic: 200 (override via `budgets.max_task_calls_per_epic`)
- identical failure fingerprint max: 2
- full Heavy rerun max per epic: 1

Budget exhaust → status `blocked`, never “almost done.” Resume with `Continue run <run_id>` after adjusting config caps if needed.

## Done predicate

MVP is done only when:

- every mandatory product, epic, and wave clause is `PASS`
- discovery coverage meets the required threshold for touched modules
- no open blockers remain in the DAG
- every required `multi_pass/*.json` for completed waves, the accepted plan, and the final epic has `consensus: PASS` and `status: complete`
- no open `merged_blockers` in those multi-pass artifacts
- core vertical flow and build/start path are verified
