# Multi-Tenant Sprite Architecture

## Overview

Sprites are ephemeral agent containers that execute marketing work for tenants. Each tenant (organization) gets isolated sprite instances that can be spawned on-demand and coordinate as a swarm.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CONTROL PLANE (GCP)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Frontend   │  │   API        │  │   Coordinator        │   │
│  │  (SvelteKit) │──│  (FastAPI)   │──│   (Swarm Manager)    │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                            │                    │                │
│                            ▼                    │                │
│                    ┌──────────────┐             │                │
│                    │  Firestore   │◄────────────┘                │
│                    │  (State)     │                              │
└────────────────────┴──────────────┴──────────────────────────────┘
                            │
                            │ Fly.io API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA PLANE (Fly.io)                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Tenant: acme-corp                        ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    ││
│  │  │ Director │  │Strategist│  │Copywriter│  │  Editor  │    ││
│  │  │  Sprite  │──│  Sprite  │──│  Sprite  │──│  Sprite  │    ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Tenant: startup-xyz                      ││
│  │  ┌──────────┐  ┌──────────┐                                 ││
│  │  │ Director │  │Copywriter│  (smaller plan = fewer sprites) ││
│  │  │  Sprite  │──│  Sprite  │                                 ││
│  │  └──────────┘  └──────────┘                                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌──────────────┐                                               │
│  │ Upstash Redis│  (Inter-sprite pub/sub, tenant-scoped)       │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Tenant Model

### Hierarchy
```
Tenant (Organization)
├── Users (people who can access)
├── Projects (active work)
├── Sprites (running agents)
├── Brand Context (shared knowledge)
└── Config (plan, limits, settings)
```

### Firestore Schema
```
tenants/{tenant_id}
├── name: "Acme Corp"
├── plan: "growth"  # starter | growth | enterprise
├── config:
│   ├── enabled_agents: ["director", "strategist", "copywriter", "editor"]
│   ├── max_concurrent_sprites: 4
│   ├── sprite_idle_timeout_seconds: 300
│   └── monthly_token_budget: 10000000
├── brand:
│   ├── voice: "Professional but warm..."
│   ├── guidelines: "..."
│   └── context: {...}
├── usage:
│   ├── tokens_used_this_month: 1234567
│   └── sprites_spawned_this_month: 42
│
├── users/{user_id}
│   ├── email: "user@acme.com"
│   ├── role: "admin"  # admin | member | viewer
│   └── added_at: timestamp
│
├── projects/{project_id}
│   ├── name: "Q1 Launch Campaign"
│   ├── status: "active"
│   ├── brief: "..."
│   ├── sprites_assigned: ["sprite_abc", "sprite_def"]
│   └── deliverables: [...]
│
├── sprites/{sprite_id}
│   ├── agent_type: "copywriter"
│   ├── fly_machine_id: "e286de4f711986"
│   ├── status: "working"  # idle | working | blocked | stopped
│   ├── current_task: "Writing hero section"
│   ├── project_id: "project_123"
│   └── last_heartbeat: timestamp
│
└── work/{work_id}
    ├── type: "write_copy"
    ├── status: "in_progress"
    ├── assigned_sprite: "sprite_abc"
    ├── input: {...}
    ├── output: null
    ├── created_at: timestamp
    └── completed_at: null
```

## Sprite Lifecycle

### 1. Spawn
```python
# Coordinator receives work request
coordinator.spawn_sprite(
    tenant_id="acme-corp",
    agent_type="copywriter",
    project_id="project_123"
)

# Creates Fly machine via API
fly_machine = fly.machines.create(
    app_name="highera-sprites",
    config={
        "image": "registry.fly.io/highera-sprite:latest",
        "env": {
            "TENANT_ID": "acme-corp",
            "AGENT_TYPE": "copywriter",
            "PROJECT_ID": "project_123",
            "COORDINATOR_URL": "https://api.highera.com",
            "REDIS_URL": "redis://..."
        },
        "guest": {"cpu_kind": "shared", "cpus": 1, "memory_mb": 512},
        "auto_destroy": True,  # Clean up when stopped
    }
)

# Register in Firestore
db.collection("tenants/acme-corp/sprites").add({
    "agent_type": "copywriter",
    "fly_machine_id": fly_machine.id,
    "status": "starting",
    ...
})
```

### 2. Boot
```python
# sprite.py - runs inside container
class Sprite:
    def __init__(self):
        self.tenant_id = os.environ["TENANT_ID"]
        self.agent_type = os.environ["AGENT_TYPE"]
        self.project_id = os.environ["PROJECT_ID"]

        # Load persona
        self.persona = load_persona(self.agent_type)

        # Load tenant brand context
        self.brand = fetch_brand_context(self.tenant_id)

        # Connect to Redis for pub/sub
        self.redis = redis.from_url(os.environ["REDIS_URL"])
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(f"sprite:{self.id}:inbox")

        # Signal ready
        self.report_status("idle")

    def run(self):
        """Main loop - wait for work, execute, repeat."""
        while True:
            # Check for messages
            message = self.pubsub.get_message(timeout=1.0)
            if message and message["type"] == "message":
                task = json.loads(message["data"])
                self.execute_task(task)

            # Heartbeat
            self.heartbeat()

            # Check idle timeout
            if self.idle_too_long():
                self.shutdown()
```

