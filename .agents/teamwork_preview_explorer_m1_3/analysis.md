# Comprehensive Quality & Compliance Analysis & Automated Inspection Suite Design

**Author**: teamwork_preview_explorer (Quality & Compliance Explorer)  
**Date**: 2026-07-23  
**Working Directory**: `/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_explorer_m1_3/`  
**Target Project**: Bowncer Sportz Cricket Academy Website  

---

## 1. Executive Summary & Scope

As Quality & Compliance Explorer, this investigation establishes the exact specification, design, and script architecture required to enforce the strict guidelines of `DESIGN-SYSTEM.md`, `QA-CHECKLIST.md`, `TECH-NOTES.md`, and `AGENTS.md`.

The Bowncer Sportz website is a static, cinematic dark sports editorial website. To maintain visual harmony and technical integrity across iterations, automated compliance tooling and responsive verification strategies are required to validate three primary compliance dimensions:
1. **Color Compliance**: Elimination of unapproved hardcoded hex colors in CSS files and HTML `<style>` / inline `style` attributes, ensuring usage of `:root` CSS variables defined in `DESIGN-SYSTEM.md`.
2. **Typography Compliance**: Strict enforcement of approved display (`Bebas Neue`) and body (`Archivo`) font families, flagging banned fonts (`Inter`, `Roboto`, `Arial`, `system-ui`, `monospace`, etc.).
3. **Protocol & Responsive Verification**: Automated layout, console error, touch target, and overflow testing across both `http://localhost` and direct `file://` disk access at desktop (`~1600px`) and mobile (`~390px`) viewports.

---

## 2. Synthesis of Specifications & Existing Codebase Audit Findings

### 2.1 Specification Baseline
- **`DESIGN-SYSTEM.md`**: Defines fixed CSS custom properties:
  - `--ink`: `#f4f1ea` (primary off-white text)
  - `--ink-dim`: `#b8b2a4` (secondary text)
  - `--void`: `#07080a` (primary dark background)
  - `--void-2`: `#0d0f12` (secondary dark background)
  - `--ember`: `#e2380a` (primary CTA accent)
  - `--ember-glow`: `#ff5622` (accent hover/glow)
  - `--gold`: `#c9a15a` (reserved credential accent)
  - `--line`: `rgba(244,241,234,0.14)` (dividers)
  - **Typography Rules**: Display headlines MUST use `Bebas Neue`. Body copy MUST use `Archivo`. Pure white (`#fff`) text and generic fonts (`Inter`, `Roboto`, `Arial`, `system-ui`, `monospace`) are prohibited.
- **`QA-CHECKLIST.md`**: Requires verification at `~1600px` (desktop) and `~390px` (mobile), zero horizontal scroll/overflow, minimum 44x44px tap targets, zero console errors under both `file://` and `http://localhost`, and WebP image optimization.
- **`TECH-NOTES.md`**: Documents the critical `file://` CORS gotcha: ES modules (`<script type="module">` / `importmap`) break when loaded via `file://`. Plain classic global scripts (`vendor/three.min.js`) must be used.

### 2.2 Baseline Codebase Inspection Observations
An exploratory scan of the existing HTML/CSS code (`index.html`, `about.html`, `programs.html`, `locations.html`) revealed several compliance violations that automated scripts must catch:
1. **Hardcoded Hex Colors**:
   - `index.html` lines 894, 906, 930, 936, 954, 959 use hardcoded `#fff` or `rgba(255,255,255,...)` for text and headlines.
   - `index.html` lines 944–946 use hardcoded UI hex colors (`#ff5f56`, `#ffbd2e`, `#27c93f`) in dashboard dot mockups.
   - `index.html` line 899 uses hardcoded gradient hex `#ffd700`.
