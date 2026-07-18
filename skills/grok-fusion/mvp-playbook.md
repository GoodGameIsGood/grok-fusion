# MVP Playbook

Startup-oriented product planning for the MVP tier. Prefer the smallest end-to-end vertical slice over horizontal completeness.

## Working backwards: PR/FAQ first

Before the Heavy spine pass, write a PR/FAQ into `prfaq.json`:

1. A one-page future-dated press release: customer, problem, benefit, how it works. If the press release does not excite the target user, rework the idea before building.
2. FAQ: the hardest customer and internal questions (effort, risks, economics, dependencies).
3. Riskiest assumptions as testable claims, each mapped to the earliest wave that can falsify it cheaply (riskiest assumption test).
4. Acceptance criteria in EARS form: "WHEN <trigger> THE SYSTEM SHALL <response>". These become acceptance clauses.

Detailed implementation plans for waves follow `planning-contract.md`; PR/FAQ alone is not a substitute for an executable plan.

The Heavy spine pass receives the PR/FAQ as part of the canonical brief.

## Walking skeleton rule

Wave 1 after discovery is always a walking skeleton: the thinnest end-to-end path through the real architecture (request to persisted state to observable output) that builds, starts, and is exercised by one automated check. Features attach to the skeleton; the skeleton is never postponed.

## TDD wave loop

Inside every mutating wave: write or extend a failing repository-native test for the wave's acceptance first, implement the minimum to pass, then refactor with tests green. A wave without a runnable test needs an explicitly accepted reason recorded in its summary. After steps are green, run [multi-pass-verification.md](multi-pass-verification.md) before marking the wave complete.

## Required planning shape

1. User outcome and who it is for
2. Non-goals and explicit deferrals
3. Core loop: the smallest repeated user action that delivers value
4. Vertical slice: one path from input to persisted result to observable output
5. Data and security minimums
6. Operability: logs, errors, basic health, rollback
7. Adoption: how a first user starts
8. Deployment/start path that actually works in this repo
9. Acceptance clauses that prove the slice works
10. Simplicity rule: if two designs satisfy the outcome, choose the one with fewer moving parts

## Vertical-slice order

1. Runnable core flow
2. Persistence and integration
3. UX/completeness for the same slice
4. Hardening, observability, and deployment polish

Do not build admin panels, extra roles, or secondary surfaces before the core loop works.

## Product clause examples

- A first user can complete the core loop without manual DB edits
- The app builds and starts with a documented command
- Failure modes surface actionable errors
- Secrets are not committed
- One rollback path exists for the first migration, if any
- A scripted demo of the core loop runs end-to-end from a documented command

## Anti-patterns

- platform before product
- multi-tenant complexity before one working tenant
- speculative microservices
- inventing metrics or SLOs without measurement
- expanding scope during later waves without gate G4
