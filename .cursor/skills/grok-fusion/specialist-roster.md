# Specialist Roster

Optional narrow specialists for Grok Fusion multi-pass Phase D. All roles run as `gf-reviewer` with `mode=specialist_panel` plus `role` and `scenario`. Do not create separate agent files per role.

**Max 3** optional specialists per Phase D round (plus the core 5). See [multi-pass-verification.md](multi-pass-verification.md).

## Core panel (always on — not optional)

| Role id | Focus |
|---|---|
| `correctness_engineer` | bugs, edges, tests |
| `systems_architect` | boundaries, cohesion, long-term evolution |
| `security_reliability` | threats, failure modes, misuse |
| `product_acceptance` | EARS/DoD, user-zero path |
| `ops_maintainability` | rollback, ops debt, observability |

## Optional roster (22)

| Role id | Focus | Typical triggers |
|---|---|---|
| `api_compat` | public APIs, semver, breaking clients | G2; paths `**/api/**`, OpenAPI, SDK |
| `data_migration` | schema, backfill, dual-write, rollback | G1; `**/migrations/**`, prisma/alembic |
| `performance` | N+1, hot paths, payloads, timeouts | loops in hot modules; queue/worker packs |
| `ux_accessibility` | user-zero, a11y, empty/error states | UI/frontend packs; product MVP UI waves |
| `test_strategist` | coverage gaps, flake risk, missing regression | weak/absent `verify_cmd`; flake history in lessons |
| `dependency_supply_chain` | new deps, pins, licenses, supply risk | `package.json`/`Cargo.toml`/`go.mod` changes |
| `concurrency` | races, locks, idempotency, at-least-once | workers, async, shared mutable state |
| `observability` | logs, metrics, traces, actionable errors | new services; ops debt; production paths |
| `authz_tenancy` | authn/z, tenancy isolation, IDOR | auth/permissions; multi-tenant hints |
| `privacy_compliance` | PII, retention, secrets in logs | user data fields; analytics; exports |
| `network_resilience` | retries, timeouts, circuit breakers, backoff | HTTP clients, webhooks, external APIs |
| `cache_consistency` | TTL, invalidation, stale reads | Redis/cache layers |
| `frontend_state` | state machines, stale UI, optimistic updates | React/Vue/store files |
| `dx_tooling` | DX, scripts, CI glue, developer traps | `scripts/`, CI workflows, Makefile |
| `docs_accuracy` | docs vs code drift (mutating docs) | README/docs edits |
| `i18n_localization` | strings, locales, RTL, pluralization | `locales/`, i18n keys |
| `cost_finops` | token/cloud/cost amplifiers | LLM calls, heavy jobs, egress |
| `release_rollback` | feature flags, canary, revert path | deploy waves; G3 |
| `threat_abuse` | abuse cases beyond baseline security | public endpoints, uploads, auth |
| `data_model_integrity` | invariants, FK, uniqueness, orphan rows | models/schema without full migration |
| `search_indexing` | index drift, eventual consistency | search/index modules |
| `mobile_offline` | offline, sync conflicts | mobile/offline packs |

## Scenario templates

Every optional (and core) specialist prompt sets `scenario: recheck|improve|advise`.

### Shared output fields

```yaml
mode: specialist_panel
role: ""
scenario: recheck|improve|advise
verdict: SHIP|REWORK|BLOCK
blockers: []
improvements: []
advice: []
long_term_risk: high|medium|low
confidence: high|medium|low
checks_performed: []
```

### recheck

Find evidence-backed defects or holes in the scoped role. Prefer concrete blockers. `SHIP` requires nonempty `checks_performed`.

### improve

Propose at least one concrete improvement with path or step. If already minimal and correct, state that explicitly and still fill `checks_performed`. Put proposals in `improvements`.

### advise

Recommend next steps without silent rubber-stamp `SHIP`. Usual verdicts: `REWORK` with advice, or `SHIP` only when checks prove no further advice is needed. Advise alone cannot create multi-pass `consensus: PASS` without the core panel.

### Default scenario

- Full Phase D panel → `recheck`
- User asked to improve/advise, or polish after `REWORK` without `BLOCK` → `improve` / `advise`
- **Consult** (single Task outside full panel): `improve` or `advise` only; write to `events.jsonl` / notes; do **not** change `consensus` on the multi_pass artifact

## Selection algorithm

```text
1. Start with empty optional set.
2. Apply trigger rules in table order; add role if trigger matches.
3. Cap at 3: keep highest-severity first (G1/G2/G3/security-related roles win ties).
4. Never duplicate a core role under another id.
5. Docs-only mutating: prefer docs_accuracy + structure roles; still max 3 optional.
6. Record selected roles+scenarios in multi_pass JSON field optional_panel.
```

Parent must also persist the selection record (and may call `scripts/select_optional_specialists.py` for the same result):

```yaml
selection:
  triggers_matched: []
  selected: [{role: "", scenario: recheck}]
  dropped_by_cap: []
```

Store the same object on multi_pass as `optional_selection`. Honor project config `preferred_specialists`, `disabled_specialists`, and `multi_pass.max_optional_specialists`.

### Severity priority for the cap

`authz_tenancy` = `data_migration` = `api_compat` = `threat_abuse` = `privacy_compliance` > `release_rollback` > `concurrency` > others.

### Stance notes (per role)

Each role must stay inside its focus: do not re-litigate other specialists’ domains. Unknown `role` ids are invalid votes.
