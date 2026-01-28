#!/bin/bash
# Deploy Sprite Runtime to Fly.io
#
# This script builds and deploys the sprite container image.
# Sprites are spawned on-demand via the Machines API, not `fly deploy`.
#
# Prerequisites:
# - flyctl installed and authenticated (fly auth login)
# - FLY_API_TOKEN set for machine spawning
#
# Usage:
#   ./deploy/deploy-sprites.sh

set -e

# Configuration
APP_NAME="${FLY_APP_NAME:-highera-sprites}"
REGION="${FLY_REGION:-iad}"
RUNTIME_DIR="agency/runtime"

echo "=========================================="
echo "Deploying Sprite Runtime to Fly.io"
echo "=========================================="
echo ""
echo "App: $APP_NAME"
echo "Region: $REGION"
echo ""

# Check prerequisites
if ! command -v fly &> /dev/null; then
    echo "Error: flyctl is not installed."
    echo "Install it with: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check authentication
if ! fly auth whoami &> /dev/null; then
    echo "Error: Not authenticated with Fly.io"
    echo "Run: fly auth login"
    exit 1
fi

# Check if app exists
if ! fly apps list | grep -q "$APP_NAME"; then
    echo "Creating Fly.io app: $APP_NAME"
    fly apps create "$APP_NAME" --org personal
fi

# Copy agent personas to runtime directory for build
echo "Copying agent personas..."
mkdir -p "$RUNTIME_DIR/agents"
cp agency/agents/*.md "$RUNTIME_DIR/agents/"

# Build and push the image
echo ""
echo "Building sprite image..."
cd "$RUNTIME_DIR"

# Deploy (builds and pushes image)
fly deploy \
    --app "$APP_NAME" \
    --region "$REGION" \
    --build-only \
    --push

echo ""
echo "=========================================="
echo "Sprite image deployed!"
echo "=========================================="
echo ""
echo "The sprite image is now available at:"
echo "  registry.fly.io/$APP_NAME:latest"
echo ""
echo "Sprites will be spawned on-demand by the coordinator."
echo ""
echo "To set up secrets for sprites:"
echo "  fly secrets set ANTHROPIC_API_KEY=sk-... --app $APP_NAME"
echo "  fly secrets set REDIS_URL=redis://... --app $APP_NAME"
echo "  fly secrets set COORDINATOR_URL=https://your-api.run.app --app $APP_NAME"
echo ""
echo "To view spawned machines:"
echo "  fly machines list --app $APP_NAME"
echo ""

# Clean up copied personas
rm -rf "$RUNTIME_DIR/agents"
