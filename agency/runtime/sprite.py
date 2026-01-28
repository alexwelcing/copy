"""
Sprite Runtime

A sprite is an ephemeral agent container that executes marketing work.
Each sprite loads a persona, connects to the swarm, and processes tasks.
"""

import os
import sys
import json
import time
import signal
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from persona import PersonaLoader
from executor import ClaudeExecutor
from comms import SpriteComms, Message, MessageType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SpriteConfig:
    """Configuration loaded from environment."""
    sprite_id: str
    tenant_id: str
    agent_type: str
    project_id: Optional[str]
    coordinator_url: str
    redis_url: str
    anthropic_api_key: str
    idle_timeout_seconds: int = 300
    heartbeat_interval_seconds: int = 30

    @classmethod
    def from_env(cls) -> "SpriteConfig":
        return cls(
            sprite_id=os.environ.get("SPRITE_ID", f"sprite-{os.getpid()}"),
            tenant_id=os.environ["TENANT_ID"],
            agent_type=os.environ["AGENT_TYPE"],
            project_id=os.environ.get("PROJECT_ID"),
            coordinator_url=os.environ["COORDINATOR_URL"],
            redis_url=os.environ["REDIS_URL"],
            anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
            idle_timeout_seconds=int(os.environ.get("IDLE_TIMEOUT", "300")),
            heartbeat_interval_seconds=int(os.environ.get("HEARTBEAT_INTERVAL", "30")),
        )


@dataclass
class SpriteState:
    """Current sprite state."""
    status: str = "starting"  # starting | idle | working | blocked | stopping
    current_task: Optional[Dict] = None
    last_task_completed: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None
    tasks_completed: int = 0
    tokens_used: int = 0


