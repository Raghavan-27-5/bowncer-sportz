## 2026-07-23T07:12:59Z
You are teamwork_preview_worker (Worker M2-1).
Your working directory is: /home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1/
Parent conversation ID: ca9d74ce-15c5-4c8a-b09e-a7452318cf9b

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task: Implement the YouTube Media Showcase section for Bowncer Sportz Cricket Academy website.

Detailed instructions:
1. Read the Explorer reports from Milestone 1:
   - /home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_explorer_m1_1/analysis.md
   - /home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_explorer_m1_2/analysis.md
   - /home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_explorer_m1_3/analysis.md
2. Read AGENTS.md, DESIGN-SYSTEM.md, CONTENT-FACTS.md, TECH-NOTES.md, QA-CHECKLIST.md.
3. Modify `/home/raghavan/projects/bowncer_sportz/index.html` to insert the new `#media-showcase` section ("THE PROCESS IN MOTION") between `.manifesto-section` and `.pathway-section` (~line 984).
4. Include all CSS styles in the `<style>` block of `index.html` (or dedicated stylesheet if appropriate), strictly using CSS custom properties (`--void`, `--void-2`, `--ember`, `--ember-glow`, `--ink`, `--ink-dim`, `--line`, `--gold`). DO NOT introduce any new hardcoded hex color values in the CSS rules for `#media-showcase`.
5. Ensure display typography uses `Bebas Neue` and body text uses `Archivo`.
6. Implement the Lite-YouTube facade player pattern:
   - Featured video stage (large video card)
   - Secondary playlist thumbnails grid / vertical card stack (with active thumbnail state)
   - SVG Ember Play Button overlay
   - Click-to-play facade poster swap with privacy-enhanced YouTube iframe (`https://www.youtube-nocookie.com/embed/...`)
   - Channel Subscribe CTA linking to official channel / WhatsApp CTA (`https://wa.me/919840568137`)
   - Offline / `file://` protocol fallback card with WhatsApp CTA if iframe/network is unavailable.
7. Generate valid WebP thumbnail assets in `/home/raghavan/projects/bowncer_sportz/assets/` (e.g. `assets/showcase_thumb_featured.webp`, `assets/showcase_thumb_2.webp`, `assets/showcase_thumb_3.webp`) using Python/Pillow or image processing.
8. Any unverified video titles/IDs must be clearly marked `[PENDING VERIFICATION]` per CONTENT-FACTS.md.
9. Verify your changes: test both desktop (~1600px) and mobile (~390px) responsiveness, ensure `file://` compatibility, and verify zero console errors.
10. Update `progress.md` in your working directory as you complete steps.
11. Summarize your implementation in `changes.md` and `handoff.md` in your working directory.
12. When done, send a message to parent (ID: ca9d74ce-15c5-4c8a-b09e-a7452318cf9b) with your implementation report.
