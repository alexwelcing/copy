"""
Swarm API Endpoints

FastAPI routes for managing sprites and tenant swarms.
"""

import os
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel

from service.core.auth import get_current_user
from service.core.db import get_db

# Import swarm components
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from agency.swarm import (
    SwarmCoordinator,
    AgentType,
    FlySpawner,
    TenantState,
    SpriteRecord,
    BrandContext
)

router = APIRouter(prefix="/swarm", tags=["swarm"])


# ============================================================================
# Request/Response Models
# ============================================================================

class SpawnRequest(BaseModel):
    agent_type: str
    project_id: Optional[str] = None


class SpawnResponse(BaseModel):
    sprite_id: str
    agent_type: str
    status: str
    fly_machine_id: str


class WorkSubmitRequest(BaseModel):
    description: str
    input: Optional[dict] = None
    context: Optional[dict] = None
    agent_type: Optional[str] = None
    project_id: Optional[str] = None


class WorkResponse(BaseModel):
    work_id: str
    status: str


class ProjectCreateRequest(BaseModel):
    name: str
    brief: str
    agents_needed: List[str]


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    status: str
    agents_spawned: int


class BrandContextRequest(BaseModel):
    voice: Optional[str] = None
    tone: Optional[str] = None
    audience: Optional[str] = None
    guidelines: Optional[str] = None
    keywords: Optional[List[str]] = None
    avoid: Optional[List[str]] = None


class TenantStatusResponse(BaseModel):
    tenant_id: str
    plan: str
    sprites_active: int
    sprites_limit: int
    tokens_used: int
    token_budget: int


# ============================================================================
# Dependency: Get Coordinator
# ============================================================================

_coordinator: Optional[SwarmCoordinator] = None


def get_coordinator() -> SwarmCoordinator:
    """Get or create the swarm coordinator singleton."""
    global _coordinator

    if _coordinator is None:
        import redis
        from google.cloud import firestore

        db = firestore.Client()
        redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))
        fly_spawner = FlySpawner(
            app_name=os.environ.get("FLY_APP_NAME", "highera-sprites"),
            api_token=os.environ.get("FLY_API_TOKEN")
        )

        _coordinator = SwarmCoordinator(db, redis_client, fly_spawner)

    return _coordinator


# ============================================================================
# Tenant Endpoints
# ============================================================================

