"""
Stripe Client

Handles subscription management, invoicing, and payment processing.
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass

import stripe
from google.cloud import secretmanager

logger = logging.getLogger(__name__)


# Plan configuration
PLANS = {
    "starter": {
        "name": "Starter",
        "stripe_price_id": os.environ.get("STRIPE_PRICE_STARTER", "price_starter_monthly"),
        "tokens_included": 1_000_000,
        "max_concurrent_sprites": 2,
        "monthly_price_cents": 4900,  # $49
        "overage_per_million_cents": 1000,  # $10 per 1M tokens
    },
    "growth": {
        "name": "Growth",
        "stripe_price_id": os.environ.get("STRIPE_PRICE_GROWTH", "price_growth_monthly"),
        "tokens_included": 10_000_000,
        "max_concurrent_sprites": 4,
        "monthly_price_cents": 19900,  # $199
        "overage_per_million_cents": 800,  # $8 per 1M tokens
    },
    "enterprise": {
        "name": "Enterprise",
        "stripe_price_id": os.environ.get("STRIPE_PRICE_ENTERPRISE", "price_enterprise_monthly"),
        "tokens_included": 100_000_000,
        "max_concurrent_sprites": 10,
        "monthly_price_cents": 99900,  # $999
        "overage_per_million_cents": 500,  # $5 per 1M tokens
    }
}


@dataclass
class Customer:
    """Stripe customer data."""
    id: str
    email: str
    name: str
    tenant_id: str


@dataclass
class Subscription:
    """Stripe subscription data."""
    id: str
    customer_id: str
    plan: str
    status: str
    current_period_start: datetime
    current_period_end: datetime


class StripeClient:
    """
    Stripe integration for billing.

    Handles:
    - Customer creation
    - Subscription management
    - Usage-based billing (metered)
    - Invoicing
    """

    def __init__(self):
        self._init_stripe()

    def _init_stripe(self):
        """Initialize Stripe with API key from Secret Manager."""
        api_key = os.environ.get("STRIPE_SECRET_KEY")

        if not api_key:
            try:
                api_key = self._get_secret("stripe-secret-key")
            except Exception as e:
                logger.warning(f"Could not load Stripe key from Secret Manager: {e}")
                api_key = os.environ.get("STRIPE_SECRET_KEY_FALLBACK")

        if api_key:
            stripe.api_key = api_key
        else:
            logger.warning("Stripe API key not configured - billing disabled")

    def _get_secret(self, secret_id: str) -> str:
        """Get secret from Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.environ.get("GCP_PROJECT_ID")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    # =========================================================================
    # Customer Management
    # =========================================================================

    def create_customer(
        self,
        tenant_id: str,
        email: str,
        name: str,
        metadata: Optional[Dict] = None
    ) -> Customer:
        """Create a Stripe customer for a tenant."""
        customer_metadata = {
            "tenant_id": tenant_id,
            **(metadata or {})
        }

        customer = stripe.Customer.create(
            email=email,
            name=name,
            metadata=customer_metadata
        )

        logger.info(f"Created Stripe customer {customer.id} for tenant {tenant_id}")

        return Customer(
            id=customer.id,
            email=email,
            name=name,
            tenant_id=tenant_id
        )

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return Customer(
                id=customer.id,
                email=customer.email,
                name=customer.name,
                tenant_id=customer.metadata.get("tenant_id")
            )
        except stripe.error.InvalidRequestError:
            return None

    def update_customer(
        self,
        customer_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None
    ):
        """Update customer details."""
        updates = {}
        if email:
            updates["email"] = email
        if name:
            updates["name"] = name

        if updates:
            stripe.Customer.modify(customer_id, **updates)

    # =========================================================================
    # Subscription Management
    # =========================================================================

    def create_subscription(
        self,
        customer_id: str,
        plan: str,
        tenant_id: str
    ) -> Subscription:
        """Create a subscription for a customer."""
        if plan not in PLANS:
            raise ValueError(f"Invalid plan: {plan}")

        plan_config = PLANS[plan]

        # Create subscription with base price + metered overage
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[
                {"price": plan_config["stripe_price_id"]},
                # Metered component for overage (if configured)
                # {"price": plan_config.get("stripe_overage_price_id")}
            ],
            metadata={
                "tenant_id": tenant_id,
                "plan": plan
            }
        )

        logger.info(f"Created subscription {subscription.id} for customer {customer_id}")

        return Subscription(
            id=subscription.id,
            customer_id=customer_id,
            plan=plan,
            status=subscription.status,
            current_period_start=datetime.fromtimestamp(subscription.current_period_start),
            current_period_end=datetime.fromtimestamp(subscription.current_period_end)
        )

    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get subscription by ID."""
        try:
            sub = stripe.Subscription.retrieve(subscription_id)
            return Subscription(
                id=sub.id,
                customer_id=sub.customer,
                plan=sub.metadata.get("plan", "starter"),
                status=sub.status,
                current_period_start=datetime.fromtimestamp(sub.current_period_start),
                current_period_end=datetime.fromtimestamp(sub.current_period_end)
            )
        except stripe.error.InvalidRequestError:
            return None

    def change_plan(self, subscription_id: str, new_plan: str) -> Subscription:
        """Change subscription plan."""
        if new_plan not in PLANS:
            raise ValueError(f"Invalid plan: {new_plan}")

        plan_config = PLANS[new_plan]

        # Get current subscription
        sub = stripe.Subscription.retrieve(subscription_id)

        # Update to new price
        stripe.Subscription.modify(
            subscription_id,
            items=[{
                "id": sub["items"]["data"][0]["id"],
                "price": plan_config["stripe_price_id"]
            }],
            metadata={"plan": new_plan},
            proration_behavior="create_prorations"
        )

        return self.get_subscription(subscription_id)

    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ):
        """Cancel a subscription."""
        if at_period_end:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
        else:
            stripe.Subscription.delete(subscription_id)

        logger.info(f"Cancelled subscription {subscription_id}")

    # =========================================================================
    # Usage-Based Billing
    # =========================================================================

    def report_usage(
        self,
        subscription_id: str,
        tokens_used: int
    ):
        """
        Report token usage for metered billing.

        Called at end of billing period to report overage.
        """
        sub = stripe.Subscription.retrieve(subscription_id)
        plan = sub.metadata.get("plan", "starter")
        plan_config = PLANS[plan]

        # Calculate overage
        tokens_included = plan_config["tokens_included"]
        overage_tokens = max(0, tokens_used - tokens_included)

        if overage_tokens == 0:
            return

        # Find metered subscription item
        metered_item = None
        for item in sub["items"]["data"]:
            if item["price"]["recurring"]["usage_type"] == "metered":
                metered_item = item
                break

        if not metered_item:
            logger.warning(f"No metered item found for subscription {subscription_id}")
            return

        # Report usage in billing units (per million tokens)
        # Stripe expects integer cents, so we calculate:
        # overage_tokens / 1M * price_per_million_cents
        overage_million = overage_tokens / 1_000_000
        overage_cents = int(overage_million * plan_config["overage_per_million_cents"])

        stripe.SubscriptionItem.create_usage_record(
            metered_item["id"],
            quantity=overage_cents,
            action="set"  # Set absolute value for the period
        )

        logger.info(
            f"Reported usage for {subscription_id}: "
            f"{overage_tokens:,} overage tokens = ${overage_cents/100:.2f}"
        )

    # =========================================================================
    # Invoicing
    # =========================================================================

    def get_upcoming_invoice(self, customer_id: str) -> Optional[Dict]:
        """Get upcoming invoice for customer."""
        try:
            invoice = stripe.Invoice.upcoming(customer=customer_id)
            return {
                "amount_due": invoice.amount_due,
                "currency": invoice.currency,
                "period_start": datetime.fromtimestamp(invoice.period_start),
                "period_end": datetime.fromtimestamp(invoice.period_end),
                "lines": [
                    {
                        "description": line.description,
                        "amount": line.amount
                    }
                    for line in invoice.lines.data
                ]
            }
        except stripe.error.InvalidRequestError:
            return None

    def list_invoices(
        self,
        customer_id: str,
        limit: int = 10
    ) -> list:
        """List invoices for customer."""
        invoices = stripe.Invoice.list(
            customer=customer_id,
            limit=limit
        )

        return [
            {
                "id": inv.id,
                "number": inv.number,
                "status": inv.status,
                "amount_due": inv.amount_due,
                "amount_paid": inv.amount_paid,
                "created": datetime.fromtimestamp(inv.created),
                "pdf_url": inv.invoice_pdf
            }
            for inv in invoices.data
        ]

    # =========================================================================
    # Payment Methods
    # =========================================================================

    def create_setup_intent(self, customer_id: str) -> str:
        """Create setup intent for adding payment method."""
        intent = stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=["card"]
        )
        return intent.client_secret

    def get_payment_methods(self, customer_id: str) -> list:
        """List payment methods for customer."""
        methods = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"
        )

        return [
            {
                "id": pm.id,
                "brand": pm.card.brand,
                "last4": pm.card.last4,
                "exp_month": pm.card.exp_month,
                "exp_year": pm.card.exp_year
            }
            for pm in methods.data
        ]

    def set_default_payment_method(
        self,
        customer_id: str,
        payment_method_id: str
    ):
        """Set default payment method for customer."""
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                "default_payment_method": payment_method_id
            }
        )


# Singleton instance
_client: Optional[StripeClient] = None


def get_stripe_client() -> StripeClient:
    """Get Stripe client singleton."""
    global _client
    if _client is None:
        _client = StripeClient()
    return _client
