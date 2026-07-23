#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

REPO_ROOT = Path("/home/raghavan/projects/bowncer_sportz").resolve()
INDEX_HTML = REPO_ROOT / "index.html"
FILE_URL = f"file://{INDEX_HTML}"

VIEWPORTS = {
    "desktop": {"width": 1600, "height": 900},
    "mobile": {"width": 390, "height": 844}
}

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        has_errors = False
        
        for vp_name, vp_size in VIEWPORTS.items():
            print(f"\n--- Testing file:// protocol at {vp_name} ({vp_size['width']}x{vp_size['height']}) ---")
            context = await browser.new_context(viewport=vp_size)
            page = await context.new_page()

            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: console_errors.append(err.message))

            await page.goto(FILE_URL, wait_until="networkidle")

            # Check console errors
            if console_errors:
                print(f"❌ Console Errors [{vp_name}]: {console_errors}")
                has_errors = True
            else:
                print(f"✅ Zero console errors at {vp_name}.")

            # Check horizontal overflow
            scroll_width = await page.evaluate("document.documentElement.scrollWidth")
            client_width = await page.evaluate("document.documentElement.clientWidth")
            if scroll_width > client_width:
                print(f"❌ Horizontal overflow detected! scrollWidth ({scroll_width}) > clientWidth ({client_width})")
                has_errors = True
            else:
                print(f"✅ Zero horizontal overflow at {vp_name} (width: {client_width}px).")

            # Verify #media-showcase element presence & visibility
            showcase = page.locator("#media-showcase")
            is_visible = await showcase.is_visible()
            if not is_visible:
                print(f"❌ #media-showcase is not visible at {vp_name}!")
                has_errors = True
            else:
                print(f"✅ #media-showcase section is present and visible.")

            # Scroll into view to trigger reveal animation
            await showcase.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)

            # Test interaction: click Play button
            play_btn = page.locator("#stage-play-btn")
            await play_btn.click()
            await page.wait_for_timeout(300)

            # Under file:// protocol, play click triggers offline/file fallback notice card
            offline_card = page.locator(".video-offline-card")
            offline_visible = await offline_card.is_visible()
            if offline_visible:
                print(f"✅ Click-to-play correctly rendered Offline / file:// protocol fallback notice card!")
            else:
                print(f"❌ Offline fallback notice card was not displayed on play click under file://")
                has_errors = True

            # Reset back to poster
            reset_btn = page.locator("#reset-facade-btn")
            await reset_btn.click()
            await page.wait_for_timeout(300)

            # Test thumbnail card switching
            cards = page.locator("#media-showcase .video-card")
            card_count = await cards.count()
            print(f"  Found {card_count} video thumbnail cards in playlist reel.")
            if card_count >= 2:
                # Click second card
                await cards.nth(1).click()
                await page.wait_for_timeout(300)
                stage_title_text = await page.locator("#stage-title").inner_text()
                print(f"  Selected Card 2 -> Stage Title updated to: '{stage_title_text}'")

            # Check touch targets on mobile
            if vp_name == "mobile":
                play_box = await play_btn.bounding_box()
                if play_box and (play_box["width"] < 44 or play_box["height"] < 44):
                    print(f"⚠️ Play button target size ({play_box['width']}x{play_box['height']}) is under 44x44px")
                else:
                    print(f"✅ Mobile play button touch target is compliant ({play_box['width']}x{play_box['height']}px >= 44x44px).")

            # Take screenshot artifact
            screenshot_path = f"/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1/screenshot_{vp_name}.png"
            await page.screenshot(path=screenshot_path, full_page=False)
            print(f"  📸 Saved viewport screenshot: {screenshot_path}")

            await context.close()

        await browser.close()
        
        if has_errors:
            print("\n❌ Verification FAILED!")
            sys.exit(1)
        else:
            print("\n✅ Verification PASSED CLEANLY across desktop, mobile, file:// protocol, and play interactions!")
            sys.exit(0)

if __name__ == "__main__":
    asyncio.run(run_verification())
