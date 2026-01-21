#!/bin/bash
# Deploy full Marketing Agency stack to Google Cloud Run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "Marketing Agency - Full Stack Deployment"
echo "========================================"
echo ""

# Deploy API first
echo "Step 1: Deploying API..."
"$SCRIPT_DIR/deploy.sh"
echo ""

# Get API URL
export API_URL=$(gcloud run services describe marketing-agency-api \
    --project="$GCP_PROJECT_ID" \
    --region="${GCP_REGION:-us-central1}" \
    --format="value(status.url)")

echo "API deployed at: $API_URL"
echo ""

# Deploy frontend
echo "Step 2: Deploying Frontend..."
"$SCRIPT_DIR/deploy-frontend.sh"
echo ""

echo "========================================"
echo "Deployment Complete!"
echo "========================================"
