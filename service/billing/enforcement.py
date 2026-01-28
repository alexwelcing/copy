"""
Billing Enforcement

Real-time limit checking and enforcement for multi-tenant billing.
"""

import os
import logging
from functools import wraps
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from google.cloud import firestore
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Plan limits configuration
PLAN_LIMITS = {
    "starter": {
        "tokens_per_period": 1_000_000,
        "max_concurrent_sprites": 2,
        "sprites_per_period": 100,
        "overage_enabled": False,  # Hard cap
        "enabled_agents": ["director", "copywriter", "editor"]
    },
    "growth": {
        "tokens_per_period": 10_000_000,
        "max_concurrent_sprites": 4,
        "sprites_per_period": 500,
        "overage_enabled": True,  # Can go over, will be charged
        "enabled_agents": ["director", "strategist", "copywriter", "editor", "optimizer", "analyst"]
    },
    "enterprise": {
        "tokens_per_period": 100_000_000,
        "max_concurrent_sprites": 10,
        "sprites_per_period": 2000,
        "overage_enabled": True,
        "enabled_agents": ["director", "strategist", "copywriter", "editor", "optimizer", "analyst"]
    }
}


class BillingEnforcement:
    """
    Enforces billing limits in real-time.

    Checks are performed before:
    - Spawning sprites
    - Executing work (token usage)
    - Accessing premium features
    """

    def __init__(self, db: Optional[firestore.Client] = None):
        self.db = db or firestore.Client()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = 60  # seconds

    async def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant data with caching."""
        # Simple in-memory cache (use Redis in production)
        cache_key = f"tenant:{tenant_id}"
        cached = self._cache.get(cache_key)

        if cached and (datetime.now(timezone.utc) - cached["fetched_at"]).seconds < self._cache_ttl:
            return cached["data"]

        doc = self.db.collection("tenants").document(tenant_id).get()
        if not doc.exists:
            raise HTTPException(404, f"Tenant {tenant_id} not found")

        data = doc.to_dict()
        self._cache[cache_key] = {
            "data": data,
            "fetched_at": datetime.now(timezone.utc)
        }

        return data

    def invalidate_cache(self, tenant_id: str):
        """Invalidate tenant cache."""
        cache_key = f"tenant:{tenant_id}"
        self._cache.pop(cache_key, None)

    async def check_billing_status(self, tenant_id: str) -> str:
        """
        Check tenant billing status.

        Returns: 'active', 'past_due', 'suspended', 'cancelled'
        Raises: HTTPException if access should be denied
        """
        tenant = await self.get_tenant(tenant_id)
        billing = tenant.get("billing", {})
        status = billing.get("status", "active")

        if status == "suspended":
            raise HTTPException(
                status_code=402,
                detail="Account suspended. Please update your payment method at billing.highera.com"
            )

        if status == "cancelled":
            raise HTTPException(
                status_code=402,
                detail="Subscription cancelled. Please reactivate at billing.highera.com"
            )

        return status

    async def check_can_spawn_sprite(
        self,
        tenant_id: str,
        agent_type: str
    ) -> bool:
        """
        Check if tenant can spawn another sprite.

        Raises HTTPException if not allowed.
        """
        await self.check_billing_status(tenant_id)

        tenant = await self.get_tenant(tenant_id)
        plan = tenant.get("plan", "starter")
        limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["starter"])

        # Check if agent type is enabled
        if agent_type not in limits["enabled_agents"]:
            raise HTTPException(
                status_code=403,
                detail=f"Agent type '{agent_type}' not available on {plan} plan. Upgrade to access."
            )

        # Check concurrent sprite limit
        active_sprites = await self._count_active_sprites(tenant_id)
        if active_sprites >= limits["max_concurrent_sprites"]:
            raise HTTPException(
                status_code=429,
                detail=f"Concurrent sprite limit reached ({limits['max_concurrent_sprites']}). "
                       f"Stop an existing sprite or upgrade your plan."
            )

        # Check sprites spawned this period
        usage = tenant.get("usage", {})
        sprites_spawned = usage.get("sprites_spawned_this_period", 0)
        if sprites_spawned >= limits["sprites_per_period"]:
            raise HTTPException(
                status_code=429,
                detail=f"Monthly sprite spawn limit reached ({limits['sprites_per_period']}). "
                       f"Limit resets at the start of your billing cycle."
            )

        return True

    async def check_can_use_tokens(
        self,
        tenant_id: str,
        estimated_tokens: int
    ) -> bool:
        """
        Check if tenant has token budget for estimated usage.

        Raises HTTPException if hard limit exceeded.
        """
        await self.check_billing_status(tenant_id)

        tenant = await self.get_tenant(tenant_id)
        plan = tenant.get("plan", "starter")
        limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["starter"])

        usage = tenant.get("usage", {})
        tokens_used = usage.get("tokens_this_period", 0)
        token_limit = limits["tokens_per_period"]

        # Check if this would exceed limit
        projected_usage = tokens_used + estimated_tokens

        if projected_usage > token_limit:
            if limits["overage_enabled"]:
                # Warn but allow (will be charged overage)
                logger.info(
                    f"Tenant {tenant_id} exceeding token limit: "
                    f"{projected_usage:,} / {token_limit:,}"
                )
                return True
            else:
                # Hard cap - deny
                raise HTTPException(
                    status_code=429,
                    detail=f"Monthly token limit exceeded. "
                           f"Used: {tokens_used:,} / {token_limit:,}. "
                           f"Upgrade to Growth plan for higher limits."
                )

        # Warn at 80%
        if projected_usage > token_limit * 0.8:
            logger.warning(
                f"Tenant {tenant_id} at {projected_usage/token_limit*100:.0f}% of token limit"
            )

        return True

    async def get_usage_summary(self, tenant_id: str) -> Dict[str, Any]:
        """Get current usage summary for tenant."""
        tenant = await self.get_tenant(tenant_id)
        plan = tenant.get("plan", "starter")
        limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["starter"])
        usage = tenant.get("usage", {})

        tokens_used = usage.get("tokens_this_period", 0)
        sprites_spawned = usage.get("sprites_spawned_this_period", 0)
        active_sprites = await self._count_active_sprites(tenant_id)

        return {
            "plan": plan,
            "tokens": {
                "used": tokens_used,
                "limit": limits["tokens_per_period"],
                "percentage": round(tokens_used / limits["tokens_per_period"] * 100, 1),
                "overage_enabled": limits["overage_enabled"]
            },
            "sprites": {
                "active": active_sprites,
                "concurrent_limit": limits["max_concurrent_sprites"],
                "spawned_this_period": sprites_spawned,
                "period_limit": limits["sprites_per_period"]
            },
            "enabled_agents": limits["enabled_agents"]
        }

    async def _count_active_sprites(self, tenant_id: str) -> int:
        """Count active sprites for tenant."""
        sprites_ref = self.db.collection("tenants").document(tenant_id).collection("sprites")
        query = sprites_ref.where("status", "not-in", ["stopped", "failed"])

        count = 0
        for _ in query.stream():
            count += 1

        return count


def require_billing_active(func):
    """
    Decorator to enforce billing status on endpoint.

    Usage:
        @require_billing_active
        async def my_endpoint(tenant_id: str, ...):
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract tenant_id from kwargs or first positional arg
        tenant_id = kwargs.get("tenant_id")
        if not tenant_id and args:
            tenant_id = args[0]

        if not tenant_id:
            raise HTTPException(400, "tenant_id required")

        enforcement = BillingEnforcement()
        await enforcement.check_billing_status(tenant_id)

        return await func(*args, **kwargs)

    return wrapper


# Singleton instance
_enforcement: Optional[BillingEnforcement] = None


def get_enforcement() -> BillingEnforcement:
    """Get billing enforcement singleton."""
    global _enforcement
    if _enforcement is None:
        _enforcement = BillingEnforcement()
    return _enforcement