@router.get("/status", response_model=TenantStatusResponse)
async def get_tenant_status(
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Get current swarm status for the authenticated tenant."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    status = await coordinator.get_tenant_status(tenant_id)

    return TenantStatusResponse(
        tenant_id=status["tenant_id"],
        plan=status["plan"],
        sprites_active=status["sprites"]["active"],
        sprites_limit=status["sprites"]["limit"],
        tokens_used=status["usage"]["tokens_used_this_month"],
        token_budget=status["usage"]["token_budget"]
    )


@router.get("/brand")
async def get_brand_context(
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Get brand context for the tenant."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    brand = await coordinator.get_brand_context(tenant_id)
    return brand or {}


@router.put("/brand")
async def update_brand_context(
    request: BrandContextRequest,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Update brand context for the tenant."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    brand = BrandContext(
        voice=request.voice,
        tone=request.tone,
        audience=request.audience,
        guidelines=request.guidelines,
        keywords=request.keywords or [],
        avoid=request.avoid or []
    )

    await coordinator.state.save_brand_context(tenant_id, brand)
    return {"status": "updated"}


# ============================================================================
# Sprite Endpoints
# ============================================================================

@router.get("/sprites")
async def list_sprites(
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """List active sprites for the tenant."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    sprites = await coordinator.state.get_active_sprites(tenant_id)
    return {"sprites": [
        {
            "sprite_id": s.sprite_id,
            "agent_type": s.agent_type,
            "status": s.status,
            "current_task": s.current_task,
            "tasks_completed": s.tasks_completed,
            "tokens_used": s.tokens_used
        }
        for s in sprites
    ]}


@router.post("/sprites", response_model=SpawnResponse)
async def spawn_sprite(
    request: SpawnRequest,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Spawn a new sprite."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    try:
        agent_type = AgentType(request.agent_type)
    except ValueError:
        raise HTTPException(400, f"Invalid agent type: {request.agent_type}")

    try:
        sprite = await coordinator.spawn_sprite(
            tenant_id=tenant_id,
            agent_type=agent_type,
            project_id=request.project_id
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    return SpawnResponse(
        sprite_id=sprite.sprite_id,
        agent_type=sprite.agent_type,
        status=sprite.status,
        fly_machine_id=sprite.fly_machine_id
    )


@router.delete("/sprites/{sprite_id}")
async def stop_sprite(
    sprite_id: str,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Stop a sprite."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    try:
        await coordinator.stop_sprite(tenant_id, sprite_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

    return {"status": "stopped"}


@router.post("/sprites/{sprite_id}/heartbeat")
async def sprite_heartbeat(
    sprite_id: str,
    status: str,
    tasks_completed: int = 0,
    tokens_used: int = 0,
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Receive heartbeat from a sprite (internal use)."""
    # Extract tenant from sprite ID or require it
    # For now, parse from sprite_id format: sprite-{tenant[:8]}-{agent}-{random}
    parts = sprite_id.split("-")
    if len(parts) < 3:
        raise HTTPException(400, "Invalid sprite ID format")

    # TODO: Proper tenant lookup from sprite record
    await coordinator.handle_sprite_heartbeat(
        tenant_id="unknown",  # Would need to look this up
        sprite_id=sprite_id,
        status=status,
        tasks_completed=tasks_completed,
        tokens_used=tokens_used
    )

    return {"status": "ok"}


# ============================================================================
# Work Endpoints
# ============================================================================

@router.post("/work", response_model=WorkResponse)
async def submit_work(
    request: WorkSubmitRequest,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Submit work to be executed by a sprite."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    agent_type = None
    if request.agent_type:
        try:
            agent_type = AgentType(request.agent_type)
        except ValueError:
            raise HTTPException(400, f"Invalid agent type: {request.agent_type}")

    task = {
        "description": request.description,
        "input": request.input,
        "context": request.context
    }

    work_id = await coordinator.submit_work(
        tenant_id=tenant_id,
        task=task,
        agent_type=agent_type,
        project_id=request.project_id
    )

    return WorkResponse(work_id=work_id, status="assigned")


@router.get("/work/{work_id}")
async def get_work_status(
    work_id: str,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Get status of a work item."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    work = await coordinator.state.get_work(tenant_id, work_id)
    if not work:
        raise HTTPException(404, "Work not found")

    return {
        "work_id": work.work_id,
        "status": work.status,
        "agent_type": work.agent_type,
        "assigned_sprite": work.assigned_sprite,
        "output": work.output,
        "error": work.error,
        "tokens_used": work.tokens_used
    }


@router.post("/work/{work_id}/complete")
async def complete_work(
    work_id: str,
    sprite_id: str,
    output: str,
    tokens_used: int = 0,
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Mark work as complete (called by sprites)."""
    # Extract tenant from work record
    # TODO: Proper implementation
    await coordinator.handle_work_complete(
        tenant_id="unknown",
        work_id=work_id,
        sprite_id=sprite_id,
        output=output,
        tokens_used=tokens_used
    )

    return {"status": "ok"}


@router.post("/work/{work_id}/fail")
async def fail_work(
    work_id: str,
    sprite_id: str,
    error: str,
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Mark work as failed (called by sprites)."""
    await coordinator.handle_work_failed(
        tenant_id="unknown",
        work_id=work_id,
        sprite_id=sprite_id,
        error=error
    )

    return {"status": "ok"}


# ============================================================================
# Project Endpoints
# ============================================================================

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    request: ProjectCreateRequest,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Create a new project and spawn required agents."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    agents = []
    for agent_name in request.agents_needed:
        try:
            agents.append(AgentType(agent_name))
        except ValueError:
            raise HTTPException(400, f"Invalid agent type: {agent_name}")

    project_id = await coordinator.start_project(
        tenant_id=tenant_id,
        name=request.name,
        brief=request.brief,
        agents_needed=agents
    )

    return ProjectResponse(
        project_id=project_id,
        name=request.name,
        status="active",
        agents_spawned=len(agents)
    )


@router.get("/projects")
async def list_projects(
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """List active projects for the tenant."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    projects = await coordinator.state.get_active_projects(tenant_id)
    return {"projects": projects}


@router.get("/projects/{project_id}")
async def get_project(
    project_id: str,
    user_info: tuple[str, bool] = Depends(get_current_user),
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Get project details."""
    user_id, _ = user_info
    tenant_id = await _get_tenant_for_user(user_id)

    project = await coordinator.state.get_project(tenant_id, project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    return project


# ============================================================================
# Handoff Endpoints
# ============================================================================

@router.post("/handoffs")
async def request_handoff(
    from_sprite: str,
    to_agent: str,
    context: dict,
    project_id: Optional[str] = None,
    coordinator: SwarmCoordinator = Depends(get_coordinator)
):
    """Handle a handoff request from a sprite."""
    try:
        agent_type = AgentType(to_agent)
    except ValueError:
        raise HTTPException(400, f"Invalid agent type: {to_agent}")

    # TODO: Get tenant from sprite record
    await coordinator.handle_handoff_request(
        tenant_id="unknown",
        from_sprite=from_sprite,
        to_agent=agent_type,
        context=context,
        project_id=project_id
    )

    return {"status": "ok"}


# ============================================================================
# Helpers
# ============================================================================

async def _get_tenant_for_user(user_id: str) -> str:
    """
    Get tenant ID for a user.

    In a real implementation, this would look up the user's organization.
    For now, we use the user_id as the tenant_id (single-user tenants).
    """
    # TODO: Implement proper tenant lookup
    # - Check users collection for tenant membership
    # - Support multiple users per tenant
    # - Handle tenant creation for new users

    return user_id
