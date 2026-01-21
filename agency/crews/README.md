# Crews: Agent Workspaces

Crews represent the workspace structure for agents (polecats) working on marketing projects.

## Structure

```
crews/
├── README.md
├── active/           # Currently working agents
└── hooks/            # Persistent state for agents
```

## Polecat Agents

Polecats are ephemeral worker agents spawned by the Mayor to complete specific tasks.

### Characteristics

- **Specialized**: Each polecat works with a specific skill
- **Ephemeral**: Created for tasks, terminated when done
- **Tracked**: State persisted through hooks
- **Parallel**: Multiple polecats can work simultaneously

### Polecat Lifecycle

1. **Spawn**: Mayor creates polecat with assigned skill
2. **Assign**: Polecat receives bead (work unit)
3. **Work**: Polecat completes task using skill
4. **Report**: Output returned to convoy
5. **Terminate**: Polecat released after completion

## Hook System

Hooks provide persistent storage for agent work, surviving restarts.

### Hook Structure

```
hooks/
├── polecat-1/
│   ├── state.json      # Current work state
│   ├── context.md      # Accumulated context
│   └── outputs/        # Work outputs
├── polecat-2/
│   └── ...
```

### State File

```json
{
  "id": "polecat-1",
  "skill": "copywriting",
  "bead": "mkt-abc01",
  "status": "working",
  "started": "2024-01-15T10:30:00Z",
  "progress": 0.6,
  "notes": "Completed headline variations, working on body copy"
}
```

## Crew Commands

### Spawn Polecat

```bash
/agency polecat spawn copywriting
# Returns: polecat-abc12 created with copywriting skill
```

### Assign Work

```bash
/agency polecat assign polecat-abc12 mkt-abc01
# Assigns bead mkt-abc01 to polecat-abc12
```

### Check Status

```bash
/agency polecat status
# Lists all active polecats and their current work
```

### Recall Polecat

```bash
/agency polecat recall polecat-abc12
# Terminates polecat and saves final state
```

## Best Practices

1. **Right skill for the job** - Match polecat skill to bead requirement
2. **Parallel when possible** - Spawn multiple polecats for independent work
3. **Monitor progress** - Check in regularly on long tasks
4. **Clean up** - Recall polecats when work is complete
5. **Persist state** - Use hooks for work that may be interrupted
