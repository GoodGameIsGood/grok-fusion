# Task Packs

Select one task pack after tier routing. Packs choose lenses, evidence focus, and verification. Do not force the architecture pack on every request.

## simple-code-edit

Use for local code changes, renames, small fixes, and clear implementation requests.

Pipeline emphasis:

1. Inspect the exact files and nearby tests
2. Make the minimal change
3. Run repository-native checks
4. One correctness reviewer

Preferred lenses: implementation-realist, failure-and-security

Forbidden default: greenfield rewrite

## debugging

Use for bugs, flakes, incidents, and unexpected behavior.

Pipeline emphasis:

1. Reproduce or define a falsifiable observation
2. Produce competing root-cause hypotheses
3. Falsify weak hypotheses
4. Apply the minimal fix
5. Add or run a regression check

Preferred lenses: failure-and-security, implementation-realist, persona-free wildcard

## research

Use for comparisons, literature/docs research, and factual tradeoffs.

Pipeline emphasis:

1. Primary-source scout
2. Independent corroboration
3. Claim/evidence map
4. Explicit uncertainty labels

Preferred lenses: product-and-requirements, first-principles, persona-free wildcard

Social/X posts are signals only.

## product-mvp

Use for MVP/product builds and multi-wave feature delivery.

Pipeline emphasis:

1. User outcome and non-goals
2. Core loop and smallest vertical slice
3. Adoption, operability, and data/security minimums
4. Wave DAG and acceptance clauses

Preferred lenses: product-and-requirements, minimal-change, evolution-and-scale, implementation-realist

## architecture

Use for system design, boundaries, migrations, and irreversible structural choices.

Pipeline emphasis: ATAM-lite from `architecture-playbook.md`

Preferred lenses: all eight Heavy lenses unless the router explicitly narrows them

## refactoring-migration

Use for large brownfield refactors, framework or library migrations, and incremental rewrites.

Pipeline emphasis:

1. Characterization tests for current behavior before any change
2. Strangler-fig or incremental steps; never a big-bang rewrite by default
3. Old and new paths coexist behind a seam where applicable
4. Compatibility checks and a rollback step for every stage
5. Delete the old path only after the new path is verified

Preferred lenses: minimal-change, implementation-realist, evolution-and-scale

Forbidden default: big-bang rewrite without characterization tests

## writing-explanation

Use for docs, explanations, plans, and communication artifacts.

Pipeline emphasis:

1. Audience and intent
2. Accuracy against evidence
3. Clarity and structure
4. Concise verifier for factual claims

Preferred lenses: product-and-requirements, persona-free wildcard

## Lens selection rule

- Quick: parent solves; optional one verifier using the pack's primary lens
- Standard: choose exactly three preferred lenses from the pack
- Heavy architecture: default to all eight lenses
- MVP spine: use architecture or product-mvp pack for the initial Heavy pass; later waves use simple-code-edit, debugging, or product-mvp as needed
- Large refactors: use refactoring-migration; single-batch scope stays Heavy, multi-wave scope escalates to MVP-tier durable state