2. **Unapproved Font Declarations**:
   - `index.html` lines 907, 929, 937, 947, 950, 953, 961 use `font-family: monospace;` for labels, numbers, and stats.
   - `about.html` lines 148, 222 use `font-family: monospace;`.
   - `locations.html` line 100 uses `font-family: monospace;`.
   - `programs.html` line 262 uses `font-family: monospace;`.

These findings confirm the necessity of automated linting scripts to prevent compliance regression.

---

## 3. Automated Check #1: Hex Color Scanner Script Architecture

### 3.1 Design Requirements
- **Target Files**: All `.css` files, HTML `<style>` blocks, and inline `style="..."` attributes within `index.html`, `about.html`, `programs.html`, `locations.html`, etc.
- **Exclusions**: `node_modules/`, `vendor/`, `.git/`, `.agents/`, `venv/`.
- **Approved Hex Whitelist**:
  - Declarations defining `:root` variables: `--ink` (`#f4f1ea`), `--ink-dim` (`#b8b2a4`), `--void` (`#07080a`), `--void-2` (`#0d0f12`), `--ember` (`#e2380a`), `--ember-glow` (`#ff5622`), `--gold` (`#c9a15a`).
  - Equivalent short/case variations of approved variables: `#f4f1ea`, `#b8b2a4`, `#07080a`, `#0d0f12`, `#e2380a`, `#ff5622`, `#c9a15a` (case-insensitive).
- **Rule Enforcement**: Any other hex color (e.g. `#fff`, `#ffffff`, `#333`, `#27c93f`, `#ffd700`) outside of `:root` variable definitions is reported as a violation.

### 3.2 Python Script Implementation Specification (`check_hex_colors.py`)

```python
#!/usr/bin/env python3
"""
Hex Color Compliance Scanner
Scans CSS files and HTML style tags/attributes for unapproved hardcoded hex colors.
"""

import sys
import re
from pathlib import Path

# Approved hex colors defined in DESIGN-SYSTEM.md (normalized to lowercase 6-digit hex)
APPROVED_HEX_COLORS = {
    "#f4f1ea", # --ink / --line base
    "#b8b2a4", # --ink-dim
    "#07080a", # --void
    "#0d0f12", # --void-2
    "#e2380a", # --ember
    "#ff5622", # --ember-glow
    "#c9a15a", # --gold
}

HEX_REGEX = re.compile(r'#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b')

def normalize_hex(hex_str):
    h = hex_str.lower()
    if len(h) == 4: # #abc -> #aabbcc
        return f"#{h[1]*2}{h[2]*2}{h[3]*2}"
    elif len(h) == 9: # #aabbccdd (ignore alpha for base color check)
        return h[:7]
    return h

def scan_file(file_path):
    violations = []
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    for line_num, line in enumerate(lines, 1):
        # Ignore comments or :root variable declarations where hex values are defined
        if "--ink:" in line or "--ink-dim:" in line or "--void:" in line or \
           "--void-2:" in line or "--ember:" in line or "--ember-glow:" in line or \
           "--gold:" in line:
            continue

        matches = HEX_REGEX.findall(line)
        for match in matches:
            norm = normalize_hex(match)
            if norm not in APPROVED_HEX_COLORS:
                violations.append({
                    "file": str(file_path),
                    "line": line_num,
                    "hex": match,
                    "normalized": norm,
                    "content": line.strip()
                })
    return violations

def main():
    repo_root = Path(__file__).resolve().parent.parent
    html_css_files = list(repo_root.glob("*.html")) + list(repo_root.glob("assets/**/*.css"))
    
    total_violations = []
    for f in html_css_files:
        violations = scan_file(f)
        total_violations.extend(violations)

    if total_violations:
        print(f"❌ FAIL: Found {len(total_violations)} unapproved hex color(s):")
        for v in total_violations:
            print(f"  {v['file']}:{v['line']} -> Found '{v['hex']}' (Normalized: {v['normalized']})")
            print(f"    Line: {v['content']}")
        sys.exit(1)
    else:
        print("✅ PASS: All CSS and HTML hex colors strictly comply with DESIGN-SYSTEM.md.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 4. Automated Check #2: Font Family Scanner Script Architecture

### 4.1 Design Requirements
- **Target Files**: All `.css` files and HTML `<style>` / `style="..."` attributes.
- **Approved Font Families**:
  - `Bebas Neue` (Display / Headline)
  - `Archivo` (Body / UI)
  - Generic fallback `sans-serif` when accompanying Bebas Neue or Archivo.
- **Prohibited Fonts**: `Inter`, `Roboto`, `Arial`, `system-ui`, `Helvetica`, `monospace`, `Times New Roman`, `Courier New`, etc.
- **Rule Enforcement**: Any `font-family` declaration referencing an unapproved font name is flagged with line details.

### 4.2 Python Script Implementation Specification (`check_font_families.py`)

```python
#!/usr/bin/env python3
"""
Font Family Compliance Scanner
Scans CSS and HTML files to enforce allowed font families ('Bebas Neue' and 'Archivo').
"""

