# Handoff Report: YouTube Media & Static Data Strategy
**Agent:** `teamwork_preview_explorer_m1_2` (Explorer 2 - Media & Static Data Strategy Explorer)
**Date:** 2026-07-23
**Handoff Type:** Hard (Milestone 1 Explorer Analysis Complete)

---

## 1. Observation

1. **Project Stack & Workspace Inspection:**
   - Stack: Pure HTML/CSS/JS (no framework, no build tool, no bundler, no package dependency).
   - Core files inspected: `CONTENT-FACTS.md` (lines 1–128), `BRAND-ASSETS.md` (lines 1–103), `TECH-NOTES.md` (lines 1–112), `DESIGN-SYSTEM.md` (lines 1–164), `AGENTS.md`, and `assets/` directory (`logo.webp`, `thiyagarajan_hero_graded.webp`, `arun_karthik.webp`, `shiva_vashist.webp`, `thiyagarajan_rcb.webp`).
2. **Technical Constraints Observed:**
   - `TECH-NOTES.md` line 33: `<script type="module">` breaks under `file://` protocol due to browser CORS origin restrictions. All JS must be plain classic script syntax.
   - `AGENTS.md` constraint #3 & `BRAND-ASSETS.md` line 95: All photographic raster assets must be WebP format.
   - `CONTENT-FACTS.md` line 118: No unverified video IDs or fees exist in facts. Unverified YouTube data must be rendered with `[PENDING VERIFICATION]`.
3. **Design System Specification:**
   - Colors: `--void` (`#07080a`), `--void-2` (`#0d0f12`), `--ember` (`#e2380a`), `--ember-glow` (`#ff5622`), `--ink` (`#f4f1ea`), `--ink-dim` (`#b8b2a4`), `--line` (`rgba(244,241,234,0.14)`), `--gold` (`#c9a15a`).
   - Fonts: Headlines in `Bebas Neue`, body/meta in `Archivo`.

---

## 2. Logic Chain

1. **Zero-Backend Requirement → Static Data Object Schema:**
   - Because no backend API or server-side DB is permitted, YouTube showcase metadata must be defined statically via client-side JavaScript object arrays (`YOUTUBE_SHOWCASE_DATA`) or pre-rendered HTML `data-*` attributes.
   - This removes runtime API key dependencies, YouTube Data API quota issues, and external network delays on initial render.

2. **Core Web Vitals & `file://` Compatibility → Facade Poster Pattern:**
   - Direct `<iframe>` embeds automatically fetch ~1MB+ of YouTube runtime scripts and tracking cookies, causing layout shifts (CLS) and thread blocking.
   - Under `file://` or offline preview, direct YouTube `<iframe>` embeds render broken CORS frame boxes.
   - Using a **Lite Facade Poster** image frame delays iframe instantiation until user clicks the play button, guaranteeing fast page loads (< 2.5s LCP), zero third-party script execution on load, and clean offline poster rendering.

3. **Offline & Network Resilience → Multi-Tier Poster Fallbacks:**
   - Storing local WebP poster images (`assets/video-posters/*.webp`) provides an immediate visual fallback if remote YouTube CDN thumbnails (`img.youtube.com`) are unreachable.
   - Detecting `window.location.protocol === 'file:'` or offline status enables displaying a clean, dark sports editorial notice card with direct WhatsApp CTA (`https://wa.me/919840568137`).

---

## 3. Caveats

- **YouTube Video IDs:** Official YouTube Video IDs for Bowncer Sportz YouTube channel are not yet listed in `CONTENT-FACTS.md`. Placeholder IDs in data files/HTML MUST remain explicitly tagged with `[PENDING VERIFICATION]`.
- **Local WebP Poster Assets:** New local WebP poster images (`assets/video-posters/*.webp`) need to be processed and placed in `assets/` by implementers during Milestone 2.

---

## 4. Conclusion

The recommended architecture for the YouTube Showcase section is a **Zero-Backend Static Data + Lite Facade Poster Player** featuring:
- Asymmetric 2-column layout (Main stage player spotlight + sidebar thumbnail playlist on desktop, full-width responsive stack on mobile ~390px).
- Click-to-play Lite Facade pattern with instant dynamic iframe swapping.
- Pre-processed WebP poster fallback pipeline (`assets/video-posters/*.webp`).
- Automatic offline / `file://` preview fallback with branded WhatsApp CTA banner.
- Strict visual compliance with `DESIGN-SYSTEM.md` color variables (`--void`, `--void-2`, `--ember`, `--ink`), `Bebas Neue` display headers, and `fadeUp` entry animations.

Detailed specifications, data schemas, and CSS blueprints are documented in `.agents/teamwork_preview_explorer_m1_2/analysis.md`.

---

## 5. Verification Method

1. **Data Model Verification:**
   - Inspect `analysis.md` section 2.1 for the complete `YOUTUBE_SHOWCASE_DATA` schema and HTML `data-*` attribute layout.
2. **`file://` Protocol Local Preview:**
   - Open `index.html` via `file:///` in any modern browser. Verify zero console errors, clean poster facade rendering, and proper fallback UI state when offline.
3. **Responsive Breakpoint Verification:**
   - Inspect layout at desktop (1600px) and mobile (~390px) viewports to verify seamless card stacking and play button scaling.
