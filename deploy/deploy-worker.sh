#!/bin/bash
# Deploy Marketing Agency Worker to Google Cloud Run

set -euo pipefail

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="marketing-agency-worker"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Prerequisites check
if [ -z "$PROJECT_ID" ]; then
    echo "GCP_PROJECT_ID environment variable is required"
    exit 1
fi

log "Building worker image..."
# Build with Cloud Build
gcloud builds submit . \
    --project="$PROJECT_ID" \
    --tag="$IMAGE_NAME:latest" \
    --timeout=600s

log "Deploying worker to Cloud Run..."
# Worker is a background job, but we'll run it as a service with min instances 1 for now
# or ideally as a Cloud Run Job. For simplicity/consistency in this phase, let's use a Service 
# that just runs the loop. Cloud Run Jobs is better for discrete tasks, but our worker
# listens to Pub/Sub continuously.
# Better pattern: Use Eventarc to trigger Cloud Run on Pub/Sub message.
# HOWEVER, our architecture chose "Pull Subscription" (worker.py).
# So we need a persistent container. Cloud Run "always on" (min-instances 1) is the way.

gcloud run deploy "$SERVICE_NAME" \
    --project="$PROJECT_ID" \
    --region="$REGION" \
    --image="$IMAGE_NAME:latest" \
    --command="python3" \
    --args="service/worker.py" \
    --no-allow-unauthenticated \
    --min-instances=1 \
    --max-instances=5 \
    --memory=2Gi \
    --cpu=2 \
    --set-env-vars="CLAUDE_MODEL=claude-sonnet-4-20250514,GCP_PROJECT_ID=${PROJECT_ID}" \
    --set-secrets="ANTHROPIC_API_KEY=anthropic-api-key:latest"

log "Worker deployment complete!"
