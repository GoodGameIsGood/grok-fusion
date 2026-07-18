# Adaptive Router

Deterministic tier selection for every Grok Fusion run.

## Read project config before tier

Load [project-config.md](project-config.md) and `.grok-fusion/config.json` (or plugin defaults) **before** choosing a tier. Precedence: in-chat override > project config > defaults.

## Profile application

### quality_profile: max (or tier_policy: force_mvp)

- Select `MVP` for every request.
- Run Task probe, then full Heavy P0–P7 spine on answer and build tracks.
- No parent-only shortcut. No “label MVP without spine.”
- Footer: `Fusion tier: MVP`.
- Mutating paths also write durable state under `.grok-fusion/runs/<run-id>/`.
- Explicit Quick/Standard/Heavy in-chat requests are remapped to this max policy unless the user changes project config.

### quality_profile: balanced (default when no config)

Use the tier rules below (Quick / Standard / Heavy / MVP).

### quality_profile: fast

Prefer Quick/Standard from the rules below. Do not escalate to Heavy/MVP unless triggers clearly match (architecture, security, migration, multi-wave). Answer track may skip full Heavy spine when `allow_quick_shortcut` is true.

## Tiers

### Quick

Use when all are true (and profile is not `max`):

- goal is clear
- work is local, reversible, and low-risk
- single-step or single-file, or a tiny explanation/edit
- no architecture choice, migration, security boundary, or multi-module redesign
- `answer_track.allow_quick_shortcut` is true (balanced/fast)

Pipeline:

1. Parent solves directly.
2. One isolated `gf-worker` verifier checks correctness and missed edge cases.
3. Return a direct answer.

Target: 1–2 subagent calls.

Output: direct answer plus `Fusion tier: Quick`.

### Standard

Use when (and profile is not `max`):

- moderate ambiguity
- ordinary debugging, research, comparison, or 2–8 file changes
- not an architecture/security/migration decision
- not a multi-wave MVP

Pipeline:

1. One framing call
2. One evidence scout
3. Three isolated candidates from the selected task pack
4. Two absolute-score judges
5. One verifier/revision pass

Target: 7–8 subagent calls.

Output: Verdict, Evidence, Risks, then `Fusion tier: Standard`.

### Heavy

Use when any is true (and profile is not `max`):

- architecture or ATAM-level design
- security, auth, permissions, or threat modeling
- migration or destructive data change
- cross-module / high-stakes decision
- large brownfield refactor or framework/library migration in one batch
- user explicitly asks for deep analysis or `/grok-fusion` Heavy behavior
- `answer_track.require_heavy_spine` is true for this answer-track request

Pipeline: full P0–P7 from `SKILL.md` (~24 calls).

Output: full seven-section report plus `Fusion tier: Heavy`.

### MVP

Use when any is true:

- `quality_profile` is `max` or `tier_policy` is `force_mvp`
- user asks to build a product, MVP, or large feature set
- work spans more than one wave or two top-level modules
- resumable long-horizon implementation is required
- a refactor or migration spans multiple waves and needs durable state

Pipeline:

1. Heavy once for the architecture/product spine (always on `max`)
2. Discovery wave when modules will be touched
3. Epic/wave DAG when multi-step work is required
4. Autonomous wave loop with G0–G4 safety gates for mutating work

Output: wave/MVP progress with durable state under `.grok-fusion/runs/<run-id>/`, plus `Fusion tier: MVP`.

## Escalation

Escalate Quick → Standard → Heavy → MVP when new evidence shows higher stakes. Never silently label a lighter tier than the work performed.

On `max` / `force_mvp` there is no downward tier: stay on MVP + Heavy spine.

## Forced tiers (config-driven)

- `max` / `force_mvp` → every request uses `MVP` + mandatory full Heavy P0–P7 Task spine
- Parent-only or simulated-council replies must not use the Fusion footer; say Fusion did not run instead
- Mutating work always requires multi-pass specialist consensus regardless of profile (profile only changes answer-track depth)
