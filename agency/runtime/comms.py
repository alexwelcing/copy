"""
Sprite Communications

Handles Redis pub/sub for inter-sprite messaging and coordinator HTTP API.
"""

import json
import time
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable
import redis
import httpx

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of messages sprites can receive."""
    TASK = "task"
    HANDOFF = "handoff"
    REVIEW_REQUEST = "review_request"
    REVIEW_RESPONSE = "review_response"
    STATUS_UPDATE = "status_update"
    PING = "ping"
    SHUTDOWN = "shutdown"


@dataclass
class Message:
    """A message received by a sprite."""
    type: MessageType
    payload: Dict[str, Any]
    from_sprite: Optional[str] = None
    timestamp: Optional[float] = None


class SpriteComms:
    """
    Handles all sprite communications:
    - Redis pub/sub for inter-sprite messaging
    - HTTP to coordinator for state updates
    """

    def __init__(
        self,
        sprite_id: str,
        tenant_id: str,
        redis_url: str,
        coordinator_url: str
    ):
        self.sprite_id = sprite_id
        self.tenant_id = tenant_id
        self.redis_url = redis_url
        self.coordinator_url = coordinator_url.rstrip('/')

        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.http_client: Optional[httpx.Client] = None

        self._subscribed_channels: list[str] = []

    # =========================================================================
    # Connection Management
    # =========================================================================

    def connect(self):
        """Connect to Redis and HTTP client."""
        logger.info(f"Connecting to Redis: {self.redis_url[:30]}...")
        self.redis_client = redis.from_url(
            self.redis_url,
            decode_responses=True,
            socket_timeout=5.0,
            socket_connect_timeout=5.0
        )

        # Test connection
        self.redis_client.ping()
        logger.info("Redis connected")

        # Initialize pub/sub
        self.pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)

        # Initialize HTTP client
        self.http_client = httpx.Client(
            base_url=self.coordinator_url,
            timeout=30.0,
            headers={"X-Sprite-ID": self.sprite_id}
        )
        logger.info("HTTP client initialized")

    def disconnect(self):
        """Clean disconnect from all services."""
        if self.pubsub:
            try:
                self.pubsub.unsubscribe()
                self.pubsub.close()
            except Exception as e:
                logger.warning(f"Error closing pubsub: {e}")

        if self.redis_client:
            try:
                self.redis_client.close()
            except Exception as e:
                logger.warning(f"Error closing Redis: {e}")

        if self.http_client:
            try:
                self.http_client.close()
            except Exception as e:
                logger.warning(f"Error closing HTTP client: {e}")

        logger.info("Disconnected")

    # =========================================================================
    # Channel Subscriptions
    # =========================================================================

    def subscribe_to_inbox(self):
        """Subscribe to this sprite's direct inbox."""
        channel = f"sprite:{self.sprite_id}:inbox"
        self.pubsub.subscribe(channel)
        self._subscribed_channels.append(channel)
        logger.info(f"Subscribed to: {channel}")

    def subscribe_to_project(self, project_id: str):
        """Subscribe to project-wide updates."""
        channel = f"project:{project_id}:updates"
        self.pubsub.subscribe(channel)
        self._subscribed_channels.append(channel)
        logger.info(f"Subscribed to: {channel}")

    def subscribe_to_tenant_handoffs(self):
        """Subscribe to tenant-wide handoff requests."""
        channel = f"tenant:{self.tenant_id}:handoffs"
        self.pubsub.subscribe(channel)
        self._subscribed_channels.append(channel)
        logger.info(f"Subscribed to: {channel}")

    # =========================================================================
    # Message Receiving
    # =========================================================================

    def get_message(self, timeout: float = 1.0) -> Optional[Message]:
        """
        Get next message from subscribed channels.
        Returns None if no message within timeout.
        """
        if not self.pubsub:
            return None

        try:
            raw = self.pubsub.get_message(timeout=timeout)
            if raw and raw["type"] == "message":
                return self._parse_message(raw["data"])
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            # Attempt reconnect
            self._reconnect_redis()
        except Exception as e:
            logger.error(f"Error getting message: {e}")

        return None

    def _parse_message(self, data: str) -> Optional[Message]:
        """Parse raw message data into Message object."""
        try:
            payload = json.loads(data)
            msg_type = MessageType(payload.get("type", "task"))

            return Message(
                type=msg_type,
                payload=payload.get("payload", payload),
                from_sprite=payload.get("from_sprite"),
                timestamp=payload.get("timestamp", time.time())
            )
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Error parsing message: {e}")
            return None

    def _reconnect_redis(self):
        """Attempt to reconnect to Redis."""
        logger.info("Attempting Redis reconnect...")
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                decode_responses=True
            )
            self.pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)

            # Resubscribe to channels
            for channel in self._subscribed_channels:
                self.pubsub.subscribe(channel)

            logger.info("Redis reconnected")
        except Exception as e:
            logger.error(f"Reconnect failed: {e}")

    # =========================================================================
    # Message Sending
    # =========================================================================

    def publish(self, channel: str, message: Dict[str, Any]):
        """Publish a message to a channel."""
        message["from_sprite"] = self.sprite_id
        message["timestamp"] = time.time()
        self.redis_client.publish(channel, json.dumps(message))

    def send_to_sprite(self, sprite_id: str, message: Dict[str, Any]):
        """Send a direct message to another sprite."""
        channel = f"sprite:{sprite_id}:inbox"
        self.publish(channel, message)

    def request_handoff(
        self,
        to_agent: str,
        context: Dict[str, Any],
        artifact: str,
        project_id: Optional[str] = None
    ):
        """Request a handoff to another agent type."""
        channel = f"tenant:{self.tenant_id}:handoffs"
        self.publish(channel, {
            "type": "handoff",
            "payload": {
                "to_agent": to_agent,
                "context": context,
                "artifact": artifact,
                "project_id": project_id
            }
        })

        # Also notify coordinator via HTTP
        try:
            self.http_client.post(
                f"/tenants/{self.tenant_id}/handoffs",
                json={
                    "from_sprite": self.sprite_id,
                    "to_agent": to_agent,
                    "context": context,
                    "project_id": project_id
                }
            )
        except Exception as e:
            logger.warning(f"Failed to notify coordinator of handoff: {e}")

    def request_review(
        self,
        artifact: str,
        questions: list[str],
        project_id: Optional[str] = None
    ):
        """Request a review from the Editor agent."""
        channel = f"tenant:{self.tenant_id}:reviews"
        self.publish(channel, {
            "type": "review_request",
            "payload": {
                "artifact": artifact,
                "questions": questions,
                "project_id": project_id
            }
        })

    def pong(self):
        """Respond to a ping."""
        # Pong goes to coordinator via HTTP
        try:
            self.http_client.post(
                f"/tenants/{self.tenant_id}/sprites/{self.sprite_id}/pong"
            )
        except Exception as e:
            logger.warning(f"Pong failed: {e}")

    # =========================================================================
    # Coordinator Communication
    # =========================================================================

    def fetch_brand_context(self) -> Optional[Dict[str, Any]]:
        """Fetch brand context from coordinator."""
        try:
            response = self.http_client.get(
                f"/tenants/{self.tenant_id}/brand"
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.warning(f"Failed to fetch brand context: {e}")
        return None

    def report_status(self, status: str, current_task: Optional[str] = None):
        """Report current status to coordinator."""
        try:
            self.http_client.patch(
                f"/tenants/{self.tenant_id}/sprites/{self.sprite_id}",
                json={
                    "status": status,
                    "current_task": current_task
                }
            )
        except Exception as e:
            logger.warning(f"Failed to report status: {e}")

    def heartbeat(self, status: str, tasks_completed: int, tokens_used: int):
        """Send heartbeat to coordinator."""
        try:
            self.http_client.post(
                f"/tenants/{self.tenant_id}/sprites/{self.sprite_id}/heartbeat",
                json={
                    "status": status,
                    "tasks_completed": tasks_completed,
                    "tokens_used": tokens_used
                }
            )
        except Exception as e:
            logger.warning(f"Heartbeat failed: {e}")

    def complete_task(self, task_id: str, output: str, tokens_used: int):
        """Report task completion to coordinator."""
        try:
            self.http_client.post(
                f"/tenants/{self.tenant_id}/work/{task_id}/complete",
                json={
                    "sprite_id": self.sprite_id,
                    "output": output,
                    "tokens_used": tokens_used
                }
            )
        except Exception as e:
            logger.warning(f"Failed to report task completion: {e}")

    def fail_task(self, task_id: str, error: str):
        """Report task failure to coordinator."""
        try:
            self.http_client.post(
                f"/tenants/{self.tenant_id}/work/{task_id}/fail",
                json={
                    "sprite_id": self.sprite_id,
                    "error": error
                }
            )
        except Exception as e:
            logger.warning(f"Failed to report task failure: {e}")
