# Billing & Enforcement Architecture

Multi-tenant billing system using GCP services + Stripe.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BILLING FLOW                                 │
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Sprite  │───►│  Pub/Sub │───►│ Cloud Fn │───►│ BigQuery │      │
│  │ (usage)  │    │ (events) │    │ (process)│    │ (store)  │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│                                                        │            │
│                                        ┌───────────────┘            │
│                                        ▼                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Stripe  │◄───│ Cloud Fn │◄───│ Scheduler│◄───│ Firestore│      │
│  │ (charge) │    │ (invoice)│    │ (monthly)│    │ (summary)│      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │                                                             │
│       ▼                                                             │
│  ┌──────────┐    ┌──────────┐                                      │
│  │ Webhook  │───►│ Firestore│  (update tenant status)              │
│  │ (events) │    │ (tenant) │                                      │
│  └──────────┘    └──────────┘                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## GCP Services Used

| Service | Purpose |
|---------|---------|
| **Pub/Sub** | Usage event ingestion |
| **Cloud Functions** | Event processing, Stripe webhooks |
| **BigQuery** | Usage storage and analytics |
| **Cloud Scheduler** | Monthly billing cycles |
| **Firestore** | Tenant state, real-time limits |
| **Secret Manager** | Stripe API keys |

## 1. Usage Tracking

### Events to Track

```python
# Usage event schema
{
    "event_type": "token_usage",  # or sprite_spawn, sprite_time, storage
    "tenant_id": "tenant_abc",
    "timestamp": "2024-01-15T14:30:00Z",
    "data": {
        "tokens": 1500,
        "model": "claude-sonnet-4-20250514",
        "sprite_id": "sprite_xyz",
        "work_id": "work_123"
    }
}
```

### Pub/Sub Topic Setup

```bash
# Create usage events topic
gcloud pubsub topics create usage-events

# Create subscription for Cloud Function
gcloud pubsub subscriptions create usage-processor \
    --topic=usage-events \
    --push-endpoint=https://REGION-PROJECT.cloudfunctions.net/process-usage
```

### Publishing Usage Events

```python
# In sprite runtime or coordinator
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, "usage-events")

def track_usage(tenant_id: str, event_type: str, data: dict):
    event = {
        "event_type": event_type,
        "tenant_id": tenant_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    publisher.publish(topic_path, json.dumps(event).encode())
```

## 2. Usage Processing (Cloud Function)

```python
# functions/process_usage/main.py

import json
import base64
from google.cloud import bigquery
from google.cloud import firestore

bq = bigquery.Client()
db = firestore.Client()

def process_usage(event, context):
    """Process usage event from Pub/Sub."""

    # Decode event
    data = json.loads(base64.b64decode(event['data']).decode())

    # 1. Write to BigQuery for analytics
    table_id = f"{PROJECT_ID}.billing.usage_events"
    bq.insert_rows_json(table_id, [data])

    # 2. Update real-time counters in Firestore
    tenant_ref = db.collection("tenants").document(data["tenant_id"])

    if data["event_type"] == "token_usage":
        tenant_ref.update({
            "usage.tokens_this_period": firestore.Increment(data["data"]["tokens"]),
            "usage.last_updated": firestore.SERVER_TIMESTAMP
        })

    elif data["event_type"] == "sprite_spawn":
        tenant_ref.update({
            "usage.sprites_spawned_this_period": firestore.Increment(1)
        })

    # 3. Check if approaching/exceeding limits
    tenant = tenant_ref.get().to_dict()
    check_limits(data["tenant_id"], tenant)

def check_limits(tenant_id: str, tenant: dict):
    """Check if tenant is approaching or exceeding limits."""
    usage = tenant.get("usage", {})
    plan = tenant.get("plan", "starter")

    limits = get_plan_limits(plan)
    tokens_used = usage.get("tokens_this_period", 0)

    # 80% warning
    if tokens_used >= limits["tokens"] * 0.8:
        send_usage_warning(tenant_id, tokens_used, limits["tokens"])

    # 100% - enforce limit
    if tokens_used >= limits["tokens"]:
        enforce_limit(tenant_id)

def get_plan_limits(plan: str) -> dict:
    return {
        "starter": {"tokens": 1_000_000, "sprites": 100},
        "growth": {"tokens": 10_000_000, "sprites": 500},
        "enterprise": {"tokens": 100_000_000, "sprites": 2000}
    }.get(plan, {"tokens": 1_000_000, "sprites": 100})
```

