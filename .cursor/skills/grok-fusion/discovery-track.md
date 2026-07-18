# Discovery Track

Wave 0 for MVP and any Standard/Heavy run that must touch unread modules.

## Goal

Map only the modules needed for the current spine. Never invent unread APIs, paths, packages, schemas, or commands.

## discovery.json schema

```json
{
  "schema_version": 1,
  "coverage_targets": [
    {
      "module": "",
      "required_reads": [],
      "status": "UNREAD|PARTIAL|READ",
      "evidence_ids": []
    }
  ],
  "verification_commands": [
    {
      "cmd": "",
      "source": "VERIFIED",
      "source_path": ""
    }
  ],
  "ignored_or_large_file_risks": [],
  "apis_and_contracts": [],
  "migrations": [],
  "external_dependencies": [],
  "unknowns_queue": [],
  "read_budget": {"max_files": 0, "files_read": 0},
  "complete": false
}
```

## Required discovery work

- module topology and ownership boundaries
- existing tests and repository-native verification commands
- build/start/deploy commands that actually exist
- relevant `.cursor/rules`, `AGENTS.md`, and project constraints
- ignored, invisible, or oversized files that could hide truth
- public/internal APIs, data models, and migrations
- external services and credentials boundaries

## Coverage gate

Implementation must not edit a module whose required discovery targets are `UNREAD`.

`PARTIAL` is allowed only for explicitly accepted unknowns recorded in `unknowns_queue`.

## Worker rules

- Use readonly `gf-worker` scouts.
- Output only discovery deltas and evidence records.
- Do not recommend product or architecture solutions in discovery.
- Re-enter discovery when a later wave owns a module that is still `UNREAD`.

## Large repository strategy

For repositories too large to read fully, discovery is budgeted and ranked:

1. Set `read_budget.max_files` per discovery wave and record every read.
2. Rank targets: entry points, build/CI files, public interfaces of owned modules, then implementations.
3. Read interfaces and contracts before implementations.
4. Use dependency edges and test locations to pick the next read, not alphabetical order.
5. When the budget is spent, list remaining gaps in `unknowns_queue` instead of guessing.
