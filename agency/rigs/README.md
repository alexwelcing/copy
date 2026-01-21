# Rigs: Project Containers

Rigs are project containers that wrap marketing campaigns and client work, providing isolated workspaces with their own context and assets.

## Structure

```
rigs/
├── README.md
├── [project-name]/
│   ├── rig.json        # Rig configuration
│   ├── brief.md        # Project brief
│   ├── brand/          # Brand assets and guidelines
│   ├── assets/         # Marketing assets
│   ├── outputs/        # Generated deliverables
│   └── convoys/        # Project-specific convoys
```

## Rig Configuration

```json
{
  "name": "acme-product-launch",
  "client": "Acme Corp",
  "created": "2024-01-15",
  "status": "active",
  "brief": "./brief.md",
  "brand": {
    "guidelines": "./brand/guidelines.md",
    "assets": "./brand/",
    "voice": "professional, innovative, approachable"
  },
  "team": {
    "lead": "mayor",
    "polecats": []
  },
  "settings": {
    "autoReview": true,
    "requireApproval": true
  }
}
```

## Creating a Rig

### Command

```bash
/agency rig create "Project Name" --client "Client Name"
```

### This creates:

1. Project directory structure
2. Initial rig.json configuration
3. Brief template to fill out
4. Brand guidelines template
5. Asset directories

## Rig Workflow

### 1. Setup

```bash
# Create the rig
/agency rig create "Q1 Launch Campaign" --client "TechCo"

# Add brand context
# Edit rigs/q1-launch-campaign/brand/guidelines.md
```

### 2. Brief

```bash
# Fill out the brief
# Edit rigs/q1-launch-campaign/brief.md

# Have Mayor analyze
/agency brief analyze q1-launch-campaign
```

### 3. Execute

```bash
# Mayor creates convoy and assigns work
# Polecats execute tasks
# Outputs saved to rigs/q1-launch-campaign/outputs/
```

### 4. Deliver

```bash
# Review all deliverables
/agency rig review q1-launch-campaign

# Export final package
/agency rig export q1-launch-campaign
```

## Brand Context

Each rig can have client-specific brand information:

### guidelines.md

```markdown
# Brand Guidelines: [Client Name]

## Voice & Tone
- Primary voice: [description]
- Tone variations: [contexts]

## Visual Identity
- Primary colors: [hex codes]
- Fonts: [font names]
- Logo usage: [rules]

## Messaging
- Key messages: [list]
- Value propositions: [list]
- Prohibited terms: [list]

## Examples
- Good: [examples]
- Avoid: [examples]
```

## Multi-Project Management

### List Rigs

```bash
/agency rig list
# Shows all rigs with status
```

### Switch Context

```bash
/agency rig use "project-name"
# Sets active rig for subsequent commands
```

### Archive

```bash
/agency rig archive "project-name"
# Moves to archived state, preserves history
```

## Best Practices

1. **One rig per client/campaign** - Keep work organized
2. **Complete brand context** - Better outputs with more context
3. **Detailed briefs** - Clear requirements = better results
4. **Regular backups** - Export rigs periodically
5. **Clean handoffs** - Use export for client deliverables
