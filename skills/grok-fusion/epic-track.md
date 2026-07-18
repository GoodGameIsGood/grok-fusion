# Epic Track

Acyclic epic and wave DAG for MVP execution.

## dag.json schema

```json
{
  "schema_version": 1,
  "epics": [
    {
      "id": "",
      "goal": "",
      "definition_of_done": [],
      "waves": [
        {
          "id": "",
          "depends_on": [],
          "owns_paths": [],
          "reads_paths": [],
          "forbidden_paths": [],
          "produces": [],
          "test_commands": [],
          "acceptance_clause_ids": [],
          "rollback": {
            "git_ref": "",
            "revert_steps": []
          },
          "status": "pending|active|blocked|complete",
          "gates_required": []
        }
      ]
    }
  ]
}
```

## Planning rules

- DAG must be acyclic.
- Exactly one active write owner per path prefix.
- Overlapping `owns_paths` across active waves is forbidden.
- `depends_on` must reference existing wave ids.
- Wave 0 is discovery when required by `discovery-track.md`.
- Prefer vertical-slice waves over horizontal layer waves.

## Ownership rules

- Parent may write only the active wave `owns_paths`.
- Workers may read `reads_paths` and never write.
- Touching `forbidden_paths` is a hard stop.
- Before a wave starts, the git tree must be clean or a user gate must accept a dirty tree.

## Execution rule

Do not start wave N+1 until:

- all dependencies are `complete`
- every mandatory acceptance clause for wave N is `PASS`
- discovery coverage for owned modules is satisfied

Violation is fail closed, not “mostly done.”

## Planner/reviewer flow

1. One `gf-worker` produces the initial DAG after the Heavy spine and discovery.
2. One readonly reviewer audits acyclicity, ownership overlap, missing tests, and unsafe migrations.
3. Gate G0 must approve scope before the first mutating wave.

## Epic integration check

When the last wave of an epic completes:

1. Run the full verified test/build command set from `discovery.json`, not only wave-scoped checks.
2. Launch one `gf-auditor` call with a mandatory spine-conformance clause: the implemented code still satisfies `spine.json` invariants and boundaries.
3. A FAIL or UNVERIFIED spine-conformance clause blocks the next epic.
4. On the final epic, add a user-zero walkthrough: one `gf-reviewer` call follows the documented quickstart and demo command literally, as a first-time user, and fails the audit on any missing step, undocumented dependency, or broken command.
