#!/usr/bin/env python3
"""
Pitch Deck Asset Generator

Generates premium visual assets for the Law.com executive pitch deck
using Fal.ai turbo models.

Usage:
    python generate_pitch_assets.py --all
    python generate_pitch_assets.py --slide 1
    python generate_pitch_assets.py --type backgrounds
"""

import asyncio
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))

import fal_client
import httpx
from dotenv import load_dotenv

load_dotenv()

# Ensure FAL_KEY is set
if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
    os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


# =============================================================================
# Configuration
# =============================================================================

# Premium model for high-quality presentation assets
MODEL = "fal-ai/flux/schnell"  # Fast + quality for iteration
MODEL_PRO = "fal-ai/flux-pro/v1.1"  # Use for final production assets

OUTPUT_DIR = Path(__file__).parent / "generated"

# Design tokens
STYLE_SUFFIX = """
premium consulting deck aesthetic, dark navy (#0A1628) background,
golden amber (#C9A227) accents, sophisticated corporate style,
extremely clean and minimal, no text unless specified,
McKinsey meets Bloomberg visual language, photorealistic rendering
"""


# =============================================================================
# Asset Prompts
# =============================================================================

SLIDE_ASSETS = {
    "cover": {
        "name": "cover-bg",
        "size": "landscape_16_9",
        "prompt": f"""
            Abstract premium executive presentation background,
            deep navy blue gradient with subtle gold accent lines
            suggesting data streams and intelligence networks,
            minimalist geometric patterns flowing diagonally,
            corporate luxury aesthetic, extremely sophisticated,
            {STYLE_SUFFIX}
        """
    },

    "timeline": {
        "name": "timeline-convergence",
        "size": "landscape_16_9",
        "prompt": f"""
            Abstract visualization of converging timelines,
            five thin golden lines converging from edges to a bright
            central focal point, suggesting critical inflection moment,
            dark navy void background, premium data visualization,
            elegant and minimal, sense of urgency and opportunity,
            {STYLE_SUFFIX}
        """
    },

    "market_gap": {
        "name": "market-comparison",
        "size": "landscape_4_3",
        "prompt": f"""
            Minimalist bar chart abstract visualization,
            two vertical bars - one dramatically tall (golden amber),
            one much shorter (muted gray), approximately 3:1 ratio,
            suggests market dominance gap, clean geometric style,
            no axis lines or labels, premium data visualization,
            {STYLE_SUFFIX}
        """
    },

    "funnel_leak": {
        "name": "funnel-leak",
        "size": "landscape_4_3",
        "prompt": f"""
            Dramatic visualization of a conversion funnel with leaks,
            wide opening at top tapering to narrow bottom,
            golden light particles escaping through fractures
            along the funnel walls, suggesting lost value and opportunity,
            abstract business visualization, premium consulting style,
            {STYLE_SUFFIX}
        """
    },

    "pillars_assets": {
        "name": "exclusive-assets",
        "size": "landscape_16_9",
        "prompt": f"""
            Three elegant golden pillar or trophy icons arranged in a row,
            premium minimalist 3D rendering, each pillar glowing subtly,
            representing valuable exclusive assets,
            architectural sophistication, museum quality presentation,
            {STYLE_SUFFIX}
        """
    },

    "positioning_map": {
        "name": "positioning-map",
        "size": "landscape_4_3",
        "prompt": f"""
            Strategic positioning quadrant visualization,
            subtle grid with four quadrants, a golden curved arrow
            moving from bottom-left to top-right quadrant,
            suggesting strategic repositioning journey,
            elegant business strategy diagram,
            {STYLE_SUFFIX}
        """
    },

    "strategy_pillars": {
        "name": "strategy-pillars",
        "size": "landscape_16_9",
        "prompt": f"""
            Three classical Greek columns supporting a triangular pediment,
            rendered in elegant golden tones, architectural visualization,
            suggesting strength and strategic foundation,
            minimalist neoclassical style, premium and sophisticated,
            {STYLE_SUFFIX}
        """
    },

    "competitive_moat": {
        "name": "competitive-moat",
        "size": "landscape_4_3",
        "prompt": f"""
            Abstract geometric visualization of a fortress with moat,
            golden wireframe castle structure surrounded by
            protective barrier rendered as flowing lines,
            suggesting competitive defense and barriers to entry,
            premium architectural diagram style,
            {STYLE_SUFFIX}
        """
    },

    "transformation": {
        "name": "transformation-split",
        "size": "landscape_16_9",
        "prompt": f"""
            Split-screen transformation visualization,
            left half shows chaotic scattered geometric fragments
            suggesting disorder and noise,
            right half shows organized elegant dashboard layout
            with clean aligned elements,
            transition from chaos to order, before/after contrast,
            {STYLE_SUFFIX}
        """
    },

    "roi_growth": {
        "name": "roi-growth",
        "size": "landscape_4_3",
        "prompt": f"""
            Dramatic exponential growth arrow visualization,
            golden arrow starting small at bottom left,
            expanding and curving upward to large finish at top right,
            suggesting massive return on investment,
            premium data visualization, dynamic and aspirational,
            {STYLE_SUFFIX}
        """
    },

    "risk_decline": {
        "name": "risk-decline",
        "size": "landscape_4_3",
        "prompt": f"""
            Descending trend line with warning markers,
            line starting high on left, declining steeply to right,
            three red/amber warning indicator points along the decline,
            suggesting risk and negative trajectory,
            urgent but professional data visualization,
            {STYLE_SUFFIX}
        """
    },
}

