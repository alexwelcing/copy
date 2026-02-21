#!/bin/bash
#
# Deploy Image Generation Cloud Function
#
# Prerequisites:
#   - gcloud CLI configured with project
#   - FAL API key stored in Secret Manager as 'fal-api-key'
#
# Usage:
#   ./deploy-image-function.sh [project-id]
#

set -e

PROJECT_ID=${1:-$(gcloud config get-value project)}
REGION="us-central1"
BUCKET_NAME="marketing-copy-assets"
SERVICE_ACCOUNT="marketing-agency-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "============================================"
echo "Deploying Image Generation Function"
echo "============================================"
echo "Project: ${PROJECT_ID}"
echo "Region:  ${REGION}"
echo "Bucket:  ${BUCKET_NAME}"
echo ""

# Check if FAL API key secret exists
echo "Checking for fal-api-key secret..."
if ! gcloud secrets describe fal-api-key --project="${PROJECT_ID}" &>/dev/null; then
    echo ""
    echo "Secret 'fal-api-key' not found."
    echo "Create it with:"
    echo "  echo -n 'your-fal-api-key' | gcloud secrets create fal-api-key --data-file=- --project=${PROJECT_ID}"
    echo ""
    read -p "Enter your Fal API key to create it now (or Ctrl+C to cancel): " FAL_KEY
    echo -n "${FAL_KEY}" | gcloud secrets create fal-api-key \
        --data-file=- \
        --project="${PROJECT_ID}"
    echo "Secret created."
fi

# Grant service account access to secret
echo "Granting secret access to service account..."
gcloud secrets add-iam-policy-binding fal-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor" \
    --project="${PROJECT_ID}" \
    --quiet

# Grant storage admin for GCS uploads
echo "Granting storage access..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/storage.objectAdmin" \
    --quiet

# Create Pub/Sub topic for async generation (if not exists)
echo "Creating Pub/Sub topic..."
gcloud pubsub topics create image-generation-queue \
    --project="${PROJECT_ID}" 2>/dev/null || true

# Deploy HTTP function
echo ""
echo "Deploying HTTP function..."
gcloud functions deploy generate-image \
    --gen2 \
    --runtime=python312 \
    --region="${REGION}" \
    --source=functions/generate_image \
    --entry-point=generate_image_http \
    --trigger-http \
    --allow-unauthenticated \
    --memory=512MB \
    --timeout=540s \
    --service-account="${SERVICE_ACCOUNT}" \
    --set-env-vars="GCP_PROJECT=${PROJECT_ID},GCS_BUCKET=${BUCKET_NAME}" \
    --project="${PROJECT_ID}"

# Deploy Pub/Sub function (for async batch generation)
echo ""
echo "Deploying Pub/Sub function..."
gcloud functions deploy generate-image-async \
    --gen2 \
    --runtime=python312 \
    --region="${REGION}" \
    --source=functions/generate_image \
    --entry-point=generate_image_pubsub \
    --trigger-topic=image-generation-queue \
    --memory=512MB \
    --timeout=540s \
    --service-account="${SERVICE_ACCOUNT}" \
    --set-env-vars="GCP_PROJECT=${PROJECT_ID},GCS_BUCKET=${BUCKET_NAME}" \
    --project="${PROJECT_ID}"

# Get function URL
FUNCTION_URL=$(gcloud functions describe generate-image \
    --gen2 \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format='value(serviceConfig.uri)')

echo ""
echo "============================================"
echo "Deployment Complete"
echo "============================================"
echo ""
echo "HTTP Endpoint:"
echo "  ${FUNCTION_URL}"
echo ""
echo "Usage:"
echo "  curl -X POST ${FUNCTION_URL} \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{"
echo "      \"prompt\": \"Abstract golden light on navy background\","
echo "      \"model\": \"flux-pro-1.1\","
echo "      \"size\": \"landscape_16_9\","
echo "      \"output_path\": \"pitch/cover.png\","
echo "      \"tenant_id\": \"law-com-audit\""
echo "    }'"
echo ""
echo "Async (Pub/Sub):"
echo "  gcloud pubsub topics publish image-generation-queue \\"
echo "    --message='{\"prompt\": \"...\", \"output_path\": \"...\"}'"
echo ""
