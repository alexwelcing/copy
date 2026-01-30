#!/usr/bin/env python3
"""
HIGH ERA AGENCY - EXECUTIVE PITCH ASSETS
Law.com Strategic Transformation

Premium visual assets for the executive pitch deck.
Uses Flux Pro 1.1 for quality that matches the strategy.

Run: python generate_premium.py
"""

import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Configuration
FAL_KEY = os.getenv("FAL_KEY", "af087bda-e123-4614-a945-02d6c8277a19:cd9aaf828cd2cd1cfc92b98ecaf4e550")
MODEL = "fal-ai/flux-pro/v1.1"  # Quality matters
OUTPUT_DIR = Path("./generated_assets")

# Design System
PALETTE = {
    "navy": "#0A1628",
    "gold": "#C9A227",
    "cream": "#F8F6F1",
}

# The prompts - crafted with actual taste
ASSETS = {
    "cover": {
        "slide": 1,
        "prompt": """
            Cinematic abstract composition for executive presentation.
            Deep void of navy blue gradually revealing elegant golden filaments
            that trace paths like neural networks or data flows.
            Inspired by James Turrell light installations and Bloomberg terminal aesthetics.
            Single point of warm golden light emerging from darkness.
            Extremely minimal, contemplative, premium.
            No text, no logos, no obvious symbols.
            Photographic quality, shallow depth of field on light elements.
        """
    },

    "inflection": {
        "slide": 2,
        "prompt": """
            Abstract visualization of convergence and critical moment.
            Five thin threads of golden light traveling through deep blue-black space,
            converging toward a single luminous point.
            Sense of inevitable collision, of forces gathering.
            Like light rays in a cathedral or fiber optics meeting.
            Minimal, elegant, tension before release.
            Premium consulting aesthetic, no decorative elements.
        """
    },

    "dominance": {
        "slide": 3,
        "prompt": """
            Stark abstract comparison visualization.
            Two vertical forms - one towering column of warm golden light,
            one modest pillar of cool gray.
            The golden form is three times the height, undeniable dominance.
            Set against deep navy void.
            Clean, geometric, no embellishment.
            The visual speaks for itself - market leadership gap.
        """
    },

    "leaking_value": {
        "slide": 4,
        "prompt": """
            Abstract visualization of value escaping.
            A vessel shape in golden light, wide at top narrowing severely.
            Particles of light - like gold dust or data points -
            streaming out through fractures in the sides.
            Beautiful but urgent. Loss rendered elegant.
            Deep navy background, cinematic lighting.
            Metaphor for conversion leak without being literal.
        """
    },

    "three_assets": {
        "slide": 5,
        "prompt": """
            Three luminous objects arranged in contemplative composition.
            Like museum pieces or relics - precious, singular, irreplaceable.
            Each glowing with inner golden light against deep darkness.
            Abstract forms suggesting trophies or monuments.
            Premium, reverent, exclusive.
            The feeling of viewing something valuable and rare.
        """
    },

    "repositioning": {
        "slide": 6,
        "prompt": """
            Abstract journey visualization.
            A golden arc of light tracing a path from lower left to upper right,
            leaving a trail through deep blue-black space.
            Sense of deliberate movement, strategic trajectory.
            The path curves elegantly upward - aspiration made visible.
            Minimal quadrant suggestion through subtle value shifts in background.
        """
    },

    "foundation": {
        "slide": 7,
        "prompt": """
            Three vertical columns of light, architectural in feeling.
            Classical proportions rendered in pure luminosity.
            Supporting an implied structure above - strategy as architecture.
            Golden light against navy void.
            Elegant, stable, foundational.
            Timeless forms suggesting enduring strategic framework.
        """
    },

    "fortress": {
        "slide": 10,
        "prompt": """
            Abstract defensive structure visualization.
            Geometric golden forms suggesting fortification,
            surrounded by a flowing boundary of light - the moat.
            Strategic protection rendered elegant.
            Not literal castle - abstract impression of defended position.
            Premium, sophisticated, powerful without aggression.
        """
    },

    "transformation": {
        "slide": 11,
        "prompt": """
            Diptych composition - two states in one frame.
            Left: scattered fragments, chaos, entropy - rendered in cool grays.
            Right: organized harmony, aligned elements - rendered in warm gold.
            The transition between disorder and order.
            Before and after without being literal.
            Elegant visualization of transformation.
        """
    },

    "growth": {
        "slide": 17,
        "prompt": """
            Exponential curve rendered in pure light.
            Starting small and humble in lower left,
            sweeping upward in golden arc that expands dramatically.
            The visual vocabulary of ROI - investment becomes return.
            Against deep navy, the growth feels inevitable.
            Aspirational without being naive.
        """
    },

    "decline": {
        "slide": 18,
        "prompt": """
            Descending trajectory visualization.
            A line of light beginning bright, fading as it falls rightward.
            Three points along the descent marked with subtle amber warnings.
            Elegant rendering of risk - beautiful but concerning.
            The aesthetic of a medical monitor showing decline.
            Urgent without being alarmist.
        """
    },

    "section_break": {
        "slide": "divider",
        "prompt": """
            Pure minimal composition for section transition.
            Deep navy field with single geometric element in gold -
            perhaps a thin horizontal line or subtle angular form.
            Vast negative space for typography overlay.
            Breathing room, contemplative pause.
            The visual equivalent of a deep breath before continuing.
        """
    },

    "intelligence": {
        "slide": "hero",
        "prompt": """
            Network visualization suggesting intelligence and insight.
            Nodes of golden light connected by fine luminous threads,
            radiating from a brighter central hub.
            Data becoming knowledge becoming wisdom.
            Against deep navy, like stars forming constellations of meaning.
            Premium technology aesthetic, not sci-fi.
        """
    },

    "rankings": {
        "slide": "hero",
        "prompt": """
            Abstract podium or hierarchy visualization.
            Tiered forms of golden light suggesting ranking and order.
            The visual language of benchmark and standing.
            Elegant, not competitive or aggressive.
            Achievement rendered in light and geometry.
            Premium, contemplative, aspirational.
        """
    },
}


