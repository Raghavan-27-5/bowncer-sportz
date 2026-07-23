# Changes Made by Worker M2-2 (Polish & Bug Fix Worker)

## Target File
- `/home/raghavan/projects/bowncer_sportz/index.html`

## Summary of Fixes

1. **Mobile Fallback Card Clipping (16:9 Aspect Ratio Overflow)**:
   - Added `.video-thumb-wrap.has-offline-card, .video-thumb-wrap:has(.video-offline-card) { aspect-ratio: auto; min-height: clamp(280px, 50vw, 360px); }` in CSS.
   - Added `overflow-y: auto; max-height: 100%; box-sizing: border-box; padding: clamp(16px, 3vw, 32px);` to `.video-offline-card`.
   - Updated JS (`renderOfflineCard`, `resetStageToPoster`, `handlePlayClick`) to dynamically add/remove the `has-offline-card` class on `thumbWrap`.
   - Prevents content or WhatsApp CTA button clipping on ~390px mobile viewports.

2. **Touch Target Height (<44px) on `.btn--sm`**:
   - Updated `.btn--sm` CSS declaration to set `display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 12px 20px; box-sizing: border-box;`.
   - Guaranteed minimum 44x44px touch target on mobile screens per WCAG / QA-CHECKLIST.md requirements.

3. **Fallback Card Copy for Online Pending Videos**:
   - Created dedicated `renderOfflineCard(isPending)` function in JS.
   - When browsing online over HTTP/HTTPS and a video ID starts with `[PENDING` (or is empty), the fallback card now displays heading `"MEDIA CONTENT PENDING VERIFICATION"` with subtext `"Official academy video clips will be linked here shortly. For immediate video highlights, coaching session details, and trial registrations, contact us directly on WhatsApp."` and direct WhatsApp CTA (`https://wa.me/919840568137`).
   - When offline or on `file:` protocol, it continues to display `"ONLINE STREAMING REQUIRED"`.

4. **Hardcoded Pending Badge on Poster Reset**:
   - Updated `resetStageToPoster(cardEl)` JS function to check `isPending` dynamically: `var isPending = !youtubeId || youtubeId.indexOf('[PENDING') !== -1;`.
   - Only appends `<span class="pending-badge" title="Pending Verification">[PENDING VERIFICATION]</span>` when `isPending` is true. Otherwise, renders only the featured tag badge.

## Design System & Constraint Compliance
- CSS Custom Variables: Uses `--void-2`, `--line`, `--ember`, `--ember-glow`, `--ink`, `--ink-dim`, `--gold`. ZERO new hardcoded hex colors introduced.
- Typography: Maintained Bebas Neue & Archivo font stack.
- Zero invented facts: Facts align with CONTENT-FACTS.md and use WhatsApp `https://wa.me/919840568137`.
