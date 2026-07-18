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
  summaries/
  checkpoints/
```

If `.git` exists, add `.grok-fusion/` to `.git/info/exclude` when available. Prefer that over changing a tracked `.gitignore`.

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

Reflexion memory. Appended after every wave retro; read in every wave preamble.

```json
{
  "schema_version": 1,
  "lessons": [
    {"id": "", "wave_id": "", "observation": "", "rule": "", "applies_to": ""}
  ]
}
```

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

## Spine lock

The spine lives in `spine.json`. These fields are immutable without gate G4:

- goal
- invariants
- non-goals
- forbidden_paths
- epic boundaries

Any G4-approved spine change must rewrite `spine.json` and append a `gate` event to `events.jsonl`.

## Anti-loop budgets

- per-wave max edit cycles: 3
- identical failure fingerprint max: 2
- full Heavy rerun max per epic: 1

## Done predicate

MVP is done only when:

- every mandatory product, epic, and wave clause is `PASS`
- discovery coverage meets the required threshold for touched modules
- no open blockers remain in the DAG
- core vertical flow and build/start path are verified