import sys
import re
from pathlib import Path

APPROVED_FONTS = {"bebas neue", "archivo", "sans-serif"}
FONT_FAMILY_REGEX = re.compile(r'font-family\s*:\s*([^;}"\']+);?', re.IGNORECASE)

def scan_font_families(file_path):
    violations = []
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    for line_num, line in enumerate(lines, 1):
        matches = FONT_FAMILY_REGEX.findall(line)
        for match in matches:
            # Split comma-separated font stacks (e.g. 'Bebas Neue', sans-serif)
            fonts = [f.strip(" '\"").lower() for f in match.split(",")]
            unapproved = [f for f in fonts if f not in APPROVED_FONTS]
            
            if unapproved:
                violations.append({
                    "file": str(file_path),
                    "line": line_num,
                    "found": match.strip(),
                    "unapproved": unapproved,
                    "content": line.strip()
                })
    return violations

def main():
    repo_root = Path(__file__).resolve().parent.parent
    target_files = list(repo_root.glob("*.html")) + list(repo_root.glob("assets/**/*.css"))

    total_violations = []
    for f in target_files:
        violations = scan_font_families(f)
        total_violations.extend(violations)

    if total_violations:
        print(f"❌ FAIL: Found {len(total_violations)} unapproved font family declaration(s):")
        for v in total_violations:
            print(f"  {v['file']}:{v['line']} -> Declared: '{v['found']}' | Disallowed: {v['unapproved']}")
            print(f"    Line: {v['content']}")
        sys.exit(1)
    else:
        print("✅ PASS: All font-family declarations comply with DESIGN-SYSTEM.md (Bebas Neue + Archivo).")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 5. Verification Strategy: Viewports (~1600px / ~390px) & Protocol (`file://` vs `http://`)

### 5.1 Dual-Protocol & Dual-Viewport Matrix

| Verification Aspect | Mode 1: Local HTTP Server | Mode 2: Direct Disk File (`file://`) |
| :--- | :--- | :--- |
| **URL Format** | `http://localhost:8000/index.html` | `file:///home/raghavan/projects/bowncer_sportz/index.html` |
| **Desktop (~1600px)** | Viewport `1600 x 900` | Viewport `1600 x 900` |
| **Mobile (~390px)** | Viewport `390 x 844` | Viewport `390 x 844` |
| **Console Checks** | Zero JS errors, 0 failed network requests | Zero CORS errors, zero script load failures |
| **Layout Checks** | Zero horizontal overflow (`scrollWidth <= clientWidth`) | Zero horizontal overflow (`scrollWidth <= clientWidth`) |
| **Interactive Targets**| Tap targets >= 44x44px on mobile | Tap targets >= 44x44px on mobile |

### 5.2 Automated Playwright Runner Architecture (`verify_responsive_and_protocol.js` / `.py`)

