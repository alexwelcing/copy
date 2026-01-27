# Sync Protocol

Regular status updates keep the agency running smoothly. This protocol defines how agents communicate progress.

## Status Update Format

```
STATUS: [Agent]

## Currently Working On
[Active task]

## Progress
[What's done, what's remaining]

## Blockers
[Anything slowing you down - or "None"]

## Next Up
[What you'll do after current task]

## ETA to Handoff
[When this work will be ready to pass on]
```

## Board Update

When status changes, update the agency board:

```json
// agency/board/status.json
{
  "last_updated": "2024-01-15T14:30:00Z",
  "agents": {
    "director": {
      "status": "coordinating",
      "current": "Reviewing TaskFlow deliverables"
    },
    "strategist": {
      "status": "idle",
      "last_completed": "TaskFlow positioning"
    },
    "copywriter": {
      "status": "working",
      "current": "TaskFlow email sequence"
    },
    "editor": {
      "status": "reviewing",
      "current": "TaskFlow landing page draft"
    },
    "optimizer": {
      "status": "idle",
      "last_completed": "Homepage audit"
    },
    "analyst": {
      "status": "idle",
      "last_completed": "Q4 campaign analysis"
    }
  }
}
```

## Status Values

| Status | Meaning |
|--------|---------|
| `idle` | Available for new work |
| `working` | Actively producing |
| `reviewing` | Evaluating someone else's work |
| `blocked` | Waiting on something |
| `coordinating` | Managing/orchestrating (Director only) |

## Project Sync

For active projects, maintain a project status:

```json
// agency/board/active.json
{
  "projects": [
    {
      "name": "TaskFlow Landing Page",
      "status": "in_progress",
      "phase": "content",
      "owner": "director",
      "agents_involved": ["strategist", "copywriter", "editor"],
      "deliverables": [
        {"name": "Positioning brief", "status": "complete", "owner": "strategist"},
        {"name": "Landing page copy", "status": "in_review", "owner": "copywriter"},
        {"name": "Email sequence", "status": "in_progress", "owner": "copywriter"}
      ],
      "blockers": [],
      "next_milestone": "Copy complete"
    }
  ]
}
```

## Sync Triggers

Update status when:
- Starting new work
- Completing a deliverable
- Hitting a blocker
- Handing off to another agent
- Finishing a review

## Inbox System

Pending requests live in the inbox:

```json
// agency/board/inbox.json
{
  "requests": [
    {
      "id": "req-001",
      "type": "review",
      "from": "copywriter",
      "to": "editor",
      "subject": "Landing page hero review",
      "priority": "high",
      "created": "2024-01-15T14:00:00Z",
      "status": "pending"
    },
    {
      "id": "req-002",
      "type": "handoff",
      "from": "strategist",
      "to": "copywriter",
      "subject": "Email sequence brief ready",
      "priority": "normal",
      "created": "2024-01-15T13:30:00Z",
      "status": "accepted"
    }
  ]
}
```

## Sync Norms

1. **Update proactively.** Don't wait to be asked.
2. **Be honest about blockers.** Hidden problems become big problems.
3. **Keep it brief.** Status updates should be scannable.
4. **Include ETAs.** Others are planning around your work.
5. **Acknowledge handoffs.** Confirm when you receive work.
