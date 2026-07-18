# Orchestration Checklist

One-page parent path. Deep contracts stay linked; do not invent a parallel pipeline.

```text
P0  Load project-config.md + .grok-fusion/config.json (or defaults)
    → adaptive-router.md (tier from quality_profile)
    → task-packs.md (visual UI → pack visual-ui; may load grok-design + grok-web-ui)
    → Task probe when Standard/Heavy/MVP

P1+ Answer track: SKILL Heavy/Standard/Quick spine as selected
    Plan needed? → planning-contract.md until plan_quality + multi_pass PASS
    Debug pack? → debugging-playbook.md (Repair Card before any edit)
    Mutating? → implementation-track.md (parent edits only)

Verify  Run verify_cmd; record verification_runs (verify hard gate)
        Debug: characterization + blast-radius suite before multi-pass

Multi   multi-pass-verification.md
        A step_recheck → B hunts → C gf-auditor → selection (specialist-roster.md /
        select_optional_specialists.py) → D core5 + ≤3 optional
        Inject lessons.json when lessons.inject_recurring

Close   done_evidence pack → must-not-break walkthrough → Phase E blind final_confirmation
        → closure: CONFIRMED (required before user-facing done)

Done    consensus PASS + closure CONFIRMED + verify gate + no open blockers
Footer  Fusion tier: <actual> [| profile=… | tasks=… | multi_pass=… | verify=… | closure=…]
Resume  Continue run <run_id> → recovery-track.md
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
| Implementation | [implementation-track.md](implementation-track.md) |
| Multi-pass / Phase E | [multi-pass-verification.md](multi-pass-verification.md) |
| Answer closure | [verification-gate.md](verification-gate.md) |
| Specialists | [specialist-roster.md](specialist-roster.md), [specialist-evidence-packs.md](specialist-evidence-packs.md) |
| Visual UI craft | sibling skills `grok-design`, `grok-web-ui` (not Fusion contracts) |
| Discovery | [discovery-track.md](discovery-track.md) |
| Durable MVP | [long-horizon-contract.md](long-horizon-contract.md) |
| Recovery | [recovery-track.md](recovery-track.md) |
| MVP product | [mvp-playbook.md](mvp-playbook.md), [epic-track.md](epic-track.md) |
