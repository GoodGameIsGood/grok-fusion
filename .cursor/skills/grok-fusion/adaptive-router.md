# Adaptive Router

Deterministic tier selection for every Grok Fusion run. Choose exactly one tier before acting.

## Tiers

### Quick

Use when all are true:

- goal is clear
- work is local, reversible, and low-risk
- single-step or single-file, or a tiny explanation/edit
- no architecture choice, migration, security boundary, or multi-module redesign

Pipeline:

1. Parent solves directly.
2. One isolated `gf-worker` verifier checks correctness and missed edge cases.
3. Return a direct answer.

Target: 1–2 subagent calls.

Output: direct answer plus `Fusion tier: Quick`.

### Standard

Use when:

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

Use when any is true:

- architecture or ATAM-level design
- security, auth, permissions, or threat modeling
- migration or destructive data change
- cross-module / high-stakes decision
- large brownfield refactor or framework/library migration in one batch
- user explicitly asks for deep analysis or `/grok-fusion` Heavy behavior

Pipeline: full P0–P7 from `SKILL.md` (~24 calls).

Output: full seven-section report plus `Fusion tier: Heavy`.

### MVP

Use when any is true:

- user asks to build a product, MVP, or large feature set
- work spans more than one wave or two top-level modules
- resumable long-horizon implementation is required
- a refactor or migration spans multiple waves and needs durable state

Pipeline:

1. Heavy once for the architecture/product spine
2. Discovery wave
3. Epic/wave DAG
4. Autonomous wave loop with G0–G4 safety gates

Output: wave/MVP progress with durable state under `.grok-fusion/runs/<run-id>/`, plus `Fusion tier: MVP`.

## Escalation

Escalate to a deeper tier when:

- unknowns block a correct Quick answer
- Standard candidates disagree on a safety/architecture point
- implementation scope grows beyond the current tier assumptions

Never silently escalate while still labeling the lighter tier.

## Forced tiers

- `/grok-fusion heavy ...` or explicit “deep analysis” → Heavy
- `/grok-fusion mvp ...` or “build the MVP” → MVP
- `/grok-fusion quick ...` → Quick
- bare `/grok-fusion` without override → router decides, defaulting upward on ambiguity
