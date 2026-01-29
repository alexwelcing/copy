import asyncio
import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.core.assets import get_asset_manager

async def run_recovery():
    print("🚀 INITIALIZING HIGH ERA: PROJECT 'RESTORATION'...")
    asset_manager = get_asset_manager()
    
    results = {
        "images": {}
    }

    # "Neo-Madison" Prompts: Warm, Tactile, Expensive
    skills_to_visualize = {
        "copywriting": "A minimalist mid-century modern typewriter on a walnut desk. Warm golden hour sunlight hitting the paper. Cinematic depth of field, photorealistic, elegant, high texture.",
        "page-cro": "A pristine architectural drafting table with blueprints and a magnifying glass. 1960s aesthetic, clean lines, warm lighting, obsession with detail. Photorealistic.",
        "marketing-ideas": "A classic Eames lounge chair in a thoughtful, sunlit library. Walls of books, atmosphere of deep strategy and wisdom. Cinematic, quiet luxury.",
        "remotion-script": "A vintage 16mm film editing station. Splicing tape, film reels, warm analog equipment. The craft of storytelling. Cinematic, photorealistic."
    }

    print("\n🎨 GENERATING 'NEO-MADISON' ASSETS...")
    for skill, prompt in skills_to_visualize.items():
        print(f"  > Generating visual for {skill}...")
        try:
            img_res = await asset_manager.generate_image(prompt)
            results["images"][skill] = img_res["url"]
            print(f"    -> Generated: {img_res['url']}")
        except Exception as e:
            print(f"    x Failed: {e}")

    # Save Results
    with open("restoration_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✨ RESTORATION DATA GENERATED.")

if __name__ == "__main__":
    asyncio.run(run_recovery())
