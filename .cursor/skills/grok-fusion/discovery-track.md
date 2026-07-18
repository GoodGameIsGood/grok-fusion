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

1. Set `read_budget.max_files` from project config `budgets.discovery_max_files` (default 40) per discovery wave and record every read. Never “read everything.”
2. Build a symbol/path map for owned modules before plan edits: entry points, public interfaces, tests, then implementations.
3. Rank targets: entry points, build/CI files, public interfaces of owned modules, then implementations.
4. Read interfaces and contracts before implementations.
5. Use dependency edges and test locations to pick the next read, not alphabetical order.
6. When the budget is spent, list remaining gaps in `unknowns_queue` instead of guessing.
7. Ungrounded paths in plans (not present in discovery coverage or evidence) → plan quality FAIL.

## Debug blast-radius mode

When pack is `debugging` and `debugging.blast_radius_discovery` is true:

1. Use `debugging.discovery_max_files_debug` (default 80) as `read_budget.max_files` instead of the normal discovery cap.
2. Ranked reads: failure site → callers → tests → contracts/APIs → adjacent modules.
3. Build a symbol/path map of the blast radius before any edit; list it on the Repair Card as `blast_radius_paths`.
4. Do not edit paths that remain `UNREAD` in coverage targets.
