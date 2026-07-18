# Project Config

Per-project knobs for Grok Fusion. Parent **must** load this in P0 before tier selection.

## Location

```text
.grok-fusion/config.json
```

Tracked in git when present. Durable runs stay under `.grok-fusion/runs/` (local / excluded).

## Precedence

1. Explicit in-chat user override (e.g. “use Quick Fusion”)
2. Project `.grok-fusion/config.json`
3. Plugin defaults below

## Defaults (no config file)

```json
{
  "schema_version": 1,
  "quality_profile": "balanced",
  "tier_policy": "adaptive",
  "answer_track": {
    "require_heavy_spine": false,
    "allow_quick_shortcut": true
  },
  "multi_pass": {
    "max_optional_specialists": 3,
    "verify_hard_gate": true,
    "require_selection_record": true
  },
  "budgets": {
    "max_fix_cycles": 6,
    "max_consensus_rounds": 5,
    "max_task_calls_per_wave": 40,
    "max_task_calls_per_epic": 200,
    "discovery_max_files": 40
  },
  "lessons": {
    "inject_recurring": true,
    "min_lessons_on_defect": 1
  },
  "telemetry": {
    "footer_stats": true
  },
  "preferred_specialists": [],
  "disabled_specialists": []
}
```

## Schema

| Field | Values | Meaning |
|---|---|---|
| `quality_profile` | `fast` \| `balanced` \| `max` | Depth profile |
| `tier_policy` | `adaptive` \| `force_mvp` | How tiers are chosen |
| `answer_track.require_heavy_spine` | bool | Full Heavy P0–P7 on answer track |
| `answer_track.allow_quick_shortcut` | bool | Parent-only Quick allowed |
| `multi_pass.max_optional_specialists` | 0–3 | Cap optional Phase D roles |
| `multi_pass.verify_hard_gate` | bool | Require successful `verify_cmd` before done |
| `multi_pass.require_selection_record` | bool | Require `optional_selection` on multi_pass |
| `budgets.*` | ints | Soft caps (exhaust → `blocked`, never PASS) |
| `lessons.inject_recurring` | bool | Inject recurring lessons into reviewer prompts |
| `telemetry.footer_stats` | bool | Extend Fusion footer with profile/stats |
| `preferred_specialists` | role ids | Prefer when triggers tie |
| `disabled_specialists` | role ids | Never select |

## Profiles

### fast

- Router may pick Quick/Standard.
- Answer track: no mandatory Heavy spine; Quick shortcut allowed when router says Quick.
- Mutating work still requires multi-pass specialist consensus (cannot SHIP without panel).
- `verify_hard_gate` may be false only for pure answer track.

### balanced

- Full adaptive router (Quick / Standard / Heavy / MVP).
- MVP durable state only when router selects MVP.
- Mutating/plan: multi-pass + verify hard gate on.

### max

- Effective tier label `MVP` every request.
- `tier_policy` should be `force_mvp`.
- Full Heavy P0–P7 Task spine on every answer and build request.
- Mutating + plan: full multi-pass; verify hard gate on.
- No Quick/Standard/Heavy footers.

## Read project config before tier

Parent algorithm:

```text
1. Load .grok-fusion/config.json if present; else use defaults.
2. Apply quality_profile / tier_policy from config.
3. Apply in-chat override if any (unless profile is max and user did not ask to change config).
4. Select tier per adaptive-router.md.
5. Record effective profile + tier in RunEnvelope / run.json when durable.
```
