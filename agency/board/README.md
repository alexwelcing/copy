# Agency Board

Live state for the agency. These files track what's happening right now.

## Files

### status.json
Current status of all agents. Who's working, who's idle, who's blocked.

```json
{
  "agents": {
    "director": {"status": "coordinating", "current": "TaskFlow project"},
    "copywriter": {"status": "working", "current": "Landing page copy"}
  }
}
```

### active.json
All active projects and their current state.

```json
{
  "projects": [
    {
      "name": "TaskFlow Landing Page",
      "phase": "content",
      "deliverables": [...]
    }
  ]
}
```

### inbox.json
Pending requests between agents - handoffs, reviews, escalations.

```json
{
  "requests": [
    {"type": "review", "from": "copywriter", "to": "editor", "status": "pending"}
  ]
}
```

## Reading the Board

Check agency state before starting work:

```
Read agency/board/status.json
```

See active projects:

```
Read agency/board/active.json
```

Check pending requests:

```
Read agency/board/inbox.json
```

## Updating the Board

Agents update state through the sync protocol (see `protocols/sync.md`).

Status should be updated when:
- Starting new work
- Completing a task
- Handing off work
- Hitting a blocker
- Finishing a review
