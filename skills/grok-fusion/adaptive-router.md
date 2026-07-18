# Adaptive Router

Deterministic tier selection for every Grok Fusion run.

## Forced policy (this deployment)

**Always select `MVP` for every request.** Do not choose Quick, Standard, or Heavy as the selected tier.

**Maximum quality:** every request must run the full Heavy P0–P7 council via Task (`gf-worker`) after the runtime probe. No parent-only shortcut. No “label MVP without spine.” Short Q&A is not exempt.

Pipeline for every request:

1. Task probe per `runtime-contract.md` (fail closed on mismatch)
2. Full Heavy P0–P7 spine (framing → evidence → candidates → selection → minority → falsify/revise → verify) for every answer-track and build-track request
3. PR/FAQ working-backwards pass when product/build intent is present
4. Discovery wave when modules will be touched
5. Epic/wave DAG when multi-step work is required
6. Autonomous wave loop with G0–G4 safety gates for mutating work

Output: full Heavy-depth verdict under footer `Fusion tier: MVP`. When implementing, also write durable state under `.grok-fusion/runs/<run-id>/`.

Answer-track Q&A still runs steps 1–2 fully; skip durable wave machinery only when no implementation was requested. Never skip the Heavy spine.

## Tiers (reference only — not selected in this deployment)

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
- **this deployment: every request**

Pipeline:

1. Heavy once for the architecture/product spine
2. Discovery wave
3. Epic/wave DAG
4. Autonomous wave loop with G0–G4 safety gates

Output: wave/MVP progress with durable state under `.grok-fusion/runs/<run-id>/`, plus `Fusion tier: MVP`.

## Escalation

In this deployment there is no upward escalation: the tier is already MVP.

Never silently label a lighter tier.

## Forced tiers

- Every request → `MVP` + mandatory full Heavy P0–P7 Task spine
- `/grok-fusion` with any wording → `MVP` + mandatory full Heavy P0–P7 Task spine
- Explicit Quick/Standard/Heavy requests are remapped to this maximum MVP policy
- Parent-only or simulated-council replies must not use the Fusion footer; say Fusion did not run instead
