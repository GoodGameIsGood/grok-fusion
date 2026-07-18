# Examples

## Architecture answer

User:

```text
/grok-fusion Design a job queue for our Node API that already uses Postgres. We need retries, idempotency, and operator visibility. Do not rewrite the service.
```

Expected behavior:

- answer track
- framing catches rewrite pressure and existing Postgres constraint
- candidates include minimal-change versus evolution designs
- spine preserves Postgres-first optionality unless evidence rejects it
- final answer includes ADR, rejected alternative, risks, and dissent

## Codebase design

User:

```text
/grok-fusion How should we split the billing module so subscriptions and invoices can evolve independently?
```

Expected behavior:

- scouts map current billing boundaries and tests
- architecture playbook scenarios and fitness functions appear
- no file edits

## Factual research

User:

```text
/grok-fusion Compare open-source feature-flag systems for a Go service with strong audit requirements.
```

Expected behavior:

- dual evidence scouts and primary-source checks
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
