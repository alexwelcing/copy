import asyncio
import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.core.executor import get_executor
from service.api.schemas import WorkRequest, SkillName
from service.core.assets import get_asset_manager

async def run_overhaul():
    print("🚀 INITIALIZING HIGH ERA: PROJECT 'BREAKOUT'...")
    executor = get_executor()
    asset_manager = get_asset_manager()
    
    results = {
        "theme": {},
        "copy": {},
        "images": {}
    }

    # 1. THEME & VIBE (Marketing Ideas)
    print("\n🧠 PHASE 1: IDEATION (Freaking Out)...")
    theme_req = WorkRequest(
        skill=SkillName.MARKETING_IDEAS,
        task="Develop a 'Break Out, Freak Out, Geek Out' visual identity for High Era. Move beyond safe Mid-Century Modern into 'Cyber-Noir Madison Avenue' or 'Analog Future'. Describe the color palette, typography mood, and image style.",
        context={"current_style": "Safe Mid-Century", "goal": "Radical differentiation"}
    )
    theme_res = executor.execute(theme_req)
    results["theme"] = theme_res.output
    print(">> Theme Concept Generated.")

    # 2. NEW COPY (Copywriting)
    print("\n✍️ PHASE 2: COPY REWRITE (Geeking Out)...")
    copy_req = WorkRequest(
        skill=SkillName.COPYWRITING,
        task="Rewrite the High Era Hero Headline and Subhead. It must be bold, slightly aggressive, and deeply intelligent. Use the 'Cyber-Noir Madison Avenue' vibe.",
        context={"old_headline": "Build Once. Brief Forever.", "audience": "Visionary CMOs"}
    )
    copy_res = executor.execute(copy_req)
    results["copy"] = copy_res.output
    print(">> New Copy Generated.")

    # 3. ASSET GENERATION (Breaking Out)
    print("\n🎨 PHASE 3: ASSET PRODUCTION (The Art Dept)...")
    
    skills_to_visualize = {
        "copywriting": "A cinematic, moody close-up of a typewriter where the keys are glowing fiber-optic cables. Cyber-noir aesthetic, smoke, neon orange and deep navy lighting. 8k resolution, photorealistic.",
        "page-cro": "A futuristic laboratory clean room where a landing page is being dissected by laser scanners. Blueprint overlays, holographic UI elements, teal and magenta lighting. High tech, precision.",
        "marketing-ideas": "A chaotic but beautiful storm of golden geometric shapes forming a lightbulb filament in a dark void. Abstract, conceptual, 3d render, octane render.",
        "remotion-script": "A film editing suite console from the year 2099. Multiple screens showing timeline sequences, analog dials mixed with holographic displays. Cinematic lighting."
    }

    for skill, prompt in skills_to_visualize.items():
        print(f"  > Generating visual for {skill}...")
        try:
            # We use the sync wrapper or ensure async works in this context
            # assets.py has async generate_image
            img_res = await asset_manager.generate_image(prompt)
            results["images"][skill] = img_res["url"]
            print(f"    -> Generated: {img_res['url']}")
        except Exception as e:
            print(f"    x Failed: {e}")

    # Save Results
    with open("overhaul_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✨ OVERHAUL DATA GENERATED. CHECK overhaul_results.json")

if __name__ == "__main__":
    asyncio.run(run_overhaul())
