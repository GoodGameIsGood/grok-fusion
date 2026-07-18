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
- for mutating/MVP: multi-pass consensus, `closure: CONFIRMED` when the closure gate is on, and repo-native test evidence (multi-pass alone cannot raise confidence to `high` without tests)

Do not use the model’s self-reported confidence percentage.

## Devil's advocate pass

Before answering:

- **Readonly answer track** (Quick/Standard/Heavy/MVP with no edits): run one adversarial pass whose only goal is to prove the answer wrong.
  - Quick: the parent argues against its own answer inline (strongest counterargument plus one concrete failure scenario). WHEN tier is Quick, do not launch a dedicated provocation Task; parent-inline DA only (see [provocation-contract.md](provocation-contract.md)).
  - Standard/Heavy/MVP answer track: one dedicated `gf-worker` call receives the draft answer and evidence pack, and must return the strongest evidence-backed objection, one checkable failure scenario, and one cheaper alternative. Cite [provocation-contract.md](provocation-contract.md) for assumption/lateral challenge quality; do not stamp identical operator boilerplate into Error Hunt #1.
  - A checkable flaw triggers at most one revision; an unresolved objection is reported as dissent with lowered confidence. Never suppress the objection.
- **Planning or mutating track**: do **not** rely on this single-revision DA alone. Run the full [multi-pass-verification.md](multi-pass-verification.md) pipeline through Phase E (devil’s-advocate pressure is folded into Error Hunt #1 or a pre-panel falsifier; final confirmation is Phase E). Planning/mutating “at most one revision” does **not** apply; use multi-pass repair budgets instead.

## Final confirmation (answer track)

When project config `closure.require_final_confirmation` is true, after the devil’s advocate pass and pre-answer checklist:

1. Build a lightweight `done_evidence` for the answer (`request_restatement`, checks, `unknowns`, `open_dissent`).
2. Run one readonly `gf-reviewer` or `gf-worker` with prompt tag `final_confirmation` against the draft answer + evidence only (no parent self-praise).
3. Require:

```yaml
mode: final_confirmation
verdict: CONFIRMED|FOUND_ISSUES
falsify_attempt: ""
checks_performed: []
blockers: []
```

4. `FOUND_ISSUES` → at most one revision, then lower confidence if still unresolved. Never claim `high` confidence without `closure: CONFIRMED`.
5. Empty «всё идеально» / «багов нет» without checks is invalid when `closure.forbid_empty_perfect` is true.

## Pre-answer checklist

- [ ] Full eligible pipeline ran, or Fusion explicitly did not run
- [ ] Spine is one coherent proposal
- [ ] Incompatible alternatives were not averaged
- [ ] Evidence-backed dissent is preserved
- [ ] Architecture tasks include ATAM-lite scenarios and rejected alternatives
- [ ] No workspace mutation occurred on the answer track
- [ ] Uncertainty labels are present where evidence is weak
- [ ] If planning was required, plan quality gate is PASS, multi-pass consensus is PASS, `closure: CONFIRMED` when gate on, and plan dissent is resolved or reported
- [ ] If mutation ran, multi-pass consensus is PASS, `closure: CONFIRMED` when gate on (wave/one-shot; epic/product 5/5 when applicable)
- [ ] Devil's advocate pass ran (answer track) or multi-pass error hunt covered adversarial pressure (planning/mutating), and objections are resolved or reported
- [ ] Final confirmation ran when required; `falsify_attempt` and `checks_performed` are nonempty
- [ ] External claims carry `retrieved_at` per `freshness-contract.md`
- [ ] C2+ external claims are live-verified or labeled SPECULATIVE/INSUFFICIENT (no silent bare assertions)
- [ ] C2+ claims cite researcher `evidence_id`s; no unlabeled memory facts in the final answer
- [ ] P2b freshness_critic ran when required (Heavy/MVP always; Standard when C2+ or web/registry/docs/changelog/lockfile records)

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
