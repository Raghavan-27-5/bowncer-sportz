# Implementation Plan: YouTube Media Showcase Section

## Overview
Build a cinematic dark sports editorial YouTube media showcase section for the Bowncer Sportz Cricket Academy website adhering strictly to static site constraints, `DESIGN-SYSTEM.md`, and `QA-CHECKLIST.md`.

## Milestones & Tasks

### Milestone 1: Codebase Exploration & Technical Design
- Spawn 3 Explorer subagents to analyze `index.html`, `assets/`, `vendor/`, existing CSS/JS, and existing section layouts.
- Formulate implementation strategy: static video embeds / thumbnail cards, responsive grid/carousel layout, CSS variables usage, modal lightbox or inline player swap, and zero external runtime API dependence for basic rendering.

### Milestone 2: YouTube Showcase Implementation
- Worker subagent updates `index.html` (or CSS/JS files) to insert the new YouTube section.
- Design: Featured Video hero player + thumbnail gallery/carousel of academy highlights.
- Aesthetic: Cinematic dark sports editorial using `--void`, `--void-2`, `--ember`, `--ink`, `--ink-dim`, `--line`, Bebas Neue headlines, Archivo body text, subtle background gradients, `fadeUp` keyframe animations.
- Offline/Local File Support: `file://` compatibility guaranteed.

### Milestone 3: Automated Quality & Compliance Checks
- Worker/Challenger subagent writes automated verification script(s) to:
  1. Check for unapproved hex colors in CSS files.
  2. Check for unapproved fonts in CSS/HTML files.
  3. Validate HTML structure and relative asset paths.

### Milestone 4: QA-CHECKLIST Verification & Forensic Audit
- Reviewers & Challengers execute `QA-CHECKLIST.md` (desktop ~1600px and mobile ~390px viewports, `file://` vs `http://` testing).
- Forensic Auditor runs integrity checks to ensure authentic implementation without mock cheats or hardcoded bypasses.
