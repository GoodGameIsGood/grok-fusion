---
name: grok-fusion
description: Adaptive same-model Grok council for simple tasks, architecture, research, debugging, MVP builds, and expensive decisions. Auto-routed by grok-fusion-auto; also invokable as /grok-fusion.
---

# Grok Fusion

Adaptive deliberation skill. Do not redesign this pipeline.

## Before any phase

Read [grok-harness.md](grok-harness.md), [runtime-contract.md](runtime-contract.md), [freshness-contract.md](freshness-contract.md), and [adaptive-router.md](adaptive-router.md). Choose a task pack from [task-packs.md](task-packs.md).

## Five Iron Rules

1. Run the full eligible pipeline or state that Fusion did not run.
2. Every substantive claim has evidence or an uncertainty label.
3. Select one coherent spine; never average incompatible designs.
4. Preserve evidence-backed dissent and minority warnings.
5. Do not mutate the workspace unless implementation was explicitly requested.

## Orchestration

Use the Cursor Task tool targeting custom agent `gf-worker` for isolated phase work. Use `gf-reviewer` after edits and `gf-auditor` on MVP wave acceptance. Launch all calls for one phase in one parallel tool-message batch. Keep `fusion_depth=1`. Never simulate subagents inline.

For Standard, Heavy, and MVP: run one Task probe first. If the subagent model badge is not Grok, fail closed.

Never write a Quick/Standard/Heavy `RunEnvelope` to disk. MVP durable state follows [long-horizon-contract.md](long-horizon-contract.md).

### P0 — Preflight

- Preserve the original query verbatim.
- Choose tier from [adaptive-router.md](adaptive-router.md): `Quick | Standard | Heavy | MVP`.
- Classify task pack from [task-packs.md](task-packs.md).
- Choose `answer track` unless the user explicitly requested mutation or an MVP/build path.
- Confirm Task/custom subagents for Standard/Heavy/MVP; otherwise fail closed.
- Initialize an in-memory `RunEnvelope` with `tier`, `track`, and `fusion_depth=1`.

### Quick

Parent solves. One optional `gf-worker` verifier. Direct answer. Footer: `Fusion tier: Quick`.

### Standard

1. One framing call
2. One scout
3. Three pack lenses as candidates
4. Two judges
5. One verifier

Output: Verdict, Evidence, Risks. Footer: `Fusion tier: Standard`.

### Heavy — P1 to P7

#### P1 — Framing x3

Read [framing-and-evidence.md](framing-and-evidence.md). Three parallel framers. Build the `canonical brief`.

#### P2 — Evidence x2

Two parallel scouts. Atomic evidence records only. Never invent unread APIs or paths. Apply [freshness-contract.md](freshness-contract.md): live verification, dated records.

#### P3 — Candidates

Read [candidate-lenses.md](candidate-lenses.md) and [candidate-card.md](candidate-card.md). Architecture tasks also read [architecture-playbook.md](architecture-playbook.md). Launch pack-selected isolated candidates. Quorum: at least 6 of 8 after one retry when using eight lenses; for narrower packs require at least 2 of 3.

#### P4 — Selection

Read [selector.md](selector.md). Absolute scores, Top-3, position-swapped pairwise, one `spine`. Judge quorum: at least 4 of 5 when using five judges; for Standard use both judges.

#### P5 — Minority sentinel

Read [minority-sentinel.md](minority-sentinel.md). Overturn only for new evidence or a checkable fatal flaw.

#### P6 — Falsify and revise

Read [falsify-and-revise.md](falsify-and-revise.md). One revision maximum.

#### P7 — Verify and answer

Read [verification-gate.md](verification-gate.md). Full seven-section output. Footer: `Fusion tier: Heavy`.

### MVP

0. PR/FAQ working-backwards pass per [mvp-playbook.md](mvp-playbook.md) before the Heavy spine
1. Heavy once for the product/architecture spine
2. Discovery via [discovery-track.md](discovery-track.md)
3. Epic/wave DAG via [epic-track.md](epic-track.md) and [mvp-playbook.md](mvp-playbook.md)
4. Autonomous waves via [implementation-track.md](implementation-track.md), [long-horizon-contract.md](long-horizon-contract.md), and [recovery-track.md](recovery-track.md)
5. Wave retros append to `lessons.json`; final epic ends with a user-zero walkthrough

Footer: `Fusion tier: MVP`.

## Implementation track

If mutation was requested, read [implementation-track.md](implementation-track.md). Only the parent edits. Then run repository-native verification, reviewers, and for MVP waves the auditor.

## Fail closed

If tools, model inheritance, quorum, or schema requirements fail, say that Fusion did not run. Never return a solo answer as Fusion.

## Examples

See [examples.md](examples.md).
