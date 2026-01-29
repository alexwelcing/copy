
import asyncio
import os
import sys
import time

# Add root to path
sys.path.append(os.getcwd())

from service.core.browser import capture_screenshot
from service.core.executor import get_executor
from service.api.schemas import WorkRequest, SkillName

async def run_audit():
    print("Waiting for frontend to warm up...")
    await asyncio.sleep(15) # Give Vite time to build
    
    target_url = "http://localhost:5173"
    print(f"Capturing screenshot of {target_url}...")
    
    try:
        image_b64 = await capture_screenshot(target_url)
        print(f"Screenshot captured. Size: {len(image_b64)} chars")
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
        return

    print("Analyzing with PAGE_CRO skill...")
    
    executor = get_executor()
    
    req = WorkRequest(
        skill=SkillName.PAGE_CRO,
        task="Audit this landing page. Focus on the user journey, clarity of the value proposition, and the 'twin-engine' workflow visualization. Identify friction points in the onboarding path.",
        image_data=image_b64,
        context={
            "product": "Agency AI",
            "audience": "Marketing Agencies",
            "goal": "User Onboarding"
        }
    )
    
    try:
        result = executor.execute(req)
        print("\n=== AUDIT RESULTS ===\n")
        print(result.output)
        print("\n=====================\n")
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_audit())
