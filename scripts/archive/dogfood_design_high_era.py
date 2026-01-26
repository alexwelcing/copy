import asyncio
import os
import json
from service.core.executor import get_executor
from service.api.schemas import SkillName, WorkRequest
from service.core.assets import get_asset_manager
from dotenv import load_dotenv

load_dotenv()

async def dogfood_high_era_design():
    executor = get_executor()
    asset_manager = get_asset_manager()
    
    print("--- Phase 1: Dogfooding 'marketing-ideas' for High Era Visual Design ---")
    
    design_task = """
    Design a sophisticated visual brief for our AI Marketing Agency: 'The High Era'.
    We need:
    1. A prompt for a hero image: Think Mad Men, 1960s Madison Avenue office, cinematic realism, tactile textures.
    2. A prompt for a background video: Subtle cinematic motion, film grain, a slow pan across a high-end advertising storyboard or a glass of scotch on a mahogany desk.
    3. A soundscape prompt: Jazz-inflected ambient, the sound of a typewriter, distant city traffic, sophisticated and low-key.
    
    NO NEON. NO FUTURISM. Focus on humanity and craft.
    """
    
    request = WorkRequest(
        skill=SkillName.MARKETING_IDEAS,
        task=design_task,
        context={
            "product": "Marketing Agency Platform",
            "persona": "The High Era",
            "target": "Elite Marketers & Founders"
        }
    )
    
    design_result = executor.execute(request)
    print("High Era Visual Design Brief Generated!")
    
    with open("agency/rigs/copy-agency-launch/outputs/visual-design-brief-high-era.md", "w") as f:
        f.write(design_result.output)

    print("\n--- Phase 2: Generating High Era Assets ---")
    
    # Sophisticated prompts derived from the High Era pivot
    image_prompt = "Cinematic 35mm film shot of a mid-century modern advertising executive office, sunlight streaming through large windows, a heavy oak desk with a vintage typewriter and a leather-bound portfolio, Kodak Portra 400 aesthetic, realistic textures, highly detailed, 1960s Madison Avenue."
    video_prompt = "A slow, cinematic pan across a series of hand-drawn advertising storyboards pinned to a cork wall, subtle film grain, soft natural lighting, realistic textures, 24fps, high fidelity."

    print("Generating Image (Flux 2 Pro)...")
    image_asset = await asset_manager.generate_image(image_prompt, model="fal-ai/flux-2-pro")
    print(f"Image: {image_asset['url']}")

    print("Generating Video (LTX2 Distilled)...")
    video_asset = await asset_manager.generate_video(video_prompt, model="fal-ai/ltx-2-19b/distilled/text-to-video")
    print(f"Video: {video_asset['url']}")

    return {
        "image": image_asset,
        "video": video_asset,
        "brief": design_result.output
    }

if __name__ == "__main__":
    if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]
        
    asyncio.run(dogfood_high_era_design())
