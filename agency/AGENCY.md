# The Agency

This is a living marketing agency powered by specialized AI agents. Not documentation—actual agents you can spawn and orchestrate.

## Quick Start

```
# Bring in the Director for any project
"Director, I need a landing page for [product]"

# Or spawn specific agents directly
"I need the Strategist to analyze [competitor]"
"Get the Copywriter to write [deliverable]"
"Have the Editor review this copy"
```

## The Team

### Director (agency/agents/director.md)
The orchestrator. Receives briefs, assembles teams, tracks progress, ensures delivery. Think: Executive Creative Director who actually ships.

### Strategist (agency/agents/strategist.md)
Market positioning, competitive analysis, audience psychology. Thinks before anyone writes. Asks the uncomfortable questions.

### Copywriter (agency/agents/copywriter.md)
Headlines, pages, emails, ads. Masters frameworks (PAS, AIDA, Before-After-Bridge) but knows when to break them.

### Editor (agency/agents/editor.md)
Polish, consistency, voice. Cuts the fluff. Makes good copy great. Has opinions and isn't afraid to push back.

### Optimizer (agency/agents/optimizer.md)
CRO specialist. Sees pages as conversion systems. Tests everything. Data over opinions.

### Analyst (agency/agents/analyst.md)
Measurement, tracking, attribution. Turns metrics into insights. Knows what's worth measuring.

## How They Work Together

Agents communicate through structured handoffs:

```
Strategist → "Brief ready, positioning locked. Handing to Copywriter."
Copywriter → "Draft complete. Flagging Editor for review."
Editor     → "Polished. Two concerns flagged for Strategist."
Optimizer  → "Page structure reviewed. Three friction points identified."
```

The Director orchestrates, but agents can request each other directly.

## Agency State

The board tracks live status:
- `agency/board/status.json` - Who's working on what
- `agency/board/active.json` - Current projects and assignments
- `agency/board/inbox.json` - Pending requests and handoffs

## Spawning Agents

To work with an agent, load their definition and give them a task:

```
Read agency/agents/copywriter.md
"Write a hero section for [product]. Target: [audience]. Key benefit: [value]."
```

For complex projects, start with the Director:

```
Read agency/agents/director.md
"New project: [brief]. Assemble the team."
```

## Principles

1. **Agents have opinions.** They push back when something's off.
2. **Strategy before execution.** Strategist works before Copywriter touches a keyboard.
3. **Handoffs are explicit.** Work transfers include context, not just files.
4. **The Director owns delivery.** Someone is always accountable.
5. **Quality over speed.** Editor has veto power on rushed work.
