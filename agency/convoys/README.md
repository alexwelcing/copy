# Convoys: Work Tracking System

Convoys are the primary work tracking mechanism in the Agency. Each convoy represents a project or campaign and contains multiple beads (work units).

## Structure

```
convoys/
├── README.md
├── active/           # Currently in-progress convoys
├── completed/        # Finished convoys
└── templates/        # Convoy templates
```

## Convoy Format

Each convoy is a JSON file:

```json
{
  "id": "convoy-abc12",
  "name": "Product Launch Campaign",
  "created": "2024-01-15T10:00:00Z",
  "status": "active",
  "brief": "Launch new SaaS product to market",
  "beads": [
    {
      "id": "mkt-abc01",
      "skill": "copywriting",
      "task": "Write landing page copy",
      "status": "completed",
      "assignee": "polecat-1",
      "output": "./outputs/landing-copy.md"
    },
    {
      "id": "mkt-abc02",
      "skill": "page-cro",
      "task": "Optimize landing page structure",
      "status": "in_progress",
      "assignee": "polecat-2",
      "depends_on": ["mkt-abc01"]
    }
  ],
  "deliverables": [],
  "notes": []
}
```

## Bead States

- `pending` - Not yet started
- `assigned` - Assigned to polecat
- `in_progress` - Work underway
- `review` - Awaiting review
- `revision` - Needs changes
- `completed` - Done

## Commands

### Create Convoy

```bash
# From Agency command
/agency convoy create "Campaign Name" --brief "Description"
```

### Add Beads

```bash
/agency bead add <convoy-id> --skill copywriting --task "Write hero section"
```

### Check Status

```bash
/agency convoy status <convoy-id>
```

### Complete Bead

```bash
/agency bead complete <bead-id> --output ./path/to/output.md
```

## Best Practices

1. **One convoy per project** - Keep related work together
2. **Clear bead descriptions** - Be specific about what's needed
3. **Set dependencies** - Identify what must complete first
4. **Regular status checks** - Update convoy as work progresses
5. **Archive when done** - Move to completed/ when finished
