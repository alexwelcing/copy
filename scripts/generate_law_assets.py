#!/usr/bin/env python3
"""
Generate visual assets for Law.com case study.
This script uses FAL.ai turbo models to generate high-quality images for the case study showcase.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Check for FAL key
FAL_KEY = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")
if not FAL_KEY:
    print("⚠️  FAL_KEY environment variable not set.")
    print("   Using placeholder assets. Set FAL_KEY to generate real assets.")
    USE_PLACEHOLDERS = True
else:
    USE_PLACEHOLDERS = False
    import fal_client
    import httpx

# Image generation prompts for Law.com case study
LAW_COM_PROMPTS = [
    {
        "scene": 1,
        "name": "law_scene_01_typing",
        "prompt": """
            Professional hands typing on modern laptop keyboard in dark office environment,
            subtle blue ambient lighting from screen, close-up cinematic shot,
            legal professional working late, high-end tech aesthetic,
            photorealistic, shallow depth of field, moody lighting,
            modern minimalist office, premium product photography style
        """,
        "image_size": "portrait_16_9"
    },
    {
        "scene": 2,
        "name": "law_scene_02_split_screen",
        "prompt": """
            Split screen composition showing contrast: left side shows stressed attorney
            at messy desk with paper documents piled high, fluorescent lighting, tired expression,
            right side shows calm professional using laptop with clean modern interface,
            natural lighting, confident and relaxed, dramatic before/after comparison,
            photorealistic, professional photography, high contrast lighting
        """,
        "image_size": "landscape_16_9"
    },
    {
        "scene": 3,
        "name": "law_scene_03_interface",
        "prompt": """
            Elegant AI legal research interface on modern display, neural network visualization
            showing case precedents mapping in real-time, clean data visualization with
            glowing blue nodes and connections, dark navy background (#1a1f36),
            electric blue accents (#0066ff), crisp typography showing legal metrics,
            high-end enterprise software aesthetic, futuristic but professional,
            cinematic UI design, photorealistic screen render
        """,
        "image_size": "landscape_16_9"
    },
    {
        "scene": 4,
        "name": "law_scene_04_general_counsel",
        "prompt": """
            Confident female General Counsel in modern glass boardroom, professional business attire,
            holding premium tablet showing legal interface, natural window lighting,
            corporate office setting with city view, professional headshot style,
            photorealistic, authoritative but approachable, executive presence,
            high-end corporate photography, shallow depth of field, warm professional lighting
        """,
        "image_size": "portrait_4_3"
    }
]

# Placeholder image service (for when FAL key is not available)
PLACEHOLDER_SERVICE = "https://storage.googleapis.com/marketing-copy-assets/images/"

async def generate_with_fal(prompt_config):
    """Generate image using FAL.ai"""
    try:
        clean_prompt = " ".join(prompt_config["prompt"].split())
        
        print(f"  Generating scene {prompt_config['scene']}: {prompt_config['name']}")
        
        handler = fal_client.submit(
            "fal-ai/flux/schnell",  # Fast, high-quality model
            arguments={
                "prompt": clean_prompt,
                "image_size": prompt_config.get("image_size", "landscape_16_9"),
                "num_images": 1
            }
        )
        
        result = handler.get()
        
        # Get image URL
        if "images" in result:
            image_url = result["images"][0]["url"]
        elif "image" in result:
            image_url = result["image"]["url"]
        else:
            print(f"    ⚠️  Unexpected response format")
            return None
        
        # Download image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prompt_config['name']}_{timestamp}.png"
        filepath = Path("generated_assets") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url, timeout=60.0)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"    ✓ Saved: {filepath}")
                return image_url
        
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return None

def use_placeholder(prompt_config):
    """Use placeholder image when FAL key is not available"""
    # Use existing assets from the storage bucket as placeholders
    scene = prompt_config['scene']
    # Map to existing showcase assets for consistency
    placeholder_map = {
        1: "generated_4ddacda7-cde3-4f0f-922f-d6d3496c2be5.png",
        2: "generated_7b502618-8843-44bf-b08f-c9b07e57e33c.png", 
        3: "generated_836bb2e3-f5db-444a-a4e0-c71ffbfa7c53.png",
        4: "generated_c46bed9c-bf11-44f3-8aba-6dcf6d121b8e.png"
    }
    return f"{PLACEHOLDER_SERVICE}{placeholder_map.get(scene, placeholder_map[1])}"

async def main():
    """Generate all Law.com case study assets"""
    print("🎨 Law.com Case Study Asset Generator")
    print("=" * 50)
    
    if USE_PLACEHOLDERS:
        print("📝 Using placeholder assets (set FAL_KEY for real generation)")
    else:
        print("🚀 Generating real assets with FAL.ai")
    
    # Load existing visuals file
    visuals_file = Path("law_campaign_visuals.json")
    with open(visuals_file, 'r') as f:
        visuals = json.load(f)
    
    # Generate images for each scene
    for i, prompt_config in enumerate(LAW_COM_PROMPTS):
        scene_num = prompt_config['scene']
        
        if USE_PLACEHOLDERS:
            image_url = use_placeholder(prompt_config)
            print(f"Scene {scene_num}: Using placeholder")
        else:
            image_url = await generate_with_fal(prompt_config)
        
        # Update visuals data
        if image_url and i < len(visuals):
            visuals[i]['image_url'] = image_url
            print(f"  ✓ Updated scene {scene_num}")
    
    # Save updated visuals
    with open(visuals_file, 'w') as f:
        json.dump(visuals, f, indent=2)
    
    print("\n✅ Law.com case study assets generated successfully!")
    print(f"📄 Updated: {visuals_file}")
    print("\nNext steps:")
    print("1. Update frontend to display law.com case study")
    print("2. Deploy to GCP")
    print("3. Verify deployment at showcase URL")

if __name__ == "__main__":
    asyncio.run(main())
