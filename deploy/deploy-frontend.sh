#!/bin/bash
# Deploy Marketing Agency Frontend to Google Cloud Run

set -euo pipefail

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="marketing-agency-frontend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
API_URL="${API_URL:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    if [ -z "$PROJECT_ID" ]; then
        error "GCP_PROJECT_ID environment variable is required"
    fi

    if [ -z "$API_URL" ]; then
        warn "API_URL not set. Attempting to get from deployed API service..."
        API_URL=$(gcloud run services describe marketing-agency-api \
            --project="$PROJECT_ID" \
            --region="$REGION" \
            --format="value(status.url)" 2>/dev/null || echo "")

        if [ -z "$API_URL" ]; then
            error "API_URL is required. Deploy the API first or set API_URL environment variable."
        fi
        log "Using API URL: $API_URL"
    fi

    log "Prerequisites OK"
}

# Build and push
build_and_push() {
    log "Building frontend container..."

    REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

    gcloud builds submit "$REPO_ROOT/frontend" \
        --project="$PROJECT_ID" \
        --tag="$IMAGE_NAME:latest" \
        --timeout=600s

    log "Image built: $IMAGE_NAME:latest"
}

# Deploy
deploy() {
    log "Deploying frontend to Cloud Run..."

    gcloud run deploy "$SERVICE_NAME" \
        --project="$PROJECT_ID" \
        --region="$REGION" \
        --image="$IMAGE_NAME:latest" \
        --platform=managed \
        --allow-unauthenticated \
        --memory=512Mi \
        --cpu=1 \
        --timeout=60 \
        --concurrency=100 \
        --min-instances=0 \
        --max-instances=5 \
        --set-env-vars="VITE_API_URL=$API_URL,ORIGIN=https://${SERVICE_NAME}-*.run.app"

    log "Deployment complete!"
}

# Get URLs
get_urls() {
    FRONTEND_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --project="$PROJECT_ID" \
        --region="$REGION" \
        --format="value(status.url)")

    log "Frontend URL: $FRONTEND_URL"
    log "API URL: $API_URL"
    echo ""
    echo "Open in browser: $FRONTEND_URL"
}

# Main
main() {
    log "Deploying Marketing Agency Frontend"
    check_prerequisites
    build_and_push
    deploy
    get_urls
    log "Done!"
}

main "$@"