```javascript
/**
 * Playwright Verification Script for Responsive Layouts and Protocol Compatibility
 */
const { chromium } = require('playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const VIEWPORTS = {
  desktop: { width: 1600, height: 900 },
  mobile: { width: 390, height: 844 }
};

const PROTOCOLS = [
  { name: 'http', url: 'http://localhost:8000/index.html' },
  { name: 'file', url: `file://${path.resolve(__dirname, '../index.html')}` }
];

async function verifyPage() {
  const browser = await chromium.launch({ headless: true });
  let hasErrors = false;

  for (const proto of PROTOCOLS) {
    for (const [vpName, vpSize] of Object.entries(VIEWPORTS)) {
      const context = await browser.newContext({ viewport: vpSize });
      const page = await context.newPage();

      const consoleErrors = [];
      page.on('console', msg => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });
      page.on('pageerror', err => consoleErrors.push(err.message));

      console.log(`Testing ${proto.name} protocol at ${vpName} (${vpSize.width}x${vpSize.height})...`);
      await page.goto(proto.url, { waitUntil: 'networkidle' });

      // 1. Check for Console Errors
      if (consoleErrors.length > 0) {
        console.error(`❌ Console Errors [${proto.name} - ${vpName}]:`, consoleErrors);
        hasErrors = true;
      }

      // 2. Check for Horizontal Scroll / Overflow
      const overflow = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });
      if (overflow) {
        console.error(`❌ Horizontal Overflow detected [${proto.name} - ${vpName}]!`);
        hasErrors = true;
      }

      // 3. Check Touch Targets on Mobile
      if (vpName === 'mobile') {
        const smallTargets = await page.evaluate(() => {
          const elements = Array.from(document.querySelectorAll('a, button, input, select'));
          return elements.filter(el => {
            const rect = el.getBoundingClientRect();
            return (rect.width > 0 && rect.height > 0) && (rect.width < 44 || rect.height < 44);
          }).map(el => ({ tag: el.tagName, class: el.className, text: el.innerText.substring(0, 20) }));
        });
        if (smallTargets.length > 0) {
          console.warn(`⚠️ Warning: ${smallTargets.length} interactive target(s) smaller than 44x44px on mobile.`);
        }
      }

      // 4. Capture Screenshot
      const screenshotPath = path.resolve(__dirname, `screenshot_${proto.name}_${vpName}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`  📸 Saved screenshot: ${screenshotPath}`);

      await context.close();
    }
  }

  await browser.close();
  if (hasErrors) {
    process.exit(1);
  } else {
    console.log("✅ PASS: All protocol and responsive layout checks passed cleanly!");
    process.exit(0);
  }
}

verifyPage().catch(err => {
  console.error("Fatal test execution error:", err);
  process.exit(1);
});
```

---

## 6. Verification Method & Actionable Next Steps

### 6.1 Independent Verification Method
To verify this analysis and script specification:
1. Save `check_hex_colors.py` and `check_font_families.py` into a helper script directory or execute via Python.
2. Run `python3 check_hex_colors.py` against `index.html` to confirm it accurately flags lines 894, 899, 906, 930, 936, 944–946, 954, 959.
3. Run `python3 check_font_families.py` against `index.html` to confirm it accurately flags `font-family: monospace` on lines 907, 929, 937, 947, 950, 953, 961.
4. Execute Playwright / HTTP server verification to generate screenshots and validate `file://` compatibility.

### 6.2 Implementation Roadmap for Worker Agents
- **M2 (YouTube Showcase Implementation)**: When constructing `#youtube-showcase`, strictly use CSS variables (`var(--void)`, `var(--ember)`, `var(--ink)`) and allowed fonts (`Bebas Neue`, `Archivo`).
- **M3 (Automated Quality Script Commit)**: Save `check_hex_colors.py` and `check_font_families.py` as project compliance utilities.
- **M4 (QA & Audit)**: Run the automated inspection suite to achieve 100% compliance before declaring completion.
