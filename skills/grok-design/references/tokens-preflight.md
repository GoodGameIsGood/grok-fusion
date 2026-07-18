# Tokens Preflight

Run this checklist **before** writing CSS/components for a new visual surface.

## 1. Brief lock

- Subject / product name
- Audience
- Single job of the page or screen
- Existing design system? If yes → extract tokens from code; stop inventing a new palette

## 2. Token map (write down, then code)

```text
color:
  --bg, --fg, --muted, --accent, --accent-fg  (+ optional --danger/--success)
type:
  display: <family> <weight>
  body: <family> <weight>
  utility: <optional>
space: 4/8/12/16/24/32/48 (or project scale)
radius: none | sm | md (pick a strategy; do not randomize per component)
elevation: 0–2 levels max unless product already uses more
signature: <one sentence — the memorable element>
```

## 3. Archetype

Pick **one** visual direction justified by the subject (not a generic “modern SaaS” default). If the choice matches a banned anti-slop cluster in `design-canon.md`, revise unless the brief explicitly requested that look.

## 4. Assets

- Logo paths (light/dark if needed) for branded work
- Hero / product imagery or intentional placeholder policy
- Do not substitute CSS silhouettes for real brand recognition assets when assets are available

## 5. Gate

Only after steps 1–4: implement with `grok-web-ui` (or brownfield patterns). Mid-render invention of new hex values or fonts without updating the token map is a fail.
