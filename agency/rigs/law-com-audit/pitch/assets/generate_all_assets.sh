#!/bin/bash
#
# HIGH ERA AGENCY - PITCH ASSET GENERATOR
# Law.com Strategic Transformation
#
# Run this script locally with your Fal API key to generate all presentation assets.
#
# Usage:
#   chmod +x generate_all_assets.sh
#   ./generate_all_assets.sh
#
# Prerequisites:
#   - curl
#   - jq (for JSON parsing)
#   - FAL_KEY environment variable set
#

set -e

# Configuration
FAL_KEY="${FAL_KEY:-af087bda-e123-4614-a945-02d6c8277a19:cd9aaf828cd2cd1cfc92b98ecaf4e550}"
MODEL="fal-ai/flux/schnell"
OUTPUT_DIR="./generated_assets"
MANIFEST_FILE="$OUTPUT_DIR/manifest.json"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Style base for all prompts
STYLE="premium executive presentation, dark navy #0A1628 background, golden amber #C9A227 accents, sophisticated McKinsey meets Bloomberg consulting aesthetic, photorealistic, extremely clean minimal"

echo "============================================================"
echo "HIGH ERA AGENCY - PITCH ASSET GENERATION"
echo "Law.com Strategic Transformation"
echo "============================================================"
echo ""
echo "Model: $MODEL"
echo "Output: $OUTPUT_DIR"
echo ""

# Function to generate an asset
generate_asset() {
    local id=$1
    local prompt=$2
    local filename="$OUTPUT_DIR/${id}.png"

    echo "[$id] Generating..."

    # Submit to Fal queue
    response=$(curl -s -X POST "https://queue.fal.run/$MODEL" \
        -H "Authorization: Key $FAL_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"prompt\":\"$prompt, $STYLE\",\"image_size\":\"landscape_16_9\",\"num_images\":1}")

    # Check for request_id (async) or direct result
    if echo "$response" | jq -e '.request_id' > /dev/null 2>&1; then
        request_id=$(echo "$response" | jq -r '.request_id')
        echo "    Request ID: $request_id"

        # Poll for result
        while true; do
            result=$(curl -s "https://queue.fal.run/$MODEL/requests/$request_id/status" \
                -H "Authorization: Key $FAL_KEY")

            status=$(echo "$result" | jq -r '.status // "UNKNOWN"')

            if [ "$status" = "COMPLETED" ]; then
                # Get the result
                result=$(curl -s "https://queue.fal.run/$MODEL/requests/$request_id" \
                    -H "Authorization: Key $FAL_KEY")
                break
            elif [ "$status" = "FAILED" ]; then
                echo "    ✗ Failed"
                return 1
            fi

            sleep 2
        done
    else
        result="$response"
    fi

    # Extract image URL
    image_url=$(echo "$result" | jq -r '.images[0].url // .image.url // empty')

    if [ -n "$image_url" ]; then
        # Download image
        curl -s -o "$filename" "$image_url"
        echo "    ✓ Saved: $filename"
        echo "    URL: $image_url"

        # Add to manifest
        echo "{\"id\":\"$id\",\"url\":\"$image_url\",\"local\":\"$filename\"}" >> "$OUTPUT_DIR/assets.jsonl"
    else
        echo "    ✗ No image URL in response"
        echo "$result" | jq . 2>/dev/null || echo "$result"
        return 1
    fi
}

# Clear previous manifest
rm -f "$OUTPUT_DIR/assets.jsonl"

echo "Generating 14 pitch deck assets..."
echo ""

# Generate all assets
generate_asset "cover" \
    "Abstract premium executive presentation background for legal intelligence company, deep navy blue gradient with elegant gold accent lines suggesting data streams and intelligence networks flowing diagonally, minimalist geometric patterns, corporate luxury"

generate_asset "timeline" \
    "Abstract visualization of converging timelines representing critical business inflection point, five thin golden lines converging from edges toward bright central focal point, elegant data visualization suggesting urgency and pivotal moment"

generate_asset "market_gap" \
    "Minimalist bar chart abstract visualization showing dramatic competitive gap, two vertical bars one dramatically tall golden amber one much shorter muted gray showing 3:1 ratio, clean geometric data viz"

generate_asset "funnel" \
    "Dramatic visualization of business conversion funnel with leaks, wide golden opening at top tapering severely to narrow bottom, golden light particles escaping through fractures, lost revenue visualization"

generate_asset "pillars" \
    "Three elegant golden pillar trophy icons arranged horizontally, premium minimalist 3D rendering, each with subtle glow, representing exclusive valuable business assets"

generate_asset "positioning" \
    "Strategic quadrant positioning visualization, subtle grid with four quadrants, elegant golden curved arrow moving from bottom-left commodity to top-right premium, repositioning journey"

generate_asset "strategy" \
    "Three classical Greek columns supporting triangular pediment structure, rendered in elegant golden tones, architectural visualization suggesting strategic strength and foundation"

generate_asset "moat" \
    "Abstract geometric visualization of fortress with protective moat, golden wireframe castle structure surrounded by flowing defensive barrier, competitive defense"

generate_asset "transformation" \
    "Split-screen business transformation visualization, left half chaotic scattered geometric fragments suggesting disorder, right half organized elegant dashboard with clean aligned elements, before after contrast"

generate_asset "roi" \
    "Dramatic exponential growth arrow visualization for investment return, golden arrow starting small at bottom left expanding and curving upward to large impressive finish at top right"

generate_asset "risk" \
    "Descending trend line visualization with warning markers, line starting high on left declining steeply to right, three amber red warning indicator points along decline, urgency"

generate_asset "divider_strategy" \
    "Minimalist premium section divider background, deep navy with single elegant gold geometric accent off-center, extremely clean with large negative space for text overlay"

generate_asset "hero_intel" \
    "Abstract visualization of legal intelligence platform concept, network of connected nodes suggesting data insights and knowledge, central glowing hub radiating golden connections outward"

generate_asset "hero_bench" \
    "Abstract visualization of benchmarking and competitive rankings, elegant tiered podium or ranking visualization with golden accents, market leadership and positioning"

echo ""
echo "============================================================"

# Create final manifest
echo "{" > "$MANIFEST_FILE"
echo "  \"generated_at\": \"$(date -Iseconds)\"," >> "$MANIFEST_FILE"
echo "  \"model\": \"$MODEL\"," >> "$MANIFEST_FILE"
echo "  \"project\": \"law-com-pitch\"," >> "$MANIFEST_FILE"
echo "  \"assets\": [" >> "$MANIFEST_FILE"

# Convert JSONL to array
first=true
while read -r line; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> "$MANIFEST_FILE"
    fi
    echo -n "    $line" >> "$MANIFEST_FILE"
done < "$OUTPUT_DIR/assets.jsonl"

echo "" >> "$MANIFEST_FILE"
echo "  ]" >> "$MANIFEST_FILE"
echo "}" >> "$MANIFEST_FILE"

rm -f "$OUTPUT_DIR/assets.jsonl"

echo "COMPLETE!"
echo "Manifest: $MANIFEST_FILE"
echo "Assets: $OUTPUT_DIR/*.png"
echo "============================================================"
