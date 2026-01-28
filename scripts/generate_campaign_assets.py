#!/usr/bin/env python3
"""
Campaign Asset Generator

Generates diverse creative assets for all audience segments and ad platforms
using Fal.ai turbo models for speed and creative variety.

Usage:
    python scripts/generate_campaign_assets.py --audience founders
    python scripts/generate_campaign_assets.py --all
    python scripts/generate_campaign_assets.py --type og
    python scripts/generate_campaign_assets.py --type ads
"""

import asyncio
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import fal_client
import httpx
from dotenv import load_dotenv

load_dotenv()

# Ensure FAL_KEY is set
if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
    os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]


# =============================================================================
# Model Configuration - Turbo models for speed + diversity
# =============================================================================

TURBO_MODELS = {
    "flux_schnell": "fal-ai/flux/schnell",           # Fast, high quality
    "sdxl_lightning": "fal-ai/fast-lightning-sdxl",  # Ultra fast
    "fast_sdxl": "fal-ai/fast-sdxl",                 # Balanced
    "flux_dev": "fal-ai/flux/dev",                   # Quality focus
    "recraft": "fal-ai/recraft-v3",                  # Design/vector focus
}

# Default to schnell for speed
DEFAULT_MODEL = TURBO_MODELS["flux_schnell"]


# =============================================================================
# Creative Prompts - Diverse styles representing range of work
# =============================================================================

