import asyncio
import os
import sys
import time
from service.core.executor import get_executor
from service.api.schemas import SkillName, WorkRequest
from service.core.assets import get_asset_manager
from dotenv import load_dotenv

# Ensure logs are flushed immediately
def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

async def run_dogfood():
    load_dotenv()
    if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
        os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]

    log("--- STARTING HIGH ERA DOGFOOD PROCESS ---")
    
    executor = get_executor()
    asset_manager = get_asset_manager()
    
    # STEP 1: SKILL EXECUTION
    log("Step 1: Calling MiniMax for the 'High Era' Visual Brief...")
    design_task = """
    Create a precise visual direction for our landing page. 
    Focus: 'The High Era'. Madison Avenue realism. 
    We need specific prompts for:
    1. A hero image (Flux 2 Pro)
    2. A cinematic video (LTX2)
    Requirement: 1960s sophistication, Kodak film aesthetic, NO neon.
    """
    
    request = WorkRequest(
        skill=SkillName.MARKETING_IDEAS,
        model="MiniMax-M2.1",
        task=design_task,
        context={"product": "Marketing Agency", "persona": "The High Era"}
    )
    
    try:
        # This is a synchronous call in our current executor
        log("Sending request to MiniMax (this may take 30-60s)...")
        result = await asyncio.to_thread(executor.execute, request)
        log("Success: Visual Brief generated.")
        
        with open("agency/rigs/copy-agency-launch/outputs/visual-design-brief-high-era.md", "w") as f:
            f.write(result.output)
        log("Brief saved to agency/rigs/copy-agency-launch/outputs/visual-design-brief-high-era.md")
        
    except Exception as e:
        log(f"FAILED Step 1: {str(e)}")
        return

    # STEP 2: IMAGE GENERATION
    log("Step 2: Generating SOTA Image (Flux 2 Pro)...")
    # Prompt derived from the 'High Era' pivot
    image_prompt = "Cinematic 35mm film shot of a mid-century modern advertising executive office, sunlight streaming through large windows, a heavy oak desk with a vintage typewriter and a leather-bound portfolio, Kodak Portra 400 aesthetic, realistic textures, highly detailed, 1960s Madison Avenue."
    
    try:
        log(f"Calling FAL with prompt: {image_prompt[:50]}...")
        image_asset = await asset_manager.generate_image(image_prompt, model="fal-ai/flux-2-pro")
        log(f"Success: Image generated. URL: {image_asset['url']}")
    except Exception as e:
        log(f"FAILED Step 2: {str(e)}")
        # Continue to video even if image fails

    # STEP 3: VIDEO GENERATION
    log("Step 3: Generating Cinematic Video (LTX2 Distilled)...")
    video_prompt = "A slow, cinematic pan across a series of hand-drawn advertising storyboards pinned to a cork wall, subtle film grain, soft natural lighting, realistic textures, 24fps, high fidelity, 1960s agency vibe."
    
    try:
        log(f"Calling FAL (LTX2) with prompt: {video_prompt[:50]}...")
        video_asset = await asset_manager.generate_video(video_prompt, model="fal-ai/ltx-2-19b/distilled/text-to-video")
        log(f"Success: Video generated. URL: {video_asset['url']}")
    except Exception as e:
        log(f"FAILED Step 3: {str(e)}")

    log("--- DOGFOOD PROCESS COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_dogfood())
