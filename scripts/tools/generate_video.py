import asyncio
import os
import sys
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from service.core.assets import get_asset_manager
from dotenv import load_dotenv

load_dotenv()

async def generate_skill_video():
    manager = get_asset_manager()
    print("Starting Skill Video Generation...")
    
    prompt = "A futuristic 3D camera fly-through of a neon-lit digital city where the buildings are made of scrolling code, morphing into a floating glass dashboard showing video analytics, electric indigo lighting, high frame rate."
    
    try:
        # Using Luma for faster prototype generation
        result = await manager.generate_video(
            prompt=prompt, 
            model="fal-ai/luma-dream-machine"
        )
        print(f"Video Generated Successfully!")
        print(f"URL: {result['url']}")
        print(f"GCS Path: {result['gcs_path']}")
        return result
    except Exception as e:
        print(f"Error generating video: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(generate_skill_video())
