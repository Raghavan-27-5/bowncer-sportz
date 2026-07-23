## 2026-07-23T07:36:46Z
You are teamwork_preview_worker (Worker M2-2 - Polish & Bug Fix Worker).
Your working directory is: /home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_2/
Parent conversation ID: ca9d74ce-15c5-4c8a-b09e-a7452318cf9b

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task: Fix the 4 issues identified during Reviewer 2 and Challenger 2 evaluation of `/home/raghavan/projects/bowncer_sportz/index.html`.

Issues to fix:
1. **Mobile Fallback Card Clipping (16:9 Aspect Ratio Overflow)**:
   - On ~390px mobile viewports, `.video-thumb-wrap` locks stage height to 16:9 (~192px). The injected `.video-offline-card` has ~312px of content height. Lacking overflow handling, the fallback card (including WhatsApp CTA button) is clipped.
   - Fix: Ensure `.video-thumb-wrap` or `.video-offline-card` has `overflow-y: auto; max-height: 100%;` or allows container growth when fallback card is rendered, so all text and CTA buttons are 100% visible and accessible on mobile.

2. **Touch Target Height (<44px) on `.btn--sm`**:
   - `.btn--sm` currently has padding resulting in ~35px height (< 44px requirement).
   - Fix: Update CSS for `.btn--sm` to set `min-height: 44px; display: inline-flex; align-items: center; justify-content: center;` (and verify padding `13px 20px` or similar) so every button satisfies the mandatory 44x44px touch target height on mobile screens per QA-CHECKLIST.md.

3. **Fallback Card Copy for Online Pending Videos**:
   - When browsing online over HTTP, clicking a pending video renders a card stating "ONLINE STREAMING REQUIRED", which misinforms users that their internet connection is missing.
   - Fix: Update JavaScript logic in `renderOfflineCard()` to differentiate offline/file protocol vs online pending video:
     - If `!navigator.onLine` or `location.protocol === 'file:'`: display "OFFLINE / LOCAL PREVIEW MODE" or "ONLINE STREAMING REQUIRED".
     - If online (`location.protocol !== 'file:' && navigator.onLine`) and video ID is `[PENDING VERIFICATION]`: display "MEDIA CONTENT PENDING VERIFICATION" with subtext explaining that official academy video clips will be linked here shortly, along with the WhatsApp CTA (`https://wa.me/919840568137`).

4. **Hardcoded Pending Badge on Poster Reset**:
   - `resetStageToPoster()` currently hardcodes `<span class="pending-badge">[PENDING VERIFICATION]</span>` into `badgeGroup.innerHTML`.
   - Fix: Make badge rendering dynamic based on `item.pending` (or whether `item.youtubeId` starts with `[PENDING`). If `item.pending` is true, render the badge; otherwise clear `badgeGroup.innerHTML`.

Instructions:
1. Modify `/home/raghavan/projects/bowncer_sportz/index.html` to apply these 4 fixes cleanly.
2. Ensure CSS custom properties (`--void`, `--void-2`, `--ember`, `--ember-glow`, `--ink`, `--ink-dim`, `--line`, `--gold`) and typography (`Bebas Neue` & `Archivo`) remain 100% compliant with ZERO new hardcoded hex colors.
3. Test your fixes locally (run automated scripts / check mobile layout at 390px).
4. Update `progress.md` in your working directory.
5. Write `changes.md` and `handoff.md` summarizing your fixes.
6. When done, send a message to parent (ID: ca9d74ce-15c5-4c8a-b09e-a7452318cf9b).
