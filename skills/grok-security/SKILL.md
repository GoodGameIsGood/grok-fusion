---
name: grok-security
description: "AppSec hub for Grok Fusion. Use for security review, threat model, OWASP/ASVS audit, vuln findings, authz harden, аудит безопасности, уязвимости, закрыть дыры. Loads security-canon and Finding/Remediation cards. Prefer Fusion pack appsec-review. Do not load for pure visual-ui, Fusion-only non-security, or inventing exploit PoCs."
---

# Grok Security (hub)

Craft layer for application security review and defensive remediation. Fusion (`grok-fusion`) remains judgment / multi-pass; this skill is AppSec execution guidance.

## Load order

1. Read [references/security-canon.md](references/security-canon.md)
2. Read [references/asvs-l1-checklist.md](references/asvs-l1-checklist.md) for audit passes
3. Read [references/cards.md](references/cards.md) before emitting Finding or Remediation cards
4. On design/boundary changes: read [references/threat-model-lite.md](references/threat-model-lite.md)

Do not load more than **two** security skill bodies in one turn (this hub + one reference deep-dive is enough; prefer citing refs over pasting).

## When to use

- Security audit / review / threat model / OWASP / ASVS (EN|RU)
- Authz, injection, secrets, supply-chain, abuse (rate/size/upload/redirect)
- Explicit fix/close/harden of a finding (requires Remediation Card via Fusion playbook)
- Russian triggers: аудит безопасности, угрозы, уязвимост*, закрыть дыры, права доступа

## When not to use

- Pure visual-ui / design without security intent
- Ordinary bug/flake without AppSec-primary verbs (use debugging pack; MAY consult this craft)
- Writing exploits, weaponized PoCs, or attacking remote systems

## Fusion compose

- AppSec-primary intent → Fusion pack **`appsec-review`** (not Cursor Task `security-review`)
- Other packs MAY consult this craft (**MUST NOT** force `appsec-review` or remediate without ask)
- Do not redesign the Fusion pipeline

## Modes

| Mode | Output | Mutate? |
|---|---|---|
| Audit | Finding Cards only | No |
| Remediate | Remediation Card then parent edits | Only on explicit user ask + confidence ≥ config |

Zero findings ⇒ `limited_coverage` with `checks_performed` and unread scope — never «всё безопасно» / “no vulns” without evidence.
