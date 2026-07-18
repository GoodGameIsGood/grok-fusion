# Selector

Bias-resistant selection of the `spine` from candidate cards. This file outranks examples and agent prompts.

## Goals

- Prefer absolute scoring before pairwise comparison
- Mitigate role, style, verbosity, and position bias
- Never use majority vote
- Never average incompatible designs into a merged design

## Inputs

Normalized candidate cards only. Strip:

- lens and role names
- confidence rhetoric
- stylistic padding
- identity cues

Present every card with identical field order.

Keep `provocation_challenges` substance (kinds, questions, `decision_delta`) when present. For cards from lens `dual-provocation`, empty or missing required kinds / empty `decision_delta` is a `must_pass_failures` item on correctness or risk axes — do not ignore the field as stylistic padding. Novelty-only challenges without a decision change do not raise scores.

## Absolute judges

Launch parallel `gf-worker` Task calls. Each judge scores every candidate independently with absolute rubric scores. Judges do not rank and do not see other judges.

### Judge axes

Heavy uses all five:

1. Correctness and evidence grounding
2. ATAM architecture quality
3. Codebase feasibility and migration
4. Risk, security, and operability
5. Requirements value and simplicity

Standard uses two pack-relevant axes, usually correctness/evidence and risk/value.

### Absolute score contract

```yaml
judge_axis:
candidate_scores:
  - candidate_id:
    score: 0-10
    confidence: high | medium | low
    must_pass_failures: []
    notes:
```

Use the robust median across judges to form Top-3. For Standard with three candidates, Top-3 is the full set ordered by median.

## Pairwise confirmation

After Top-3 are known, launch selector Task calls that compare Top-3 in swapped presentation orders.

### Pairwise output schema

```yaml
pair_id:
order: A_then_B | B_then_A
preferred: A | B | tie
confidence: high | medium | low
decision_drivers: []
disqualifiers: []
```

Rules:

- Compare A/B and B/A for each pair needed to stabilize Top-3
- Discard position-inconsistent preferences
- Do not reveal earlier absolute scores to these selector calls when avoidable
- Prefer the card with strong absolute median plus consistent pairwise wins

## Rebuttal round (selective)

Research shows always-on debate wastes tokens; run a rebuttal only when triggered:

- top-2 absolute medians differ by 1 point or less, or
- any judge flags a `must_pass_failure` on the leading candidate, or
- pairwise preferences flip across position swaps.

Protocol (one extra batch, 3 calls):

1. Two advocate calls: each receives its own card plus the rival card, and must attack the rival and defend its own with evidence ids only — no new unverified claims.
2. One fresh selector call judges the exchange on evidence quality, not rhetoric.

The rebuttal verdict breaks the tie. Without a trigger, skip the round entirely.

## Spine selection

The selected card becomes the `spine`.

```yaml
spine_id:
absolute_median:
pairwise_consistent_wins:
compatible_insights: []
dissent: []
```

Selection must remain one coherent proposal. Compatible unique insights from other cards may be listed for later surgical revision, but incompatible alternatives stay in dissent.

## Forbidden aggregation

- majority vote
- naive synthesis or averaging
- choosing the longest or most confident-sounding card
- discarding evidence-backed minority claims without sentinel review
