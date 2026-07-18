# ASVS L1 checklist (lite)

Default verification depth for `grok-security` audits. Escalate to L2-style depth only when severity is High/Critical or the change touches authz/tenancy.

Map findings to OWASP Top 10:2025 + CWE. Record every pass in Finding `checks_performed` or audit `limited_coverage`.

## V1 — Architecture

- [ ] Trust boundaries identified for changed modules
- [ ] Sensitive data flows documented (or residual_unknowns listed)

## V2 — Authentication

- [ ] Auth required on new protected routes
- [ ] Session/token handling not weakened (flags, storage, expiry)

## V3 — Session management

- [ ] Logout/invalidation path exists where sessions apply
- [ ] No session fixation via user-controlled identifiers

## V4 — Access control

- [ ] Object-level authz on read/write by id (no IDOR)
- [ ] Tenant/user scope on queries and mutations

## V5 — Validation / business logic

- [ ] Server-side validation for untrusted input
- [ ] Dangerous sinks (SQL/OS/template/eval) not fed raw input

## V6 — Cryptography

- [ ] No hard-coded secrets in code
- [ ] Strong primitives for new crypto (no homemade)

## V7 — Error handling / logging

- [ ] Errors fail closed; no stack traces to clients in prod paths
- [ ] Logs omit secrets/PII; security events present where relevant

## V8 — Data protection

- [ ] Sensitive fields not logged or exported unbounded
- [ ] Transport assumptions (TLS) not bypassed in new clients

## V9 — Communication

- [ ] External HTTP: timeouts; no blind trust of redirects/SSRF-prone URLs

## V10 — Malicious software / integrity

- [ ] New deps pinned; no unexplained install scripts
- [ ] Webhooks/callbacks verify authenticity when present

## V11 — Business logic abuse

- [ ] Rate / size limits on expensive or public operations
- [ ] Uploads constrained; open redirects blocked

## V12 — Files / resources

- [ ] Path traversal blocked on file ops
- [ ] Resource exhaustion bounded (loops, fan-out, large payloads)

## V13 — API

- [ ] New endpoints documented with authz expectations
- [ ] Mass-assignment / over-posting resisted on write DTOs

## V14 — Configuration

- [ ] Debug/admin surfaces not exposed by default
- [ ] CORS and cookie flags not loosened without rationale

If a section was not inspected, list it under `residual_unknowns` / unread scope — do not claim clean.
