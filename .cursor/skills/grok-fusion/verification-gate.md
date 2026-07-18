# Verification Gate

Final gate before answering the user. Prefer tools over verbal checking.

## Required checks

| Claim type | Preferred verification |
|---|---|
| Code or math | Tests, typecheck, static analysis, or executable examples that already exist or are created only on the implementation track |
| Current facts | Primary-source retrieval and independent corroboration |
| Architecture | ATAM scenarios, sensitivity/tradeoff points, migration/rollback, fitness functions |
| Unverifiable claims | Explicit `INSUFFICIENT` or `SPECULATIVE` labels |

## Confidence basis

Final confidence is `high`, `medium`, or `low`. Derive it from observable signals only:

- evidence coverage
- selector stability after position swaps
- unresolved critical risks
- tool or test verification
- framing stability

Do not use the model’s self-reported confidence percentage.

## Devil's advocate pass

Before answering, at every tier, run one adversarial pass whose only goal is to prove the answer wrong:

- Quick: the parent argues against its own answer inline (strongest counterargument plus one concrete failure scenario).
- Standard/Heavy/MVP: one dedicated `gf-worker` call receives the draft answer and evidence pack, and must return the strongest evidence-backed objection, one checkable failure scenario, and one cheaper alternative.
- A checkable flaw triggers one revision; an unresolved objection is reported as dissent with lowered confidence. Never suppress the objection.

## Pre-answer checklist

- [ ] Full eligible pipeline ran, or Fusion explicitly did not run
- [ ] Spine is one coherent proposal
- [ ] Incompatible alternatives were not averaged
- [ ] Evidence-backed dissent is preserved
- [ ] Architecture tasks include ATAM-lite scenarios and rejected alternatives
- [ ] No workspace mutation occurred on the answer track
- [ ] Uncertainty labels are present where evidence is weak
- [ ] If planning was required, plan quality gate is PASS and devil's advocate on the plan is resolved or reported
- [ ] Devil's advocate pass ran and its objection is resolved or reported
- [ ] External claims carry `retrieved_at` per `freshness-contract.md`

If the checklist fails, run at most one revision pass. Then answer with lowered confidence rather than inventing certainty.

## Final output order

1. Verdict
2. Evidence
3. Decision or ADR
4. Validation
5. Risks
6. Panel dissent
7. Confidence basis

Follow the user’s language.
