# Responsive and Accessibility

## Breakpoints

- Design mobile and desktop as intentional layouts (not only “stack everything”)
- Primary CTA reachable without horizontal scroll
- Touch targets ≥44px where pointer input is expected
- Images: meaningful `alt` or empty alt for decorative; prefer modern formats when the stack allows

## Accessibility checklist

- Semantic landmarks (`header`, `main`, `nav`, `footer`) and one `h1`
- Interactive elements are `<button>` / `<a>` (not clickable `div`s)
- Visible `:focus-visible` styles from tokens
- Color contrast for text and UI chrome (AA intent)
- Form inputs have associated labels
- Errors describe what failed and how to fix
- `prefers-reduced-motion: reduce` disables non-essential animation

## Performance hygiene (UI)

- Avoid huge unoptimized hero assets when a lighter crop works
- Prefer CSS for simple motion over heavy animation libraries unless already in the project
