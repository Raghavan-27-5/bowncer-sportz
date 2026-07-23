#!/usr/bin/env python3
"""
Verification Script: Font Family Compliance for index.html
Project: Bowncer Sportz Cricket Academy Website
"""
import re
import sys

INDEX_PATH = "/home/raghavan/projects/bowncer_sportz/index.html"

def verify_font_families():
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

    # Check font-family rules in media showcase
    media_font_matches = re.findall(r"font-family:\s*([^;]+);", media_css)
    
    print("=== FONT FAMILY COMPLIANCE CHECK ===")
    print("Media Showcase font-family declarations:")
    media_fonts_valid = True
    for idx, font in enumerate(media_font_matches, 1):
        font_clean = font.strip()
        is_approved = ("'Bebas Neue'" in font_clean or "Bebas Neue" in font_clean or
                        "'Archivo'" in font_clean or "Archivo" in font_clean)
        status = "OK" if is_approved else "UNAPPROVED"
        if not is_approved:
            media_fonts_valid = False
        print(f"  [{status}] Decl #{idx}: {font_clean}")

    # Check all font-family declarations across index.html
    all_font_matches = re.findall(r"font-family:\s*([^;]+);", full_css)
    print(f"\nTotal font-family declarations in index.html: {len(all_font_matches)}")
    
    unapproved_fonts = []
    for font in all_font_matches:
        font_clean = font.strip()
        if not any(approved in font_clean for approved in ["Bebas Neue", "Archivo", "sans-serif", "monospace"]):
            unapproved_fonts.append(font_clean)

    if unapproved_fonts:
        print(f"FAILED: Found unapproved font families: {unapproved_fonts}")
    else:
        print("PASSED: All font families adhere to approved typography standards ('Bebas Neue', 'Archivo', sans-serif fallback, and monospace for technical mockups).")

    return media_fonts_valid and len(unapproved_fonts) == 0

if __name__ == "__main__":
    success = verify_font_families()
    sys.exit(0 if success else 1)
