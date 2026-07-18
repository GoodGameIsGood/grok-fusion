# Finding and Remediation cards

Schemas for `grok-security` + Fusion `security-playbook.md`. Distinct from debugging `repair_card`.

## Finding Card (audit anytime)

```yaml
mode: finding_card
finding_id: ""
severity: critical|high|medium|low|info
asset_path: ""
owasp_id: ""    # e.g. A01:2025
cwe_id: ""      # e.g. CWE-639
evidence: ""    # ONLY path:line | missing_control | config_absence
impact: ""
residual_unknowns: []
checks_performed: []
```

Rules:

- Emit one card per distinct issue (or clearly grouped family)
- `evidence` MUST match the allowlist; PoC/payload text ⇒ invalid / multi-pass FAIL
- Empty findings ⇒ status `limited_coverage` + nonempty `checks_performed` + unread scope
- Audit mode: Finding Cards only — **no file edits**

## Remediation Card (explicit fix only)

```yaml
mode: remediation_card
finding_ids: []
observation: ""
patch_intent: []
allowed_paths: []
must_not_break: []
do_not_fix: []
blast_radius_paths: []
characterization_cmds: []  # same evidence allowlist; static only; no PoC
confidence: high|medium|low
fix_rationale: ""
```

Rules:

- Required before any AppSec mutate when `security.require_remediation_card` is true
- `confidence` must be ≥ `security.min_fix_confidence` (default `high`) or no edits
- Every touched path ⊆ `allowed_paths`; divergence from `patch_intent` ⇒ multi-pass FAIL
- `characterization_cmds` must not contain exploit/PoC payloads

## Namespace

| Card | Pack / mode |
|---|---|
| `finding_card` / `remediation_card` | `appsec-review` |
| `repair_card` | `debugging` only |

Do not reuse Repair Card fields for AppSec mutate. If both bug-fix and vuln language appear, follow Fusion precedence (AppSec-primary verbs → `appsec-review`).
