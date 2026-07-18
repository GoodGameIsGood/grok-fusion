# Blind evaluation runbook

## Purpose

Compare solo Grok, Grok Fusion, and solo Fable on the same sanitized cases. Do not tune prompts against these cases.

## Protocol

1. Use identical sanitized prompts and context packs for all three systems.
2. Collect outputs, then anonymize and randomize presentation order.
3. Have three independent evaluators score atomic rubric items.
4. Apply negative criteria with documented severity.
5. For close pairs, repeat judgment with position swap.
6. Humans review all ties and all critical errors.
7. Publish per-category means, latency, model-call counts, and failure cases.
8. Reject prompt changes that are benchmark-specific tricks.

## Release thresholds

- Architecture category mean: Grok Fusion >= solo Fable + 3 weighted points
- Overall bootstrap 95% CI lower bound >= -2 for parity language
- Public claim language stronger than parity only when lower bound > 0
- Critical violation rate no worse than solo Fable

## Evidence rule

Do not claim these thresholds passed unless a recorded benchmark evidence file exists and matches this runbook.
