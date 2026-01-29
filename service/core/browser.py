
import asyncio
from playwright.async_api import async_playwright
import base64

async def capture_screenshot(url: str) -> str:
    """
    Captures a screenshot of the given URL.
    Returns the base64 encoded image string.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set viewport for a desktop-like view
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=15000)
        except Exception:
            # Fallback if networkidle takes too long
            pass
            
        screenshot_bytes = await page.screenshot(type="jpeg", quality=80)
        await browser.close()
        
        return base64.b64encode(screenshot_bytes).decode("utf-8")
