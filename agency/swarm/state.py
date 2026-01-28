"""
Tenant State Management

Manages tenant, sprite, and work state in Firestore.
"""

import logging
from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List
from google.cloud import firestore

logger = logging.getLogger(__name__)


@dataclass
class SpriteRecord:
    """Record of a sprite in Firestore."""
    sprite_id: str
    tenant_id: str
    agent_type: str
    fly_machine_id: str
    status: str  # starting | idle | working | blocked | stopped
    project_id: Optional[str] = None
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tokens_used: int = 0
    created_at: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None


@dataclass
class WorkRecord:
    """Record of a work item in Firestore."""
    work_id: str
    tenant_id: str
    task: Dict[str, Any]
    agent_type: str
    status: str  # pending | assigned | in_progress | completed | failed
    project_id: Optional[str] = None
    assigned_sprite: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    tokens_used: int = 0
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class TenantConfig:
    """Tenant configuration."""
    tenant_id: str
    name: str
    plan: str  # starter | growth | enterprise
    enabled_agents: List[str] = field(default_factory=list)
    max_concurrent_sprites: int = 2
    sprite_idle_timeout: int = 300
    monthly_token_budget: int = 1_000_000


@dataclass
class BrandContext:
    """Tenant brand context."""
    voice: Optional[str] = None
    tone: Optional[str] = None
    audience: Optional[str] = None
    guidelines: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    avoid: List[str] = field(default_factory=list)


