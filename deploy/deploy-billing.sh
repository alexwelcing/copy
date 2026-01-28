#!/bin/bash
# Deploy Billing Infrastructure
#
# Sets up:
# - Pub/Sub topic for usage events
# - BigQuery dataset and tables
# - Cloud Functions for event processing
# - Cloud Scheduler for monthly billing
# - Secret Manager secrets
#
# Prerequisites:
# - gcloud CLI authenticated
# - GCP project configured
# - Stripe account with API keys
#
# Usage:
#   ./deploy/deploy-billing.sh

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project)}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_ACCOUNT="${SERVICE_ACCOUNT:-billing@$PROJECT_ID.iam.gserviceaccount.com}"

echo "=========================================="
echo "Deploying Billing Infrastructure"
echo "=========================================="
echo ""
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# ============================================================================
# 1. Enable required APIs
# ============================================================================
echo "Enabling required APIs..."
gcloud services enable \
    pubsub.googleapis.com \
    bigquery.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudscheduler.googleapis.com \
    secretmanager.googleapis.com \
    --project="$PROJECT_ID"

# ============================================================================
# 2. Create Pub/Sub topic
# ============================================================================
echo ""
echo "Creating Pub/Sub topic..."
if ! gcloud pubsub topics describe usage-events --project="$PROJECT_ID" &>/dev/null; then
    gcloud pubsub topics create usage-events --project="$PROJECT_ID"
    echo "Created topic: usage-events"
else
    echo "Topic already exists: usage-events"
fi

# ============================================================================
# 3. Create BigQuery dataset and tables
# ============================================================================
echo ""
echo "Creating BigQuery dataset..."
if ! bq show --dataset "$PROJECT_ID:billing" &>/dev/null; then
    bq mk --dataset \
        --description "Billing and usage data" \
        --location=US \
        "$PROJECT_ID:billing"
    echo "Created dataset: billing"
else
    echo "Dataset already exists: billing"
fi

echo "Creating BigQuery tables..."
bq query --use_legacy_sql=false --project_id="$PROJECT_ID" <<'EOF'
CREATE TABLE IF NOT EXISTS billing.usage_events (
    event_id STRING,
    event_type STRING,
    tenant_id STRING,
    timestamp TIMESTAMP,
    tokens INT64,
    model STRING,
    sprite_id STRING,
    work_id STRING,
    project_id STRING,
    user_id STRING,
    raw_data STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY tenant_id, event_type;
EOF
echo "Created table: usage_events"

# ============================================================================
# 4. Create service account for billing
# ============================================================================
echo ""
echo "Creating service account..."
if ! gcloud iam service-accounts describe "$SERVICE_ACCOUNT" --project="$PROJECT_ID" &>/dev/null; then
    gcloud iam service-accounts create billing \
        --display-name="Billing Service Account" \
        --project="$PROJECT_ID"
fi

# Grant required permissions
echo "Granting permissions..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/datastore.user" \
    --condition=None

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/bigquery.dataEditor" \
    --condition=None

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor" \
    --condition=None

# ============================================================================
# 5. Set up secrets
# ============================================================================
echo ""
echo "Setting up secrets..."
echo "(You'll need to add the actual values manually)"

# Create secrets if they don't exist
for secret in stripe-secret-key stripe-webhook-secret; do
    if ! gcloud secrets describe "$secret" --project="$PROJECT_ID" &>/dev/null; then
        echo "placeholder" | gcloud secrets create "$secret" \
            --data-file=- \
            --project="$PROJECT_ID"
        echo "Created secret: $secret (placeholder - update with real value)"
    else
        echo "Secret already exists: $secret"
    fi
done

echo ""
echo "To set secret values:"
echo "  echo 'sk_live_...' | gcloud secrets versions add stripe-secret-key --data-file=-"
echo "  echo 'whsec_...' | gcloud secrets versions add stripe-webhook-secret --data-file=-"

# ============================================================================
# 6. Deploy Cloud Functions
# ============================================================================
echo ""
echo "Deploying Cloud Functions..."

# Usage processor
echo "Deploying process-usage function..."
gcloud functions deploy process-usage \
    --gen2 \
    --runtime=python312 \
    --region="$REGION" \
    --source=functions/process_usage \
    --entry-point=process_usage \
    --trigger-topic=usage-events \
    --service-account="$SERVICE_ACCOUNT" \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
    --memory=256MB \
    --timeout=60s \
    --project="$PROJECT_ID"

# Stripe webhook
echo "Deploying stripe-webhook function..."
gcloud functions deploy stripe-webhook \
    --gen2 \
    --runtime=python312 \
    --region="$REGION" \
    --source=functions/stripe_webhook \
    --entry-point=stripe_webhook \
    --trigger-http \
    --allow-unauthenticated \
    --service-account="$SERVICE_ACCOUNT" \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
    --memory=256MB \
    --timeout=60s \
    --project="$PROJECT_ID"

WEBHOOK_URL=$(gcloud functions describe stripe-webhook --region="$REGION" --format='value(url)' --project="$PROJECT_ID")
echo ""
echo "Stripe webhook URL: $WEBHOOK_URL"
echo "Configure this URL in your Stripe Dashboard under Developers > Webhooks"

# Monthly billing
echo "Deploying monthly-billing function..."
gcloud functions deploy monthly-billing \
    --gen2 \
    --runtime=python312 \
    --region="$REGION" \
    --source=functions/monthly_billing \
    --entry-point=run_monthly_billing \
    --trigger-http \
    --service-account="$SERVICE_ACCOUNT" \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
    --memory=512MB \
    --timeout=540s \
    --project="$PROJECT_ID"

# ============================================================================
# 7. Create Cloud Scheduler job
# ============================================================================
echo ""
echo "Creating Cloud Scheduler job..."

BILLING_URL=$(gcloud functions describe monthly-billing --region="$REGION" --format='value(url)' --project="$PROJECT_ID")

if ! gcloud scheduler jobs describe monthly-billing --location="$REGION" --project="$PROJECT_ID" &>/dev/null; then
    gcloud scheduler jobs create http monthly-billing \
        --location="$REGION" \
        --schedule="0 0 1 * *" \
        --uri="$BILLING_URL" \
        --http-method=POST \
        --oidc-service-account-email="$SERVICE_ACCOUNT" \
        --project="$PROJECT_ID"
    echo "Created scheduler job: monthly-billing (runs 1st of each month at midnight UTC)"
else
    echo "Scheduler job already exists: monthly-billing"
fi

# ============================================================================
# Done
# ============================================================================
echo ""
echo "=========================================="
echo "Billing Infrastructure Deployed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Update Stripe secrets with real values:"
echo "   gcloud secrets versions add stripe-secret-key --data-file=- <<< 'sk_live_...'"
echo "   gcloud secrets versions add stripe-webhook-secret --data-file=- <<< 'whsec_...'"
echo ""
echo "2. Configure Stripe webhook in Dashboard:"
echo "   URL: $WEBHOOK_URL"
echo "   Events: customer.subscription.*, invoice.*, payment_method.attached"
echo ""
echo "3. Create Stripe products and prices:"
echo "   - Starter: \$49/month base + metered overage"
echo "   - Growth: \$199/month base + metered overage"
echo "   - Enterprise: \$999/month base + metered overage"
echo ""
echo "4. Update STRIPE_PRICE_* environment variables in Cloud Run service"
echo ""
echo "5. Test the webhook with Stripe CLI:"
echo "   stripe listen --forward-to $WEBHOOK_URL"
echo ""
