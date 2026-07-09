# Bowncer Sportz — Home Hero (v1.1)

## For AI coding agents (Claude Code, Cursor, Copilot, etc.)

**Read `AGENTS.md` first.** It's the entrypoint doc and links to
everything else you need: verified facts (`CONTENT-FACTS.md`), the fixed
visual language (`DESIGN-SYSTEM.md`), asset usage rules
(`BRAND-ASSETS.md`), technical gotchas (`TECH-NOTES.md`), and a
pre-completion checklist (`QA-CHECKLIST.md`). These docs assume you have
no prior context, no reference images, and no access to the conversation
that produced this site — everything you need is written down.

## For humans

## How to view
Open `index.html` directly in a browser (double-click it), or serve
locally:
```
cd site
python3 -m http.server 8000
```
Then visit `http://localhost:8000`.

Both methods now work correctly — see the fix note below.

## v1.1 fix: the 3D ball wasn't visible
If you tested v1 and the cricket ball never appeared: that was a real
bug, not a fluke. It used an ES module (`<script type="module">`) to load
Three.js from a local file, which browsers block when a page is opened
directly via `file://` (double-clicking the HTML file) rather than
served over `http://`. Fixed by switching to the classic global-script
Three.js build (`vendor/three.min.js`) — this works identically whether
you double-click the file or serve it. Confirmed working in both modes
before this zip was built. Full explanation in `TECH-NOTES.md`.

## What's in this hero
- Dark stadium-at-dusk environment (CSS gradients + floodlight glows, no images)
- Thiyagarajan's suit photo: background removed, cinematically color-graded
  (cool shadows / warm highlights), composited into the scene
- Headline: "BUILT FROM THE INSIDE" with gradient accent on the last word
- Credential strip: 20+ players to Nationals, 4 countries coached, ICC+BCCI L1
- Bowncer Sportz logo integrated as a badge next to the brand name
- 3D cricket ball (Three.js, WebGL) that idles near the headline and
  follows the cursor as a trailing companion on desktop; on touch devices
  it sits static in the upper-right, no cursor tracking
- Subtle grain overlay, custom cursor dot, scroll cue
- Fully responsive: mobile layout re-stacks with portrait as a dim backdrop
  behind the text (not fighting it) rather than shrinking the desktop layout

## Known sandbox-only caveat
While building this I hit a Google Fonts request returning 403 in my own
build sandbox, because that domain isn't on my sandbox's network
allowlist. This is NOT a real bug — it will not happen on GitHub Pages or
in your actual browser. Google Fonts will load normally there.

## What I did NOT touch
- The rest of the existing site (about, programs, contact, etc.) — untouched,
  per your instruction to scope to home hero only
- No fees, batch timings, or unverified claims were invented — all credential
  numbers (20+, 4 countries, ICC/BCCI L1) came directly from the PPT slide
  you sent
- Form/backend decisions (Formspree etc.) — deferred as agreed

## Performance
- Portrait: 840KB PNG → 102KB WebP
- Logo: 1.3MB PNG → 86KB WebP
- Three.js: vendored locally (~1.1MB, loaded once, cached)

## Suggested next step
Once you review this hero and either approve it or mark up what's off,
next scope would logically be: the section immediately below the hero
(same discipline — one section at a time, not the whole site).
