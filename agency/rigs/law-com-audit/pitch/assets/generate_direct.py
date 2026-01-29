#!/usr/bin/env python3
"""
Direct Pitch Asset Generator

Generates all visual assets using Fal directly, saving the URLs
for use in the pitch deck.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Ensure FAL_KEY
if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
    os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]

import fal_client

# Model
MODEL = "fal-ai/flux/schnell"

# Style base
STYLE = """premium executive presentation, dark navy #0A1628 background,
golden amber #C9A227 accents, sophisticated consulting aesthetic,
clean minimal, McKinsey meets Bloomberg style"""

# Assets to generate
ASSETS = [
    ("cover", "Abstract premium background for executive pitch, deep navy gradient with elegant gold accent lines suggesting data and intelligence, minimalist geometric, corporate luxury"),
    ("timeline", "Converging timeline visualization, five golden lines meeting at bright central point suggesting critical moment, elegant data viz"),
    ("market_gap", "Minimalist bar chart, two vertical bars one tall golden one short gray showing 3:1 ratio, competitive gap visualization"),
    ("funnel", "Conversion funnel with leaks, wide top narrow bottom, golden particles escaping through cracks, lost value visualization"),
    ("pillars", "Three elegant golden trophy pillars in a row, premium 3D, representing exclusive valuable assets"),
    ("positioning", "Strategic quadrant map with golden arrow moving from bottom-left to top-right, repositioning journey"),
    ("strategy", "Three classical Greek columns supporting pediment, golden tones, architectural strength and foundation"),
    ("moat", "Abstract fortress with moat, golden wireframe castle with protective barrier, competitive defense"),
    ("transformation", "Split screen before/after, left chaotic fragments right organized dashboard, digital transformation"),
    ("roi", "Exponential growth arrow, golden arrow small bottom-left to large top-right, ROI visualization"),
    ("risk", "Descending trend line with warning markers, decline with three amber warning points, urgency"),
    ("divider", "Minimalist section divider, navy with single gold geometric accent, space for text overlay"),
    ("hero_intel", "Intelligence platform visualization, network of connected nodes with central glowing hub, data insights"),
    ("hero_bench", "Benchmarking visualization, tiered podium with golden accents, competitive rankings"),
]


def generate_assets():
    """Generate all assets."""
    print("=" * 60)
    print("HIGH ERA AGENCY - PITCH ASSET GENERATION")
    print("=" * 60)
    print()

    results = []

    for i, (asset_id, base_prompt) in enumerate(ASSETS, 1):
        prompt = f"{base_prompt}, {STYLE}"
        print(f"[{i}/{len(ASSETS)}] Generating: {asset_id}")

        try:
            handler = fal_client.submit(
                MODEL,
                arguments={
                    "prompt": prompt,
                    "image_size": "landscape_16_9",
                    "num_images": 1
                }
            )

            result = handler.get()

            if "images" in result:
                url = result["images"][0]["url"]
            elif "image" in result:
                url = result["image"]["url"]
            else:
                print(f"    Error: unexpected response")
                continue

            results.append({
                "id": asset_id,
                "url": url,
                "request_id": handler.request_id
            })
            print(f"    ✓ {url}")

        except Exception as e:
            print(f"    ✗ Error: {e}")

        print()

    # Save manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "model": MODEL,
        "assets": results
    }

    manifest_path = Path(__file__).parent / "generated_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("=" * 60)
    print(f"Generated {len(results)}/{len(ASSETS)} assets")
    print(f"Manifest: {manifest_path}")
    print("=" * 60)

    # Print markdown for docs
    print("\n## Asset URLs for Documentation\n")
    print("```markdown")
    for r in results:
        print(f"![{r['id']}]({r['url']})")
    print("```")

    return results


if __name__ == "__main__":
    generate_assets()
