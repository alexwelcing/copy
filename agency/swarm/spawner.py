"""
Fly.io Machine Spawner

Manages sprite machines on Fly.io via the Machines API.
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)


@dataclass
class SpawnConfig:
    """Configuration for spawning a sprite."""
    tenant_id: str
    agent_type: str
    project_id: Optional[str]
    idle_timeout: int
    coordinator_url: str
    redis_url: str
    anthropic_api_key: str


@dataclass
class FlyMachine:
    """Represents a Fly.io machine."""
    id: str
    name: str
    state: str
    region: str
    instance_id: str
    private_ip: str


class FlySpawner:
    """
    Spawns and manages sprite machines on Fly.io.

    Uses the Fly Machines API:
    https://fly.io/docs/machines/api/
    """

    API_BASE = "https://api.machines.dev/v1"

    def __init__(
        self,
        app_name: str = "highera-sprites",
        api_token: Optional[str] = None,
        image: Optional[str] = None,
        region: str = "iad"
    ):
        self.app_name = app_name
        self.api_token = api_token or os.environ.get("FLY_API_TOKEN")
        self.image = image or f"registry.fly.io/{app_name}:latest"
        self.region = region

        if not self.api_token:
            raise ValueError("FLY_API_TOKEN is required")

        self.client = httpx.AsyncClient(
            base_url=f"{self.API_BASE}/apps/{app_name}",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )

    async def spawn(self, config: SpawnConfig) -> FlyMachine:
        """Spawn a new sprite machine."""

        sprite_id = f"sprite-{config.tenant_id[:8]}-{config.agent_type}-{os.urandom(4).hex()}"

        machine_config = {
            "name": sprite_id,
            "region": self.region,
            "config": {
                "image": self.image,
                "env": {
                    "SPRITE_ID": sprite_id,
                    "TENANT_ID": config.tenant_id,
                    "AGENT_TYPE": config.agent_type,
                    "PROJECT_ID": config.project_id or "",
                    "COORDINATOR_URL": config.coordinator_url,
                    "REDIS_URL": config.redis_url,
                    "ANTHROPIC_API_KEY": config.anthropic_api_key,
                    "IDLE_TIMEOUT": str(config.idle_timeout),
                },
                "guest": {
                    "cpu_kind": "shared",
                    "cpus": 1,
                    "memory_mb": 512
                },
                "auto_destroy": True,  # Clean up when stopped
                "restart": {
                    "policy": "no"  # Don't auto-restart, coordinator will respawn if needed
                },
                "metadata": {
                    "tenant_id": config.tenant_id,
                    "agent_type": config.agent_type,
                    "managed_by": "highera-coordinator"
                }
            }
        }

        logger.info(f"Spawning machine: {sprite_id}")

        response = await self.client.post("/machines", json=machine_config)
        response.raise_for_status()

        data = response.json()

        return FlyMachine(
            id=data["id"],
            name=data["name"],
            state=data["state"],
            region=data["region"],
            instance_id=data.get("instance_id", ""),
            private_ip=data.get("private_ip", "")
        )

    async def stop(self, machine_id: str):
        """Stop a machine."""
        logger.info(f"Stopping machine: {machine_id}")

        response = await self.client.post(f"/machines/{machine_id}/stop")
        response.raise_for_status()

    async def destroy(self, machine_id: str):
        """Destroy a machine permanently."""
        logger.info(f"Destroying machine: {machine_id}")

        response = await self.client.delete(f"/machines/{machine_id}?force=true")
        response.raise_for_status()

    async def get_machine(self, machine_id: str) -> Optional[FlyMachine]:
        """Get machine details."""
        try:
            response = await self.client.get(f"/machines/{machine_id}")
            response.raise_for_status()
            data = response.json()

            return FlyMachine(
                id=data["id"],
                name=data["name"],
                state=data["state"],
                region=data["region"],
                instance_id=data.get("instance_id", ""),
                private_ip=data.get("private_ip", "")
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def list_machines(self, tenant_id: Optional[str] = None) -> list[FlyMachine]:
        """List all machines, optionally filtered by tenant."""
        response = await self.client.get("/machines")
        response.raise_for_status()

        machines = []
        for data in response.json():
            # Filter by tenant if specified
            if tenant_id:
                metadata = data.get("config", {}).get("metadata", {})
                if metadata.get("tenant_id") != tenant_id:
                    continue

            machines.append(FlyMachine(
                id=data["id"],
                name=data["name"],
                state=data["state"],
                region=data["region"],
                instance_id=data.get("instance_id", ""),
                private_ip=data.get("private_ip", "")
            ))

        return machines

    async def cleanup_stale_machines(self, max_age_hours: int = 24):
        """Clean up machines that have been stopped for too long."""
        machines = await self.list_machines()

        for machine in machines:
            if machine.state == "stopped":
                # In production, check created_at/updated_at timestamps
                logger.info(f"Cleaning up stale machine: {machine.id}")
                await self.destroy(machine.id)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