BACKGROUND_ASSETS = {
    "divider_strategy": {
        "name": "divider-strategy",
        "size": "landscape_16_9",
        "prompt": f"""
            Minimalist section divider background,
            deep navy with single elegant gold geometric accent
            positioned off-center, extremely clean,
            large negative space for text overlay,
            {STYLE_SUFFIX}
        """
    },

    "divider_execution": {
        "name": "divider-execution",
        "size": "landscape_16_9",
        "prompt": f"""
            Minimalist section divider background,
            deep navy with subtle gold angular line element,
            suggesting forward movement and action,
            large negative space for text overlay,
            {STYLE_SUFFIX}
        """
    },

    "divider_investment": {
        "name": "divider-investment",
        "size": "landscape_16_9",
        "prompt": f"""
            Minimalist section divider background,
            deep navy with subtle gold circular/currency-like accent,
            suggesting value and investment,
            large negative space for text overlay,
            {STYLE_SUFFIX}
        """
    },

    "chart_background": {
        "name": "chart-bg-dark",
        "size": "landscape_4_3",
        "prompt": f"""
            Extremely subtle grid pattern background,
            very dark navy with barely visible geometric grid lines,
            designed for data chart overlays,
            minimalist and unobtrusive, premium consulting aesthetic,
            almost solid dark color with hint of structure,
            {STYLE_SUFFIX}
        """
    },
}

HERO_ASSETS = {
    "intelligence_platform": {
        "name": "hero-intelligence",
        "size": "landscape_16_9",
        "prompt": f"""
            Abstract visualization of legal intelligence platform,
            network of connected nodes suggesting data and insights,
            central brain or hub icon radiating golden connections,
            represents transformation from news to intelligence,
            futuristic but grounded, premium tech aesthetic,
            {STYLE_SUFFIX}
        """
    },

    "data_benchmark": {
        "name": "hero-benchmark",
        "size": "landscape_16_9",
        "prompt": f"""
            Abstract visualization of benchmarking and rankings,
            tiered podium or ranking visualization with golden accents,
            suggests competitive positioning and market leadership,
            premium data visualization aesthetic,
            {STYLE_SUFFIX}
        """
    },
}


# =============================================================================
# Generator Class
# =============================================================================

