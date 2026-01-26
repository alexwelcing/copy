import asyncio
import json
import base64
from playwright.async_api import async_playwright
import sys
import os
import random

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.core.executor import get_executor

# Config
BASE_URL = "https://marketing-agency-frontend-bexuyahqvq-uc.a.run.app"
CAMPAIGNS_FILE = "frontend/src/lib/data/campaigns.json"
OUTPUT_DIR = "scripts/qa_artifacts"

async def capture_html(slug: str) -> str:
    import httpx
    url = f"{BASE_URL}/"
    print(f"Fetching HTML from {url}...")
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        return res.text

async def analyze_with_vision(html_content: str, slug: str):
    executor = get_executor()
    
    # We are now doing Code Analysis since we can't screenshot
    print(f"Analyzing {slug} HTML for High Era compliance...")
    
    client = executor.anthropic_client
    
    prompt = f"""
    You are the Creative Director of 'Agency AI'.
    Our brand aesthetic is 'High Era': Mid-Century Modern, Tactile, Serious.
    
    Review this raw HTML/CSS structure of our homepage.
    
    HTML CONTENT:
    ```html
    {html_content[:15000]} 
    ```
    (Truncated if too long)
    
    CRITERIA:
    1. Do the CSS classes (e.g. 'paper-card', 'brief-panel', 'typewriter') reflect the aesthetic?
    2. Is the hierarchy logical?
    3. Are there any obvious structural issues?
    
    Output a JSON summary ONLY:
    {{
        "score": (1-10),
        "aesthetic_match": boolean,
        "critique": "One sentence critique.",
        "improvements": ["Fix 1", "Fix 2"]
    }}
    """
    
    # Using text model for code analysis
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    
    return message.content[0].text

async def run():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Starting Code QA on Homepage...")
    
    try:
        html = await capture_html("")
        analysis_text = await analyze_with_vision(html, "HOMEPAGE")
        print(f"\n--- REPORT FOR HOMEPAGE ---")
        print(analysis_text)
        print("--------------------------------\n")
        
        try:
            analysis_json = json.loads(analysis_text)
            report = [{"slug": "homepage", "analysis": analysis_json}]
        except:
            report = [{"slug": "homepage", "analysis": analysis_text}]
            
        with open(f"{OUTPUT_DIR}/report.json", "w") as f:
            json.dump(report, f, indent=2)
            
    except Exception as e:
        print(f"Failed to process homepage: {e}")

if __name__ == "__main__":
    asyncio.run(run())