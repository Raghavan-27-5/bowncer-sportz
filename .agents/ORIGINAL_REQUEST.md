# Original User Request

## 2026-07-23T07:07:54Z

A new, visually striking section for the Bowncer Sportz Cricket Academy website that integrates and showcases their official YouTube channel content. The section must adhere to the 'cinematic dark sports editorial' aesthetic defined in DESIGN-SYSTEM.md and should act as a premium media showcase. It will be a dedicated full-bleed cinematic section featuring a large "Featured Video" and a carousel/grid of other videos, with the agent team determining the best approach for populating the content within the static site constraints.

Working directory: /home/raghavan/projects/bowncer_sportz
Integrity mode: development

## Verification Resources
- `QA-CHECKLIST.md` in the repository root contains the mandatory checklist for marking any section as complete.
- `DESIGN-SYSTEM.md` contains the fixed visual language (colors, fonts, motion).

## Requirements

### R1. Implement a YouTube media showcase section
Create a new section that prominently features a main video alongside a grid or carousel of secondary videos. The solution must respect the static site constraint (no server-side code) while populating content.

### R2. Adhere strictly to the established design system
The layout, typography, motion, and color palette must strictly follow the "cinematic dark sports editorial" aesthetic. No generic templates or external CDN dependencies for critical rendering are permitted (ensure `file://` previews do not break).

## Acceptance Criteria

### Technical & Aesthetic Validation
- [ ] An automated script or programmatic check confirms no new hardcoded hex colors were introduced in the CSS (only approved variables like `var(--void)`, `var(--ember)`).
- [ ] An automated check confirms no unapproved fonts (e.g., Inter, Roboto) were added.
- [ ] The `QA-CHECKLIST.md` is fully executed and passed by an independent agent evaluator, specifically verifying desktop (~1600px) and mobile (~390px) responsive layouts.
- [ ] The page visually renders correctly even when opened via the `file://` protocol.
- [ ] The section requires zero backend infrastructure or databases to function.
