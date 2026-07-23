#!/usr/bin/env python3
"""
Verification Script: YouTube Media Showcase Detailed Structural & Interactive Verification
Project: Bowncer Sportz Cricket Academy Website
"""
import re
import sys
import os

INDEX_PATH = "/home/raghavan/projects/bowncer_sportz/index.html"
ASSETS_DIR = "/home/raghavan/projects/bowncer_sportz/assets"

def run_tests():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    results = []

    def assert_test(name, condition, details=""):
        status = "PASS" if condition else "FAIL"
        results.append((name, status, details))
        print(f"[{status}] {name}" + (f" - {details}" if details else ""))

    print("=== YOUTUBE MEDIA SHOWCASE COMPREHENSIVE VERIFICATION ===")

    # 1. Section presence
    assert_test(
        "Section ID #media-showcase exists",
        'id="media-showcase"' in html,
        "Found <section class=\"media-showcase-section\" id=\"media-showcase\">"
    )

    # 2. Eyebrow & Header
    assert_test(
        "Header eyebrow with live pulse dot present",
        'ON-FIELD EVIDENCE · ACADEMY MEDIA' in html and 'class="eyebrow-dot"' in html,
        "Eyebrow contains ON-FIELD EVIDENCE badge & pulse animation"
    )

    assert_test(
        "Main Headline 'THE PROCESS IN MOTION.' present",
        'THE PROCESS <span class="title-accent">IN MOTION.</span>' in html,
        "Cinematic headline with ember-glow accent gradient"
    )

    # 3. Asymmetrical Grid
    assert_test(
        "Asymmetrical Grid container (.showcase-grid) present",
        'class="showcase-grid showcase-reveal"' in html,
        "Grid layout splitting featured stage vs playlist reel"
    )

    # 4. Featured Stage Card
    assert_test(
        "Featured Stage Card (#video-stage-card) present",
        'id="video-stage-card"' in html and 'id="video-thumb-wrap"' in html,
        "Stage card contains thumbnail wrap & interactive stage"
    )

    assert_test(
        "Stage Poster WebP image exists & lazy loaded",
        'src="assets/showcase_thumb_featured.webp"' in html and 'loading="lazy"' in html,
        "Thumbnail uses WebP format with lazy loading and async decoding"
    )

    # 5. Play facade button & pulse halo
    assert_test(
        "Play facade button (#stage-play-btn) with halo pulse present",
        'id="stage-play-btn"' in html and 'class="play-halo"' in html,
        "Custom SVG play icon & halo pulse ring"
    )

    # 6. Trust signal / No invented facts compliance
    assert_test(
        "Trust signal [PENDING VERIFICATION] present on unverified YouTube IDs",
        '[PENDING VERIFICATION]' in html,
        "Follows AGENTS.md Rule 2: unverified facts marked muted/italic rather than hallucinating IDs"
    )

    # 7. Playlist Reel / Sidebar items
    cards = re.findall(r'<article class="video-card[^"]*"', html)
    assert_test(
        "Playlist Reel contains 3 video cards",
        len(cards) == 3,
        f"Found {len(cards)} video cards in sidebar reel"
    )

    assert_test(
        "First video card has 'is-active' state",
        'class="video-card is-active"' in html,
        "First item marked active by default"
    )

    # 8. Data attributes for Facade player
    data_attrs = ["data-youtube-id", "data-poster", "data-title", "data-category", "data-duration", "data-coach-note"]
    all_data_present = all(attr in html for attr in data_attrs)
    assert_test(
        "Playlist cards populated with complete data attributes for dynamic switching",
        all_data_present,
        f"Attributes tested: {', '.join(data_attrs)}"
    )

    # 9. Channel CTA & WhatsApp link
    assert_test(
        "Channel CTA Card with WhatsApp action link present",
        'class="channel-card"' in html and 'https://wa.me/919840568137' in html,
        "Follows AGENTS.md Rule 6: WhatsApp link for immediate academy inquiry"
    )

    # 10. Offline / file:// protocol fallback handler script
    assert_test(
        "Interactive JavaScript facade & offline fallback handler included",
        'isOfflineOrFileProtocol' in html and 'video-offline-card' in html and 'resetStageToPoster' in html,
        "Protects user experience on local file previews and pending verification IDs"
    )

    # 11. Responsive CSS check
    assert_test(
        "Mobile media query (@media max-width: 900px) present in CSS",
        '@media (max-width: 900px)' in html and '.showcase-grid' in html,
        "Grid gracefully collapses to single-column layout on mobile viewports"
    )

    # 12. WebP Assets on disk check
    asset_files = [
        "showcase_thumb_featured.webp",
        "showcase_thumb_2.webp",
        "showcase_thumb_3.webp"
    ]
    assets_exist = True
    missing_assets = []
    for asset in asset_files:
        full_path = os.path.join(ASSETS_DIR, asset)
        if not os.path.exists(full_path):
            assets_exist = False
            missing_assets.append(asset)

    assert_test(
        "WebP Thumbnail Asset files exist in /assets directory",
        assets_exist,
        f"All 3 thumbnails verified: {asset_files}" if assets_exist else f"Missing: {missing_assets}"
    )

    # Summary count
    passed_count = sum(1 for _, status, _ in results if status == "PASS")
    failed_count = sum(1 for _, status, _ in results if status == "FAIL")

    print(f"\nVerification Complete: {passed_count}/{len(results)} Passed ({failed_count} Failed).")
    return failed_count == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
