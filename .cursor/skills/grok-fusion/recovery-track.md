# Recovery Track

Resume, compaction, and loop control for MVP runs.

## Resume checks

On every MVP continuation, validate before writing:

- workspace path matches `run.json.workspace_identity`
- branch/HEAD or worktree matches the recorded checkpoint when git is used
- `schema_version` is supported
- `active_wave` exists in `dag.json`
- `spine.json` exists, parses, and `spine_id` matches `run.json`; a missing or invalid `spine.json` for an active MVP run is fail closed
- DAG is acyclic and ownership does not overlap for active waves
- interrupted waves are `blocked`, never partially `PASS`

If validation fails, stop and report the blocker.

## Resume behavior

- Reload `run.json`, `spine.json`, current wave, unresolved blockers/dissent, and completed-wave summaries.
- Do not rerun Heavy unless the spine changed through gate G4.
- Cap full Heavy reruns to one per epic.
- Continue from the last checkpoint for a `blocked` or incomplete active wave.

## Wave summary contract

```json
{
  "schema_version": 1,
  "wave_id": "",
  "spine_constraints_upheld": [],
  "files_changed": [],
  "tests_run": [{"cmd": "", "exit": 0, "hash": ""}],
  "acceptance": [{"clause": "", "status": "PASS|FAIL|UNVERIFIED"}],
  "open_blockers": [],
  "dissent_carried_forward": [],
  "discard_from_active_context": []
}
```

Active context keeps only:

- spine lock
- current wave
- unresolved blockers and dissent
- completed-wave summaries
- lessons.json

Archive stale evidence and candidate cards under the run directory; do not keep them in chat context.

## Failure fingerprints

Normalize repeated failures as:

```text
cmd|exit|first_error_line|touched_paths_hash
```

Rules:

- append each failure to `events.jsonl`
- two identical fingerprints in one wave trigger rollback to the wave checkpoint
- after rollback, open a user gate instead of another automatic edit cycle

## Crash and tool failure

- Mid-wave tool/quorum failure: set wave status `blocked`, write recovery event, do not mark PASS
- Session loss: next invocation enters recovery mode using durable state
- Never invent missing state files
