# Convoy: [Project Name]

**ID**: convoy-[id]
**Created**: [Date]
**Status**: [active/paused/completed]

## Brief Summary

[1-2 sentence summary of what this convoy is delivering]

## Work Units (Beads)

### Pending

| ID | Skill | Task | Priority | Depends On |
|----|-------|------|----------|------------|
| mkt-xxx01 | [skill] | [task description] | P1 | - |
| mkt-xxx02 | [skill] | [task description] | P2 | mkt-xxx01 |

### In Progress

| ID | Skill | Task | Assignee | Started | Progress |
|----|-------|------|----------|---------|----------|
| mkt-xxx03 | [skill] | [task description] | polecat-1 | [date] | 60% |

### Completed

| ID | Skill | Task | Completed | Output |
|----|-------|------|-----------|--------|
| mkt-xxx04 | [skill] | [task description] | [date] | [link] |

## Progress

```
[=========>          ] 45% Complete

Completed: 5/11 beads
In Progress: 2 beads
Pending: 4 beads
```

## Active Polecats

| ID | Skill | Current Bead | Status |
|----|-------|--------------|--------|
| polecat-1 | copywriting | mkt-xxx03 | working |
| polecat-2 | page-cro | mkt-xxx05 | working |

## Deliverables

### Ready for Review
- [ ] [Deliverable 1] - [link to output]

### Approved
- [x] [Deliverable 2] - [link to output]

### Pending
- [ ] [Deliverable 3] - Not yet started

## Timeline

| Milestone | Target | Actual | Status |
|-----------|--------|--------|--------|
| Kickoff | [date] | [date] | Done |
| First drafts | [date] | - | In progress |
| Review | [date] | - | Pending |
| Final delivery | [date] | - | Pending |

## Notes

### [Date]
[Note about progress, decisions, or issues]

### [Date]
[Note]

## Blockers

- [ ] [Blocker description] - [Owner] - [Status]

## Dependencies

```
mkt-xxx01 (copywriting)
    └── mkt-xxx02 (page-cro)
        └── mkt-xxx03 (ab-test-setup)

mkt-xxx04 (email-sequence) [parallel]
```

---

## Commands

```bash
# Check status
/agency convoy status [convoy-id]

# Add bead
/agency bead add [convoy-id] --skill [skill] --task "[description]"

# Mark complete
/agency bead complete [bead-id] --output [path]

# Add note
/agency convoy note [convoy-id] "[note text]"
```
