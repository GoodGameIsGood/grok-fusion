# Design Canon

Single source of truth for Grok design craft. Subagents must follow this file; do not rely on user rules reaching Task workers.

## Tokens-first

Before writing UI code, lock a compact token system:

- **Color:** 4–6 named CSS variables (or theme tokens), not one-off hex mid-render
- **Type:** display + body (+ utility if needed); no Inter / Roboto / Arial / system default stacks unless the existing design system already uses them
- **Space / radius / elevation:** named scale; consistent rhythm
- **Signature:** one memorable element justified by the brief

Derive every color and type decision from tokens after the preflight pass.

## Anti-slop clusters

Do **not** default to these (legitimate only when the brief explicitly asks):

- Purple-on-white or purple-to-indigo gradient themes
- Warm cream background near `#F4F1EA` with high-contrast serif + terracotta accent
- Broadsheet layout: hairline rules, zero border-radius, dense newspaper columns
- Inter / Roboto / Arial / generic system font stacks as the “modern” choice
- Card-as-default wrapping of every section
- Pill clusters, stat strips, icon rows, or fake metrics in the hero
- Glow kits, multi-layer shadows, emoji decoration as style substitutes
- Generic “revolutionize your workflow” copy and fabricated stats

## Brand-first / hero rules

Folded hard rules for branded and promotional surfaces:

1. **One composition** — first viewport reads as one composition, not a dashboard (unless it is a dashboard)
2. **Brand first** — brand/product name is hero-level, not only nav text
3. **Brand test** — if removing the nav makes the first viewport belong to another brand, branding is too weak
4. **Typography** — expressive, purposeful faces; avoid default stacks
5. **Background** — not flat single-color; gradients, imagery, or subtle atmosphere
6. **Full-bleed hero** — dominant edge-to-edge visual plane by default on landings; avoid inset/side-panel/rounded-card heroes unless the existing DS requires it
7. **Hero budget** — brand, one headline, one short supporting sentence, one CTA group, one dominant image; no stats/schedules/address blocks/promos in the first viewport
8. **No hero overlays** — no detached labels, floating badges, promo stickers, or callout chips on hero media
9. **Cards** — default is no cards; never in the hero; cards only when they are the container for user interaction
10. **One job per section** — one purpose, one headline, usually one short supporting sentence
11. **Real visual anchor** — product, place, atmosphere, or context; abstract decoration is not the main idea
12. **Reduce clutter** — cut competing text blocks and decorative chrome
13. **Motion** — at least 2–3 intentional motions on visually led work; respect `prefers-reduced-motion`

When an **existing design system** is present, preserve its tokens and patterns; do not invent a parallel look.

## A11y floor

- Visible keyboard focus; operable without pointer-only
- Contrast sufficient for text and controls (WCAG AA intent)
- Labels for controls; no icon-only without accessible names
- Respect `prefers-reduced-motion`
- Empty and error states explain what to do next

## IP / originality

- Do not clone living artists’ styles or trademarked brand systems as “inspiration paste”
- For branded work: **assets > hex** — logo and real product/UI imagery beat invented color alone
- Prefer original composition for this brief

## Claim hygiene

- Do not claim “best”, “perfect”, “production-ready”, or “any design task covered” without an eval fixture id or evidence
- Soft screenshot critique is a **warn**, not a vanity ship claim

## Soft vs hard screenshot DoD

- **Soft (default):** self-critique checklist; screenshot when browser tooling is available; missing screenshot → WARN, not BLOCK
- **Hard (visual-MVP mutate only):** before/after or final viewport evidence + critique checklist + a11y floor evidence required before done

Screenshots never replace a11y checks. Do not use exploit/PoC “demo UI” as DoD evidence.

## Ambient conflict

When ambient `frontend-design` (or similar) also loads: **canon bans win** on anti-slop, hero, brand, and card rules. Ambient guidance may inform exploration only.
