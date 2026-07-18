# Specialist Evidence Packs

Evidence focus for optional `gf-reviewer` roles. Load the matching section for `role` during `specialist_panel`. Do not rubber-stamp: cite paths/commands from this pack in `checks_performed`.

## api_compat

- Read: public handlers, OpenAPI/SDK, changelog, semver notes
- Check: breaking request/response fields, auth headers, pagination
- Red flags: silent field renames, removed endpoints, tighter validation without migration

## data_migration

- Read: migration files, schema models, dual-write/backfill notes
- Check: forward + rollback path, nullability, backfill idempotency
- Red flags: destructive DROP without backup, no dual-write window

## performance

- Read: hot loops, N+1 query sites, payload sizes, timeouts
- Check: bounded queries, pagination, cache hits on hot paths
- Red flags: unbounded `SELECT *`, sync work on request path

## ux_accessibility

- Read: UI entry flows, empty/error states, labels
- Check: keyboard path, contrast/labels, user-zero first run
- Red flags: icon-only controls, silent failures, missing empty states

## test_strategist

- Read: `verify_cmd`, new tests, flake history in `lessons.json`
- Check: regression for the bugfix, deterministic fixtures
- Red flags: no test for changed behavior, sleeps as sync, skipped asserts

## dependency_supply_chain

- Read: lockfiles, new deps, license headers
- Check: pinned versions, minimal new surface, known CVEs if checked
- Red flags: unpinned latest, unused deps, postinstall scripts

## concurrency

- Read: workers, shared mutable state, locks, queues
- Check: idempotency keys, at-least-once handlers, race windows
- Red flags: check-then-act without lock, non-idempotent retries

## observability

- Read: logs/metrics/traces on new paths
- Check: actionable errors, correlation ids, no secret leakage
- Red flags: swallow exceptions, PII in logs, no failure metric

## authz_tenancy

- Read: authn/z middleware, tenancy filters, IDOR-prone IDs
- Check: every read/write scoped to tenant/user
- Red flags: IDOR by object id, missing auth on new route

## privacy_compliance

- Read: user data fields, exports, analytics events
- Check: retention, redaction, consent boundaries
- Red flags: secrets/PII in logs, unbounded exports

## network_resilience

- Read: HTTP clients, webhooks, external API calls
- Check: timeouts, retries with backoff, circuit breakers
- Red flags: infinite retry, no timeout, retrying non-idempotent POST

## cache_consistency

- Read: cache keys, TTL, invalidation paths
- Check: write-through/invalidate on mutate, stale-read windows
- Red flags: forever TTL, cache without invalidation

## frontend_state

- Read: store/state machines, optimistic updates
- Check: rollback on failure, stale prop/state sync
- Red flags: optimistic write without reconcile, duplicated sources of truth

## dx_tooling

- Read: scripts/, Makefile, CI workflows
- Check: docs match commands, fail-fast scripts
- Red flags: undocumented required env, CI-only magic

## docs_accuracy

- Read: README/docs vs code paths and commands
- Check: commands run, paths exist, flags match
- Red flags: stale install steps, invented APIs

## i18n_localization

- Read: locale files, string keys, RTL assumptions
- Check: no hardcoded user strings, plural rules
- Red flags: concatenated sentences, missing keys

## cost_finops

- Read: LLM/cloud calls, batch jobs, egress
- Check: caps, caching, pagination of heavy jobs
- Red flags: unbounded fan-out, chatty per-row remote calls

## release_rollback

- Read: feature flags, deploy notes, revert path
- Check: canary/flag off, forward-fix + rollback
- Red flags: irreversible migrate-then-deploy with no flag

## threat_abuse

- Read: public endpoints, uploads, auth flows
- Check: rate limits, size limits, abuse cases beyond baseline authz
- Red flags: open upload, missing rate limit, user-controlled redirects

## data_model_integrity

- Read: models/schema without full migration set
- Check: uniqueness, FK, orphan prevention, invariants
- Red flags: soft-delete without queries updated, missing unique constraints

## search_indexing

- Read: index writers/readers, sync jobs
- Check: eventual consistency windows, rebuild path
- Red flags: index drift after mutate, no backfill

## mobile_offline

- Read: sync queues, conflict resolution, offline stores
- Check: conflict policy, retry, clock skew handling
- Red flags: last-write-wins without user notice, lost updates
