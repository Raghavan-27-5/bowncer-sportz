# Project: Bowncer Sportz YouTube Media Showcase Section

## Architecture
- Static HTML/CSS/JS architecture (zero backend, zero database, zero build step).
- Dedicated full-bleed cinematic section (`#media-showcase`) inserted at Line 984 in `index.html` between Manifesto (.manifesto-section) and Pathway to Pro (.pathway-section).
- Asymmetrical layout: Dominant featured video stage (70% / 1.5fr) + vertical playlist card gallery and YouTube channel CTA (30% / 1fr) on desktop; single-column stack on mobile (<= 900px / 390px).
- Lite-YouTube Facade pattern: High-performance WebP poster images with SVG ember play button (`--ember`, `--ember-glow`), dynamic iframe swap (`youtube-nocookie.com`) on click.
- Offline & `file://` protocol resilience: Local WebP poster fallback + WhatsApp CTA (`https://wa.me/919840568137`).
- Colors: Strict usage of CSS custom properties (`--void`, `--void-2`, `--ember`, `--ember-glow`, `--ink`, `--ink-dim`, `--line`, `--gold`).
- Fonts: `Bebas Neue` display headers, `Archivo` body text.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Exploration & Architecture | Analyze codebase, design section layout & static data structure | None | DONE |
| 2 | Media Showcase Implementation | Implement YouTube section HTML, CSS, JS, thumbnails, responsive layout | M1 | IN_PROGRESS |
| 3 | Automated Compliance Checks | Programmatic scripts checking hex colors and font compliance | M2 | PLANNED |
| 4 | Review, QA & Forensic Audit | Verification via QA-CHECKLIST.md, Playwright/headless tests, Forensic Integrity Audit | M3 | PLANNED |

## Interface Contracts
- Section HTML ID: `#media-showcase`
- CSS Custom Properties: `:root` (`--void`, `--void-2`, `--ember`, `--ember-glow`, `--ink`, `--ink-dim`, `--line`, `--gold`)
- Display Font: `Bebas Neue`
- Body Font: `Archivo`
- Static Data Object: `YOUTUBE_SHOWCASE_DATA`
- WhatsApp CTA: `https://wa.me/919840568137`

## Code Layout
- `index.html` — Main landing page containing section markup, CSS styles, and inline Vanilla JS facade controller
- `assets/` — CSS, WebP poster images (`assets/showcase_thumb_featured.webp`, `assets/showcase_thumb_2.webp`, etc.)
- `vendor/` — Locally vendored third-party libraries
- `check_hex_colors.py` — Automated hex color validator script
- `check_font_families.py` — Automated font family validator script
