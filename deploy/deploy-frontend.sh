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

# Fetch Firebase Config
get_firebase_config() {
    log "Fetching Firebase configuration..."
    
    # Check if vars are already set in environment
    if [ -n "${VITE_FIREBASE_API_KEY:-}" ]; then
        log "Using Firebase config from environment variables"
        _API_KEY="$VITE_FIREBASE_API_KEY"
        _AUTH_DOMAIN="$VITE_FIREBASE_AUTH_DOMAIN"
        _PROJECT_ID="$VITE_FIREBASE_PROJECT_ID"
        _STORAGE_BUCKET="$VITE_FIREBASE_STORAGE_BUCKET"
        _SENDER_ID="$VITE_FIREBASE_MESSAGING_SENDER_ID"
        _APP_ID="$VITE_FIREBASE_APP_ID"
        return
    fi

    # Try to fetch from Firebase CLI
    if command -v firebase &> /dev/null; then
        log "Using Firebase CLI to fetch config..."
        # We need the App ID. Try to list or assume one exists.
        # This is tricky without interactivity.
        # We'll try to find the 'web' app config.
        
        CONFIG_JSON=$(firebase apps:sdkconfig web --project "$PROJECT_ID" --json 2>/dev/null || echo "")
        
        if [ -n "$CONFIG_JSON" ] && [ "$CONFIG_JSON" != "null" ]; then
             _API_KEY=$(echo "$CONFIG_JSON" | grep -o '"apiKey": "[^"]*"' | cut -d'"' -f4)
             _AUTH_DOMAIN=$(echo "$CONFIG_JSON" | grep -o '"authDomain": "[^"]*"' | cut -d'"' -f4)
             _PROJECT_ID=$(echo "$CONFIG_JSON" | grep -o '"projectId": "[^"]*"' | cut -d'"' -f4)
             _STORAGE_BUCKET=$(echo "$CONFIG_JSON" | grep -o '"storageBucket": "[^"]*"' | cut -d'"' -f4)
             _SENDER_ID=$(echo "$CONFIG_JSON" | grep -o '"messagingSenderId": "[^"]*"' | cut -d'"' -f4)
             _APP_ID=$(echo "$CONFIG_JSON" | grep -o '"appId": "[^"]*"' | cut -d'"' -f4)
             
             if [ -n "$_API_KEY" ]; then
                 log "Firebase config fetched successfully."
                 return
             fi
        fi
    fi
    
    error "Could not determine Firebase configuration. Set VITE_FIREBASE_* environment variables."
}

# Build and push
build_and_push() {
    get_firebase_config

    log "Building frontend container..."

    REPO_ROOT="$(cd "$(dirname "$0")"/.. && pwd)"

    gcloud builds submit "$REPO_ROOT/frontend" \
        --project="$PROJECT_ID" \
        --config="$REPO_ROOT/frontend/cloudbuild.yaml" \
        --substitutions="_IMAGE_NAME=$IMAGE_NAME,_API_KEY=$_API_KEY,_AUTH_DOMAIN=$_AUTH_DOMAIN,_PROJECT_ID=$_PROJECT_ID,_STORAGE_BUCKET=$_STORAGE_BUCKET,_SENDER_ID=$_SENDER_ID,_APP_ID=$_APP_ID" \
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
        --timeout=300 \
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