"""
Usage Event Processor

Cloud Function that processes usage events from Pub/Sub.
Writes to BigQuery for analytics and checks limits.
"""

import os
import json
import base64
import logging
from datetime import datetime

from google.cloud import bigquery, firestore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
bq = bigquery.Client()
db = firestore.Client()

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATASET_ID = "billing"
TABLE_ID = "usage_events"


def process_usage(event, context):
    """
    Process usage event from Pub/Sub.

    Triggered by messages on the usage-events topic.
    """
    try:
        # Decode message
        data = json.loads(base64.b64decode(event['data']).decode('utf-8'))

        logger.info(f"Processing usage event: {data['event_type']} for {data['tenant_id']}")

        # 1. Write to BigQuery
        write_to_bigquery(data)

        # 2. Check limits and send alerts if needed
        check_limits(data)

        return "OK"

    except Exception as e:
        logger.error(f"Error processing usage event: {e}")
        raise


def write_to_bigquery(event: dict):
    """Write usage event to BigQuery."""
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    row = {
        "event_id": f"{event['tenant_id']}-{event['timestamp']}",
        "event_type": event["event_type"],
        "tenant_id": event["tenant_id"],
        "timestamp": event["timestamp"],
        "tokens": event.get("data", {}).get("tokens", 0),
        "model": event.get("data", {}).get("model"),
        "sprite_id": event.get("sprite_id"),
        "work_id": event.get("work_id"),
        "project_id": event.get("project_id"),
        "user_id": event.get("user_id"),
        "raw_data": json.dumps(event.get("data", {}))
    }

    errors = bq.insert_rows_json(table_ref, [row])

    if errors:
        logger.error(f"BigQuery insert errors: {errors}")
    else:
        logger.debug(f"Wrote event to BigQuery: {row['event_id']}")


def check_limits(event: dict):
    """Check if tenant is approaching or exceeding limits."""
    tenant_id = event["tenant_id"]
    event_type = event["event_type"]

    # Get tenant data
    tenant_ref = db.collection("tenants").document(tenant_id)
    tenant = tenant_ref.get().to_dict()

    if not tenant:
        logger.warning(f"Tenant not found: {tenant_id}")
        return

    plan = tenant.get("plan", "starter")
    usage = tenant.get("usage", {})
    limits = get_plan_limits(plan)

    # Check token limits
    if event_type == "token_usage":
        tokens_used = usage.get("tokens_this_period", 0)
        token_limit = limits["tokens"]

        percentage = tokens_used / token_limit * 100

        if percentage >= 100:
            handle_limit_exceeded(tenant_id, "tokens", tokens_used, token_limit)
        elif percentage >= 80:
            send_usage_warning(tenant_id, "tokens", percentage)

    # Check sprite limits
    elif event_type == "sprite_spawn":
        sprites_spawned = usage.get("sprites_spawned_this_period", 0)
        sprite_limit = limits["sprites"]

        if sprites_spawned >= sprite_limit:
            handle_limit_exceeded(tenant_id, "sprites", sprites_spawned, sprite_limit)
        elif sprites_spawned >= sprite_limit * 0.8:
            send_usage_warning(tenant_id, "sprites", sprites_spawned / sprite_limit * 100)


def get_plan_limits(plan: str) -> dict:
    """Get limits for a plan."""
    return {
        "starter": {"tokens": 1_000_000, "sprites": 100},
        "growth": {"tokens": 10_000_000, "sprites": 500},
        "enterprise": {"tokens": 100_000_000, "sprites": 2000}
    }.get(plan, {"tokens": 1_000_000, "sprites": 100})


def send_usage_warning(tenant_id: str, resource: str, percentage: float):
    """Send usage warning notification."""
    logger.warning(f"Tenant {tenant_id} at {percentage:.0f}% of {resource} limit")

    # Record warning in Firestore
    db.collection("tenants").document(tenant_id).collection("notifications").add({
        "type": "usage_warning",
        "resource": resource,
        "percentage": percentage,
        "timestamp": datetime.utcnow(),
        "read": False
    })

    # TODO: Send email notification
    # send_email(tenant_id, "usage_warning", {"resource": resource, "percentage": percentage})


def handle_limit_exceeded(tenant_id: str, resource: str, used: int, limit: int):
    """Handle limit exceeded."""
    logger.warning(f"Tenant {tenant_id} exceeded {resource} limit: {used:,} / {limit:,}")

    tenant_ref = db.collection("tenants").document(tenant_id)
    tenant = tenant_ref.get().to_dict()

    plan = tenant.get("plan", "starter")

    # Starter plan has hard caps
    if plan == "starter":
        logger.info(f"Enforcing hard cap for starter tenant {tenant_id}")
        tenant_ref.update({
            f"limits.{resource}_exceeded": True,
            f"limits.{resource}_exceeded_at": datetime.utcnow()
        })

    # Growth/Enterprise can go over (metered billing)
    else:
        logger.info(f"Tenant {tenant_id} in overage for {resource}")

    # Record notification
    db.collection("tenants").document(tenant_id).collection("notifications").add({
        "type": "limit_exceeded",
        "resource": resource,
        "used": used,
        "limit": limit,
        "timestamp": datetime.utcnow(),
        "read": False
    })
