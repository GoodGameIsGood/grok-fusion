# Security Playbook

Professional AppSec for Grok Fusion. Use when the task pack is `appsec-review`. Mutating still requires [multi-pass-verification.md](multi-pass-verification.md); this playbook **adds** gates — it does not replace G0–G4.

Load craft skill `grok-security` (canon → ASVS L1 → cards → threat-model-lite as needed). Pack id is **`appsec-review`** (not Cursor Task `security-review`).

## Iron gates G-S0 .. G-S5

### G-S0 — Mode split

| Mode | When | Allowed |
|---|---|---|
| Audit | Security review without explicit fix ask | Finding Cards only; **no edits** |
| Remediate | User explicitly asks to fix/close/harden a finding | Remediation Card + parent edits |

`quality_profile: max` / MVP Heavy spine ≠ permission to mutate. Audit under max still leaves the tree clean.

### G-S1 — Anti-empty-perfect

Forbid «нет уязвимостей» / “secure” / «всё безопасно» unless ASVS L1 checklist was run, `checks_performed` is nonempty, and residual unknowns/unread scope are listed. Zero findings ⇒ `limited_coverage`, never “clean”.

### G-S2 — Defensive-only

Ban exploit PoCs, weaponized payloads, and attacking remote systems. Finding `evidence` and Remediation `characterization_cmds` allowlist only: `path:line` | `missing_control` | `config_absence`. PoC-shaped content ⇒ multi-pass **FAIL**.

### G-S3 — Card namespace

`finding_card` / `remediation_card` ≠ debugging `repair_card`. Cross-pack: consult/attach only; no silent pack swap. If both cards needed, record both ids in `done_evidence`.

### G-S4 — Remediation mutate gates

Mirror debugging discipline: `allowed_paths`, `patch_intent`, `must_not_break`, `do_not_fix`, blast radius; parent-only edits; confidence ≥ `security.min_fix_confidence` (default `high`). Divergence ⇒ FAIL. ASVS L2 depth only when severity High/Critical or authz.

### G-S5 — Dual-tree / craft install

Edit Fusion contracts → sync `skills/grok-fusion` ↔ `.cursor/skills/grok-fusion`. `skills/grok-security` is **not** HARD-mirrored; Option B must copy it. Half-sync ⇒ validate FAIL.

## Precedence (E5 win-order)

1. **AppSec-primary** verbs (vuln, OWASP, ASVS, threat model, harden, аудит безопасности, уязвимост*, закрыть дыры / уязвимость, устрани дыру) → pack `appsec-review` (E1)
2. Else bug/flake/incident → `debugging` (MAY consult `grok-security`)
3. Else visual-ui / architecture / planning → those packs; E3 consult never overrides pack selection
4. E4 honesty (`limited_coverage` / no empty-perfect) always applies

Bare «исправь баг» stays debugging. «исправь / закрой уязвимость / устрани дыру» is AppSec remediate.

## Finding Card

```yaml
mode: finding_card
finding_id: ""
severity: critical|high|medium|low|info
asset_path: ""
owasp_id: ""
cwe_id: ""
evidence: ""    # ONLY path:line | missing_control | config_absence
impact: ""
residual_unknowns: []
checks_performed: []
```

When `security.require_finding_card_on_audit` is true, audit answers without Finding Cards (or explicit `limited_coverage`) are incomplete.

## Remediation Card

```yaml
mode: remediation_card
finding_ids: []
observation: ""
patch_intent: []
allowed_paths: []
must_not_break: []
do_not_fix: []
blast_radius_paths: []
characterization_cmds: []  # same allowlist; static only; no PoC
confidence: high|medium|low
fix_rationale: ""
```

When `security.require_remediation_card` is true, no AppSec edits without an approved card. Then: verify ladder + multi-pass through Phase E (`closure: CONFIRMED`).

## Methods

OWASP Top 10:2025 awareness + ASVS L1 checklist ([grok-security](../grok-security/references/asvs-l1-checklist.md)) + CWE tags + STRIDE on trust boundaries. Abuse: rate limits, size limits, uploads, open redirects.

## Stop / rollback

Do not widen scope mid-remediation without a new Remediation Card. Two identical failure fingerprints → checkpoint rollback + user gate.