## 3. BigQuery Schema

```sql
-- Create dataset
CREATE SCHEMA IF NOT EXISTS billing;

-- Usage events table
CREATE TABLE IF NOT EXISTS billing.usage_events (
    event_id STRING,
    event_type STRING,
    tenant_id STRING,
    timestamp TIMESTAMP,
    tokens INT64,
    model STRING,
    sprite_id STRING,
    work_id STRING,

    -- Partitioning for cost optimization
    _PARTITIONTIME TIMESTAMP
)
PARTITION BY DATE(timestamp)
CLUSTER BY tenant_id, event_type;

-- Monthly aggregates (materialized view)
CREATE MATERIALIZED VIEW billing.monthly_usage AS
SELECT
    tenant_id,
    DATE_TRUNC(timestamp, MONTH) as billing_month,
    SUM(tokens) as total_tokens,
    COUNT(DISTINCT sprite_id) as unique_sprites,
    COUNT(*) as total_events
FROM billing.usage_events
GROUP BY tenant_id, billing_month;
```

## 4. Stripe Integration

### Setup

```bash
# Store Stripe keys in Secret Manager
gcloud secrets create stripe-secret-key \
    --data-file=- <<< "sk_live_..."

gcloud secrets create stripe-webhook-secret \
    --data-file=- <<< "whsec_..."
```

### Tenant Subscription Model

```python
# service/billing/stripe_client.py

import stripe
from google.cloud import secretmanager

def get_stripe_key():
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/stripe-secret-key/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode()

stripe.api_key = get_stripe_key()

# Plan configuration
STRIPE_PLANS = {
    "starter": {
        "price_id": "price_starter_monthly",
        "tokens_included": 1_000_000,
        "overage_price_per_1m": 10.00  # $10 per 1M tokens over
    },
    "growth": {
        "price_id": "price_growth_monthly",
        "tokens_included": 10_000_000,
        "overage_price_per_1m": 8.00
    },
    "enterprise": {
        "price_id": "price_enterprise_monthly",
        "tokens_included": 100_000_000,
        "overage_price_per_1m": 5.00
    }
}

def create_customer(tenant_id: str, email: str, name: str) -> str:
    """Create Stripe customer for tenant."""
    customer = stripe.Customer.create(
        email=email,
        name=name,
        metadata={"tenant_id": tenant_id}
    )
    return customer.id

def create_subscription(customer_id: str, plan: str) -> str:
    """Create subscription for a plan."""
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": STRIPE_PLANS[plan]["price_id"]}],
        metadata={"plan": plan}
    )
    return subscription.id

def report_usage(subscription_id: str, tokens_used: int):
    """Report metered usage to Stripe."""
    # Find the metered price item
    subscription = stripe.Subscription.retrieve(subscription_id)

    for item in subscription["items"]["data"]:
        if item["price"]["recurring"]["usage_type"] == "metered":
            stripe.SubscriptionItem.create_usage_record(
                item["id"],
                quantity=tokens_used,
                timestamp=int(time.time()),
                action="increment"
            )
```

### Stripe Webhook Handler

```python
# functions/stripe_webhook/main.py

import stripe
from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400

    # Handle events
    if event["type"] == "customer.subscription.created":
        handle_subscription_created(event["data"]["object"])

    elif event["type"] == "customer.subscription.updated":
        handle_subscription_updated(event["data"]["object"])

    elif event["type"] == "customer.subscription.deleted":
        handle_subscription_deleted(event["data"]["object"])

    elif event["type"] == "invoice.paid":
        handle_invoice_paid(event["data"]["object"])

    elif event["type"] == "invoice.payment_failed":
        handle_payment_failed(event["data"]["object"])

    return "OK", 200

def handle_subscription_created(subscription):
    tenant_id = subscription["metadata"]["tenant_id"]
    plan = subscription["metadata"]["plan"]

    db.collection("tenants").document(tenant_id).update({
        "billing.status": "active",
        "billing.stripe_subscription_id": subscription["id"],
        "billing.stripe_customer_id": subscription["customer"],
        "plan": plan,
        "billing.current_period_start": subscription["current_period_start"],
        "billing.current_period_end": subscription["current_period_end"]
    })

def handle_payment_failed(invoice):
    customer_id = invoice["customer"]

    # Find tenant by customer ID
    tenants = db.collection("tenants").where(
        "billing.stripe_customer_id", "==", customer_id
    ).get()

    for tenant in tenants:
        tenant.reference.update({
            "billing.status": "past_due",
            "billing.payment_failed_at": firestore.SERVER_TIMESTAMP
        })

        # Optionally: disable sprites after grace period
        # schedule_enforcement(tenant.id, grace_hours=72)
```

