# BRAND-ASSETS.md — Asset Inventory & Usage Rules

## Logo

- **File:** `assets/logo.webp`
- **Source:** AI-generated badge illustration — orange background, crossed
  cricket bats, two batting helmets, a cricket ball, a running player
  silhouette, microphone icon, and the wordmark "BOWNCER SPORTZ" with
  tagline "LIVE THE MOMENT, OWN THE GAME."
- **Known limitation:** the logo has a solid orange background baked into
  the image (not a transparent PNG). Do not attempt to color-key or
  silhouette-cut this logo — the illustration contains orange/red tones
  internally (helmets, ball) that make clean background removal
  unreliable. It has been treated as a **contained badge** (circular
  crop in the hero) rather than an isolated cutout. Continue using it
  this way — inside a shape (circle, rounded rect, card) — rather than
  attempting to float it as a bare silhouette on other backgrounds.
- **Tagline on the logo itself:** "LIVE THE MOMENT, OWN THE GAME" — this
  is a *different* tagline from the site's existing "PROCESS. PROGRESS.
  PERFORM." Both are real and verified, but do not merge or confuse them.
  If asked to feature "the tagline" without specification, ask which one
  is meant — they serve different purposes (logo tagline = brand
  slogan; site tagline = coaching philosophy statement).

## Founder photos

Two source photos exist. Both are real, unedited-except-as-noted below.

1. **RCB jersey photo** — Thiyagarajan in Royal Challengers Bangalore
   kit, arms crossed, white background. Communicates playing credibility
   / athletic credential. **Not currently used on the built hero.**
   Available for future sections (e.g. an "About the Founder" page or a
   playing-career section) where his RCB history is the focus.

2. **Suit photo** — Thiyagarajan in a navy waistcoat/shirt, holding his
   jacket, grey studio background. Communicates founder/director
   authority. **This is the photo used in the current hero.**
   - Background has been removed (via `rembg`/u2net model) and the
     cutout has been color-graded: contrast +12%, saturation −8%,
     brightness −3%, plus a manual shadow/highlight split-tone (cool
     tint pushed into shadows, warm tint pushed into highlights) to
     match the ember/void palette.
   - Processed file: `assets/thiyagarajan_hero_graded.webp`
   - **Do not re-process the original source photo through a different
     grading pipeline for a new section without matching this same
     grade** — inconsistent color treatment of the same person across
     sections will look like an error, not a style choice. If a new
     section needs this photo, reuse `thiyagarajan_hero_graded.webp`
     directly rather than re-deriving it from source.

### If a new photo of Thiyagarajan is supplied later

Apply the same processing pipeline for consistency:
1. Background removal (rembg, u2net model, or equivalent)
2. Contrast +12%, saturation −8%, brightness −3%
3. Cool tint into shadows, warm tint into highlights (see
   `DESIGN-SYSTEM.md` color section for the exact hex values this should
   trend toward: shadows trend toward `--void`/`--void-2`, highlights
   trend toward `--ember-glow`)
4. Export as WebP, quality 88, target under 150KB

## Fonts

Loaded from Google Fonts CDN (this is fine — fonts are not
render-blocking in the same way JS modules are, and Google Fonts serves
proper CORS headers). See `DESIGN-SYSTEM.md` for the exact `<link>` tags.
Do not self-host fonts unless a human asks for it (e.g. for GDPR/privacy
reasons some clients want no third-party font requests — not a current
requirement here).

## Three.js (3D library)

- **File:** `vendor/three.min.js` — vendored locally, classic UMD/global
  build (not ES module), version 0.128.0.
- **Why vendored instead of CDN:** avoids CORS failures when the site is
  opened via `file://` (no server) for local preview, and removes a
  third-party runtime dependency from the production site entirely.
- **Why the classic build and not the ES module build:** ES module
  imports (`<script type="module">` + `<script type="importmap">`) are
  blocked by browsers when a page is opened directly from disk
  (`file://` origin) rather than served over `http(s)://`. The classic
  global-script build (`<script src="./vendor/three.min.js">`, which
  exposes a `THREE` global) works in both cases. **Do not switch back to
  the ES module version** unless you are certain every consumer of this
  site will always use a real HTTP server — GitHub Pages does serve over
  HTTPS, but local preview by non-technical stakeholders (opening the
  HTML file by double-click) is a real, expected use case for this
  project and must keep working.
- If you need a newer Three.js version, download it the same way this
  one was obtained: `npm pack three@<version>` → extract the tarball →
  copy `package/build/three.min.js` into `vendor/`. Do not add a
  `node_modules` dependency or build step for this — the project has no
  bundler and should not gain one without explicit instruction.

## Image format policy

All photographic/logo raster assets served to the browser must be WebP,
not PNG/JPG, unless there's a specific compatibility reason documented
inline. Source PNGs used only for processing (e.g. an original
pre-background-removal photo) do not need to be committed into the
`assets/` folder that ships to production — keep processing intermediates
out of the served path.
