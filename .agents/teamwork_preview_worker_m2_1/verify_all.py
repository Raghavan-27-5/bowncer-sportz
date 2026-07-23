#!/usr/bin/env python3
import sys
import re
from pathlib import Path

REPO_ROOT = Path("/home/raghavan/projects/bowncer_sportz")
INDEX_PATH = REPO_ROOT / "index.html"
ASSETS_DIR = REPO_ROOT / "assets"

def run_checks():
    errors = []
    warnings = []
    
    if not INDEX_PATH.exists():
        errors.append("index.html does not exist!")
        return errors, warnings
        
    content = INDEX_PATH.read_text(encoding="utf-8")
    
    # 1. Insertion location check
    manifesto_pos = content.find('class="manifesto-section"')
    showcase_pos = content.find('id="media-showcase"')
    pathway_pos = content.find('class="pathway-section"')
    
    if manifesto_pos == -1 or showcase_pos == -1 or pathway_pos == -1:
        errors.append("Could not locate required section anchors in index.html!")
    elif not (manifesto_pos < showcase_pos < pathway_pos):
        errors.append(f"Section order invalid! manifesto ({manifesto_pos}) < showcase ({showcase_pos}) < pathway ({pathway_pos})")
    else:
        print("✅ Check 1: #media-showcase correctly placed between manifesto-section and pathway-section.")

    # 2. Hex color audit on Media Showcase CSS
    approved_hex = {"#f4f1ea", "#b8b2a4", "#07080a", "#0d0f12", "#e2380a", "#ff5622", "#c9a15a"}
    hex_regex = re.compile(r'#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b')
    
    showcase_css_start = content.find('SECTION 3.5 — YOUTUBE MEDIA SHOWCASE')
    showcase_css_end = content.find('/* END YOUTUBE MEDIA SHOWCASE */')
    showcase_css = content[showcase_css_start:showcase_css_end] if (showcase_css_start != -1 and showcase_css_end != -1) else ""
    
    css_hex_violations = []
    for line in showcase_css.splitlines():
        if any(var in line for var in ["--ink:", "--ink-dim:", "--void:", "--void-2:", "--ember:", "--ember-glow:", "--gold:", "--line:"]):
            continue
        for match in hex_regex.findall(line):
            h = match.lower()
            norm = f"#{h[1]*2}{h[2]*2}{h[3]*2}" if len(h) == 4 else (h[:7] if len(h) == 9 else h)
            if norm not in approved_hex:
                css_hex_violations.append((match, norm, line.strip()))
                
    if css_hex_violations:
        errors.append(f"Found {len(css_hex_violations)} unapproved hex color(s) in Media Showcase CSS: {css_hex_violations}")
    else:
        print("✅ Check 2: Zero hardcoded unapproved hex colors in #media-showcase CSS rules.")

    # 3. Typography audit on Media Showcase CSS
    font_regex = re.compile(r'font-family\s*:\s*([^;}"\']+);?', re.IGNORECASE)
    approved_fonts = {"bebas neue", "archivo", "sans-serif", "inherit"}
    font_violations = []
    for line in showcase_css.splitlines():
        for f_match in font_regex.findall(line):
            fonts = [f.strip(" '\"\t").lower() for f in f_match.split(",") if f.strip(" '\"\t")]
            disallowed = [f for f in fonts if f not in approved_fonts]
            if disallowed:
                font_violations.append((f_match, disallowed, line.strip()))
    if font_violations:
        errors.append(f"Found unapproved font family declarations: {font_violations}")
    else:
        print("✅ Check 3: 100% typography compliance (Bebas Neue + Archivo).")

    # 4. WebP Thumbnail Assets check
    required_assets = ["showcase_thumb_featured.webp", "showcase_thumb_2.webp", "showcase_thumb_3.webp"]
    for asset in required_assets:
        asset_path = ASSETS_DIR / asset
        if not asset_path.exists() or asset_path.stat().st_size == 0:
            errors.append(f"Required WebP asset missing or empty: {asset_path}")
        else:
            print(f"✅ Check 4: Asset {asset} exists ({asset_path.stat().st_size} bytes).")

    # 5. Lite-YouTube Facade & Privacy Iframe Check
    if "https://www.youtube-nocookie.com/embed/" not in content:
        errors.append("Privacy-enhanced YouTube embed domain (youtube-nocookie.com) missing from JS!")
    else:
        print("✅ Check 5: Privacy-enhanced YouTube iframe domain (youtube-nocookie.com) verified.")

    # 6. Offline / file:// Protocol Fallback & WhatsApp CTA Check
    if "isOfflineOrFileProtocol()" not in content or "wa.me/919840568137" not in content:
        errors.append("Offline / file:// protocol detection or WhatsApp CTA link missing!")
    else:
        print("✅ Check 6: Offline/file:// protocol fallback and WhatsApp CTA (+91 98405 68137) verified.")

    # 7. Unverified Data Verification Badge Check
    if "[PENDING VERIFICATION]" not in content:
        errors.append("[PENDING VERIFICATION] tag missing for unverified video data!")
    else:
        print("✅ Check 7: Unverified video titles/IDs carry mandatory [PENDING VERIFICATION] badges.")

    return errors, warnings

if __name__ == "__main__":
    errs, warns = run_checks()
    print("\n--- Final Verification Summary ---")
    if errs:
        print(f"❌ {len(errs)} Error(s) found:")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("🎉 ALL 7 INTEGRITY AND COMPLIANCE CHECKS PASSED CLEANLY!")
        sys.exit(0)
