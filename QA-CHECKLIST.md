# QA-CHECKLIST.md — Run Before Declaring Any Section Complete

An agent must work through this checklist and be able to honestly confirm
each item before telling a human "this is done." If you cannot verify an
item (e.g. no headless browser available), say so explicitly rather than
silently skipping it.

## Visual / layout

- [ ] Viewed at desktop width (~1600px) — no element overlaps another
      unintentionally (check especially: does text run under/behind a
      photo or graphic in a way that hurts legibility?)
- [ ] Viewed at mobile width (~390px) — content re-stacks sensibly, not
      just shrunk. No text sits illegibly on top of a busy image.
- [ ] No horizontal scroll/overflow at either width
- [ ] All interactive elements (buttons, links) are large enough to tap
      on mobile — minimum ~44×44px touch target

## Content

- [ ] Every factual claim traces back to `CONTENT-FACTS.md`. Zero
      invented fees, names, stats, or testimonials.
- [ ] Any field that should be a real fact but isn't yet available is
      visually marked `[PENDING VERIFICATION]`, not silently omitted or
      guessed.
- [ ] Copy tone matches the existing site voice — direct, short
      sentences, not generic marketing filler ("unlock your potential,"
      "take your game to the next level," etc. — avoid stock phrases
      like this unless they're already established site copy).

## Design consistency

- [ ] Only uses colors defined in `DESIGN-SYSTEM.md`'s CSS variables —
      no new hardcoded hex values
- [ ] Only uses Bebas Neue (display) + Archivo (body) — no other fonts
      introduced
- [ ] New animations reuse the established `fadeUp` pattern and
      `cubic-bezier(.16,1,.3,1)` easing unless there's a documented
      reason for something different
- [ ] Background has some form of atmosphere/texture (gradient, grain,
      glow) — not a flat solid color
- [ ] Does not introduce a second competing aesthetic direction — a
      person scrolling from the hero into this new section should not
      feel like they landed on a different website

## Technical

- [ ] Opens correctly via direct `file://` access (double-click the HTML
      file) — no blank/broken components. This specifically catches the
      ES-module-under-file:// bug documented in `TECH-NOTES.md`.
- [ ] Opens correctly via `http://localhost` as well
- [ ] Checked browser console for errors in both modes above — a
      component can look fine in a screenshot while silently failing
- [ ] Any new image asset is WebP, not PNG/JPG, and has
      `loading="lazy"` + `decoding="async"` (or `fetchpriority="high"`
      if it's the largest above-the-fold image)
- [ ] No new third-party CDN script/module dependency added without
      vendoring it locally per `AGENTS.md` constraint #3
- [ ] No backend/server-side code introduced (this is a static site)

## Scope discipline

- [ ] Only built what was explicitly asked for in the current task — did
      not scaffold additional sections, pages, or features "while I was
      in there"
- [ ] If a design decision had to be made that isn't covered by
      `DESIGN-SYSTEM.md`, it was flagged explicitly in the summary to
      the human, not silently decided and buried in the diff

## Before you report "done" to a human

State explicitly:
1. What you verified (from the checklist above) and how (e.g. "screenshot
   at 1600px and 390px via Playwright, both file:// and http://")
2. What you could NOT verify and why (e.g. "no headless browser available
   in this environment — please check mobile rendering manually")
3. Any decision you made that wasn't explicitly specified, so it can be
   corrected if wrong
