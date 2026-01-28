# Spawn: Quick-Start Entry Points

These are fast paths into the agency for common scenarios.

## Entry Points

| Mode | When to Use | Agent | Link |
|------|-------------|-------|------|
| **Brief** | Full projects needing orchestration | Director | `spawn/brief.md` |
| **Write** | Fast copy, strategy already clear | Copywriter | `spawn/write.md` |
| **Audit** | Analyze existing pages/flows | Optimizer | `spawn/audit.md` |
| **Optimize** | Improve something specific | Optimizer | `spawn/optimize.md` |
| **Strategy** | Think before writing | Strategist | `spawn/strategy.md` |

## How to Use

1. Load the agent definition
2. Load the spawn mode
3. Give your request

```
Read agency/agents/[agent].md
Read agency/spawn/[mode].md

"[Your request]"
```

## Decision Tree

```
Do you know what you want?
├── Yes → Do you need multiple deliverables?
│         ├── Yes → Brief mode (Director)
│         └── No → Write mode (Copywriter)
└── No → Strategy mode (Strategist)

Do you have something to analyze?
├── Yes → Audit mode (Optimizer)
└── No → See above

Do you have something underperforming?
├── Yes → Optimize mode (Optimizer)
└── No → See above
```

## Compound Patterns

Sometimes you need multiple modes:

### Strategy → Write
First figure out positioning, then write copy.
```
1. Read agency/agents/strategist.md + spawn/strategy.md
2. Get positioning brief
3. Read agency/agents/copywriter.md + spawn/write.md
4. Hand off positioning brief
```

### Write → Audit
Write something, then check it.
```
1. Quick write with Copywriter
2. Read agency/agents/optimizer.md + spawn/audit.md
3. Audit the draft
```

### Full Project
Complete orchestration.
```
1. Read agency/agents/director.md + spawn/brief.md
2. Director handles everything
```
