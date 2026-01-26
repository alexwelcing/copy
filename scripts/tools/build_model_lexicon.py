import os
import httpx
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

async def build_lexicon():
    fal_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
    if not fal_key:
        print("Error: FAL_API_KEY not found in environment variables.")
        return

    headers = {
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json"
    }

    # Extended categories list
    categories = [
        "text-to-image", 
        "image-to-image", 
        "image-to-video", 
        "text-to-video", 
        "audio", 
        "text-to-3d", 
        "image-to-3d",
        "utilities"
    ]
    
    all_models = []

    async with httpx.AsyncClient() as client:
        for cat in categories:
            print(f"Fetching category: {cat}...")
            # Simple pagination loop
            url = f"https://api.fal.ai/v1/models?category={cat}&status=active&limit=100"
            while url:
                try:
                    response = await client.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        batch = data.get("models", [])
                        all_models.extend(batch)
                        print(f"  Found {len(batch)} models.")
                        
                        # Check for next page
                        url = data.get("next") # API usually returns next URL or None
                        if not url and len(batch) == 100:
                            # Fallback if API structure implies cursor but doesn't give explicit URL
                            # (Implementation detail: dependent on actual FAL API pagination)
                            pass 
                    else:
                        print(f"  Error {response.status_code}: {response.text}")
                        break
                except Exception as e:
                    print(f"  Exception: {e}")
                    break

    # Deduplicate by endpoint_id
    unique_models = {m["endpoint_id"]: m for m in all_models}
    sorted_models = sorted(unique_models.values(), key=lambda x: x.get("endpoint_id"))
    
    output_dir = Path(__file__).parent
    json_path = output_dir / "fal_model_catalog.json"
    
    print(f"\nTotal unique models found: {len(sorted_models)}")
    
    with open(json_path, "w") as f:
        json.dump(sorted_models, f, indent=2)
    
    print(f"Full catalog saved to: {json_path}")

    # Generate Markdown Summary (Top Picks)
    md_path = output_dir / "fal_model_summary.md"
    with open(md_path, "w") as f:
        f.write(f"# FAL Model Library Summary ({datetime.now().strftime('%Y-%m-%d')})\n\n")
        
        for cat in categories:
            f.write(f"## {cat.replace('-', ' ').title()}\n")
            cat_models = [m for m in sorted_models if m.get("metadata", {}).get("category") == cat]
            
            # Simple heuristic for "top" models: official ones first, then by date
            cat_models.sort(key=lambda x: (
                not x.get("endpoint_id", "").startswith("fal-ai/"), # fal-ai first
                x.get("metadata", {}).get("created_at", "")
            ), reverse=True)
            
            for m in cat_models[:15]: # Show top 15 per category
                eid = m.get("endpoint_id")
                desc = m.get("metadata", {}).get("description", "No description")
                f.write(f"- **`{eid}`**: {desc}\n")
            f.write("\n")
            
    print(f"Summary saved to: {md_path}")

if __name__ == "__main__":
    asyncio.run(build_lexicon())
