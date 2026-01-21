#!/bin/bash
# Deploy Marketing Agency API to Google Cloud Run

set -euo pipefail

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="marketing-agency-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    if [ -z "$PROJECT_ID" ]; then
        error "GCP_PROJECT_ID environment variable is required"
    fi

    if ! command -v gcloud &> /dev/null; then
        error "gcloud CLI is not installed"
    fi

    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
    fi

    # Check if authenticated
    if ! gcloud auth print-access-token &> /dev/null; then
        error "Not authenticated with gcloud. Run: gcloud auth login"
    fi

    log "Prerequisites OK"
}

# Create secret for API key if it doesn't exist
setup_secrets() {
    log "Setting up secrets..."

    if ! gcloud secrets describe anthropic-api-key --project="$PROJECT_ID" &> /dev/null; then
        log "Creating anthropic-api-key secret..."
        if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
            error "ANTHROPIC_API_KEY environment variable required for first-time setup"
        fi
        echo -n "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key \
            --project="$PROJECT_ID" \
            --replication-policy="automatic" \
            --data-file=-
    else
        log "Secret anthropic-api-key already exists"
    fi
}

# Build and push container
build_and_push() {
    log "Building container image..."

    # Get the repo root (one level up from deploy/)
    REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

    # Build with Cloud Build (faster, no local Docker needed)
    if [ "${USE_CLOUD_BUILD:-true}" = "true" ]; then
        log "Using Cloud Build..."
        gcloud builds submit "$REPO_ROOT" \
            --project="$PROJECT_ID" \
            --tag="$IMAGE_NAME:latest" \
            --timeout=600s
    else
        # Local build and push
        log "Building locally..."
        docker build -t "$IMAGE_NAME:latest" "$REPO_ROOT"

        log "Pushing to Container Registry..."
        docker push "$IMAGE_NAME:latest"
    fi

    log "Image built and pushed: $IMAGE_NAME:latest"
}

# Deploy to Cloud Run
deploy() {
    log "Deploying to Cloud Run..."

    gcloud run deploy "$SERVICE_NAME" \
        --project="$PROJECT_ID" \
        --region="$REGION" \
        --image="$IMAGE_NAME:latest" \
        --platform=managed \
        --allow-unauthenticated \
        --memory=2Gi \
        --cpu=2 \
        --timeout=300 \
        --concurrency=80 \
        --min-instances=0 \
        --max-instances=10 \
        --set-env-vars="CLAUDE_MODEL=claude-sonnet-4-20250514" \
        --set-secrets="ANTHROPIC_API_KEY=anthropic-api-key:latest"

    log "Deployment complete!"
}

# Get service URL
get_url() {
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --project="$PROJECT_ID" \
        --region="$REGION" \
        --format="value(status.url)")

    log "Service URL: $SERVICE_URL"
    echo ""
    echo "Test with:"
    echo "  curl $SERVICE_URL/health"
    echo ""
    echo "Execute a skill:"
    echo "  curl -X POST $SERVICE_URL/work \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"skill\": \"copywriting\", \"task\": \"Write a headline for a project management tool\"}'"
}

# Main
main() {
    log "Starting deployment of Marketing Agency API"
    log "Project: $PROJECT_ID"
    log "Region: $REGION"
    echo ""

    check_prerequisites
    setup_secrets
    build_and_push
    deploy
    get_url

    log "Done!"
}

# Run
main "$@"