class PitchAssetGenerator:
    """Generates premium assets for executive pitch deck."""

    def __init__(self, output_dir: Path = OUTPUT_DIR, use_pro: bool = False):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model = MODEL_PRO if use_pro else MODEL
        self.results: List[Dict[str, Any]] = []

    def _clean_prompt(self, prompt: str) -> str:
        """Clean multi-line prompts."""
        return " ".join(prompt.split())

    async def _generate_image(
        self,
        prompt: str,
        size: str,
        name: str
    ) -> Optional[Dict[str, Any]]:
        """Generate a single image using Fal."""
        try:
            print(f"  Generating: {name}")
            print(f"    Model: {self.model}")
            print(f"    Size: {size}")

            clean_prompt = self._clean_prompt(prompt)

            handler = fal_client.submit(
                self.model,
                arguments={
                    "prompt": clean_prompt,
                    "image_size": size,
                    "num_images": 1
                }
            )

            result = handler.get()

            if "images" in result:
                image_url = result["images"][0]["url"]
            elif "image" in result:
                image_url = result["image"]["url"]
            else:
                print(f"    Unexpected response: {result.keys()}")
                return None

            # Download and save
            filename = f"{name}.png"
            filepath = self.output_dir / filename

            async with httpx.AsyncClient() as client:
                response = await client.get(image_url, timeout=60.0)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"    Saved: {filepath}")

                    return {
                        "name": name,
                        "model": self.model,
                        "local_path": str(filepath),
                        "fal_url": image_url
                    }

        except Exception as e:
            print(f"    Error: {e}")
            return None

    async def generate_slide_assets(self) -> List[Dict[str, Any]]:
        """Generate all slide-specific assets."""
        results = []
        print("\nGenerating slide assets...")

        for key, spec in SLIDE_ASSETS.items():
            result = await self._generate_image(
                spec["prompt"],
                spec["size"],
                spec["name"]
            )
            if result:
                results.append(result)

        return results

    async def generate_backgrounds(self) -> List[Dict[str, Any]]:
        """Generate background/divider assets."""
        results = []
        print("\nGenerating background assets...")

        for key, spec in BACKGROUND_ASSETS.items():
            result = await self._generate_image(
                spec["prompt"],
                spec["size"],
                spec["name"]
            )
            if result:
                results.append(result)

        return results

    async def generate_heroes(self) -> List[Dict[str, Any]]:
        """Generate hero/feature assets."""
        results = []
        print("\nGenerating hero assets...")

        for key, spec in HERO_ASSETS.items():
            result = await self._generate_image(
                spec["prompt"],
                spec["size"],
                spec["name"]
            )
            if result:
                results.append(result)

        return results

    async def generate_all(self) -> List[Dict[str, Any]]:
        """Generate all assets."""
        all_results = []

        slide_results = await self.generate_slide_assets()
        all_results.extend(slide_results)

        bg_results = await self.generate_backgrounds()
        all_results.extend(bg_results)

        hero_results = await self.generate_heroes()
        all_results.extend(hero_results)

        return all_results

    def save_manifest(self, results: List[Dict[str, Any]]):
        """Save manifest of generated assets."""
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "model": self.model,
            "total_assets": len(results),
            "assets": results
        }

        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"\nManifest saved: {manifest_path}")


# =============================================================================
# CLI
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(description="Generate pitch deck assets")
    parser.add_argument("--all", action="store_true", help="Generate all assets")
    parser.add_argument("--slides", action="store_true", help="Generate slide assets only")
    parser.add_argument("--backgrounds", action="store_true", help="Generate backgrounds only")
    parser.add_argument("--heroes", action="store_true", help="Generate hero assets only")
    parser.add_argument("--pro", action="store_true", help="Use Flux Pro for higher quality")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="Output directory")

    args = parser.parse_args()

    if not os.getenv("FAL_KEY") and not os.getenv("FAL_API_KEY"):
        print("Error: FAL_KEY or FAL_API_KEY required")
        print("Set with: export FAL_KEY=your_key")
        sys.exit(1)

    generator = PitchAssetGenerator(
        output_dir=Path(args.output),
        use_pro=args.pro
    )

    results = []

    if args.all:
        print("Generating ALL pitch deck assets...")
        print(f"Using model: {'Flux Pro' if args.pro else 'Flux Schnell'}")
        results = await generator.generate_all()
    elif args.slides:
        results = await generator.generate_slide_assets()
    elif args.backgrounds:
        results = await generator.generate_backgrounds()
    elif args.heroes:
        results = await generator.generate_heroes()
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python generate_pitch_assets.py --all")
        print("  python generate_pitch_assets.py --slides")
        print("  python generate_pitch_assets.py --all --pro  # Higher quality")
        sys.exit(0)

    if results:
        generator.save_manifest(results)
        print(f"\n{'='*50}")
        print(f"Generated {len(results)} assets")
        print(f"Output: {generator.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
