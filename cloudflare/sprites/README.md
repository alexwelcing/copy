# High Era Agency - Cloudflare Sprite Runtime

AI agent runtime using Cloudflare Durable Objects.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Worker (Edge)                        │
│  Routes requests to Durable Objects                     │
└─────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Swarm     │  │   Sprite    │  │   Sprite    │
│ Coordinator │  │ (Director)  │  │(Copywriter) │
│     DO      │  │     DO      │  │     DO      │
└─────────────┘  └─────────────┘  └─────────────┘
         │                │                │
         └────────────────┼────────────────┘
                          ▼
                    ┌──────────┐
                    │    R2    │
                    │ (Assets) │
                    └──────────┘
```

**Durable Objects:**
- **Sprite**: Individual AI agent with state, WebSocket support
- **SwarmCoordinator**: Manages sprites for a tenant, routes work

**External APIs:**
- Claude API (Anthropic) for agent intelligence
- Fal API for image generation
- R2 for asset storage

## Setup

```bash
# Install dependencies
npm install

# Login to Cloudflare
npx wrangler login

# Create R2 bucket
npx wrangler r2 bucket create highera-assets

# Set secrets
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put FAL_API_KEY

# Deploy
npm run deploy
```

## API

### Tenant Operations

**Initialize Tenant**
```bash
curl -X POST https://highera-sprites.<account>.workers.dev/tenant/TENANT_ID/init \
  -H "Content-Type: application/json" \
  -d '{"tenantId": "TENANT_ID"}'
```

**Spawn Sprite**
```bash
curl -X POST https://highera-sprites.<account>.workers.dev/tenant/TENANT_ID/spawn \
  -H "Content-Type: application/json" \
  -d '{
    "tenantId": "TENANT_ID",
    "agentType": "copywriter",
    "brandContext": {
      "voice": "Professional yet approachable",
      "tone": "Confident",
      "audience": "B2B decision makers",
      "guidelines": ["No jargon", "Lead with value"]
    }
  }'
```

**Submit Work**
```bash
curl -X POST https://highera-sprites.<account>.workers.dev/tenant/TENANT_ID/work \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "id": "task-123",
      "description": "Write a hero section for our AI platform landing page"
    },
    "agentType": "copywriter"
  }'
```

**List Sprites**
```bash
curl https://highera-sprites.<account>.workers.dev/tenant/TENANT_ID/sprites
```

### Sprite Operations

**Get Status**
```bash
curl https://highera-sprites.<account>.workers.dev/sprite/TENANT_ID/SPRITE_ID/status
```

**Submit Work Directly**
```bash
curl -X POST https://highera-sprites.<account>.workers.dev/sprite/TENANT_ID/SPRITE_ID/work \
  -H "Content-Type: application/json" \
  -d '{
    "id": "task-456",
    "description": "Edit this copy for clarity..."
  }'
```

**Generate Image**
```bash
curl -X POST https://highera-sprites.<account>.workers.dev/sprite/TENANT_ID/SPRITE_ID/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Abstract golden light on navy background, premium aesthetic",
    "outputPath": "pitch/cover.png"
  }'
```

**WebSocket Connection**
```javascript
const ws = new WebSocket(
  'wss://highera-sprites.<account>.workers.dev/sprite/TENANT_ID/SPRITE_ID'
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Sprite event:', data);
  // { type: 'working', taskId: '...' }
  // { type: 'complete', taskId: '...', output: '...' }
};
```

## Agent Types

| Type | Role | Triggers |
|------|------|----------|
| `director` | Orchestrates projects | Default for ambiguous tasks |
| `strategist` | Positioning, psychology | "strategy", "position", "competitor" |
| `copywriter` | Headlines, pages, emails | "write", "copy", "headline" |
| `editor` | Polish, consistency | "edit", "review", "polish" |
| `optimizer` | CRO, conversions | "convert", "optimize", "cro" |
| `analyst` | Tracking, measurement | "track", "measure", "analytics" |

## Development

```bash
# Local development
npm run dev

# Tail logs
npm run tail

# Generate types from wrangler.toml
npm run types
```

## Cost Estimate

- **Durable Objects**: $0.15/million requests + $0.50/GB-month storage
- **Workers**: Free tier covers 100k requests/day
- **R2**: $0.015/GB-month storage, free egress

For typical usage (1000 agent tasks/day):
- ~$5/month Durable Objects
- ~$1/month R2 storage
- Claude/Fal API costs (variable)

## Comparison to Fly.io

| Aspect | Fly.io (Previous) | Cloudflare (New) |
|--------|-------------------|------------------|
| Cold start | ~2-5s VM boot | <50ms DO wake |
| State | Redis required | Built into DO |
| WebSocket | Manual setup | Native in DO |
| Scaling | Manual machines | Automatic |
| Network | Intra-VM | Global edge |
| Cost | ~$5/VM/month | Pay per request |
