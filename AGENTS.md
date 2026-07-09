# AGENTS.md — Bowncer Sportz Cricket Academy Website

This file is the entrypoint for any AI coding agent (Claude Code, Cursor,
Copilot, Windsurf, etc.) working on this repository. Read this file fully
before making any change. Then read the other files in this repo root as
directed below, based on what you're being asked to do.

## What this project is

A static marketing website for **Bowncer Sportz Cricket Academy**, a
cricket coaching academy in Chennai, India, founded by **S. Thiyagarajan**
(Ex-IPL RCB player, ICC/BCCI Level 1 certified coach). The site is hosted
on GitHub Pages at a static URL — no backend, no database, no build
pipeline unless explicitly introduced.

The audience is primarily **Indian parents** evaluating cricket coaching
for their children (ages 6–18), browsing on **mobile phones**, in a
market where **trust signals and institutional credibility matter more
than flash**.

## Non-negotiable constraints — read before writing any code

1. **Static site only.** No server-side code, no database, unless a human
   explicitly instructs otherwise in a task file. GitHub Pages serves
   static files only.

2. **No invented facts.** Never invent fees, batch timings, coach names,
   phone numbers, addresses, testimonials, or statistics. If a field is
   required but not supplied, render it visually marked as
   `[PENDING VERIFICATION]` (muted color, italic) rather than guessing.
   See `CONTENT-FACTS.md` for the only facts you are allowed to state.

3. **No CDN dependencies for critical rendering.** Any JS library required
   for the page to render correctly (e.g. Three.js) must be vendored
   locally into `/vendor/` and referenced with a relative path. Do not
   use `<script type="importmap">` or ES module CDN imports — they break
   when the file is opened directly via `file://` (no server), which is
   how non-technical stakeholders will often preview the site. Use the
   classic global-script build (`<script src="./vendor/x.min.js">`)
   instead of ES modules unless you are certain the file will only ever
   be served over `http(s)://`.

4. **Mobile-first, always.** Every layout decision must be verified at a
   ~390px viewport before it is considered done. The primary audience is
   on phones. See `DESIGN-SYSTEM.md` for specific breakpoints.

5. **No generic AI-template aesthetics.** Do not default to Inter,
   system-ui, or Roboto. Do not use purple gradients on white. Do not
   produce a generic hero→3-cards→testimonials→footer template. See
   `DESIGN-SYSTEM.md` for the actual visual direction, which is fixed —
   do not reinterpret or "improve" it without being asked.

6. **WhatsApp over generic contact forms.** In the Indian market, WhatsApp
   CTAs (`https://wa.me/91XXXXXXXXXX`) convert far better than web forms.
   Prefer WhatsApp links for any "contact us" or "book a trial" action
   unless a task file specifies otherwise.

7. **Image performance discipline.** All photographic assets must be
   converted to WebP before being committed (not left as source PNG/JPG
   in the served path). Target: hero-critical images under 150KB each.
   Use `loading="lazy"` and `decoding="async"` on every `<img>` that is
   not above-the-fold; use `fetchpriority="high"` on the one image that
   is the LCP (largest contentful paint) element.

8. **One section at a time.** This project is being built incrementally,
   section by section (hero first, then the section below it, etc.), on
   purpose — to avoid producing a mediocre, unfocused website. Do not
   scaffold pages, sections, or features that were not explicitly
   requested in the current task, even if they seem like obvious next
   steps. Ask, or leave a `<!-- TODO(next-section): ... -->` comment,
   rather than building ahead of scope.

## Files in this repo root — read what's relevant to your task

- `CONTENT-FACTS.md` — the only verified facts about the academy and its
  founder that may be used as copy. Treat this as the single source of
  truth. If you need a fact not listed here, stop and ask rather than
  inventing or inferring one.
- `DESIGN-SYSTEM.md` — the fixed visual language: colors, type, spacing,
  motion rules, and the specific aesthetic direction already chosen for
  this project. Not a suggestion — a specification.
- `BRAND-ASSETS.md` — inventory of logo, photos, and other visual assets,
  where they live, and rules for how each may/may not be used or altered.
- `TECH-NOTES.md` — known gotchas specific to this codebase (e.g. the
  `file://` module-loading bug below), plus how to run and test locally.
- `QA-CHECKLIST.md` — the checklist that must be run and pass before any
  section is considered complete. Run this before saying you're done.

## How to behave with no reference images or human taste available

You will often be asked to build something without a screenshot or mockup
attached to the task. In that situation:

- Do not default to safe/generic choices "to be safe." `DESIGN-SYSTEM.md`
  already encodes the taste decisions that would normally come from a
  human reviewing references — use it as if it were the reference.
- If a task requires a genuinely new design decision not covered by
  `DESIGN-SYSTEM.md` (e.g. a section type that doesn't exist yet), make
  the boldest choice consistent with the existing direction, implement
  it, and flag the decision explicitly in your summary so a human can
  correct it — do not silently pick the safest/blandest option.
- Never introduce a second competing visual style "for variety." Every
  new section must look like it was designed by the same person who
  built the hero.