### 3. Execute
```python
def execute_task(self, task):
    self.report_status("working", task["description"])

    try:
        # Build prompt with persona + brand + task
        prompt = self.build_prompt(task)

        # Call Claude
        response = anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=self.persona.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse output
        output = self.parse_response(response)

        # Check for handoff requests
        if output.needs_handoff:
            self.request_handoff(output.handoff_to, output.handoff_context)

        # Report completion
        self.complete_task(task["id"], output)

    except Exception as e:
        self.fail_task(task["id"], str(e))

    self.report_status("idle")
```

### 4. Handoff
```python
def request_handoff(self, target_agent: str, context: dict):
    """Request work handoff to another agent type."""
    # Publish to coordinator
    self.redis.publish(f"tenant:{self.tenant_id}:handoffs", json.dumps({
        "from_sprite": self.id,
        "from_agent": self.agent_type,
        "to_agent": target_agent,
        "project_id": self.project_id,
        "context": context
    }))
```

### 5. Shutdown
```python
def shutdown(self):
    """Clean shutdown - unsubscribe, report, exit."""
    self.pubsub.unsubscribe()
    self.report_status("stopped")
    # Fly will auto-destroy the machine
    sys.exit(0)
```

## Inter-Sprite Communication

### Pub/Sub Channels (Redis)
```
# Per-sprite inbox (direct messages)
sprite:{sprite_id}:inbox

# Tenant-wide channels
tenant:{tenant_id}:handoffs     # Handoff requests
tenant:{tenant_id}:reviews      # Review requests
tenant:{tenant_id}:broadcasts   # Announcements

# Project channels
project:{project_id}:updates    # Project status updates
```

### Message Types
```python
# Task assignment
{
    "type": "task",
    "id": "work_abc123",
    "description": "Write hero section",
    "input": {...},
    "deadline": null
}

# Handoff request
{
    "type": "handoff",
    "from_agent": "copywriter",
    "to_agent": "editor",
    "context": {
        "copy": "...",
        "notes": "Please check tone"
    }
}

# Review request
{
    "type": "review",
    "from_agent": "copywriter",
    "artifact": "hero_copy_v1",
    "content": "...",
    "questions": ["Is the CTA strong enough?"]
}

# Status broadcast
{
    "type": "status",
    "sprite_id": "...",
    "agent_type": "copywriter",
    "status": "working",
    "current_task": "Writing hero section"
}
```

## Coordinator API

### New Endpoints
```python
# Spawn a sprite for a tenant
POST /tenants/{tenant_id}/sprites
{
    "agent_type": "copywriter",
    "project_id": "optional"
}

# List active sprites
GET /tenants/{tenant_id}/sprites

# Stop a sprite
DELETE /tenants/{tenant_id}/sprites/{sprite_id}

# Send work to a sprite
POST /tenants/{tenant_id}/sprites/{sprite_id}/work
{
    "type": "write_copy",
    "input": {...}
}

# Get sprite status
GET /tenants/{tenant_id}/sprites/{sprite_id}

# Start a project (spawns required sprites)
POST /tenants/{tenant_id}/projects
{
    "name": "Q1 Campaign",
    "brief": "...",
    "agents_needed": ["director", "strategist", "copywriter"]
}
```

## Tenant Plans

| Feature | Starter | Growth | Enterprise |
|---------|---------|--------|------------|
| Concurrent sprites | 2 | 4 | 10 |
| Agent types | 3 | All | All |
| Monthly tokens | 1M | 10M | Unlimited |
| Sprite idle timeout | 60s | 300s | 3600s |
| Priority routing | No | Yes | Yes |
| Custom personas | No | No | Yes |
| SSO | No | No | Yes |

## Security

### Tenant Isolation
- Sprites can only access their tenant's data
- Redis channels are tenant-scoped
- Fly machines are tagged with tenant_id
- All API calls validate tenant membership

### Secrets
- `ANTHROPIC_API_KEY` - Shared (or per-tenant for enterprise)
- `FLY_API_TOKEN` - For spawning machines
- `REDIS_URL` - Upstash connection
- `COORDINATOR_SECRET` - Sprite-to-coordinator auth

### Network
- Sprites communicate via Fly private network
- Redis accessible only from Fly network
- Coordinator exposed via Cloud Run (public API with auth)

## Deployment

### Fly.io Setup
```bash
# Create the sprites app
fly apps create highera-sprites

# Set secrets
fly secrets set ANTHROPIC_API_KEY=... REDIS_URL=... COORDINATOR_URL=...

# Deploy sprite image
fly deploy --dockerfile agency/runtime/Dockerfile

# Machines are spawned on-demand via API, not fly deploy
```

### Directory Structure
```
agency/
├── runtime/
│   ├── sprite.py           # Main sprite runtime
│   ├── persona.py          # Persona loader
│   ├── executor.py         # Claude API wrapper
│   ├── comms.py            # Redis pub/sub
│   ├── Dockerfile          # Sprite container
│   ├── fly.toml            # Fly.io config
│   └── requirements.txt    # Python deps
│
├── swarm/
│   ├── coordinator.py      # Swarm orchestration
│   ├── spawner.py          # Fly machine management
│   ├── router.py           # Work routing
│   └── state.py            # Firestore state management
│
├── agents/                 # Persona definitions (existing)
│   ├── director.md
│   ├── strategist.md
│   └── ...
│
└── ARCHITECTURE.md         # This file
```
