---
name: grok-design
description: "Design hub for Grok visual craft. Use for web UI, landing pages, visual redesign, UI polish, brand layouts, макет, лендинг, вёрстка, интерфейс, дизайн страницы. Establishes design-canon and tokens-preflight; routes to grok-web-ui. Do not load for Fusion-only deliberation, non-UI backend, CLI-only, or planning without a visual deliverable."
---

# Grok Design (hub)

Craft layer for visual work. Fusion (`grok-fusion`) remains judgment / multi-pass; this skill is execution guidance.

## Load order

1. Read [references/design-canon.md](references/design-canon.md)
2. Read [references/tokens-preflight.md](references/tokens-preflight.md) before painting UI
3. For web/HTML/CSS/React UI: load `grok-web-ui` and follow its refs
4. Before claiming visual done: read [references/screenshot-critique.md](references/screenshot-critique.md)

Do not load more than **two** design skill bodies in one turn (this hub + one satellite).

## When to use

- Landing / marketing / product UI redesign or greenfield visual pages
- Visual polish, hero/composition, brand-facing first viewport
- Russian triggers: макет, лендинг, вёрстка, интерфейс, дизайн страницы, визуальный редизайн

## When not to use

- Pure architecture, debugging, research, or Fusion council without UI output
- Backend APIs, migrations, CLI tools with no visual surface
- Planning-only requests that defer UI to a later wave

## Ambient skills

If ambient `frontend-design` (or similar) also loads, **design-canon bans win** on anti-slop, hero, and brand rules. Exploration tips from ambient skills may inform, but must not override canon bans.

## Fusion compose

On UI/visual mutate waves, prefer Fusion pack `visual-ui` and optional specialist `visual_design_critique`. Do not redesign the Fusion pipeline.

## Roadmap (not shipped in v0.3)

Ideal catalog — phase later, do not claim as shipped:

- Phase 1: `grok-design-audit`, `grok-product-app-ui`, `grok-motion-ui`
- Phase 2: `grok-design-tokens`, `grok-brand-kit`, `grok-design-systems`
- Phase 3: `grok-design-static`, `grok-email-ui`, `grok-illustration`

v0.3 ships **web/UI excellence + design canon only** — not “any design task.”
