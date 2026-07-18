# Orchestration Checklist

One-page parent path. Deep contracts stay linked; do not invent a parallel pipeline.

```text
P0  Load project-config.md + .grok-fusion/config.json (or defaults)
    → adaptive-router.md (tier from quality_profile)
    → task-packs.md
    → Task probe when Standard/Heavy/MVP

P1+ Answer track: SKILL Heavy/Standard/Quick spine as selected
    Plan needed? → planning-contract.md until plan_quality + multi_pass PASS
    Mutating? → implementation-track.md (parent edits only)

Verify  Run verify_cmd; record verification_runs (verify hard gate)

Multi   multi-pass-verification.md
        A step_recheck → B hunts → C gf-auditor → selection (specialist-roster.md /
        select_optional_specialists.py) → D core5 + ≤3 optional
        Inject lessons.json when lessons.inject_recurring

Done    consensus PASS + verify gate + no open blockers
Footer  Fusion tier: <actual> [| profile=… | tasks=… | multi_pass=… | verify=…]
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
| Implementation | [implementation-track.md](implementation-track.md) |
| Multi-pass | [multi-pass-verification.md](multi-pass-verification.md) |
| Specialists | [specialist-roster.md](specialist-roster.md), [specialist-evidence-packs.md](specialist-evidence-packs.md) |
| Discovery | [discovery-track.md](discovery-track.md) |
| Durable MVP | [long-horizon-contract.md](long-horizon-contract.md) |
| Recovery | [recovery-track.md](recovery-track.md) |
| MVP product | [mvp-playbook.md](mvp-playbook.md), [epic-track.md](epic-track.md) |
