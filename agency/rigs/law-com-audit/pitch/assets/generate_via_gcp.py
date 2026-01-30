#!/usr/bin/env python3
"""
HIGH ERA AGENCY - Generate Pitch Assets via GCP

Uses the deployed Cloud Function to generate images.
Images are stored directly in GCS, no local files needed.

Usage:
    # Set the Cloud Function URL (after deployment)
    export IMAGE_FUNCTION_URL='https://generate-image-xxxxx.run.app'

    # Generate all assets
    python generate_via_gcp.py

    # Preview mode (one asset)
    python generate_via_gcp.py --preview
"""

import os
import sys
import json
from datetime import datetime

# Add service to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../"))

from service.core.image_gen import ImageGenerationService, ImageRequest


# Configuration
TENANT_ID = "law-com-audit"
MODEL = "flux-pro-1.1"

# Premium prompts (same as generate_premium.py)
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
        """,
        "size": "landscape_16_9"
    },
    "inflection": {
        "slide": 2,
        "prompt": """
            Abstract visualization of convergence.
            Five distinct streams of cool light converging toward a single point.
            Navy background fading to deep charcoal.
            Each stream a different subtle shade of blue and silver.
            The convergence point glows with warm golden light.
            Suggests multiple forces creating a moment of opportunity.
            Minimal, elegant, no obvious metaphors.
            Studio lighting quality, dramatic but restrained.
        """,
        "size": "landscape_16_9"
    },
    "dominance": {
        "slide": 3,
        "prompt": """
            Abstract data visualization suggesting market disparity.
            Three geometric forms on dark field - one dramatically larger.
            Cool silver-blue tones for the smaller forms.
            Warm gold for the dominant form.
            Suggests 3x relationship through proportion alone.
            No numbers, no charts, pure visual weight.
            Negative space is the primary design element.
            Matte surfaces, soft shadows, premium consulting aesthetic.
        """,
        "size": "landscape_16_9"
    },
    "leaking_value": {
        "slide": 4,
        "prompt": """
            Abstract representation of value escaping.
            Geometric container with luminous contents.
            Golden particles drifting out through gaps.
            Navy blue background, deep shadows.
            Suggests leakage without being literal.
            The escaped particles fade into darkness.
            Contemplative, slightly melancholic but elegant.
            Fine art photography aesthetic.
        """,
        "size": "landscape_16_9"
    },
    "three_assets": {
        "slide": 5,
        "prompt": """
            Three precious objects floating in void.
            Each distinct but harmonious - crystal, metal, light.
            Warm golden illumination from within.
            Navy-black background with subtle gradient.
            Suggests rare, irreplaceable assets.
            Museum lighting quality.
            No obvious symbols - abstract representations of value.
            Sharp focus, shallow depth of field between objects.
        """,
        "size": "landscape_16_9"
    },
    "repositioning": {
        "slide": 6,
        "prompt": """
            Abstract journey visualization.
            Single golden thread traveling across dark field.
            Origin point diffuse and cool.
            Destination point focused and warm.
            The path shows transformation through color shift.
            Navy to deep purple to golden amber.
            Suggests strategic movement with purpose.
            Elegant typography-worthy negative space.
        """,
        "size": "landscape_16_9"
    },
    "foundation": {
        "slide": 7,
        "prompt": """
            Three pillars of light emerging from darkness.
            Each pillar distinct yet connected at base.
            Golden light rising from navy shadows.
            Architectural precision, geometric purity.
            Suggests foundation, structure, support.
            The light is substantial, almost solid.
            Deep shadows create dramatic depth.
            Classical proportion, modern execution.
        """,
        "size": "landscape_16_9"
    },
    "fortress": {
        "slide": 10,
        "prompt": """
            Abstract defensive structure.
            Concentric geometric forms suggesting protection.
            Golden core surrounded by layers of cool blue.
            Navy background, forms emerge from shadow.
            Suggests moat, barrier, competitive defense.
            No literal castle or wall imagery.
            Pure geometric abstraction with protective feeling.
            Impenetrable but elegant, strength through design.
        """,
        "size": "landscape_16_9"
    },
    "transformation": {
        "slide": 11,
        "prompt": """
            Split composition showing metamorphosis.
            Left side: cool, fragmented, scattered light.
            Right side: warm, unified, coherent glow.
            The boundary between them is the story.
            Navy background consistent throughout.
            Suggests before/after through pure visual language.
            No obvious split screen effect - organic transition.
            The transformation feels inevitable, natural.
        """,
        "size": "landscape_16_9"
    },
    "growth": {
        "slide": 17,
        "prompt": """
            Abstract growth trajectory.
            Organic curve of golden light ascending.
            Starting from lower left, reaching upper right.
            Navy background with subtle atmospheric depth.
            The curve accelerates as it rises.
            Suggests compounding, exponential potential.
            Not a chart - a feeling of upward momentum.
            Elegant, restrained, premium investment aesthetic.
        """,
        "size": "landscape_16_9"
    },
    "decline": {
        "slide": 18,
        "prompt": """
            Abstract trajectory of entropy.
            Form dissolving from coherent to scattered.
            Cool silver-blue tones losing their structure.
            Navy-black background, deepening shadows.
            Movement from upper left to lower right.
            Suggests decay, missed opportunity, risk.
            Not alarming - contemplative, inevitable.
            The beauty in dissolution, but clearly cautionary.
        """,
        "size": "landscape_16_9"
    },
    "section_break": {
        "slide": 0,
        "prompt": """
            Minimal section divider.
            Single horizontal line of golden light.
            Centered in navy void.
            The line has slight atmospheric glow.
            Suggests pause, transition, breathing room.
            Extremely minimal - negative space dominant.
            The light is a whisper, not a shout.
            Elegant enough to use repeatedly without fatigue.
        """,
        "size": "landscape_16_9"
    },
    "intelligence": {
        "slide": 0,
        "prompt": """
            Abstract representation of intelligence.
            Network of interconnected golden nodes.
            Lines trace data pathways between them.
            Navy background with depth and atmosphere.
            Suggests insight, connection, understanding.
            Not a literal brain or circuit board.
            Organic complexity, geometric precision.
            The whole is clearly more than the parts.
        """,
        "size": "landscape_16_9"
    },
    "rankings": {
        "slide": 0,
        "prompt": """
            Abstract hierarchy visualization.
            Vertical arrangement of luminous forms.
            Top position glows brightest, warmest gold.
            Descending forms cooler, less intense.
            Navy background with dramatic depth.
            Suggests ranking, comparison, benchmark.
            Not a literal podium or bar chart.
            Pure visual hierarchy through light and color.
        """,
        "size": "landscape_16_9"
    },
}


def main():
    # Check for function URL
    function_url = os.environ.get("IMAGE_FUNCTION_URL")
    if not function_url:
        print("=" * 70)
        print("ERROR: IMAGE_FUNCTION_URL not set")
        print("=" * 70)
        print()
        print("Deploy the Cloud Function first:")
        print("  cd deploy && ./deploy-image-function.sh")
        print()
        print("Then set the URL:")
        print("  export IMAGE_FUNCTION_URL='https://...'")
        print()
        sys.exit(1)

    # Check for preview mode
    preview_mode = "--preview" in sys.argv

    print("=" * 70)
    print("HIGH ERA AGENCY")
    print("Executive Pitch Asset Generation (via GCP)")
    print("Law.com Strategic Transformation")
    print("=" * 70)
    print()
    print(f"Function: {function_url}")
    print(f"Tenant:   {TENANT_ID}")
    print(f"Model:    {MODEL}")

    if preview_mode:
        assets_to_generate = {"cover": ASSETS["cover"]}
        print(f"Mode:     PREVIEW (1 asset)")
    else:
        assets_to_generate = ASSETS
        print(f"Assets:   {len(ASSETS)}")

    print()

    # Create service
    service = ImageGenerationService(function_url=function_url)

    # Build requests
    requests = []
    asset_ids = []
    for asset_id, spec in assets_to_generate.items():
        request = ImageRequest(
            prompt=spec["prompt"].strip(),
            output_path=f"pitch/{asset_id}.png",
            model=MODEL,
            size=spec.get("size", "landscape_16_9"),
            tenant_id=TENANT_ID
        )
        requests.append(request)
        asset_ids.append(asset_id)

    # Generate in parallel (3 at a time to be nice)
    print(f"Generating {len(requests)} assets...")
    print()

    results = service.generate_batch(requests, max_workers=3)

    # Report results
    success_count = 0
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "model": MODEL,
        "tenant_id": TENANT_ID,
        "assets": {}
    }

    for asset_id, result in zip(asset_ids, results):
        spec = assets_to_generate[asset_id]
        if result.success:
            print(f"  [OK] {asset_id}")
            print(f"       {result.gcs_url}")
            success_count += 1
            manifest["assets"][asset_id] = {
                "slide": spec["slide"],
                "url": result.gcs_url,
                "path": result.gcs_path,
                "seed": result.seed
            }
        else:
            print(f"  [FAIL] {asset_id}")
            print(f"         {result.error}")
            manifest["assets"][asset_id] = {
                "slide": spec["slide"],
                "error": result.error
            }
        print()

    # Summary
    print("=" * 70)
    print(f"COMPLETE: {success_count}/{len(requests)} assets generated")
    print("=" * 70)

    if preview_mode and success_count == 1:
        print("\nPreview successful! Run without --preview for all assets.")
    elif success_count == len(requests):
        print("\nAll assets ready. URLs point directly to GCS.")
        print("Use these in the pitch deck.")
    else:
        print("\nSome assets failed - check errors above.")

    # Save manifest
    manifest_path = "generated_manifest_gcp.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest: {manifest_path}")


if __name__ == "__main__":
    main()
