import asyncio
import os
import sys
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from service.core.assets import get_asset_manager
from dotenv import load_dotenv

load_dotenv()

async def generate_hero_audio():
    manager = get_asset_manager()
    print("Starting Hero Audio Generation...")
    
    prompt = "Futuristic ambient marketing soundscape, high-tech cinematic background, subtle kinetic energy, electronic pulses, electric indigo vibes, clean and professional."
    
    try:
        result = await manager.generate_audio(
            prompt=prompt, 
            model="fal-ai/stable-audio"
        )
        print(f"Audio Generated Successfully!")
        print(f"URL: {result['url']}")
        print(f"GCS Path: {result['gcs_path']}")
        return result
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(generate_hero_audio())