AUDIENCE_PROMPTS = {
    "founders": {
        "og_image": {
            "primary": """
                Technical founder at a minimalist desk, laptop showing landing page wireframes,
                soft morning light through window, focused expression, code editor visible on second monitor,
                clean modern workspace, photorealistic, professional photography style,
                warm natural lighting, shallow depth of field
            """,
            "alt_abstract": """
                Abstract visualization of rapid iteration: flowing lines transforming into
                landing page elements, electric blue and warm amber gradient,
                geometric shapes suggesting speed and precision, modern tech aesthetic,
                dark background with glowing accents, high contrast, minimal
            """,
            "alt_symbolic": """
                Hourglass with sand transforming into golden conversion metrics mid-fall,
                sleek black background, dramatic lighting, photorealistic render,
                symbolizing time saved and results achieved, luxury product photography style
            """
        },
        "ad_creatives": {
            "google": """
                Clean split screen: left side shows messy document chaos, right side shows
                polished landing page, arrow transformation between them,
                professional marketing visual, bright clean background,
                before/after comparison style, corporate but modern
            """,
            "linkedin": """
                Professional founder reviewing polished pitch deck on tablet,
                confident expression, modern office backdrop,
                warm lighting, business casual attire, aspirational but approachable,
                LinkedIn ad style photography
            """,
            "meta": """
                Dynamic action shot: hands typing rapidly on keyboard with landing page
                materializing on screen as glowing holographic projection,
                energetic, modern, slightly futuristic but grounded,
                vibrant colors, high energy composition
            """,
            "twitter": """
                Minimal hero image: single cursor on blank page transforming into
                complete landing page with flourishing animation effect captured mid-transition,
                clean white background, blue accent colors, modern flat design aesthetic
            """
        },
        "social": {
            "testimonial_bg": """
                Soft gradient background from deep navy to warm copper,
                subtle geometric patterns, professional and premium feel,
                space for text overlay, modern marketing aesthetic
            """,
            "feature_card": """
                Isometric illustration of landing page components floating and assembling,
                colorful but cohesive palette, playful yet professional,
                modern SaaS illustration style, clean lines
            """
        }
    },

    "freelancers": {
        "og_image": {
            "primary": """
                Freelance marketer in creative home office, multiple screens showing
                client campaigns, coffee cup, plants, warm afternoon light,
                productive chaos organized, lifestyle photography style,
                authentic and relatable, not overly polished
            """,
            "alt_abstract": """
                Network visualization of client connections branching from central node,
                warm coral and teal color scheme, flowing organic lines,
                representing scalable freelance business, modern data visualization aesthetic
            """,
            "alt_symbolic": """
                Stack of glowing project cards fanning out like a hand of winning cards,
                each showing different campaign type, dramatic spotlight,
                dark cinematic background, representing diverse capabilities
            """
        },
        "ad_creatives": {
            "google": """
                Calendar view transforming from overcrowded chaos to organized
                blocks of productive work, time blocks glowing with completion,
                before/after productivity visual, clean modern UI style
            """,
            "linkedin": """
                Freelancer confidently presenting to video call grid of clients,
                professional home office setup, multiple happy client faces visible,
                warm lighting, success and scalability theme
            """,
            "meta": """
                Carousel of diverse project types spinning around central figure,
                landing pages, emails, social posts all orbiting,
                dynamic composition, colorful and energetic
            """,
            "twitter": """
                Minimal illustration: single person silhouette with radiating
                lines connecting to multiple project icons,
                clean vector style, impactful simple metaphor
            """
        },
        "social": {
            "testimonial_bg": """
                Warm gradient from coral pink to soft lavender,
                subtle brush stroke textures, creative but professional,
                space for quote overlay, Instagram-worthy aesthetic
            """,
            "feature_card": """
                Flat illustration of freelancer as superhero with cape made of
                various marketing deliverables, playful and empowering,
                vibrant color palette, modern illustration style
            """
        }
    },

    "marketing-teams": {
        "og_image": {
            "primary": """
                Modern marketing war room: team around large screen showing campaign dashboard,
                collaborative energy, diverse team members engaged in discussion,
                glass walls, post-it notes visible, high-tech but human,
                corporate photography style with warmth
            """,
            "alt_abstract": """
                Interconnected hexagonal network representing team collaboration,
                each node showing different marketing function, unified by flowing data streams,
                professional blue and white color scheme, enterprise aesthetic
            """,
            "alt_symbolic": """
                Symphony orchestra conductor's hands above dashboard that looks like
                sheet music, marketing metrics as musical notes,
                elegant metaphor for orchestrated campaigns, dramatic lighting
            """
        },
        "ad_creatives": {
            "google": """
                Side-by-side: chaotic slack messages vs unified command center dashboard,
                transformation arrow, clean corporate visual,
                problem/solution format, professional B2B aesthetic
            """,
            "linkedin": """
                Marketing team high-fiving around successful campaign results on screen,
                modern office, diverse professional team, celebratory but professional,
                aspirational team success imagery
            """,
            "meta": """
                Animated feel: team members each holding puzzle piece that connects
                to form complete campaign view, collaboration theme,
                bright energetic colors, inclusive imagery
            """,
            "twitter": """
                Minimal: multiple cursors collaboratively editing single document,
                real-time collaboration visualization, clean tech aesthetic,
                blue accent colors on white
            """
        },
        "social": {
            "testimonial_bg": """
                Professional gradient from slate blue to silver,
                subtle grid pattern suggesting structure and organization,
                enterprise-appropriate, space for quote overlay
            """,
            "feature_card": """
                Isometric office scene with team members at connected workstations,
                data flowing between them as glowing lines,
                modern corporate illustration, unified team aesthetic
            """
        }
    }
}

# Generic brand assets
BRAND_PROMPTS = {
    "hero_abstract": """
        Abstract flowing composition of marketing elements: headlines, buttons,
        form fields, all dissolving and reforming in golden light streams,
        premium dark background, electric indigo and warm amber accents,
        high-end tech aesthetic, slightly futuristic
    """,
    "hero_kinetic": """
        Kinetic typography explosion: marketing words fragmenting and reassembling,
        dynamic motion blur, bold sans-serif letters,
        dark background with bright accent lighting,
        energy and transformation theme
    """,
    "hero_minimal": """
        Single elegant cursor on pristine surface, small ripple effect spreading out,
        representing the simplicity of starting, ultra minimal,
        soft lighting, zen-like calm, premium product photography
    """,
    "pattern_tile": """
        Seamless repeating pattern of abstract marketing icons,
        subtle monochrome on cream background, sophisticated texture,
        vintage-modern hybrid aesthetic, tileable
    """,
    "gradient_premium": """
        Smooth gradient flow from deep navy through electric purple to warm copper,
        subtle noise texture, premium app background style,
        professional and distinctive
    """
}


