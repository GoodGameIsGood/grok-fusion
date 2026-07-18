---
name: grok-fusion
description: Adaptive same-model Grok council for simple tasks, architecture, research, debugging, AppSec review, MVP builds, and expensive decisions. Auto-routed by grok-fusion-auto; also invokable as /grok-fusion.
---

# Grok Fusion

Adaptive deliberation skill. Do not redesign this pipeline.

## Before any phase

Read [project-config.md](project-config.md) and load `.grok-fusion/config.json` (or defaults). Then read [orchestration-checklist.md](orchestration-checklist.md) for the P0→done path. Deep contracts: [grok-harness.md](grok-harness.md), [runtime-contract.md](runtime-contract.md), [freshness-contract.md](freshness-contract.md), and [adaptive-router.md](adaptive-router.md). Choose a task pack from [task-packs.md](task-packs.md). If planning is mandatory, also read [planning-contract.md](planning-contract.md). Mutating or plan gates also read [multi-pass-verification.md](multi-pass-verification.md) and [specialist-roster.md](specialist-roster.md). Unconventional challenges use [provocation-contract.md](provocation-contract.md) with lens `dual-provocation` (Δtasks=0; WHEN tier is Quick, do not launch a dedicated provocation Task; parent-inline DA only).

## Five Iron Rules

1. Run the full eligible pipeline or state that Fusion did not run.
2. Every substantive claim has evidence or an uncertainty label.
3. Select one coherent spine; never average incompatible designs.
4. Preserve evidence-backed dissent and minority warnings.
5. Do not mutate the workspace unless implementation was explicitly requested.

## Orchestration

Use the host Task tool (Cursor Task tool, or Grok Build `task`/`spawn_subagent` — see [runtime-contract.md](runtime-contract.md) host matrix) targeting custom agent `gf-worker` (on Grok Build prefer `grok-fusion:gf-worker`) for framing, candidates, judges, and `mode=freshness_critic`. Use `gf-researcher-repo` / `gf-researcher-web` (Grok: `grok-fusion:gf-researcher-*`) for P2a evidence. Use `gf-reviewer` and `gf-auditor` for [multi-pass-verification.md](multi-pass-verification.md) on plans and mutating work. Launch all calls for one phase (or P2a/P2b sub-step) in one parallel tool-message batch. Keep `fusion_depth=1`. Never simulate subagents inline. If `gf-researcher-*` is unresolved after reload, fail closed.

For Standard, Heavy, and MVP: run one Task probe first. If host model authority is not Grok (Cursor badge / Grok visible model — self_report is weak only), fail closed.

Never write a Quick/Standard/Heavy `RunEnvelope` to disk. MVP durable state follows [long-horizon-contract.md](long-horizon-contract.md).

G1 auto-route: Cursor uses `rules/grok-fusion-auto.mdc`. On Grok Build, prove rules auto-fire via smoke; until then consumers may need Option C `AGENTS.md` (PARTIAL auto — do not claim FULL auto-parity).

### P0 — Preflight

- Preserve the original query verbatim.
- Read project config before tier ([project-config.md](project-config.md)); choose tier from [adaptive-router.md](adaptive-router.md).
- Classify task pack from [task-packs.md](task-packs.md). If pack is `debugging`, read [debugging-playbook.md](debugging-playbook.md) before any edit. If pack is `appsec-review`, read [security-playbook.md](security-playbook.md) and load craft `grok-security` (Finding Cards on audit; Remediation Card before any edit).
- If planning is mandatory per [planning-contract.md](planning-contract.md), select `professional-planning` and do not edit until plan quality gate and multi-pass consensus are `PASS`.
- Choose `answer track` unless the user explicitly requested mutation or an MVP/build path.
- Confirm Task/custom subagents for Standard/Heavy/MVP; otherwise fail closed.
- Initialize an in-memory `RunEnvelope` with `tier`, `track`, `quality_profile`, and `fusion_depth=1`.

### Quick

Parent solves. One optional `gf-worker` verifier. Direct answer. Footer: `Fusion tier: Quick`.

### Standard

1. One framing call
2. P2a researcher(s) by claim-surface (1 or both if mixed); optional P2b `gf-worker` freshness_critic
3. Three pack lenses as candidates
4. Two judges
5. One verifier

