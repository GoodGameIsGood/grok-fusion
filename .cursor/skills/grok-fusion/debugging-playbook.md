# Debugging Playbook

Professional debugging for Grok Fusion. Use when the task pack is `debugging` (bugs, flakes, incidents, unexpected behavior). Mutating still requires [multi-pass-verification.md](multi-pass-verification.md); this playbook **adds** gates — it does not replace them.

## Iron rule (mutating)

No file edits until all hold:

1. Falsifiable observation recorded
2. ≥2 competing hypotheses with one surviving falsification (`primary_cause`)
3. Characterization or baseline green on *current* neighbor behavior (or explicit `n/a` with council BLOCK risk accepted)
4. Blast-radius paths discovered (not `UNREAD`)
5. **Repair Card** approved with `confidence: high` and concrete `patch_intent`
6. Parent implements **only** that card (no opportunistic refactors)

`confidence: medium|low` ⇒ no mutating; report findings or ask. Project config `debugging.min_fix_confidence` defaults to `high`.

## 1. Classify

Record: `bug` | `flake` | `incident` | `performance` | `data-corruption`; severity; user-visible vs latent.

## 2. Preserve goals

Read `spine.json` / plan `success_definition` / PR-FAQ when present. List **must-not-break** scenarios: primary happy path plus at least two adjacent flows. These become acceptance pressure for hunts and the auditor.

## 3. Reproduce

Minimal failing observation: command, input, expected vs actual, environment notes.  
**No reproduce → no fix** (investigate-only / answer-track).

## 4. Mental model loop

Iterate a mental model of the failing path:

1. **Backward trace** from the observed failure (symptom → callers → ownership)
2. Once localized, **forward validate** (predict behavior, check logs/tests/code)
3. Combine static structure reads with dynamic evidence — do not “guess a file”

## 5. Hypotheses

Produce ≥3 competing root-cause hypotheses. Each must be falsifiable (what evidence would kill it).

## 6. Falsify

Kill weak hypotheses with evidence. The survivor becomes `primary_cause`. Rejected hypos stay on the Repair Card. Do not edit while multiple strong hypos remain.

## 7. Characterization first

Before changing code (when `debugging.require_characterization` is true):

- Add or run a failing regression that locks the bug, **or**
- Characterize current correct neighbor behavior with repo-native commands

Green characterization/baseline of neighbors is required before the fix lands. Borrow the spirit of `refactoring-migration` characterization — never big-bang rewrite while debugging.

## 8. Blast radius

Map modules, APIs, callers, and tests in the failure radius. Use discovery with `budgets.discovery_max_files_debug` (see [discovery-track.md](discovery-track.md)). Do not edit paths that remain `UNREAD`.

## 9. Repair Card

The **only** allowed mutation plan. Produced by the council (Heavy spine and/or debug deliberation) and attached to the implementation contract / durable state.

```yaml
mode: repair_card
observation: ""
primary_cause: ""
rejected_hypotheses: []
must_not_break: []
characterization_cmds: []
blast_radius_paths: []
allowed_paths: []
patch_intent: []
confidence: high|medium|low
fix_rationale: ""
do_not_fix: []
```

- `patch_intent`: concrete steps the parent may perform
- `do_not_fix`: symptoms that look like bugs but must stay (by design / accepted debt)
- Divergence from `patch_intent` during implementation ⇒ multi-pass FAIL

## 10. Apply minimal fix

Parent edits only. Every touched path ⊆ `allowed_paths`. No drive-by cleanups, renames, or “improve while here” without a **new** Repair Card.

## 11. Verify ladder

1. Failing case / regression now green
2. Characterization cmds still green
3. Blast-radius suite / relevant verify cmds green
4. Full [multi-pass-verification.md](multi-pass-verification.md) with verify hard gate

Record runs in `verification_runs` / `events.jsonl`.

## 12. Stop / rollback

Two identical failure fingerprints → checkpoint rollback + user gate ([recovery-track.md](recovery-track.md)). Never widen scope mid-fix. Resume keeps the Repair Card.

## Answer-track (explain-only)

Reproduce + hypotheses + falsify still apply. No Repair Card required for pure explanation. Do not claim a fix was applied.

## Config knobs

See [project-config.md](project-config.md) `debugging.*`: `require_repair_card`, `min_fix_confidence`, `require_characterization`, `blast_radius_discovery`, `discovery_max_files_debug`, `preferred_specialists`.
