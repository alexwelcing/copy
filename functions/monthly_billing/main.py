"""
Monthly Billing

Cloud Function triggered by Cloud Scheduler on the 1st of each month.
Calculates usage, reports overage to Stripe, and resets counters.
"""

import os
import logging
from datetime import datetime, timedelta

import stripe
from google.cloud import bigquery, firestore, secretmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
bq = bigquery.Client()
db = firestore.Client()

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# Plan configuration
PLANS = {
    "starter": {
        "tokens_included": 1_000_000,
        "overage_enabled": False
    },
    "growth": {
        "tokens_included": 10_000_000,
        "overage_enabled": True,
        "overage_price_per_million": 800  # cents
    },
    "enterprise": {
        "tokens_included": 100_000_000,
        "overage_enabled": True,
        "overage_price_per_million": 500  # cents
    }
}


def init_stripe():
    """Initialize Stripe API."""
    api_key = os.environ.get("STRIPE_SECRET_KEY")

    if not api_key:
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{PROJECT_ID}/secrets/stripe-secret-key/versions/latest"
            response = client.access_secret_version(request={"name": name})
            api_key = response.payload.data.decode("UTF-8")
        except Exception as e:
            logger.error(f"Failed to get Stripe key: {e}")
            return False

    stripe.api_key = api_key
    return True


def run_monthly_billing(request):
    """
    Run monthly billing for all tenants.

    Triggered by Cloud Scheduler on the 1st of each month.
    """
    logger.info("Starting monthly billing run")

    if not init_stripe():
        return "Stripe not configured", 500

    # Get last month's date range
    today = datetime.utcnow()
    first_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (first_of_month - timedelta(days=1)).replace(day=1)
    last_month_end = first_of_month - timedelta(seconds=1)

    logger.info(f"Billing period: {last_month_start} to {last_month_end}")

    # Get usage from BigQuery
    usage_by_tenant = get_monthly_usage(last_month_start, last_month_end)

    # Process each tenant
    processed = 0
    errors = 0

    for tenant_id, usage in usage_by_tenant.items():
        try:
            process_tenant_billing(tenant_id, usage)
            processed += 1
        except Exception as e:
            logger.error(f"Error processing tenant {tenant_id}: {e}")
            errors += 1

    # Reset all tenant counters
    reset_all_counters()

    logger.info(f"Monthly billing complete: {processed} processed, {errors} errors")

    return {
        "status": "complete",
        "processed": processed,
        "errors": errors,
        "period_start": last_month_start.isoformat(),
        "period_end": last_month_end.isoformat()
    }


def get_monthly_usage(start: datetime, end: datetime) -> dict:
    """Get usage by tenant from BigQuery."""
    query = f"""
    SELECT
        tenant_id,
        SUM(tokens) as total_tokens,
        COUNT(*) as total_events,
        COUNT(DISTINCT sprite_id) as unique_sprites,
        COUNT(DISTINCT DATE(timestamp)) as active_days
    FROM `{PROJECT_ID}.billing.usage_events`
    WHERE timestamp >= @start_time
      AND timestamp <= @end_time
    GROUP BY tenant_id
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start),
            bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", end)
        ]
    )

    results = bq.query(query, job_config=job_config).result()

    usage = {}
    for row in results:
        usage[row.tenant_id] = {
            "tokens": row.total_tokens or 0,
            "events": row.total_events or 0,
            "sprites": row.unique_sprites or 0,
            "active_days": row.active_days or 0
        }

    return usage


def process_tenant_billing(tenant_id: str, usage: dict):
    """Process billing for a single tenant."""
    logger.info(f"Processing billing for tenant {tenant_id}")

    # Get tenant data
    tenant_ref = db.collection("tenants").document(tenant_id)
    tenant = tenant_ref.get().to_dict()

    if not tenant:
        logger.warning(f"Tenant not found: {tenant_id}")
        return

    plan = tenant.get("plan", "starter")
    billing = tenant.get("billing", {})
    subscription_id = billing.get("stripe_subscription_id")

    if not subscription_id:
        logger.info(f"Tenant {tenant_id} has no subscription, skipping")
        return

    plan_config = PLANS.get(plan, PLANS["starter"])
    tokens_used = usage.get("tokens", 0)
    tokens_included = plan_config["tokens_included"]

    # Calculate overage
    overage_tokens = max(0, tokens_used - tokens_included)

    logger.info(
        f"Tenant {tenant_id}: {tokens_used:,} tokens used, "
        f"{tokens_included:,} included, {overage_tokens:,} overage"
    )

    # Report overage to Stripe if applicable
    if overage_tokens > 0 and plan_config.get("overage_enabled"):
        report_overage_to_stripe(subscription_id, overage_tokens, plan_config)

    # Record billing summary
    tenant_ref.collection("billing_history").add({
        "period_start": datetime.utcnow().replace(day=1) - timedelta(days=1),
        "period_end": datetime.utcnow().replace(day=1) - timedelta(seconds=1),
        "plan": plan,
        "tokens_used": tokens_used,
        "tokens_included": tokens_included,
        "overage_tokens": overage_tokens,
        "sprites_spawned": usage.get("sprites", 0),
        "active_days": usage.get("active_days", 0),
        "processed_at": datetime.utcnow()
    })


def report_overage_to_stripe(subscription_id: str, overage_tokens: int, plan_config: dict):
    """Report overage usage to Stripe for metered billing."""
    try:
        # Get subscription to find metered item
        subscription = stripe.Subscription.retrieve(subscription_id)

        metered_item_id = None
        for item in subscription["items"]["data"]:
            price = item.get("price", {})
            recurring = price.get("recurring", {})
            if recurring.get("usage_type") == "metered":
                metered_item_id = item["id"]
                break

        if not metered_item_id:
            logger.warning(f"No metered item found for subscription {subscription_id}")
            return

        # Calculate overage in cents
        # overage_tokens / 1M * price_per_million
        overage_millions = overage_tokens / 1_000_000
        overage_cents = int(overage_millions * plan_config["overage_price_per_million"])

        if overage_cents > 0:
            stripe.SubscriptionItem.create_usage_record(
                metered_item_id,
                quantity=overage_cents,
                action="set"
            )

            logger.info(
                f"Reported overage to Stripe: {overage_tokens:,} tokens = ${overage_cents/100:.2f}"
            )

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error reporting overage: {e}")
        raise


def reset_all_counters():
    """Reset usage counters for all tenants."""
    logger.info("Resetting usage counters for all tenants")

    # Get all tenants
    tenants = db.collection("tenants").stream()

    batch = db.batch()
    count = 0

    for tenant in tenants:
        batch.update(tenant.reference, {
            "usage.tokens_this_period": 0,
            "usage.sprites_spawned_this_period": 0,
            "usage.api_calls_this_period": 0,
            "usage.period_reset_at": datetime.utcnow(),
            "limits.tokens_exceeded": firestore.DELETE_FIELD,
            "limits.sprites_exceeded": firestore.DELETE_FIELD
        })
        count += 1

        # Commit in batches of 500
        if count % 500 == 0:
            batch.commit()
            batch = db.batch()

    # Commit remaining
    if count % 500 != 0:
        batch.commit()

    logger.info(f"Reset counters for {count} tenants")


# For local testing
if __name__ == "__main__":
    from flask import Flask, request as flask_request
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def handler():
        return run_monthly_billing(flask_request)

    app.run(host="0.0.0.0", port=8080, debug=True)
