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

Suggested optional specialists: `test_strategist`, `dx_tooling`

Forbidden default: greenfield rewrite

## debugging

Use for bugs, flakes, incidents, and unexpected behavior. Follow [debugging-playbook.md](debugging-playbook.md).

Pipeline emphasis:

1. Reproduce or define a falsifiable observation
2. Preserve goals / must-not-break scenarios
3. Produce competing root-cause hypotheses (≥3) and falsify weak ones
4. Characterization / baseline before any edit
5. Blast-radius discovery; council **Repair Card** with `confidence: high`
6. Apply only the approved minimal `patch_intent` (no drive-by refactors)
7. Verify ladder + multi-pass; rollback on fingerprint loops

Preferred lenses: failure-and-security, implementation-realist, persona-free wildcard

Suggested optional specialists: `test_strategist`, `concurrency`, `observability`

Forbidden: mutating without Repair Card when config requires it; opportunistic refactors during a bugfix

## research

Use for comparisons, literature/docs research, and factual tradeoffs.

Pipeline emphasis:

1. Primary-source scout
2. Independent corroboration
3. Claim/evidence map
4. Explicit uncertainty labels

Preferred lenses: product-and-requirements, first-principles, persona-free wildcard

Suggested optional specialists: `docs_accuracy` (if mutating notes)

Social/X posts are signals only.

## product-mvp

Use for MVP/product builds and multi-wave feature delivery.

Pipeline emphasis:

1. User outcome and non-goals
2. Core loop and smallest vertical slice
3. Adoption, operability, and data/security minimums
4. Wave DAG and acceptance clauses
5. Multi-pass verification and specialist consensus before wave/epic done

Preferred lenses: product-and-requirements, minimal-change, evolution-and-scale, implementation-realist

Suggested optional specialists: `ux_accessibility`, `privacy_compliance`, `release_rollback`

## architecture

Use for system design, boundaries, migrations, and irreversible structural choices.

Pipeline emphasis: ATAM-lite from `architecture-playbook.md`

Preferred lenses: all eight Heavy lenses unless the router explicitly narrows them

Suggested optional specialists: `api_compat`, `data_model_integrity`, `observability`

## refactoring-migration

Use for large brownfield refactors, framework or library migrations, and incremental rewrites.

Pipeline emphasis:

1. Characterization tests for current behavior before any change
2. Strangler-fig or incremental steps; never a big-bang rewrite by default
3. Old and new paths coexist behind a seam where applicable
4. Compatibility checks and a rollback step for every stage
5. Delete the old path only after the new path is verified

Preferred lenses: minimal-change, implementation-realist, evolution-and-scale

Suggested optional specialists: `data_migration`, `api_compat`, `test_strategist`

Forbidden default: big-bang rewrite without characterization tests

## visual-ui

Use for landing pages, marketing UI, visual redesign, brand/UI polish, hero composition, and web visual deliverables (HTML/CSS/React).

Pipeline emphasis:

1. Load craft skills `grok-design` then `grok-web-ui` (canon → tokens-preflight → build)
2. Preserve existing design systems when present
3. Soft screenshot critique; hard screenshot+a11y DoD only on tagged visual-MVP mutate waves
4. Anti-slop and brand-first checks from design-canon
5. Multi-pass with visual critique + a11y when mutating UI

Preferred lenses: product-and-requirements, implementation-realist, failure-and-security

Suggested optional specialists: `visual_design_critique`, `ux_accessibility`, `frontend_state`

Forbidden default: ship UI without token preflight or anti-slop scan; claim “any design” coverage

Triggers (EN|RU): landing, redesign, visual polish, UI mock, hero, brand page, лендинг, макет, вёрстка, интерфейс, дизайн страницы, визуальный редизайн

## professional-planning

Use for plans, roadmaps, implementation plans, CreatePlan-style artifacts, and any pre-implementation design of work.

Pipeline emphasis:

1. Freshness scout for external and repo facts that the plan depends on
2. Goal-backward definition of done
3. EARS / Given-When-Then acceptance criteria
4. Atomic batches (≤5 files each) with verify commands
5. Plan quality gate plus multi-pass (double error hunt, completion quality, specialist consensus)
6. Devil's advocate folded into Error Hunt #1 or a pre-panel falsifier

Preferred lenses: product-and-requirements, implementation-realist, failure-and-security

Suggested optional specialists: `test_strategist`, `api_compat`, `data_migration`

Forbidden: prose-only plans without verify commands; big-bang single batch

## writing-explanation

Use for docs, explanations, and communication artifacts that are not implementation plans.

Pipeline emphasis:

1. Audience and intent
2. Accuracy against evidence
3. Clarity and structure
4. Concise verifier for factual claims
5. If files are mutated: multi-pass with docs-adapted specialist roles

Preferred lenses: product-and-requirements, persona-free wildcard

Suggested optional specialists: `docs_accuracy` (mutating docs; plus docs-adapted core)

## Lens selection rule

- Quick: parent solves; optional one verifier using the pack's primary lens
- Standard: choose exactly three preferred lenses from the pack
- Heavy architecture: default to all eight lenses
- MVP spine: use architecture or product-mvp pack for the initial Heavy pass; later waves use simple-code-edit, debugging, or product-mvp as needed
- Large refactors: use refactoring-migration; single-batch scope stays Heavy, multi-wave scope escalates to MVP-tier durable state
- Planning requests always select `professional-planning`
