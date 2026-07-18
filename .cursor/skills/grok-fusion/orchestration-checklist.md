# Orchestration Checklist

One-page parent path. Deep contracts stay linked; do not invent a parallel pipeline.

```text
P0  Load project-config.md + .grok-fusion/config.json (or defaults)
    → adaptive-router.md (tier from quality_profile)
    → task-packs.md (visual UI → pack visual-ui; may load grok-design + grok-web-ui;
      AppSec-primary → pack appsec-review; load grok-security + security-playbook.md)
    → Host: Cursor Task tool or Grok task/spawn_subagent (see runtime-contract host matrix)
    → Task probe when Standard/Heavy/MVP (fail closed if host subagents unavailable)
    → Agent IDs: Cursor `gf-*` ; Grok Build prefer `grok-fusion:gf-*` (verified)

P1+ Answer track: SKILL Heavy/Standard/Quick spine as selected
    One tool-message batch per phase (P2a/P2b split); never inline-simulate gf-* roles
    P2a: gf-researcher-repo + gf-researcher-web; P2b: gf-worker freshness_critic
    Plan needed? → planning-contract.md until plan_quality + multi_pass PASS
    Debug pack? → debugging-playbook.md (Repair Card before any edit)
    AppSec pack? → security-playbook.md (Finding Cards; Remediation Card before any edit)
    Mutating? → implementation-track.md (parent edits only)
    Provocation: dual-provocation lens + provocation-contract.md (Δtasks=0);
      WHEN tier is Quick, do not launch a dedicated provocation Task; parent-inline DA only

Verify  Run verify_cmd; record verification_runs (verify hard gate)
        Debug: characterization + blast-radius suite before multi-pass

Multi   multi-pass-verification.md
        A step_recheck → B hunts → C gf-auditor → selection (specialist-roster.md /
        select_optional_specialists.py) → D core5 + ≤3 optional
        Inject lessons.json when lessons.inject_recurring
        Mid-gate Task loss → blocked; do not mark PASS

Close   done_evidence pack → must-not-break walkthrough → Phase E blind final_confirmation
        → closure: CONFIRMED (required before user-facing done)

Done    consensus PASS + closure CONFIRMED + verify gate + no open blockers
Footer  Fusion tier: <actual> [| profile=… | tasks=… | multi_pass=… | verify=… | closure=…]
        MVP blocked/budget: also emit run_id, blocked_reason, remaining task_calls vs caps,
        and the exact next utterance `Continue run <run_id>`
Resume  Continue run <run_id> → recovery-track.md
Epic split  Tripwires (>80% epic Task budget, >5 waves, G4) → child epic inherits spine_id;
            block/finish parent first; emit run_id + blocked_reason + Continue run <id>
            Details: epic-track.md § Epic split UX
```

## Deep links

| Need | File |
|---|---|
| Config / profiles | [project-config.md](project-config.md) |
| Tiers | [adaptive-router.md](adaptive-router.md) |
| Runtime / parallelism | [runtime-contract.md](runtime-contract.md) |
| Freshness | [freshness-contract.md](freshness-contract.md) |
| Planning | [planning-contract.md](planning-contract.md) |
| Debugging | [debugging-playbook.md](debugging-playbook.md) |
| AppSec | [security-playbook.md](security-playbook.md); sibling skill `grok-security` |
| Implementation | [implementation-track.md](implementation-track.md) |
| Multi-pass / Phase E | [multi-pass-verification.md](multi-pass-verification.md) |
| Answer closure | [verification-gate.md](verification-gate.md) |
| Provocation / dual-provocation | [provocation-contract.md](provocation-contract.md), [candidate-lenses.md](candidate-lenses.md) |
| Specialists | [specialist-roster.md](specialist-roster.md), [specialist-evidence-packs.md](specialist-evidence-packs.md) |
| Visual UI craft | sibling skills `grok-design`, `grok-web-ui` (not Fusion contracts) |
| AppSec craft | sibling skill `grok-security` (not Fusion contracts; Option B copy) |
| Discovery | [discovery-track.md](discovery-track.md) |
| Durable MVP | [long-horizon-contract.md](long-horizon-contract.md) |
| Recovery | [recovery-track.md](recovery-track.md) |
| MVP product | [mvp-playbook.md](mvp-playbook.md), [epic-track.md](epic-track.md) |
