"""
Usage Tracking

Track and report usage events for billing.
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum

from google.cloud import pubsub_v1, firestore

logger = logging.getLogger(__name__)


class UsageEventType(str, Enum):
    """Types of billable usage events."""
    TOKEN_USAGE = "token_usage"
    SPRITE_SPAWN = "sprite_spawn"
    SPRITE_TIME = "sprite_time"  # Per-minute sprite runtime
    STORAGE = "storage"  # Asset storage
    API_CALL = "api_call"  # Direct API calls (non-sprite)


@dataclass
class UsageEvent:
    """A billable usage event."""
    event_type: UsageEventType
    tenant_id: str
    timestamp: datetime
    data: Dict[str, Any]

    # Optional context
    sprite_id: Optional[str] = None
    work_id: Optional[str] = None
    project_id: Optional[str] = None
    user_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "tenant_id": self.tenant_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "sprite_id": self.sprite_id,
            "work_id": self.work_id,
            "project_id": self.project_id,
            "user_id": self.user_id
        }


class UsageTracker:
    """
    Tracks usage events for billing.

    Events are:
    1. Published to Pub/Sub for async processing
    2. Written to Firestore for real-time counters
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        topic_id: str = "usage-events"
    ):
        self.project_id = project_id or os.environ.get("GCP_PROJECT_ID")
        self.topic_id = topic_id

        # Pub/Sub publisher
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Firestore for real-time counters
        self.db = firestore.Client()

    def track(self, event: UsageEvent):
        """
        Track a usage event.

        Publishes to Pub/Sub and updates real-time counters.
        """
        try:
            # 1. Publish to Pub/Sub for async processing
            self._publish_event(event)

            # 2. Update real-time counters in Firestore
            self._update_counters(event)

        except Exception as e:
            logger.error(f"Failed to track usage event: {e}")
            # Don't fail the request if tracking fails
            # Consider dead-letter queue for retry

    def track_tokens(
        self,
        tenant_id: str,
        tokens: int,
        model: str,
        sprite_id: Optional[str] = None,
        work_id: Optional[str] = None
    ):
        """Convenience method to track token usage."""
        event = UsageEvent(
            event_type=UsageEventType.TOKEN_USAGE,
            tenant_id=tenant_id,
            timestamp=datetime.now(timezone.utc),
            data={
                "tokens": tokens,
                "model": model
            },
            sprite_id=sprite_id,
            work_id=work_id
        )
        self.track(event)

    def track_sprite_spawn(
        self,
        tenant_id: str,
        sprite_id: str,
        agent_type: str,
        project_id: Optional[str] = None
    ):
        """Track sprite spawn event."""
        event = UsageEvent(
            event_type=UsageEventType.SPRITE_SPAWN,
            tenant_id=tenant_id,
            timestamp=datetime.now(timezone.utc),
            data={
                "agent_type": agent_type
            },
            sprite_id=sprite_id,
            project_id=project_id
        )
        self.track(event)

    def track_api_call(
        self,
        tenant_id: str,
        skill: str,
        tokens: int,
        user_id: Optional[str] = None
    ):
        """Track direct API call (non-sprite)."""
        event = UsageEvent(
            event_type=UsageEventType.API_CALL,
            tenant_id=tenant_id,
            timestamp=datetime.now(timezone.utc),
            data={
                "skill": skill,
                "tokens": tokens
            },
            user_id=user_id
        )
        self.track(event)

    def _publish_event(self, event: UsageEvent):
        """Publish event to Pub/Sub."""
        data = json.dumps(event.to_dict()).encode("utf-8")

        future = self.publisher.publish(
            self.topic_path,
            data,
            tenant_id=event.tenant_id,
            event_type=event.event_type.value
        )

        # Don't wait for result (async)
        future.add_done_callback(self._publish_callback)

    def _publish_callback(self, future):
        """Callback for Pub/Sub publish."""
        try:
            message_id = future.result()
            logger.debug(f"Published usage event: {message_id}")
        except Exception as e:
            logger.error(f"Failed to publish usage event: {e}")

    def _update_counters(self, event: UsageEvent):
        """Update real-time counters in Firestore."""
        tenant_ref = self.db.collection("tenants").document(event.tenant_id)

        updates = {
            "usage.last_updated": firestore.SERVER_TIMESTAMP
        }

        if event.event_type == UsageEventType.TOKEN_USAGE:
            tokens = event.data.get("tokens", 0)
            updates["usage.tokens_this_period"] = firestore.Increment(tokens)
            updates["usage.total_tokens"] = firestore.Increment(tokens)

        elif event.event_type == UsageEventType.SPRITE_SPAWN:
            updates["usage.sprites_spawned_this_period"] = firestore.Increment(1)
            updates["usage.total_sprites_spawned"] = firestore.Increment(1)

        elif event.event_type == UsageEventType.API_CALL:
            tokens = event.data.get("tokens", 0)
            updates["usage.tokens_this_period"] = firestore.Increment(tokens)
            updates["usage.api_calls_this_period"] = firestore.Increment(1)

        tenant_ref.update(updates)

    def get_usage(self, tenant_id: str) -> Dict[str, Any]:
        """Get current usage for tenant."""
        doc = self.db.collection("tenants").document(tenant_id).get()

        if not doc.exists:
            return {}

        return doc.to_dict().get("usage", {})

    def reset_period_usage(self, tenant_id: str):
        """Reset period usage counters (called on billing cycle)."""
        tenant_ref = self.db.collection("tenants").document(tenant_id)

        tenant_ref.update({
            "usage.tokens_this_period": 0,
            "usage.sprites_spawned_this_period": 0,
            "usage.api_calls_this_period": 0,
            "usage.period_reset_at": firestore.SERVER_TIMESTAMP
        })


# Singleton instance
_tracker: Optional[UsageTracker] = None


def get_usage_tracker() -> UsageTracker:
    """Get usage tracker singleton."""
    global _tracker
    if _tracker is None:
        _tracker = UsageTracker()
    return _tracker
