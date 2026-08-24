import asyncio
import json
from playwright.async_api import async_playwright

async def run_live_qa():
    print("Starting Live QA on Render deployment...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Go to the live URL
            await page.goto("https://yatradham-seo-pipeline.onrender.com/")
            await page.wait_for_load_state("networkidle")
            print("Successfully loaded Yatradham SEO Pipeline")
            
            # Switch to "AI Content Studio" tab
            print("Switching to AI Content Studio...")
            await page.click("button:has-text('AI Content Studio')")
            
            # Switch to "Structured Form" sub-tab inside the Studio
            print("Switching to Structured Form mode...")
            # Let's find the button. In the UI it's "📝 Structured Form"
            await page.click("button:has-text('Structured Form')")
            
            # Fill the fields
            print("Filling in test data...")
            await page.select_option("#structContentType", value="blog_post")
            await page.fill("#structTopic", "Top 10 Peaceful Ashrams in Haridwar")
            await page.fill("#structKeyword", "ashrams in haridwar")
            await page.select_option("#structTone", value="informational")
            await page.fill("#structWordCount", "500")
            
            # Click Generate
            print("Clicking Generate and waiting for AI response (this takes a moment)...")
            await page.click("#btnStructGenerate")
            
            # Wait for the preview container to populate with markdown content
            # The preview container id is `studioPreview`
            await page.wait_for_selector("#studioPreview .prose", timeout=60000)
            print("AI Generation complete!")
            
            # Extract generated content
            content_html = await page.inner_html("#studioPreview")
            content_text = await page.inner_text("#studioPreview")
            
            print("\n==================================")
            print("         QA TEST RESULTS")
            print("==================================")
            if "# TITLE" in content_text or "TITLE" in content_text or len(content_text) > 100:
                print("✅ Test Passed: The structured form successfully returned formatted content!")
                print("\nContent Snippet:")
                print(content_text[:500] + "...\n")
            else:
                print("❌ Test Failed: Content missing or malformed.")
                print(content_text)
                
        except Exception as e:
            print("❌ Test Encountered an Error:")
            print(str(e))
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_live_qa())
