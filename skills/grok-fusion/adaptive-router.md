# Adaptive Router

Deterministic tier selection for every Grok Fusion run.

## Forced policy (this deployment)

**Always select `MVP` for every request.** Do not choose Quick, Standard, or Heavy.

Pipeline for every request:

1. PR/FAQ working-backwards pass when product/build intent is present; for pure Q&A still run MVP durable planning lightly or escalate to full MVP when implementation begins
2. Heavy once for the architecture/product spine when a spine does not yet exist
3. Discovery wave when modules will be touched
4. Epic/wave DAG when multi-step work is required
5. Autonomous wave loop with G0–G4 safety gates for mutating work

Output: MVP progress with durable state under `.grok-fusion/runs/<run-id>/` when implementing, plus `Fusion tier: MVP`.

For short questions that need no durable state, still label `Fusion tier: MVP`, run the Heavy spine path for high-stakes answers, and keep fail-closed Task/probe rules.

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

- Every request → `MVP`
- `/grok-fusion` with any wording → `MVP`
- Explicit Quick/Standard/Heavy requests are remapped to `MVP` in this deployment