# =============================================================================
# Asset Generator Class
# =============================================================================

class CampaignAssetGenerator:
    """Generates diverse campaign assets using Fal turbo models."""

    def __init__(self, output_dir: str = "generated_assets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[Dict[str, Any]] = []

    def _clean_prompt(self, prompt: str) -> str:
        """Clean up multi-line prompts."""
        return " ".join(prompt.split())

    async def _generate_image(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        size: str = "landscape_16_9",
        name: str = "image"
    ) -> Optional[Dict[str, Any]]:
        """Generate a single image using Fal."""
        try:
            print(f"  Generating: {name}")
            print(f"    Model: {model}")

            clean_prompt = self._clean_prompt(prompt)

            handler = fal_client.submit(
                model,
                arguments={
                    "prompt": clean_prompt,
                    "image_size": size,
                    "num_images": 1
                }
            )

            result = handler.get()

            # Handle different response formats
            if "images" in result:
                image_url = result["images"][0]["url"]
            elif "image" in result:
                image_url = result["image"]["url"]
            else:
                print(f"    Unexpected response format: {result.keys()}")
                return None

            # Download and save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.output_dir / filename

            async with httpx.AsyncClient() as client:
                response = await client.get(image_url, timeout=60.0)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"    Saved: {filepath}")

                    return {
                        "name": name,
                        "model": model,
                        "prompt": clean_prompt,
                        "local_path": str(filepath),
                        "fal_url": image_url,
                        "request_id": handler.request_id
                    }

        except Exception as e:
            print(f"    Error: {e}")
            return None

    async def generate_og_images(self, audience: str) -> List[Dict[str, Any]]:
        """Generate Open Graph images for an audience."""
        results = []
        prompts = AUDIENCE_PROMPTS.get(audience, {}).get("og_image", {})

        if not prompts:
            print(f"No OG prompts found for audience: {audience}")
            return results

        print(f"\nGenerating OG images for: {audience}")

        # Generate all variants
        tasks = []
        for variant, prompt in prompts.items():
            name = f"og_{audience}_{variant}"
            tasks.append(self._generate_image(
                prompt,
                model=TURBO_MODELS["flux_schnell"],
                size="landscape_16_9",
                name=name
            ))

        completed = await asyncio.gather(*tasks)
        results.extend([r for r in completed if r])

        return results

    async def generate_ad_creatives(self, audience: str) -> List[Dict[str, Any]]:
        """Generate ad creatives for all platforms for an audience."""
        results = []
        prompts = AUDIENCE_PROMPTS.get(audience, {}).get("ad_creatives", {})

        if not prompts:
            print(f"No ad prompts found for audience: {audience}")
            return results

        print(f"\nGenerating ad creatives for: {audience}")

        # Platform-specific sizes
        sizes = {
            "google": "landscape_16_9",    # Display ads
            "linkedin": "square",           # Feed ads
            "meta": "square",              # FB/IG feed
            "twitter": "landscape_16_9"    # Twitter cards
        }

        tasks = []
        for platform, prompt in prompts.items():
            name = f"ad_{audience}_{platform}"
            size = sizes.get(platform, "landscape_16_9")
            tasks.append(self._generate_image(
                prompt,
                model=TURBO_MODELS["flux_schnell"],
                size=size,
                name=name
            ))

        completed = await asyncio.gather(*tasks)
        results.extend([r for r in completed if r])

        return results

    async def generate_social_assets(self, audience: str) -> List[Dict[str, Any]]:
        """Generate social media background and feature images."""
        results = []
        prompts = AUDIENCE_PROMPTS.get(audience, {}).get("social", {})

        if not prompts:
            return results

        print(f"\nGenerating social assets for: {audience}")

        tasks = []
        for asset_type, prompt in prompts.items():
            name = f"social_{audience}_{asset_type}"
            tasks.append(self._generate_image(
                prompt,
                model=TURBO_MODELS["flux_schnell"],
                size="square",
                name=name
            ))

        completed = await asyncio.gather(*tasks)
        results.extend([r for r in completed if r])

        return results

    async def generate_brand_assets(self) -> List[Dict[str, Any]]:
        """Generate generic brand assets."""
        results = []

        print("\nGenerating brand assets")

        tasks = []
        for asset_name, prompt in BRAND_PROMPTS.items():
            name = f"brand_{asset_name}"
            # Use different models for variety
            model = TURBO_MODELS["recraft"] if "pattern" in asset_name else TURBO_MODELS["flux_schnell"]
            tasks.append(self._generate_image(
                prompt,
                model=model,
                size="landscape_16_9" if "hero" in asset_name else "square",
                name=name
            ))

        completed = await asyncio.gather(*tasks)
        results.extend([r for r in completed if r])

        return results

    async def generate_for_audience(self, audience: str) -> List[Dict[str, Any]]:
        """Generate all assets for a specific audience."""
        all_results = []

        og_results = await self.generate_og_images(audience)
        all_results.extend(og_results)

        ad_results = await self.generate_ad_creatives(audience)
        all_results.extend(ad_results)

        social_results = await self.generate_social_assets(audience)
        all_results.extend(social_results)

        return all_results

    async def generate_all(self) -> List[Dict[str, Any]]:
        """Generate all assets for all audiences plus brand assets."""
        all_results = []

        # Generate for each audience
        for audience in ["founders", "freelancers", "marketing-teams"]:
            results = await self.generate_for_audience(audience)
            all_results.extend(results)

        # Generate brand assets
        brand_results = await self.generate_brand_assets()
        all_results.extend(brand_results)

        return all_results

    def save_manifest(self, results: List[Dict[str, Any]]):
        """Save a manifest of all generated assets."""
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "total_assets": len(results),
            "assets": results
        }

        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"\nManifest saved to: {manifest_path}")