def generate_image(asset_id: str, spec: dict) -> dict:
    """Generate a single image via Fal API."""

    prompt = " ".join(spec["prompt"].split())  # Clean whitespace

    url = f"https://fal.run/{MODEL}"
    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "prompt": prompt,
        "image_size": "landscape_16_9",
        "num_images": 1,
        "safety_tolerance": "5",
        "guidance_scale": 3.5,  # Pro model guidance
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))

            image_url = result.get("images", [{}])[0].get("url")
            if not image_url:
                return {"error": "No image URL in response"}

            # Download the image
            filename = OUTPUT_DIR / f"{asset_id}.png"
            urllib.request.urlretrieve(image_url, filename)

            return {
                "id": asset_id,
                "slide": spec["slide"],
                "url": image_url,
                "local": str(filename),
                "status": "success"
            }

    except urllib.error.HTTPError as e:
        return {"id": asset_id, "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"id": asset_id, "error": str(e)}


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=" * 70)
    print("HIGH ERA AGENCY")
    print("Executive Pitch Asset Generation")
    print("Law.com Strategic Transformation")
    print("=" * 70)
    print()
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Assets: {len(ASSETS)}")
    print()

    results = []

    for i, (asset_id, spec) in enumerate(ASSETS.items(), 1):
        print(f"[{i:2}/{len(ASSETS)}] {asset_id}")
        print(f"       Slide: {spec['slide']}")

        result = generate_image(asset_id, spec)
        results.append(result)

        if result.get("status") == "success":
            print(f"       ✓ {result['local']}")
        else:
            print(f"       ✗ {result.get('error', 'Unknown error')}")

        print()

        # Brief pause between requests
        if i < len(ASSETS):
            time.sleep(1)

    # Save manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "model": MODEL,
        "project": "law-com-pitch",
        "palette": PALETTE,
        "assets": results
    }

    manifest_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Summary
    success = sum(1 for r in results if r.get("status") == "success")
    print("=" * 70)
    print(f"COMPLETE: {success}/{len(ASSETS)} assets generated")
    print(f"Manifest: {manifest_path}")
    print("=" * 70)

    if success == len(ASSETS):
        print("\nAll assets ready for pitch deck.")
    else:
        print("\nSome assets failed - check errors above.")


if __name__ == "__main__":
    main()