Output: Verdict, Evidence, Risks. Footer: `Fusion tier: Standard`.

### Heavy — P1 to P7

#### P1 — Framing x3

Read [framing-and-evidence.md](framing-and-evidence.md). Three parallel framers. Build the `canonical brief`.

#### P2 — Evidence (P2a + P2b)

P2a: `gf-researcher-repo` + `gf-researcher-web` in one parallel batch. Atomic evidence records only. Never invent unread APIs or paths. Apply [freshness-contract.md](freshness-contract.md): live verification, dated records, C0–C3.
P2b: sequential `gf-worker` `mode=freshness_critic` on the merged pack (`ACCEPT` / `REJECT_WITH_GAPS`) before P3.

#### P3 — Candidates

Read [candidate-lenses.md](candidate-lenses.md) and [candidate-card.md](candidate-card.md). Architecture tasks also read [architecture-playbook.md](architecture-playbook.md). When pack selects `dual-provocation`, also load [provocation-contract.md](provocation-contract.md). Launch pack-selected isolated candidates. Quorum: at least 6 of 8 after one retry when using eight lenses; for narrower packs require at least 2 of 3.

#### P4 — Selection

Read [selector.md](selector.md). Absolute scores, Top-3, position-swapped pairwise, one `spine`. Judge quorum: at least 4 of 5 when using five judges; for Standard use both judges.

#### P5 — Minority sentinel

Read [minority-sentinel.md](minority-sentinel.md). Overturn only for new evidence or a checkable fatal flaw.

#### P6 — Falsify and revise

Read [falsify-and-revise.md](falsify-and-revise.md). One revision maximum.

#### P7 — Verify and answer

Read [verification-gate.md](verification-gate.md). Include final confirmation when the closure gate is on. Full seven-section output. Footer: `Fusion tier: Heavy`.

### MVP

When the router (or `quality_profile: max`) selects MVP:

0. PR/FAQ working-backwards pass per [mvp-playbook.md](mvp-playbook.md) when product/build intent is present (before or with the Heavy spine)
1. Full Heavy P0–P7 for the product/architecture spine (mandatory on `max` for every request, including pure Q&A)
2. Discovery via [discovery-track.md](discovery-track.md) when modules will be touched
3. Executable plan via [planning-contract.md](planning-contract.md) must `PASS` (including multi-pass and `closure: CONFIRMED` when gate on) before the epic/wave DAG
4. Epic/wave DAG via [epic-track.md](epic-track.md) and [mvp-playbook.md](mvp-playbook.md) when multi-step work is required
5. Autonomous waves via [implementation-track.md](implementation-track.md), [multi-pass-verification.md](multi-pass-verification.md), [long-horizon-contract.md](long-horizon-contract.md), and [recovery-track.md](recovery-track.md) when mutating — through Phase E
6. Wave retros append to `lessons.json`; final epic ends with user-zero walkthrough and product-level multi-pass (5/5) with `closure: CONFIRMED`

Footer: `Fusion tier: MVP` (on `max`, never emit Quick/Standard/Heavy).

## Implementation track

If mutation was requested, read [implementation-track.md](implementation-track.md), [multi-pass-verification.md](multi-pass-verification.md), and [specialist-roster.md](specialist-roster.md). For debugging pack also follow [debugging-playbook.md](debugging-playbook.md) (Repair Card + characterization before edits). Only the parent edits. Then run repository-native verification and the multi-pass gate through Phase E (`done_evidence`, must-not-break walkthrough, blind `final_confirmation`, `closure: CONFIRMED`).

## Fail closed

If tools, model inheritance, quorum, or schema requirements fail, say that Fusion did not run. Never return a solo answer as Fusion.

Never claim done / fixed / high confidence without `closure: CONFIRMED` when the closure gate is on. Forbidden empty «всё идеально» / «багов нет» without checks when `forbid_empty_perfect` is true.

When `telemetry.footer_stats` is enabled, end with:

`Fusion tier: <tier> | profile=<profile> | tasks=<n> | multi_pass=<PASS|FAIL|n/a> | verify=<code|n/a> | closure=<CONFIRMED|PENDING|n/a>`

## Examples

See [examples.md](examples.md).
