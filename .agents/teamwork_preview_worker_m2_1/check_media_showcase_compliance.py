#!/usr/bin/env python3
import sys
import re
from pathlib import Path

APPROVED_HEX = {
    "#f4f1ea", # --ink
    "#b8b2a4", # --ink-dim
    "#07080a", # --void
    "#0d0f12", # --void-2
    "#e2380a", # --ember
    "#ff5622", # --ember-glow
    "#c9a15a", # --gold
}

HEX_REGEX = re.compile(r'#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b')
FONT_FAMILY_REGEX = re.compile(r'font-family\s*:\s*([^;}"\']+);?', re.IGNORECASE)
APPROVED_FONTS = {"bebas neue", "archivo", "sans-serif", "inherit"}

def normalize_hex(h_str):
    h = h_str.lower()
    if len(h) == 4:
        return f"#{h[1]*2}{h[2]*2}{h[3]*2}"
    elif len(h) == 9:
        return h[:7]
    return h

def audit_index_html(html_path):
    content = Path(html_path).read_text(encoding="utf-8")
    
    # Extract CSS inside <style> blocks
    style_blocks = re.findall(r'<style\b[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    
    # Find media showcase CSS rules specifically
    media_showcase_css = ""
    for block in style_blocks:
        lines = block.splitlines()
        in_showcase = False
        for line in lines:
            if "YOUTUBE MEDIA SHOWCASE" in line or ".media-showcase" in line or "#media-showcase" in line:
                in_showcase = True
            if in_showcase:
                media_showcase_css += line + "\n"
                if "/* END YOUTUBE MEDIA SHOWCASE" in line:
                    in_showcase = False

    hex_violations = []
    font_violations = []

    # Lint media showcase CSS for Hex violations
    for line_idx, line in enumerate(media_showcase_css.splitlines(), 1):
        if "--ink:" in line or "--ink-dim:" in line or "--void:" in line or \
           "--void-2:" in line or "--ember:" in line or "--ember-glow:" in line or \
           "--gold:" in line or "--line:" in line:
            continue
        matches = HEX_REGEX.findall(line)
        for m in matches:
            norm = normalize_hex(m)
            if norm not in APPROVED_HEX:
                hex_violations.append((line_idx, m, norm, line.strip()))

        font_matches = FONT_FAMILY_REGEX.findall(line)
        for f_match in font_matches:
            fonts = [f.strip(" '\"\t").lower() for f in f_match.split(",") if f.strip(" '\"\t")]
            disallowed = [f for f in fonts if f not in APPROVED_FONTS]
            if disallowed:
                font_violations.append((line_idx, f_match, disallowed, line.strip()))

    print("--- Media Showcase Audit Report ---")
    if hex_violations:
        print(f"❌ Found {len(hex_violations)} unapproved hex color(s) in Media Showcase CSS:")
        for idx, orig, norm, line_text in hex_violations:
            print(f"  Line {idx}: {orig} ({norm}) -> {line_text}")
    else:
        print("✅ PASS: 0 unapproved hex colors in Media Showcase CSS.")

    if font_violations:
        print(f"❌ Found {len(font_violations)} unapproved font family declaration(s) in Media Showcase CSS:")
        for idx, decl, dis, line_text in font_violations:
            print(f"  Line {idx}: '{decl}' (disallowed: {dis}) -> {line_text}")
    else:
        print("✅ PASS: All font-family declarations strictly comply with Bebas Neue / Archivo.")

    return len(hex_violations) == 0 and len(font_violations) == 0

if __name__ == "__main__":
    html_file = "/home/raghavan/projects/bowncer_sportz/index.html"
    success = audit_index_html(html_file)
    sys.exit(0 if success else 1)