## 5. Monthly Billing Cycle

### Cloud Scheduler Job

```bash
# Run on 1st of each month at midnight UTC
gcloud scheduler jobs create http monthly-billing \
    --schedule="0 0 1 * *" \
    --uri="https://REGION-PROJECT.cloudfunctions.net/run-monthly-billing" \
    --http-method=POST \
    --oidc-service-account-email=billing@PROJECT.iam.gserviceaccount.com
```

### Monthly Billing Function

```python
# functions/monthly_billing/main.py

from google.cloud import bigquery, firestore
import stripe

bq = bigquery.Client()
db = firestore.Client()

def run_monthly_billing(request):
    """Generate invoices for all tenants."""

    # Get last month's usage from BigQuery
    query = """
    SELECT
        tenant_id,
        SUM(tokens) as total_tokens,
        COUNT(DISTINCT sprite_id) as sprites_used
    FROM billing.usage_events
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 MONTH)
    GROUP BY tenant_id
    """

    results = bq.query(query).result()

    for row in results:
        process_tenant_billing(row.tenant_id, row.total_tokens)

    return "OK", 200

def process_tenant_billing(tenant_id: str, tokens_used: int):
    """Process billing for a single tenant."""

    tenant = db.collection("tenants").document(tenant_id).get().to_dict()
    plan = tenant.get("plan", "starter")
    plan_config = STRIPE_PLANS[plan]

    # Calculate overage
    tokens_included = plan_config["tokens_included"]
    overage_tokens = max(0, tokens_used - tokens_included)

    if overage_tokens > 0:
        # Report overage to Stripe (metered billing)
        subscription_id = tenant["billing"]["stripe_subscription_id"]

        # Convert to billing units (per 1M tokens)
        overage_units = overage_tokens / 1_000_000

        stripe.SubscriptionItem.create_usage_record(
            get_metered_item_id(subscription_id),
            quantity=int(overage_units * 100),  # cents
            action="set"
        )

    # Reset usage counters
    db.collection("tenants").document(tenant_id).update({
        "usage.tokens_this_period": 0,
        "usage.sprites_spawned_this_period": 0,
        "usage.period_reset_at": firestore.SERVER_TIMESTAMP
    })
```

## 6. Enforcement

### Real-time Limit Checking

```python
# service/billing/enforcement.py

from google.cloud import firestore
from functools import wraps
from fastapi import HTTPException

db = firestore.Client()

class BillingEnforcement:
    """Enforce billing limits in real-time."""

    @staticmethod
    async def check_can_spawn_sprite(tenant_id: str) -> bool:
        """Check if tenant can spawn another sprite."""
        tenant = db.collection("tenants").document(tenant_id).get().to_dict()

        # Check billing status
        if tenant.get("billing", {}).get("status") == "suspended":
            raise HTTPException(402, "Account suspended. Please update payment method.")

        # Check sprite limit
        plan = tenant.get("plan", "starter")
        limits = get_plan_limits(plan)

        active_sprites = await get_active_sprite_count(tenant_id)
        if active_sprites >= limits["max_concurrent_sprites"]:
            raise HTTPException(429, f"Sprite limit reached ({limits['max_concurrent_sprites']})")

        return True

    @staticmethod
    async def check_can_use_tokens(tenant_id: str, estimated_tokens: int) -> bool:
        """Check if tenant has token budget remaining."""
        tenant = db.collection("tenants").document(tenant_id).get().to_dict()

        # Check billing status
        billing_status = tenant.get("billing", {}).get("status", "active")
        if billing_status == "suspended":
            raise HTTPException(402, "Account suspended")

        # For metered billing, always allow (will be charged)
        # For capped plans, check limit
        plan = tenant.get("plan", "starter")
        if plan == "starter":  # Starter has hard cap
            usage = tenant.get("usage", {})
            tokens_used = usage.get("tokens_this_period", 0)
            limit = 1_000_000

            if tokens_used + estimated_tokens > limit:
                raise HTTPException(
                    429,
                    f"Token limit exceeded. Used: {tokens_used:,}, Limit: {limit:,}"
                )

        return True

def require_billing_active(func):
    """Decorator to enforce billing status."""
    @wraps(func)
    async def wrapper(*args, tenant_id: str, **kwargs):
        tenant = db.collection("tenants").document(tenant_id).get().to_dict()

        status = tenant.get("billing", {}).get("status", "active")

        if status == "suspended":
            raise HTTPException(402, "Account suspended. Please update payment.")

        if status == "past_due":
            # Allow with warning, or restrict based on policy
            pass

        return await func(*args, tenant_id=tenant_id, **kwargs)

    return wrapper
```

