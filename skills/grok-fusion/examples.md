# Examples

## Architecture answer

User:

```text
/grok-fusion Design a job queue for our Node API that already uses Postgres. We need retries, idempotency, and operator visibility. Do not rewrite the service.
```

Expected behavior:

- answer track
- framing catches rewrite pressure and existing Postgres constraint
- candidates include minimal-change versus evolution designs; when `dual-provocation` launches, cards include both `assumption_attack` and `lateral_analogy` per provocation-contract
- spine preserves Postgres-first optionality unless evidence rejects it
- final answer includes ADR, rejected alternative, risks, and dissent

## Codebase design

User:

```text
/grok-fusion How should we split the billing module so subscriptions and invoices can evolve independently?
```

Expected behavior:

- researchers map current billing boundaries and tests
- architecture playbook scenarios and fitness functions appear
- no file edits

## Factual research

User:

```text
/grok-fusion Compare open-source feature-flag systems for a Go service with strong audit requirements.
```

Expected behavior:

- dual evidence researchers (`gf-researcher-repo` / `gf-researcher-web`) and primary-source checks
- P2b freshness_critic on dated records
- social posts treated as signals only
- speculative claims labeled
- dissent preserved when sources conflict

## Explicit implementation

User:

```text
/grok-fusion Implement the agreed retry middleware in src/queue/worker.ts and add tests. Keep public APIs stable.
```

Expected behavior:

- full P0–P7 first
- implementation contract with allowed paths
- parent-only edits
- repository-native tests
- multi-pass verification (per-step recheck, double error hunt, completion quality, 5-role specialist consensus)
- no done claim while acceptance clauses remain FAIL or UNVERIFIED, or multi-pass consensus is not PASS

## Visual UI (pack visual-ui)

User:

```text
/grok-fusion Redesign the marketing landing page for our coffee roastery. Brand-first hero, no template look.
```

Expected behavior:

- pack `visual-ui`; load craft skills `grok-design` then `grok-web-ui`
- tokens-preflight + design-canon before CSS
- optional specialist `visual_design_critique` preferred in multi-pass
- soft screenshot critique; no “any design” coverage claim

## Visual UI (Russian trigger)

User:

```text
/grok-fusion Сделай лендинг для студии йоги: выразительная типографика, без фиолетовых градиентов.
```

Expected behavior:

- RU triggers map to `visual-ui` via adaptive-router hints
- anti-slop bans applied from design-canon
- ambient `frontend-design` may load; canon bans still win

## AppSec review (pack appsec-review)

User:

```text
/grok-fusion Security review the auth middleware for IDOR and missing tenant checks. Do not change code yet.
```

Expected behavior:

- pack `appsec-review`; load craft `grok-security`
- Finding Cards only; no edits (audit)
- optional specialists `authz_tenancy`, `threat_abuse`, `privacy_compliance`

## AppSec remediate (Russian)

User:

```text
/grok-fusion Закрой уязвимость IDOR в API заказов — исправь проверку tenant.
```

Expected behavior:

- AppSec-primary RU remediate verbs → pack `appsec-review`
- Remediation Card with confidence high before edits
- evidence allowlist only; no exploit PoC