class TenantState:
    """
    Manages tenant state in Firestore.

    Schema:
    tenants/{tenant_id}
    ├── config: TenantConfig
    ├── brand: BrandContext
    ├── sprites/{sprite_id}: SpriteRecord
    ├── work/{work_id}: WorkRecord
    └── projects/{project_id}: Project
    """

    def __init__(self, db: firestore.Client):
        self.db = db

    # =========================================================================
    # Sprites
    # =========================================================================

    async def save_sprite(self, tenant_id: str, sprite: SpriteRecord):
        """Save or update a sprite record."""
        ref = self.db.collection("tenants").document(tenant_id).collection("sprites").document(sprite.sprite_id)

        data = asdict(sprite)
        # Convert datetime to Firestore timestamp
        if data.get("created_at"):
            data["created_at"] = data["created_at"]
        if data.get("last_heartbeat"):
            data["last_heartbeat"] = data["last_heartbeat"]

        ref.set(data, merge=True)

    async def get_sprite(self, tenant_id: str, sprite_id: str) -> Optional[SpriteRecord]:
        """Get a sprite by ID."""
        ref = self.db.collection("tenants").document(tenant_id).collection("sprites").document(sprite_id)
        doc = ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        return SpriteRecord(**data)

    async def get_active_sprites(self, tenant_id: str) -> List[SpriteRecord]:
        """Get all active (non-stopped) sprites for a tenant."""
        ref = self.db.collection("tenants").document(tenant_id).collection("sprites")
        docs = ref.where("status", "!=", "stopped").stream()

        sprites = []
        for doc in docs:
            data = doc.to_dict()
            sprites.append(SpriteRecord(**data))

        return sprites

    async def delete_sprite(self, tenant_id: str, sprite_id: str):
        """Delete a sprite record."""
        ref = self.db.collection("tenants").document(tenant_id).collection("sprites").document(sprite_id)
        ref.delete()

    # =========================================================================
    # Work
    # =========================================================================

    async def save_work(self, tenant_id: str, work: WorkRecord):
        """Save or update a work record."""
        ref = self.db.collection("tenants").document(tenant_id).collection("work").document(work.work_id)

        data = asdict(work)
        ref.set(data, merge=True)

    async def get_work(self, tenant_id: str, work_id: str) -> Optional[WorkRecord]:
        """Get a work record by ID."""
        ref = self.db.collection("tenants").document(tenant_id).collection("work").document(work_id)
        doc = ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        return WorkRecord(**data)

    async def get_pending_work(self, tenant_id: str, agent_type: Optional[str] = None) -> List[WorkRecord]:
        """Get pending work for a tenant, optionally filtered by agent type."""
        ref = self.db.collection("tenants").document(tenant_id).collection("work")
        query = ref.where("status", "==", "pending")

        if agent_type:
            query = query.where("agent_type", "==", agent_type)

        docs = query.order_by("created_at").stream()

        return [WorkRecord(**doc.to_dict()) for doc in docs]

    # =========================================================================
    # Projects
    # =========================================================================

    async def save_project(self, tenant_id: str, project: Dict[str, Any]):
        """Save or update a project."""
        project_id = project.get("id")
        ref = self.db.collection("tenants").document(tenant_id).collection("projects").document(project_id)
        ref.set(project, merge=True)

    async def get_project(self, tenant_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        """Get a project by ID."""
        ref = self.db.collection("tenants").document(tenant_id).collection("projects").document(project_id)
        doc = ref.get()

        if not doc.exists:
            return None

        return doc.to_dict()

    async def get_active_projects(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all active projects for a tenant."""
        ref = self.db.collection("tenants").document(tenant_id).collection("projects")
        docs = ref.where("status", "==", "active").stream()

        return [doc.to_dict() for doc in docs]

    # =========================================================================
    # Tenant Config
    # =========================================================================

    async def get_tenant_config(self, tenant_id: str) -> Optional[TenantConfig]:
        """Get tenant configuration."""
        ref = self.db.collection("tenants").document(tenant_id)
        doc = ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        return TenantConfig(
            tenant_id=tenant_id,
            name=data.get("name", "Unknown"),
            plan=data.get("plan", "starter"),
            enabled_agents=data.get("config", {}).get("enabled_agents", []),
            max_concurrent_sprites=data.get("config", {}).get("max_concurrent_sprites", 2),
            sprite_idle_timeout=data.get("config", {}).get("sprite_idle_timeout", 300),
            monthly_token_budget=data.get("config", {}).get("monthly_token_budget", 1_000_000)
        )

    async def save_tenant_config(self, config: TenantConfig):
        """Save tenant configuration."""
        ref = self.db.collection("tenants").document(config.tenant_id)
        ref.set({
            "name": config.name,
            "plan": config.plan,
            "config": {
                "enabled_agents": config.enabled_agents,
                "max_concurrent_sprites": config.max_concurrent_sprites,
                "sprite_idle_timeout": config.sprite_idle_timeout,
                "monthly_token_budget": config.monthly_token_budget
            }
        }, merge=True)

    # =========================================================================
    # Brand Context
    # =========================================================================

    async def get_brand_context(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get brand context for a tenant."""
        ref = self.db.collection("tenants").document(tenant_id)
        doc = ref.get()

        if not doc.exists:
            return None

        data = doc.to_dict()
        return data.get("brand")

    async def save_brand_context(self, tenant_id: str, brand: BrandContext):
        """Save brand context for a tenant."""
        ref = self.db.collection("tenants").document(tenant_id)
        ref.set({"brand": asdict(brand)}, merge=True)

    # =========================================================================
    # Usage Tracking
    # =========================================================================

    async def increment_usage(self, tenant_id: str, tokens: int = 0, sprites: int = 0):
        """Increment usage counters for a tenant."""
        ref = self.db.collection("tenants").document(tenant_id)
        ref.set({
            "usage": {
                "tokens_used_this_month": firestore.Increment(tokens),
                "sprites_spawned_this_month": firestore.Increment(sprites),
                "last_updated": datetime.now(timezone.utc)
            }
        }, merge=True)

    async def get_usage(self, tenant_id: str) -> Dict[str, int]:
        """Get current usage for a tenant."""
        ref = self.db.collection("tenants").document(tenant_id)
        doc = ref.get()

        if not doc.exists:
            return {"tokens_used_this_month": 0, "sprites_spawned_this_month": 0}

        return doc.to_dict().get("usage", {})

    async def reset_monthly_usage(self, tenant_id: str):
        """Reset monthly usage counters (call on billing cycle)."""
        ref = self.db.collection("tenants").document(tenant_id)
        ref.set({
            "usage": {
                "tokens_used_this_month": 0,
                "sprites_spawned_this_month": 0,
                "last_reset": datetime.now(timezone.utc)
            }
        }, merge=True)
