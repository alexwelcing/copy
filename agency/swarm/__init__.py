"""
Swarm Coordinator Package

Manages sprite lifecycle and work distribution.
"""

from .coordinator import SwarmCoordinator, AgentType, TenantPlan
from .spawner import FlySpawner, SpawnConfig, FlyMachine
from .state import TenantState, SpriteRecord, WorkRecord, TenantConfig, BrandContext

__all__ = [
    "SwarmCoordinator",
    "AgentType",
    "TenantPlan",
    "FlySpawner",
    "SpawnConfig",
    "FlyMachine",
    "TenantState",
    "SpriteRecord",
    "WorkRecord",
    "TenantConfig",
    "BrandContext"
]
