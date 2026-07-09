# DESIGN-SYSTEM.md — Visual Language Specification

This is not a style guide of suggestions. It is a specification. An agent
with no taste and no reference images should be able to build a new
section that looks like it belongs on this site by following this
document alone, without seeing the hero.

## Aesthetic direction (fixed — do not reinterpret)

**Cinematic dark sports editorial.** Think: a stadium floodlit at dusk,
not a SaaS dashboard. Every section should feel like it could be a frame
from a sports documentary, not a landing-page template.

Explicitly rejected directions — do not drift toward these even
partially: light/white backgrounds, playful/toy-like illustration,
soft pastel, minimal Scandinavian white space, corporate blue-and-grey
"trust" palettes common to SaaS sites. This is a sports brand built
around a real athlete's credibility, not a fintech product.

## Color

Defined as CSS custom properties. Use these variables — never hardcode
hex values inline.

```css
:root{
  --ink:#f4f1ea;        /* primary text on dark */
  --ink-dim:#b8b2a4;     /* secondary text on dark */
  --void:#07080a;        /* primary background */
  --void-2:#0d0f12;      /* secondary background, slightly lighter */
  --ember:#e2380a;       /* primary accent — CTAs, key emphasis */
  --ember-glow:#ff5622;  /* accent hover state, gradient endpoint */
  --gold:#c9a15a;        /* reserved accent — use sparingly, e.g. credential/trophy moments */
  --line: rgba(244,241,234,0.14); /* hairline borders/dividers */
}
```

Rules:
- Dominant palette is near-black (`--void` family) with warm ember/orange
  as the *only* saturated accent. Do not introduce a second saturated
  hue (no blues, greens, purples) without explicit instruction.
  Thiyagarajan's photo contains blue clothing — that's fine as
  photographic content, but it is not a palette color to design around.
- `--gold` exists for credential/achievement moments (e.g. a stat block,
  a trophy icon) — do not use it as a general accent, it will dilute the
  ember identity if overused.
- Never use pure white (`#fff`) as a text color on dark backgrounds —
  use `--ink` (`#f4f1ea`), which is warm off-white and matches the
  established grade.

## Typography

```css
/* Display / headline font */
font-family: 'Bebas Neue', sans-serif;
/* Body font */
font-family: 'Archivo', sans-serif;
```

Loaded via Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
```

Rules:
- **Never use Inter, Roboto, Arial, or system-ui as the primary font for
  headlines or body text.** This is the single most common "AI slop"
  signal and is explicitly banned.
- Bebas Neue is used exclusively for large display headlines — it is a
  condensed, uppercase-feeling display face. Do not use it for body
  copy or small UI text; it becomes unreadable below ~24px.
- Archivo is used for everything else: body copy, labels, buttons, nav.
- Headlines are typically set in `text-transform: uppercase` with tight
  `line-height` (0.86–0.9) — see hero implementation for exact values.
- Letter-spacing on small uppercase labels (eyebrows, nav, credential
  labels) should be wide: `0.08em`–`0.28em` depending on size. Larger
  text needs less tracking, small text needs more.

## Motion

- **One well-orchestrated load sequence per section**, not scattered
  micro-interactions. On the hero, this means staggered `fadeUp`
  animations with increasing `animation-delay` per element (brand row →
  eyebrow → headline → subcopy → CTAs). Reuse this stagger pattern for
  new sections rather than inventing a new one each time.
- Standard fade-up keyframe already established:
  ```css
  @keyframes fadeUp{
    from{ opacity:0; transform:translateY(16px); }
    to{ opacity:1; transform:translateY(0); }
  }
  ```
- Easing for entrance animation on major elements (e.g. the portrait
  rising into frame): `cubic-bezier(.16,1,.3,1)` — a fast-out, slow-in
  curve. Use this, not `ease-in-out`, for anything meant to feel
  cinematic rather than mechanical.
- Hover states on buttons/links: `transform: translateY(-3px)` plus a
  shadow/glow increase, `transition: .35s cubic-bezier(.16,1,.3,1)`.
- Do not add motion for its own sake. Every animation should either (a)
  sequence attention on load, or (b) respond to direct user action
  (hover, cursor, scroll). Ambient looping animation unconnected to
  content is discouraged outside of the hero's signature 3D ball.

## Spatial composition

- Generous negative space is preferred over dense component-grid
  layouts. This is an editorial/cinematic site, not a dashboard.
- Full-bleed sections (no max-width container hugging content to center)
  are the default for major sections — content should breathe to the
  edges of the viewport, not sit in a boxed 1200px container like a
  typical SaaS site.
- Asymmetry is preferred over centered/symmetric layouts. The hero uses
  a left-heavy text column against a right-anchored photo — new sections
  should similarly avoid perfectly centered, evenly-balanced layouts
  unless there's a specific reason (e.g. a comparison of two equal
  things).

## Backgrounds & texture

- Every section needs atmosphere, not a flat solid color. Use layered
  radial/linear gradients to simulate light (see `.flood` and
  `.hero-vignette` in the hero for the pattern: soft blurred radial
  "floodlight" glows in corners, plus a vignette darkening the edges).
- A subtle grain/noise overlay is applied globally at the `<body>` level
  (see `.grain` in hero) — this should persist site-wide, not be
  hero-only. If building a new page, carry the grain overlay over.
- Do not use flat, textureless solid-color section backgrounds. Even a
  "simple" section needs at least a subtle gradient.

## Trust & credibility patterns (sports-academy specific)

- Credential/stat blocks use a left-border accent + oversized number +
  small uppercase label pattern (see `.credential` in hero). Reuse this
  component pattern for any new stats rather than inventing a new stat
  visual language.
- Trust signals (star ratings, review counts, certifications) should be
  visually present but not desperate — small, confident, understated
  badges rather than large attention-grabbing banners.

## Responsive breakpoints

- Primary breakpoint: `max-width: 720px` (mobile). The hero currently
  only defines one breakpoint — if a new section needs a tablet-specific
  treatment, add `max-width: 1024px` as an intermediate step, but don't
  add breakpoints speculatively.
- Mobile layout philosophy: **do not just shrink the desktop layout.**
  Re-sequence content so it stacks in a sensible reading order, and
  reduce any competing visual elements (e.g. a background photo becomes
  a dim backdrop rather than a foreground element competing with text —
  see `.portrait-wrap` mobile override in the hero for the exact
  pattern).

## What "done" looks like

A new section is only complete if:
1. It uses only the color variables defined above (no new hardcoded hex
   values without updating this file first).
2. It uses Bebas Neue + Archivo, no other font.
3. It has been verified at both a desktop width (~1600px) and mobile
   width (~390px) — see `QA-CHECKLIST.md`.
4. It does not introduce a new animation timing/easing pattern without
   reusing the ones defined above, unless there's a specific reason
   documented in a code comment.
