#!/usr/bin/env python3
"""
Agency-Driven Pitch Asset Generator

Generates all visual assets for the Law.com executive pitch deck
using High Era's asset infrastructure, uploads to GCS, and creates
a manifest with public URLs.

Run with: python generate_to_gcs.py
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add project root for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from service.core.assets import get_asset_manager
from service.core.models import ImageModels

# =============================================================================
# Asset Definitions - Agency Copywriter & Strategist Approved
# =============================================================================

STYLE_BASE = """
premium executive presentation aesthetic, dark navy (#0A1628) background,
golden amber (#C9A227) accents, sophisticated corporate consulting style,
extremely clean and minimal, photorealistic high-end rendering,
McKinsey meets Bloomberg visual language
"""

PITCH_ASSETS = [
    {
        "id": "cover",
        "name": "Pitch Deck Cover Background",
        "gcs_path": "pitch/law-com/cover-bg.png",
        "prompt": f"""
            Abstract premium executive presentation background for legal intelligence company,
            deep navy blue gradient with elegant gold accent lines suggesting data streams
            and intelligence networks flowing diagonally across the frame,
            minimalist geometric patterns, extremely sophisticated corporate luxury aesthetic,
            {STYLE_BASE}
        """
    },
    {
        "id": "timeline",
        "name": "Inflection Point Timeline",
        "gcs_path": "pitch/law-com/timeline-convergence.png",
        "prompt": f"""
            Abstract visualization of converging timelines representing critical business moment,
            five thin golden lines converging from edges toward a bright central focal point,
            suggesting urgency and pivotal decision point, elegant data visualization,
            {STYLE_BASE}
        """
    },
    {
        "id": "market_gap",
        "name": "Market Preference Gap",
        "gcs_path": "pitch/law-com/market-comparison.png",
        "prompt": f"""
            Minimalist bar chart abstract visualization showing dramatic competitive gap,
            two vertical bars - one dramatically tall golden amber bar on left,
            one much shorter muted gray bar on right, approximately 3:1 ratio,
            clean geometric data visualization suggesting market dominance,
            {STYLE_BASE}
        """
    },
    {
        "id": "funnel",
        "name": "Conversion Funnel Leak",
        "gcs_path": "pitch/law-com/funnel-leak.png",
        "prompt": f"""
            Dramatic visualization of a business conversion funnel with leaks,
            wide golden opening at top tapering severely to narrow bottom,
            golden light particles and value escaping through fractures along walls,
            abstract representation of lost revenue and conversion friction,
            {STYLE_BASE}
        """
    },
    {
        "id": "pillars",
        "name": "Exclusive Assets Pillars",
        "gcs_path": "pitch/law-com/exclusive-assets.png",
        "prompt": f"""
            Three elegant golden pillar or trophy icons arranged horizontally,
            premium minimalist 3D rendering, each pillar with subtle glow,
            representing valuable exclusive business assets and competitive moats,
            architectural sophistication, museum quality presentation,
            {STYLE_BASE}
        """
    },
    {
        "id": "positioning",
        "name": "Strategic Positioning Map",
        "gcs_path": "pitch/law-com/positioning-map.png",
        "prompt": f"""
            Strategic quadrant positioning visualization for business strategy,
            subtle grid with four quadrants, elegant golden curved arrow
            moving from bottom-left commodity quadrant to top-right premium quadrant,
            suggesting strategic transformation and repositioning journey,
            {STYLE_BASE}
        """
    },
    {
        "id": "strategy",
        "name": "Strategy Pillars Architecture",
        "gcs_path": "pitch/law-com/strategy-pillars.png",
        "prompt": f"""
            Three classical Greek columns supporting a triangular pediment structure,
            rendered in elegant golden tones, architectural visualization,
            suggesting strategic strength and foundational business framework,
            neoclassical minimalist style, premium sophisticated aesthetic,
            {STYLE_BASE}
        """
    },
    {
        "id": "moat",
        "name": "Competitive Moat Defense",
        "gcs_path": "pitch/law-com/competitive-moat.png",
        "prompt": f"""
            Abstract geometric visualization of a fortress with protective moat,
            golden wireframe castle structure surrounded by flowing defensive barrier,
            suggesting competitive defense and barriers to entry,
            premium architectural diagram style, strategic business visual,
            {STYLE_BASE}
        """
    },
    {
        "id": "transformation",
        "name": "Before/After Transformation",
        "gcs_path": "pitch/law-com/transformation-split.png",
        "prompt": f"""
            Split-screen business transformation visualization,
            left half shows chaotic scattered geometric fragments suggesting disorder,
            right half shows organized elegant dashboard with clean aligned elements,
            dramatic before and after contrast, digital transformation narrative,
            {STYLE_BASE}
        """
    },
    {
        "id": "roi",
        "name": "ROI Growth Arrow",
        "gcs_path": "pitch/law-com/roi-growth.png",
        "prompt": f"""
            Dramatic exponential growth arrow visualization for investment return,
            golden arrow starting small at bottom left, expanding and curving
            dynamically upward to large impressive finish at top right,
            premium data visualization suggesting massive ROI, aspirational,
            {STYLE_BASE}
        """
    },
    {
        "id": "risk",
        "name": "Risk Decline Warning",
        "gcs_path": "pitch/law-com/risk-decline.png",
        "prompt": f"""
            Descending trend line visualization with warning markers,
            line starting high on left declining steeply to right,
            three amber/red warning indicator points along the decline,
            suggesting business risk and negative trajectory without action,
            urgent but professional data visualization,
            {STYLE_BASE}
        """
    },
    {
        "id": "divider_strategy",
        "name": "Section Divider - Strategy",
        "gcs_path": "pitch/law-com/divider-strategy.png",
        "prompt": f"""
            Minimalist premium section divider background,
            deep navy with single elegant gold geometric accent off-center,
            extremely clean with large negative space for text overlay,
            sophisticated consulting presentation aesthetic,
            {STYLE_BASE}
        """
    },
    {
        "id": "divider_execution",
        "name": "Section Divider - Execution",
        "gcs_path": "pitch/law-com/divider-execution.png",
        "prompt": f"""
            Minimalist premium section divider background,
            deep navy with subtle gold angular line element suggesting forward movement,
            clean with large negative space for text overlay,
            action-oriented consulting presentation aesthetic,
            {STYLE_BASE}
        """
    },
    {
        "id": "hero_intelligence",
        "name": "Intelligence Platform Hero",
        "gcs_path": "pitch/law-com/hero-intelligence.png",
        "prompt": f"""
            Abstract visualization of legal intelligence platform concept,
            network of connected nodes suggesting data insights and knowledge,
            central glowing hub radiating golden connections outward,
            represents transformation from news aggregation to intelligence platform,
            futuristic but grounded premium technology aesthetic,
            {STYLE_BASE}
        """
    },
    {
        "id": "hero_benchmark",
        "name": "Benchmarking Hero",
        "gcs_path": "pitch/law-com/hero-benchmark.png",
        "prompt": f"""
            Abstract visualization of benchmarking and competitive rankings,
            elegant tiered podium or ranking visualization with golden accents,
            suggests market leadership and competitive positioning intelligence,
            premium business data visualization aesthetic,
            {STYLE_BASE}
        """
    },
]


async def generate_all_assets():
    """Generate all pitch assets and upload to GCS."""

    print("=" * 60)
    print("HIGH ERA AGENCY - PITCH ASSET GENERATION")
    print("Project: Law.com Strategic Transformation")
    print("=" * 60)
    print()

    asset_manager = get_asset_manager()
    results = []
    errors = []

    for i, asset in enumerate(PITCH_ASSETS, 1):
        print(f"[{i}/{len(PITCH_ASSETS)}] Generating: {asset['name']}")
        print(f"    Path: {asset['gcs_path']}")

        try:
            # Clean the prompt
            clean_prompt = " ".join(asset['prompt'].split())

            # Generate using AssetManager (which handles GCS upload)
            result = await asset_manager.generate_image(
                prompt=clean_prompt,
                model=ImageModels.FLUX_SCHNELL  # Fast turbo model
            )

            # The AssetManager puts it in images/, we want it in our pitch path
            # So we'll need to handle this

            asset_result = {
                "id": asset['id'],
                "name": asset['name'],
                "gcs_url": result['url'],
                "gcs_path": result['gcs_path'],
                "fal_request_id": result['id'],
                "model": result['model']
            }
            results.append(asset_result)

            print(f"    ✓ Generated: {result['url']}")
            print()

        except Exception as e:
            print(f"    ✗ Error: {e}")
            errors.append({"id": asset['id'], "error": str(e)})
            print()

    # Save manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "project": "law-com-pitch",
        "total_assets": len(results),
        "errors": len(errors),
        "assets": results,
        "failed": errors
    }

    manifest_path = Path(__file__).parent / "generated_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("=" * 60)
    print(f"COMPLETE: {len(results)} assets generated, {len(errors)} errors")
    print(f"Manifest saved to: {manifest_path}")
    print("=" * 60)

    # Print summary for documentation
    print("\n## Generated Asset URLs\n")
    for r in results:
        print(f"- **{r['name']}**: {r['gcs_url']}")

    return manifest


if __name__ == "__main__":
    asyncio.run(generate_all_assets())
