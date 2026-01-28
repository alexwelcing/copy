"""
Swarm Coordinator

Orchestrates sprite lifecycle and work distribution across tenants.
Runs as part of the GCP control plane service.
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

from google.cloud import firestore
import redis

from .spawner import FlySpawner, SpawnConfig
from .state import TenantState, SpriteRecord, WorkRecord

logger = logging.getLogger(__name__)


class AgentType(str, Enum):
    DIRECTOR = "director"
    STRATEGIST = "strategist"
    COPYWRITER = "copywriter"
    EDITOR = "editor"
    OPTIMIZER = "optimizer"
    ANALYST = "analyst"


@dataclass
class TenantPlan:
    """Tenant plan limits."""
    name: str
    max_concurrent_sprites: int
    enabled_agents: List[AgentType]
    sprite_idle_timeout: int
    monthly_token_budget: int

    @classmethod
    def starter(cls) -> "TenantPlan":
        return cls(
            name="starter",
            max_concurrent_sprites=2,
            enabled_agents=[AgentType.DIRECTOR, AgentType.COPYWRITER, AgentType.EDITOR],
            sprite_idle_timeout=60,
            monthly_token_budget=1_000_000
        )

    @classmethod
    def growth(cls) -> "TenantPlan":
        return cls(
            name="growth",
            max_concurrent_sprites=4,
            enabled_agents=list(AgentType),
            sprite_idle_timeout=300,
            monthly_token_budget=10_000_000
        )

    @classmethod
    def enterprise(cls) -> "TenantPlan":
        return cls(
            name="enterprise",
            max_concurrent_sprites=10,
            enabled_agents=list(AgentType),
            sprite_idle_timeout=3600,
            monthly_token_budget=100_000_000
        )


class SwarmCoordinator:
    """
    Central coordinator for the sprite swarm.

    Responsibilities:
    - Spawn and stop sprites via Fly.io API
    - Route work to appropriate sprites
    - Handle handoff requests between sprites
    - Track tenant usage and enforce limits
    - Maintain swarm state in Firestore
    """

    def __init__(
        self,
        db: firestore.Client,
        redis_client: redis.Redis,
        fly_spawner: FlySpawner
    ):
        self.db = db
        self.redis = redis_client
        self.spawner = fly_spawner
        self.state = TenantState(db)

        # Cache of active sprites per tenant
        self._sprite_cache: Dict[str, Dict[str, SpriteRecord]] = {}

    # =========================================================================
    # Sprite Lifecycle
    # =========================================================================

    async def spawn_sprite(
        self,
        tenant_id: str,
        agent_type: AgentType,
        project_id: Optional[str] = None
    ) -> SpriteRecord:
        """Spawn a new sprite for a tenant."""

        # Check tenant limits
        plan = await self._get_tenant_plan(tenant_id)
        active_sprites = await self.state.get_active_sprites(tenant_id)

        if len(active_sprites) >= plan.max_concurrent_sprites:
            raise ValueError(
                f"Tenant {tenant_id} at sprite limit ({plan.max_concurrent_sprites})"
            )

        if agent_type not in plan.enabled_agents:
            raise ValueError(
                f"Agent type {agent_type} not enabled for plan {plan.name}"
            )

        # Check if we already have an idle sprite of this type
        for sprite in active_sprites:
            if sprite.agent_type == agent_type and sprite.status == "idle":
                logger.info(f"Reusing idle sprite {sprite.sprite_id}")
                return sprite

        # Spawn new sprite via Fly
        logger.info(f"Spawning {agent_type} sprite for tenant {tenant_id}")

        config = SpawnConfig(
            tenant_id=tenant_id,
            agent_type=agent_type.value,
            project_id=project_id,
            idle_timeout=plan.sprite_idle_timeout,
            coordinator_url=os.environ.get("COORDINATOR_URL", "https://api.highera.com"),
            redis_url=os.environ["REDIS_URL"],
            anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]
        )

        machine = await self.spawner.spawn(config)

        # Record in Firestore
        sprite = SpriteRecord(
            sprite_id=machine.id,
            tenant_id=tenant_id,
            agent_type=agent_type.value,
            fly_machine_id=machine.id,
            status="starting",
            project_id=project_id,
            created_at=datetime.now(timezone.utc)
        )

        await self.state.save_sprite(tenant_id, sprite)
        logger.info(f"Sprite {sprite.sprite_id} spawned")

        return sprite

    async def stop_sprite(self, tenant_id: str, sprite_id: str):
        """Stop a sprite."""
        sprite = await self.state.get_sprite(tenant_id, sprite_id)
        if not sprite:
            raise ValueError(f"Sprite {sprite_id} not found")

        # Stop the Fly machine
        await self.spawner.stop(sprite.fly_machine_id)

        # Update state
        sprite.status = "stopped"
        await self.state.save_sprite(tenant_id, sprite)

        logger.info(f"Sprite {sprite_id} stopped")

    async def handle_sprite_heartbeat(
        self,
        tenant_id: str,
        sprite_id: str,
        status: str,
        tasks_completed: int,
        tokens_used: int
    ):
        """Handle heartbeat from a sprite."""
        sprite = await self.state.get_sprite(tenant_id, sprite_id)
        if sprite:
            sprite.status = status
            sprite.tasks_completed = tasks_completed
            sprite.tokens_used = tokens_used
            sprite.last_heartbeat = datetime.now(timezone.utc)
            await self.state.save_sprite(tenant_id, sprite)

    # =========================================================================
    # Work Routing
    # =========================================================================

    async def submit_work(
        self,
        tenant_id: str,
        task: Dict[str, Any],
        agent_type: Optional[AgentType] = None,
        project_id: Optional[str] = None
    ) -> str:
        """Submit work to be executed by a sprite."""

        # Determine which agent should handle this
        if not agent_type:
            agent_type = self._infer_agent_type(task)

        # Create work record
        work = WorkRecord(
            work_id=f"work-{int(datetime.now().timestamp() * 1000)}",
            tenant_id=tenant_id,
            task=task,
            agent_type=agent_type.value,
            project_id=project_id,
            status="pending",
            created_at=datetime.now(timezone.utc)
        )

        await self.state.save_work(tenant_id, work)

        # Find or spawn a sprite
        sprite = await self._get_or_spawn_sprite(tenant_id, agent_type, project_id)

        # Assign work
        work.assigned_sprite = sprite.sprite_id
        work.status = "assigned"
        await self.state.save_work(tenant_id, work)

        # Send task to sprite via Redis
        self._send_task_to_sprite(sprite.sprite_id, work)

        logger.info(f"Work {work.work_id} assigned to sprite {sprite.sprite_id}")
        return work.work_id

    async def handle_work_complete(
        self,
        tenant_id: str,
        work_id: str,
        sprite_id: str,
        output: str,
        tokens_used: int
    ):
        """Handle work completion from a sprite."""
        work = await self.state.get_work(tenant_id, work_id)
        if work:
            work.status = "completed"
            work.output = output
            work.tokens_used = tokens_used
            work.completed_at = datetime.now(timezone.utc)
            await self.state.save_work(tenant_id, work)

            # Update tenant usage
            await self._track_usage(tenant_id, tokens_used)

            logger.info(f"Work {work_id} completed")

    async def handle_work_failed(
        self,
        tenant_id: str,
        work_id: str,
        sprite_id: str,
        error: str
    ):
        """Handle work failure from a sprite."""
        work = await self.state.get_work(tenant_id, work_id)
        if work:
            work.status = "failed"
            work.error = error
            work.completed_at = datetime.now(timezone.utc)
            await self.state.save_work(tenant_id, work)

            logger.error(f"Work {work_id} failed: {error}")

    # =========================================================================
    # Handoff Handling
    # =========================================================================

    async def handle_handoff_request(
        self,
        tenant_id: str,
        from_sprite: str,
        to_agent: AgentType,
        context: Dict[str, Any],
        project_id: Optional[str] = None
    ):
        """Handle a handoff request between agents."""
        logger.info(f"Handoff requested: {from_sprite} -> {to_agent}")

        # Find or spawn target sprite
        target_sprite = await self._get_or_spawn_sprite(
            tenant_id, to_agent, project_id
        )

        # Send handoff to target sprite
        self._send_handoff_to_sprite(target_sprite.sprite_id, {
            "from_sprite": from_sprite,
            "context": context,
            "project_id": project_id
        })

        logger.info(f"Handoff sent to sprite {target_sprite.sprite_id}")

    # =========================================================================
    # Project Management
    # =========================================================================

    async def start_project(
        self,
        tenant_id: str,
        name: str,
        brief: str,
        agents_needed: List[AgentType]
    ) -> str:
        """Start a new project and spawn required sprites."""

        project_id = f"proj-{int(datetime.now().timestamp() * 1000)}"

        # Save project
        project = {
            "id": project_id,
            "name": name,
            "brief": brief,
            "status": "starting",
            "agents_needed": [a.value for a in agents_needed],
            "created_at": datetime.now(timezone.utc)
        }

        await self.state.save_project(tenant_id, project)

        # Spawn sprites for the project
        for agent_type in agents_needed:
            try:
                await self.spawn_sprite(tenant_id, agent_type, project_id)
            except ValueError as e:
                logger.warning(f"Could not spawn {agent_type}: {e}")

        # Update project status
        project["status"] = "active"
        await self.state.save_project(tenant_id, project)

        logger.info(f"Project {project_id} started with {len(agents_needed)} agents")
        return project_id

    # =========================================================================
    # Tenant Management
    # =========================================================================

    async def get_tenant_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get current status for a tenant."""
        sprites = await self.state.get_active_sprites(tenant_id)
        usage = await self._get_tenant_usage(tenant_id)
        plan = await self._get_tenant_plan(tenant_id)

        return {
            "tenant_id": tenant_id,
            "plan": plan.name,
            "sprites": {
                "active": len([s for s in sprites if s.status != "stopped"]),
                "limit": plan.max_concurrent_sprites,
                "list": [asdict(s) for s in sprites]
            },
            "usage": {
                "tokens_used_this_month": usage.get("tokens", 0),
                "token_budget": plan.monthly_token_budget,
                "sprites_spawned_this_month": usage.get("sprites_spawned", 0)
            }
        }

    async def get_brand_context(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get brand context for a tenant."""
        return await self.state.get_brand_context(tenant_id)

    # =========================================================================
    # Private Helpers
    # =========================================================================

    async def _get_tenant_plan(self, tenant_id: str) -> TenantPlan:
        """Get the plan for a tenant."""
        tenant_doc = self.db.collection("tenants").document(tenant_id).get()
        if tenant_doc.exists:
            plan_name = tenant_doc.to_dict().get("plan", "starter")
            if plan_name == "growth":
                return TenantPlan.growth()
            elif plan_name == "enterprise":
                return TenantPlan.enterprise()
        return TenantPlan.starter()

    async def _get_or_spawn_sprite(
        self,
        tenant_id: str,
        agent_type: AgentType,
        project_id: Optional[str] = None
    ) -> SpriteRecord:
        """Get an idle sprite or spawn a new one."""
        active = await self.state.get_active_sprites(tenant_id)

        # Look for idle sprite of correct type
        for sprite in active:
            if sprite.agent_type == agent_type.value and sprite.status == "idle":
                return sprite

        # Spawn new one
        return await self.spawn_sprite(tenant_id, agent_type, project_id)

    def _infer_agent_type(self, task: Dict[str, Any]) -> AgentType:
        """Infer which agent should handle a task based on content."""
        description = task.get("description", "").lower()

        if any(w in description for w in ["strategy", "position", "competitor", "audience"]):
            return AgentType.STRATEGIST
        elif any(w in description for w in ["write", "copy", "headline", "email"]):
            return AgentType.COPYWRITER
        elif any(w in description for w in ["review", "edit", "polish", "proofread"]):
            return AgentType.EDITOR
        elif any(w in description for w in ["optimize", "cro", "conversion", "friction"]):
            return AgentType.OPTIMIZER
        elif any(w in description for w in ["analyze", "measure", "track", "data"]):
            return AgentType.ANALYST
        else:
            # Default to Director for orchestration
            return AgentType.DIRECTOR

    def _send_task_to_sprite(self, sprite_id: str, work: WorkRecord):
        """Send a task to a sprite via Redis."""
        channel = f"sprite:{sprite_id}:inbox"
        message = {
            "type": "task",
            "payload": {
                "id": work.work_id,
                "description": work.task.get("description"),
                "input": work.task.get("input"),
                "context": work.task.get("context")
            }
        }
        self.redis.publish(channel, json.dumps(message))

    def _send_handoff_to_sprite(self, sprite_id: str, handoff: Dict):
        """Send a handoff to a sprite via Redis."""
        channel = f"sprite:{sprite_id}:inbox"
        message = {
            "type": "handoff",
            "payload": handoff
        }
        self.redis.publish(channel, json.dumps(message))

    async def _track_usage(self, tenant_id: str, tokens: int):
        """Track token usage for a tenant."""
        usage_ref = self.db.collection("tenants").document(tenant_id).collection("usage").document("current")
        usage_ref.set({
            "tokens": firestore.Increment(tokens),
            "last_updated": datetime.now(timezone.utc)
        }, merge=True)

    async def _get_tenant_usage(self, tenant_id: str) -> Dict[str, int]:
        """Get current usage for a tenant."""
        usage_doc = self.db.collection("tenants").document(tenant_id).collection("usage").document("current").get()
        if usage_doc.exists:
            return usage_doc.to_dict()
        return {"tokens": 0, "sprites_spawned": 0}
