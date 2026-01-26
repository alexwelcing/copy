import asyncio
import os
import sys
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from service.core.assets import get_asset_manager
from dotenv import load_dotenv

load_dotenv()

async def generate_hero():
    manager = get_asset_manager()
    print("Starting Hero Image Generation...")
    
    prompt = "Cinematic abstract visualization of kinetic intelligence, glowing electric indigo and cyber mint data streams weaving into video frames, deep space background, glassmorphism textures, 8k resolution, highly detailed, futuristic marketing technology vibe."
    
    try:
        # Using Flux Pro for maximum quality
        result = await manager.generate_image(
            prompt=prompt, 
            model="fal-ai/flux-pro/v1.1"
        )
        print(f"Hero Image Generated Successfully!")
        print(f"URL: {result['url']}")
        print(f"GCS Path: {result['gcs_path']}")
        return result
    except Exception as e:
        print(f"Error generating hero: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(generate_hero())
