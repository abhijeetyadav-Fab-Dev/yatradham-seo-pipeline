import asyncio
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright

async def run():
    print("[Browser] Starting Antigravity Browser Control Session...")
    async with async_playwright() as p:
        # Launch browser (visible window)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        target_url = "https://yatradham-seo-pipeline.onrender.com/"
        print(f"[Browser] Navigating to: {target_url}")
        await page.goto(target_url, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # 1. Take initial screenshot of Dashboard
        os.makedirs("browser_captures", exist_ok=True)
        await page.screenshot(path="browser_captures/01_dashboard.png")
        print("[Browser] Captured 01_dashboard.png")

        # 2. Click on 'AI Content Studio' tab
        print("[Browser] Navigating to AI Content Studio tab...")
        await page.click("button:has-text('AI Content Studio')")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="browser_captures/02_content_studio.png")
        print("[Browser] Captured 02_content_studio.png")

        # 3. Enter a prompt into the Quick Prompt textarea
        print("[Browser] Typing test prompt into Content Studio...")
        prompt_input = page.locator("#quickPrompt")
        if await prompt_input.is_visible():
            await prompt_input.fill("Complete Spiritual Guide for Kedarnath Darshan and Dharamshala booking")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="browser_captures/03_prompt_filled.png")
            print("[Browser] Captured 03_prompt_filled.png")

            # 4. Click 'Generate Content'
            print("[Browser] Clicking 'Generate Content' button...")
            generate_btn = page.locator("#btnQuickGenerate")
            if await generate_btn.is_visible():
                await generate_btn.click()
                print("[Browser] Waiting for generation response...")
                await page.wait_for_timeout(5000)
                await page.screenshot(path="browser_captures/04_generation_state.png")
                print("[Browser] Captured 04_generation_state.png")

        # 5. Switch to 'SEO Outputs Review' tab
        print("[Browser] Checking SEO Outputs Review tab...")
        await page.click("button:has-text('SEO Outputs Review')")
        await page.wait_for_timeout(1500)
        await page.screenshot(path="browser_captures/05_outputs_review.png")
        print("[Browser] Captured 05_outputs_review.png")

        print("[Browser] Browser session test completed successfully!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
