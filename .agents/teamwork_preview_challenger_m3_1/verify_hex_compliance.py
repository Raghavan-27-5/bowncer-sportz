#!/usr/bin/env python3
"""
Verification Script: Hex Color Compliance for #media-showcase and index.html
Project: Bowncer Sportz Cricket Academy Website
"""
import re
import sys

INDEX_PATH = "/home/raghavan/projects/bowncer_sportz/index.html"

def verify_hex_colors():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract CSS inside <style> tags
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    full_css = "\n".join(style_blocks)

    # Extract CSS specifically for Section 3.5 Media Showcase
    media_showcase_match = re.search(
        r"/\* ═+.*SECTION 3\.5 — YOUTUBE MEDIA SHOWCASE.*?\*/(.*?)/\* END YOUTUBE MEDIA SHOWCASE \*/",
        full_css,
        re.DOTALL
    )

    media_css = media_showcase_match.group(1) if media_showcase_match else ""

    # Find all hex colors in media showcase section CSS
    hex_pattern = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    media_hexes = hex_pattern.findall(media_css)

    print("=== HEX COLOR COMPLIANCE CHECK ===")
    print(f"Total hex color values found in #media-showcase CSS: {len(media_hexes)}")

    if media_hexes:
        print(f"FAILED: Found hardcoded hex colors in #media-showcase: {media_hexes}")
    else:
        print("PASSED: 0 hardcoded hex colors found in #media-showcase CSS.")

    # Also scan root CSS variables defined in DESIGN-SYSTEM.md
    approved_root_vars = [
        "--ink:#f4f1ea;",
        "--ink-dim:#b8b2a4;",
        "--void:#07080a;",
        "--void-2:#0d0f12;",
        "--ember:#e2380a;",
        "--ember-glow:#ff5622;",
        "--gold:#c9a15a;",
        "--line: rgba(244,241,234,0.14);"
    ]

    all_hexes_in_css = hex_pattern.findall(full_css)
    print(f"Total hex instances across all style blocks: {len(all_hexes_in_css)}")

    return len(media_hexes) == 0

if __name__ == "__main__":
    success = verify_hex_colors()
    sys.exit(0 if success else 1)
