# TECH-NOTES.md — Technical Gotchas & Local Development

## Stack

Plain HTML/CSS/JS. No framework, no bundler, no package.json, no build
step. This is intentional — see `AGENTS.md` constraint #1 (static site
only) and constraint #3 (no CDN dependencies for critical rendering).
Do not introduce React, Vue, Webpack, Vite, or any build tooling without
explicit human instruction. If a future task genuinely requires a build
step, flag it as a decision for a human rather than silently adding one.

## How to run this locally

Two ways, both must work:

**1. Direct file open (no server)**
Double-click `index.html`, or open it via `file:///path/to/index.html`
in a browser. This MUST work with no console errors related to script
loading. This is how non-technical people (the client, stakeholders)
will typically preview the site — do not assume a server is always
running.

**2. Local server (for testing things that behave differently over HTTP)**
```
python3 -m http.server 8000
```
Then visit `http://localhost:8000`.

Anything that works differently between these two modes is a bug unless
explicitly justified. The known historical example of this class of bug
is documented below.

## Known gotcha: ES modules break under `file://`

**Symptom:** A component (e.g. the Three.js cricket ball in the hero)
renders fine when the site is served over `http://localhost:...` but is
completely invisible when the HTML file is opened directly by
double-clicking it.

**Cause:** `<script type="module">` and `<script type="importmap">` are
subject to browser CORS/security restrictions that block them entirely
under the `file://` origin. The browser silently fails to load the
module — no visible error to a non-technical user, just a missing
component. Opening dev tools shows a CORS-style console error.

**Fix already applied:** The site uses the classic global-script Three.js
build (`vendor/three.min.js`, exposes a `THREE` global) loaded via a
plain `<script src="...">` tag, not an ES module import. This works
identically under both `file://` and `http(s)://`.

**Rule going forward:** Do not introduce `<script type="module">` for
anything that needs to work when the file is opened directly from disk.
If you must use ES modules for a good reason, that's a signal the
project now requires "must be served over HTTP" as a hard requirement —
raise that explicitly with a human rather than assuming it's fine.

## WebGL / 3D rendering notes

- The cricket ball in the hero is a `THREE.SphereGeometry` with two
  offset `THREE.TorusGeometry` rings standing in for stitched seams —
  it's procedural geometry, not an imported 3D model file. There is no
  `.glb`/`.gltf`/`.obj` asset for the ball; if a more detailed/realistic
  ball model is wanted later, that would be a new asset + loader
  (`GLTFLoader`) addition, not a modification of the existing procedural
  approach.
- The renderer is intentionally small (120×120px canvas) and positioned
  as a companion element near the cursor, not a full-screen 3D scene.
  Do not scale this up into a large hero-dominating 3D element without
  being asked — the agreed design decision (see chat history / task
  brief) was explicitly that the 3D ball is a **supporting detail**, not
  the primary hero element.
- On touch devices (`@media (hover: none)`), the ball does not track the
  cursor — there is no cursor. It renders in a static idle position,
  gently auto-rotating. Do not attempt to wire touch-drag tracking to
  the ball unless asked; a static idle 3D element is the intended touch
  behavior.

## Testing / screenshotting locally with an agent

If you have access to a headless browser tool (e.g. Playwright), verify
visual changes by:
1. Starting a local server AND taking the screenshot in the same shell
   invocation/session if your environment tears down background
   processes between tool calls — a server started in one command and
   screenshotted in a separate command may fail with connection refused
   if the process doesn't persist across calls in your environment.
2. Testing at minimum two viewports: ~1600×900 (desktop) and 390×844
   (mobile — matches a standard iPhone viewport).
3. Testing both `file://` and `http://localhost` if you've touched
   anything involving `<script>` tags, to catch the module-loading class
   of bug described above before it ships.
4. Capturing browser console output (`page.on("console", ...)` and
   `page.on("pageerror", ...)` in Playwright) alongside the screenshot —
   a visually-plausible screenshot can still have a broken component if
   you don't check console errors too.

## Performance targets

- LCP (Largest Contentful Paint) < 2.5s
- CLS (Cumulative Layout Shift) < 0.1
- These are from `DESIGN-SYSTEM.md`'s parent guidance and apply
  site-wide, not just the hero.

## Deployment

GitHub Pages, serving directly from this repo. No CI/build step exists.
Pushing to the deployed branch (check repo settings for which branch —
commonly `main` or `gh-pages`) publishes immediately. Because there is no
build step, whatever is committed is exactly what ships — there is no
transpilation, minification, or bundling happening automatically. If you
want minified output, you must do it manually and commit the result.
