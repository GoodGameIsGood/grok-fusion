# Architecture Playbook

ATAM-lite contract for architecture and design tasks. Prefer this over generic checklists.

## Required analysis shape

1. Business drivers, stakeholders, and system boundary
2. Utility tree: ranked quality attributes
3. Quality scenarios using: source, stimulus, environment, artifact, response, measurable response
4. Minimal baseline plus at least two viable designs
5. Sensitivity points, tradeoff points, risks, and non-risks
6. Reversibility and option value
7. Change amplification and ownership boundaries
8. Data ownership, compatibility, migration, and rollback
9. Observability, failure containment, capacity, and recovery
10. Threat model when relevant
11. Pre-mortem at 6 months and 18 months
12. Executable architecture fitness functions
13. ADR: decision, rejected alternatives, consequences, revisit triggers

## Quality scenario template

```yaml
- name:
  source:
  stimulus:
  environment:
  artifact:
  response:
  measurable_response:
```

## Fitness functions

Turn important scenarios into executable or monitorable checks:

- dependency or module boundary checks
- migration/rollback rehearsal steps
- latency, error-budget, or capacity probes when metrics exist
- security or access-control assertions when relevant

Never invent SLO, load, or cost numbers. If numbers are missing, emit measurement questions or validation spikes instead.

## Anti-patterns

- one obvious design with no rejected alternative
- enterprise theater or premature abstraction
- ignoring existing codebase conventions
- happy-path-only designs
- silent assumption of undocumented scale targets
