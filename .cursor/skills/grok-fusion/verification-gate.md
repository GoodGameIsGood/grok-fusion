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
- for mutating/MVP: multi-pass consensus and repo-native test evidence (multi-pass alone cannot raise confidence to `high` without tests)

Do not use the model’s self-reported confidence percentage.

## Devil's advocate pass

Before answering:

- **Readonly answer track** (Quick/Standard/Heavy/MVP with no edits): run one adversarial pass whose only goal is to prove the answer wrong.
  - Quick: the parent argues against its own answer inline (strongest counterargument plus one concrete failure scenario).
  - Standard/Heavy/MVP answer track: one dedicated `gf-worker` call receives the draft answer and evidence pack, and must return the strongest evidence-backed objection, one checkable failure scenario, and one cheaper alternative.
  - A checkable flaw triggers at most one revision; an unresolved objection is reported as dissent with lowered confidence. Never suppress the objection.
- **Planning or mutating track**: do **not** rely on this single-revision DA alone. Run the full [multi-pass-verification.md](multi-pass-verification.md) pipeline (devil’s-advocate pressure is folded into Error Hunt #1 or a pre-panel falsifier). Planning/mutating “at most one revision” does **not** apply; use multi-pass repair budgets instead.

## Pre-answer checklist

- [ ] Full eligible pipeline ran, or Fusion explicitly did not run
- [ ] Spine is one coherent proposal
- [ ] Incompatible alternatives were not averaged
- [ ] Evidence-backed dissent is preserved
- [ ] Architecture tasks include ATAM-lite scenarios and rejected alternatives
- [ ] No workspace mutation occurred on the answer track
- [ ] Uncertainty labels are present where evidence is weak
- [ ] If planning was required, plan quality gate is PASS, multi-pass consensus is PASS, and plan dissent is resolved or reported
- [ ] If mutation ran, multi-pass consensus is PASS for the wave/one-shot (and epic/product 5/5 when applicable)
- [ ] Devil's advocate pass ran (answer track) or multi-pass error hunt covered adversarial pressure (planning/mutating), and objections are resolved or reported
- [ ] External claims carry `retrieved_at` per `freshness-contract.md`

If the checklist fails on the **answer track**, run at most one revision pass, then answer with lowered confidence rather than inventing certainty. If it fails on **planning/mutating**, continue multi-pass repair within budgets or fail closed / user gate — never claim done.

## Final output order

1. Verdict
2. Evidence
3. Decision or ADR
4. Validation
5. Risks
6. Panel dissent
7. Confidence basis

Follow the user’s language.
