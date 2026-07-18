# Provocation Contract

Plugin-wide unconventional pressure for Grok Fusion. Roles are prompt contracts on `gf-worker`, not Cursor agent files. Do not add `agents/gf-*.md` for provocation.

## Two challenge kinds

| Kind | Duty |
|---|---|
| `assumption_attack` | Attack a load-bearing premise with a checkable question |
| `lateral_analogy` | Offer a cross-domain analogy or lateral cut that would change the decision |

## Emit rule

When lens dual-provocation runs, card MUST include ≥1 assumption_attack and ≥1 lateral_analogy in provocation_challenges, each with nonempty decision_delta; else card invalid.

## Field shape (judge-safe)

Use flat `provocation_challenges` on the candidate card (see [candidate-card.md](candidate-card.md)). Do not use role-name keys. Parent still strips lens labels before judges; challenge content remains.

```yaml
provocation_challenges:
  - kind: assumption_attack  # or lateral_analogy
    question: ""
    decision_delta: ""
    operator_id: INVERT  # optional: INVERT | NAIVE_CUT | PREMORTEM_SEED
```

Total words across all `provocation_challenges` items: ≤180. Card still ≤900 words.

## Question operators

Use these as question mechanisms inside challenge kinds — not as substitute roles.

### INVERT

Swap goal↔non-goal or success↔failure. Ask what design the dual would demand. Prefer for `assumption_attack`.

### NAIVE_CUT

Strip jargon to one sentence a non-expert would ask; force hidden axioms into unknowns. Prefer for `assumption_attack` or `lateral_analogy`.

### PREMORTEM_SEED

Assume the ship failed in 90 days; name one concrete cause; convert that cause into a now-constraint. Prefer for `assumption_attack`.

## Quick skip

WHEN tier is Quick, do not launch a dedicated provocation Task; parent-inline DA only.

## Anti–novelty-theater

- Empty `decision_delta` → invalid challenge
- Clever wording without a decision change → invalid
- Challenges advise selection and falsification; they do not average incompatible spines (Iron Rule 3)

## Where this contract is cited

Load or cite this file only from:

1. skeptical framer in [framing-and-evidence.md](framing-and-evidence.md)
2. Devil's advocate in [verification-gate.md](verification-gate.md)
3. [minority-sentinel.md](minority-sentinel.md)
4. lens `dual-provocation` prompt construction in [candidate-lenses.md](candidate-lenses.md)

Do not stamp identical operator+assumption boilerplate into falsify or Error Hunt #1.

## Non-goals (v1)

- Dual-Brief (two competing canonical briefs before P3)
- Ninth always-on P3 lens or +Task fanout
- New Cursor agent files for provocation roles
- Phase D optional specialist for provocation quality (deferred)