class Sprite:
    """
    The sprite runtime.

    Lifecycle:
    1. Boot: Load config, persona, connect to swarm
    2. Run: Wait for tasks, execute, report
    3. Shutdown: Clean up, exit
    """

    def __init__(self, config: SpriteConfig):
        self.config = config
        self.state = SpriteState()
        self._shutdown_requested = False

        # Load persona for this agent type
        logger.info(f"Loading persona: {config.agent_type}")
        self.persona = PersonaLoader.load(config.agent_type)

        # Initialize Claude executor
        self.executor = ClaudeExecutor(
            api_key=config.anthropic_api_key,
            system_prompt=self.persona.system_prompt
        )

        # Initialize communications
        self.comms = SpriteComms(
            sprite_id=config.sprite_id,
            tenant_id=config.tenant_id,
            redis_url=config.redis_url,
            coordinator_url=config.coordinator_url
        )

        # Brand context (loaded from coordinator)
        self.brand_context: Optional[Dict] = None

        # Register signal handlers
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self._shutdown_requested = True

    def boot(self):
        """Initialize sprite and connect to swarm."""
        logger.info(f"Sprite {self.config.sprite_id} booting...")
        logger.info(f"  Tenant: {self.config.tenant_id}")
        logger.info(f"  Agent: {self.config.agent_type}")
        logger.info(f"  Project: {self.config.project_id or 'None'}")

        # Connect to Redis
        self.comms.connect()

        # Fetch brand context from coordinator
        self.brand_context = self.comms.fetch_brand_context()
        if self.brand_context:
            logger.info(f"  Brand context loaded: {len(self.brand_context)} keys")

        # Subscribe to channels
        self.comms.subscribe_to_inbox()
        if self.config.project_id:
            self.comms.subscribe_to_project(self.config.project_id)

        # Report ready
        self.state.status = "idle"
        self._report_status()
        logger.info("Sprite ready and waiting for work")

    def run(self):
        """Main loop - process messages until shutdown."""
        last_heartbeat = time.time()
        last_activity = time.time()

        while not self._shutdown_requested:
            # Check for incoming messages
            message = self.comms.get_message(timeout=1.0)

            if message:
                last_activity = time.time()
                self._handle_message(message)

            # Periodic heartbeat
            if time.time() - last_heartbeat > self.config.heartbeat_interval_seconds:
                self._heartbeat()
                last_heartbeat = time.time()

            # Check idle timeout
            if self.state.status == "idle":
                idle_time = time.time() - last_activity
                if idle_time > self.config.idle_timeout_seconds:
                    logger.info(f"Idle timeout ({idle_time:.0f}s), shutting down...")
                    break

        self.shutdown()

    def _handle_message(self, message: Message):
        """Process an incoming message."""
        logger.info(f"Received message: {message.type.value}")

        if message.type == MessageType.TASK:
            self._execute_task(message.payload)

        elif message.type == MessageType.HANDOFF:
            self._handle_handoff(message.payload)

        elif message.type == MessageType.REVIEW_REQUEST:
            self._handle_review_request(message.payload)

        elif message.type == MessageType.PING:
            self.comms.pong()

        elif message.type == MessageType.SHUTDOWN:
            logger.info("Received shutdown command")
            self._shutdown_requested = True

        else:
            logger.warning(f"Unknown message type: {message.type}")

    def _execute_task(self, task: Dict[str, Any]):
        """Execute a task using Claude."""
        task_id = task.get("id", "unknown")
        description = task.get("description", "No description")

        logger.info(f"Executing task {task_id}: {description}")
        self.state.status = "working"
        self.state.current_task = task
        self._report_status()

        try:
            # Build the prompt
            prompt = self._build_prompt(task)

            # Execute with Claude
            result = self.executor.execute(
                prompt=prompt,
                context={
                    "brand": self.brand_context,
                    "project_id": self.config.project_id,
                    "task": task
                }
            )

            # Update token usage
            self.state.tokens_used += result.tokens_used

            # Check for handoff requests in the output
            if result.handoff_requested:
                self._request_handoff(
                    to_agent=result.handoff_to,
                    context=result.handoff_context,
                    artifact=result.output
                )

            # Check for review requests
            if result.review_requested:
                self._request_review(
                    artifact=result.output,
                    questions=result.review_questions
                )

            # Report completion
            self.comms.complete_task(
                task_id=task_id,
                output=result.output,
                tokens_used=result.tokens_used
            )

            self.state.tasks_completed += 1
            self.state.last_task_completed = datetime.now(timezone.utc)
            logger.info(f"Task {task_id} completed successfully")

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            self.comms.fail_task(task_id=task_id, error=str(e))

        finally:
            self.state.status = "idle"
            self.state.current_task = None
            self._report_status()

    def _build_prompt(self, task: Dict[str, Any]) -> str:
        """Build the full prompt for Claude."""
        parts = []

        # Task description
        parts.append(f"## Task\n{task.get('description', '')}")

        # Input content if provided
        if task.get("input"):
            if isinstance(task["input"], str):
                parts.append(f"## Input\n{task['input']}")
            else:
                parts.append(f"## Input\n```json\n{json.dumps(task['input'], indent=2)}\n```")

        # Context
        if task.get("context"):
            parts.append(f"## Context\n{json.dumps(task['context'], indent=2)}")

        # Brand context
        if self.brand_context:
            brand_summary = self._summarize_brand()
            parts.append(f"## Brand\n{brand_summary}")

        # Instructions for handoffs
        parts.append("""
## Output Instructions

If you need another agent to continue this work, end your response with:

```handoff
TO: [agent_type]
CONTEXT: [what they need to know]
```

If you need a review before finalizing, end with:

```review
QUESTIONS:
- [question 1]
- [question 2]
```

Otherwise, just provide your output directly.
""")

        return "\n\n".join(parts)

    def _summarize_brand(self) -> str:
        """Create a concise brand context summary."""
        if not self.brand_context:
            return "No brand context available."

        parts = []
        if self.brand_context.get("voice"):
            parts.append(f"Voice: {self.brand_context['voice']}")
        if self.brand_context.get("tone"):
            parts.append(f"Tone: {self.brand_context['tone']}")
        if self.brand_context.get("audience"):
            parts.append(f"Audience: {self.brand_context['audience']}")
        if self.brand_context.get("guidelines"):
            parts.append(f"Guidelines: {self.brand_context['guidelines'][:500]}...")

        return "\n".join(parts) if parts else "Brand context loaded but empty."

    def _handle_handoff(self, payload: Dict[str, Any]):
        """Handle incoming handoff from another sprite."""
        from_agent = payload.get("from_agent", "unknown")
        context = payload.get("context", {})
        artifact = payload.get("artifact", "")

        logger.info(f"Received handoff from {from_agent}")

        # Create a task from the handoff
        task = {
            "id": f"handoff-{int(time.time())}",
            "description": f"Continue work from {from_agent}",
            "input": artifact,
            "context": context,
            "is_handoff": True,
            "from_agent": from_agent
        }

        self._execute_task(task)

    def _handle_review_request(self, payload: Dict[str, Any]):
        """Handle incoming review request."""
        from_agent = payload.get("from_agent", "unknown")
        artifact = payload.get("artifact", "")
        questions = payload.get("questions", [])

        logger.info(f"Received review request from {from_agent}")

        # Create a review task
        task = {
            "id": f"review-{int(time.time())}",
            "description": f"Review work from {from_agent}",
            "input": artifact,
            "context": {
                "questions": questions,
                "review_type": "peer_review",
                "from_agent": from_agent
            },
            "is_review": True
        }

        self._execute_task(task)

    def _request_handoff(self, to_agent: str, context: Dict, artifact: str):
        """Request handoff to another agent."""
        logger.info(f"Requesting handoff to {to_agent}")
        self.comms.request_handoff(
            to_agent=to_agent,
            context=context,
            artifact=artifact,
            project_id=self.config.project_id
        )

    def _request_review(self, artifact: str, questions: list):
        """Request review from Editor agent."""
        logger.info("Requesting review from Editor")
        self.comms.request_review(
            artifact=artifact,
            questions=questions,
            project_id=self.config.project_id
        )

    def _heartbeat(self):
        """Send heartbeat to coordinator."""
        self.state.last_heartbeat = datetime.now(timezone.utc)
        self.comms.heartbeat(
            status=self.state.status,
            tasks_completed=self.state.tasks_completed,
            tokens_used=self.state.tokens_used
        )

    def _report_status(self):
        """Report current status to coordinator."""
        self.comms.report_status(
            status=self.state.status,
            current_task=self.state.current_task.get("description") if self.state.current_task else None
        )

    def shutdown(self):
        """Clean shutdown."""
        logger.info("Sprite shutting down...")
        self.state.status = "stopping"
        self._report_status()

        # Disconnect from Redis
        self.comms.disconnect()

        # Final stats
        logger.info(f"Tasks completed: {self.state.tasks_completed}")
        logger.info(f"Tokens used: {self.state.tokens_used}")
        logger.info("Goodbye!")


def main():
    """Entry point."""
    try:
        config = SpriteConfig.from_env()
    except KeyError as e:
        logger.error(f"Missing required environment variable: {e}")
        sys.exit(1)

    sprite = Sprite(config)
    sprite.boot()
    sprite.run()


if __name__ == "__main__":
    main()