# =============================================================================
# CLI Interface
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(description="Generate campaign assets using Fal turbo models")
    parser.add_argument("--audience", choices=["founders", "freelancers", "marketing-teams"],
                       help="Generate assets for specific audience")
    parser.add_argument("--type", choices=["og", "ads", "social", "brand"],
                       help="Generate specific asset type")
    parser.add_argument("--all", action="store_true", help="Generate all assets")
    parser.add_argument("--output", default="generated_assets", help="Output directory")
    parser.add_argument("--model", choices=list(TURBO_MODELS.keys()),
                       help="Override model choice")

    args = parser.parse_args()

    # Check for API key
    if not os.getenv("FAL_KEY") and not os.getenv("FAL_API_KEY"):
        print("Error: FAL_KEY or FAL_API_KEY environment variable required")
        print("Set it with: export FAL_KEY=your_key_here")
        sys.exit(1)

    generator = CampaignAssetGenerator(output_dir=args.output)
    results = []

    if args.all:
        print("Generating ALL campaign assets...")
        print("This will create assets for all audiences and brand assets.")
        results = await generator.generate_all()

    elif args.audience:
        if args.type == "og":
            results = await generator.generate_og_images(args.audience)
        elif args.type == "ads":
            results = await generator.generate_ad_creatives(args.audience)
        elif args.type == "social":
            results = await generator.generate_social_assets(args.audience)
        else:
            results = await generator.generate_for_audience(args.audience)

    elif args.type == "brand":
        results = await generator.generate_brand_assets()

    else:
        parser.print_help()
        print("\nExamples:")
        print("  python generate_campaign_assets.py --all")
        print("  python generate_campaign_assets.py --audience founders")
        print("  python generate_campaign_assets.py --audience founders --type og")
        print("  python generate_campaign_assets.py --type brand")
        sys.exit(0)

    if results:
        generator.save_manifest(results)
        print(f"\n{'='*50}")
        print(f"Generated {len(results)} assets")
        print(f"Output directory: {generator.output_dir}")
    else:
        print("\nNo assets generated. Check your API key and try again.")


if __name__ == "__main__":
    asyncio.run(main())
