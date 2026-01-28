"""
Stripe Webhook Handler

Cloud Function that handles Stripe webhook events.
"""

import os
import json
import logging
from datetime import datetime

import stripe
from flask import Flask, request, jsonify
from google.cloud import firestore, secretmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
db = firestore.Client()


def get_webhook_secret():
    """Get Stripe webhook secret from Secret Manager."""
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if secret:
        return secret

    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.environ.get("GCP_PROJECT_ID")
        name = f"projects/{project_id}/secrets/stripe-webhook-secret/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to get webhook secret: {e}")
        return None


WEBHOOK_SECRET = get_webhook_secret()


@app.route("/", methods=["POST"])
def webhook():
    """Handle Stripe webhook events."""
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return jsonify({"error": "Invalid signature"}), 400

    event_type = event["type"]
    data = event["data"]["object"]

    logger.info(f"Received Stripe event: {event_type}")

    # Route to handler
    handlers = {
        "customer.subscription.created": handle_subscription_created,
        "customer.subscription.updated": handle_subscription_updated,
        "customer.subscription.deleted": handle_subscription_deleted,
        "invoice.paid": handle_invoice_paid,
        "invoice.payment_failed": handle_payment_failed,
        "invoice.finalized": handle_invoice_finalized,
        "customer.updated": handle_customer_updated,
        "payment_method.attached": handle_payment_method_attached,
    }

    handler = handlers.get(event_type)
    if handler:
        try:
            handler(data)
        except Exception as e:
            logger.error(f"Error handling {event_type}: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        logger.info(f"Unhandled event type: {event_type}")

    return jsonify({"status": "ok"}), 200


def handle_subscription_created(subscription):
    """Handle new subscription."""
    tenant_id = subscription["metadata"].get("tenant_id")
    if not tenant_id:
        logger.warning("Subscription created without tenant_id metadata")
        return

    plan = subscription["metadata"].get("plan", "starter")

    logger.info(f"Subscription created for tenant {tenant_id}: {plan}")

    db.collection("tenants").document(tenant_id).set({
        "billing": {
            "status": "active",
            "stripe_subscription_id": subscription["id"],
            "stripe_customer_id": subscription["customer"],
            "current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
            "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
            "plan_started_at": datetime.utcnow()
        },
        "plan": plan
    }, merge=True)


def handle_subscription_updated(subscription):
    """Handle subscription updates (plan changes, etc)."""
    tenant_id = subscription["metadata"].get("tenant_id")
    if not tenant_id:
        return

    plan = subscription["metadata"].get("plan")
    status = subscription["status"]

    logger.info(f"Subscription updated for tenant {tenant_id}: status={status}, plan={plan}")

    updates = {
        "billing.status": "active" if status == "active" else status,
        "billing.current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
        "billing.current_period_end": datetime.fromtimestamp(subscription["current_period_end"])
    }

    if plan:
        updates["plan"] = plan

    if subscription.get("cancel_at_period_end"):
        updates["billing.canceling"] = True
        updates["billing.cancel_at"] = datetime.fromtimestamp(subscription["cancel_at"])

    db.collection("tenants").document(tenant_id).update(updates)


def handle_subscription_deleted(subscription):
    """Handle subscription cancellation."""
    tenant_id = subscription["metadata"].get("tenant_id")
    if not tenant_id:
        return

    logger.info(f"Subscription cancelled for tenant {tenant_id}")

    db.collection("tenants").document(tenant_id).update({
        "billing.status": "cancelled",
        "billing.cancelled_at": datetime.utcnow(),
        "plan": "free"  # Downgrade to free tier
    })


def handle_invoice_paid(invoice):
    """Handle successful payment."""
    customer_id = invoice["customer"]
    tenant_id = get_tenant_by_customer(customer_id)

    if not tenant_id:
        return

    logger.info(f"Invoice paid for tenant {tenant_id}: ${invoice['amount_paid']/100:.2f}")

    db.collection("tenants").document(tenant_id).update({
        "billing.status": "active",
        "billing.last_payment_at": datetime.utcnow(),
        "billing.last_payment_amount": invoice["amount_paid"],
        "billing.payment_failed_at": firestore.DELETE_FIELD
    })

    # Record invoice
    db.collection("tenants").document(tenant_id).collection("invoices").document(invoice["id"]).set({
        "invoice_id": invoice["id"],
        "number": invoice["number"],
        "amount_paid": invoice["amount_paid"],
        "currency": invoice["currency"],
        "status": "paid",
        "paid_at": datetime.utcnow(),
        "pdf_url": invoice.get("invoice_pdf"),
        "hosted_url": invoice.get("hosted_invoice_url")
    })


def handle_payment_failed(invoice):
    """Handle failed payment."""
    customer_id = invoice["customer"]
    tenant_id = get_tenant_by_customer(customer_id)

    if not tenant_id:
        return

    logger.warning(f"Payment failed for tenant {tenant_id}")

    attempt_count = invoice.get("attempt_count", 1)

    # First failure: mark as past_due
    if attempt_count <= 1:
        db.collection("tenants").document(tenant_id).update({
            "billing.status": "past_due",
            "billing.payment_failed_at": datetime.utcnow(),
            "billing.payment_failure_count": 1
        })

    # Multiple failures: consider suspension
    elif attempt_count >= 3:
        db.collection("tenants").document(tenant_id).update({
            "billing.status": "suspended",
            "billing.suspended_at": datetime.utcnow(),
            "billing.payment_failure_count": attempt_count
        })

    # Send notification
    db.collection("tenants").document(tenant_id).collection("notifications").add({
        "type": "payment_failed",
        "attempt_count": attempt_count,
        "amount": invoice["amount_due"],
        "timestamp": datetime.utcnow(),
        "read": False
    })


def handle_invoice_finalized(invoice):
    """Handle invoice finalization (ready to be paid)."""
    customer_id = invoice["customer"]
    tenant_id = get_tenant_by_customer(customer_id)

    if not tenant_id:
        return

    logger.info(f"Invoice finalized for tenant {tenant_id}: ${invoice['amount_due']/100:.2f}")


def handle_customer_updated(customer):
    """Handle customer updates."""
    tenant_id = customer["metadata"].get("tenant_id")
    if not tenant_id:
        return

    db.collection("tenants").document(tenant_id).update({
        "billing.email": customer["email"],
        "billing.name": customer.get("name")
    })


def handle_payment_method_attached(payment_method):
    """Handle new payment method attached."""
    customer_id = payment_method["customer"]
    tenant_id = get_tenant_by_customer(customer_id)

    if not tenant_id:
        return

    logger.info(f"Payment method attached for tenant {tenant_id}")

    # If tenant was suspended due to payment failure, check if we should reactivate
    tenant = db.collection("tenants").document(tenant_id).get().to_dict()
    if tenant.get("billing", {}).get("status") == "suspended":
        # Retry the failed invoice
        # stripe.Invoice.pay(invoice_id)
        pass


def get_tenant_by_customer(customer_id: str) -> str:
    """Look up tenant by Stripe customer ID."""
    tenants = db.collection("tenants").where(
        "billing.stripe_customer_id", "==", customer_id
    ).limit(1).get()

    for tenant in tenants:
        return tenant.id

    return None


# Cloud Function entry point
def stripe_webhook(request):
    """Cloud Function entry point."""
    with app.test_request_context(
        path=request.path,
        method=request.method,
        headers=dict(request.headers),
        data=request.get_data()
    ):
        return app.full_dispatch_request()