### Integrate with Coordinator

```python
# In agency/swarm/coordinator.py

from service.billing.enforcement import BillingEnforcement

class SwarmCoordinator:

    async def spawn_sprite(self, tenant_id: str, agent_type: AgentType, ...):
        # Check billing before spawning
        await BillingEnforcement.check_can_spawn_sprite(tenant_id)

        # ... existing spawn logic ...

    async def submit_work(self, tenant_id: str, task: dict, ...):
        # Estimate token usage (rough: 4 chars = 1 token)
        estimated = len(str(task)) // 4 + 2000  # buffer for response

        await BillingEnforcement.check_can_use_tokens(tenant_id, estimated)

        # ... existing work logic ...
```

## 7. Firestore Schema for Billing

```
tenants/{tenant_id}
├── plan: "growth"
├── billing:
│   ├── status: "active"  # active | past_due | suspended | cancelled
│   ├── stripe_customer_id: "cus_xxx"
│   ├── stripe_subscription_id: "sub_xxx"
│   ├── current_period_start: timestamp
│   ├── current_period_end: timestamp
│   ├── payment_failed_at: null
│   └── suspended_at: null
├── usage:
│   ├── tokens_this_period: 5432100
│   ├── sprites_spawned_this_period: 42
│   ├── last_updated: timestamp
│   └── period_reset_at: timestamp
└── limits:  # Cached from plan, can be overridden
    ├── max_concurrent_sprites: 4
    ├── tokens_per_period: 10000000
    └── overage_enabled: true
```

## 8. Deployment Checklist

### Infrastructure Setup

```bash
# 1. Create Pub/Sub topic
gcloud pubsub topics create usage-events

# 2. Create BigQuery dataset
bq mk --dataset billing

# 3. Create Cloud Scheduler job
gcloud scheduler jobs create http monthly-billing \
    --schedule="0 0 1 * *" \
    --uri="https://..." \
    --http-method=POST

# 4. Store Stripe secrets
gcloud secrets create stripe-secret-key --data-file=-
gcloud secrets create stripe-webhook-secret --data-file=-

# 5. Deploy Cloud Functions
gcloud functions deploy process-usage \
    --runtime=python312 \
    --trigger-topic=usage-events

gcloud functions deploy stripe-webhook \
    --runtime=python312 \
    --trigger-http \
    --allow-unauthenticated

gcloud functions deploy monthly-billing \
    --runtime=python312 \
    --trigger-http
```

### Stripe Setup

1. Create products and prices in Stripe Dashboard
2. Set up metered billing for token overage
3. Configure webhook endpoint
4. Test with Stripe CLI: `stripe listen --forward-to localhost:8080/webhook`

## 9. Monitoring & Alerts

```bash
# Alert on payment failures
gcloud monitoring policies create \
    --display-name="Payment Failed" \
    --condition="..." \
    --notification-channels="..."

# Alert on high usage (80% of limit)
gcloud monitoring policies create \
    --display-name="Usage Warning" \
    --condition="..."
```

## Summary

| Component | GCP Service | Purpose |
|-----------|-------------|---------|
| Event ingestion | Pub/Sub | Collect usage events |
| Event processing | Cloud Functions | Process, aggregate, enforce |
| Usage storage | BigQuery | Analytics, monthly rollups |
| Real-time state | Firestore | Limits, status, counters |
| Secrets | Secret Manager | Stripe keys |
| Scheduling | Cloud Scheduler | Monthly billing cycle |
| Payments | Stripe | Subscriptions, invoices |
