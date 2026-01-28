# Handoff Protocol

Work transfers between agents using structured handoffs. This ensures context survives the transition and receiving agents can work autonomously.

## Handoff Format

```
HANDOFF: [Sending Agent] → [Receiving Agent]

## Context
[What the receiving agent needs to know about the project]

## What I Did
[Summary of work completed]

## Deliverable
[What's being handed off - file, content, or reference]

## For Your Work
- Constraint: [Any limits or requirements]
- Priority: [What matters most]
- Watch for: [Potential issues]

## Open Questions
- [Anything unresolved]

## I'm Available For
[What the sending agent can still help with]
```

## Example Handoffs

### Strategist → Copywriter
```
HANDOFF: Strategist → Copywriter

## Context
Landing page for TaskFlow, a project management tool targeting engineering managers
who are drowning in status meetings.

## What I Did
Competitive analysis, audience research, positioning development.

## Deliverable
Positioning brief attached below.

## For Your Work
- Constraint: Must differentiate from Asana/Monday (they own "organized")
- Priority: The "fewer meetings" angle tested best in research
- Watch for: Don't lean into "AI" - audience is skeptical

## Open Questions
- Do we have customer quotes? I couldn't find any.

## I'm Available For
Clarifying positioning, reviewing if copy feels off-strategy.

---
[Positioning brief content]
```

### Copywriter → Editor
```
HANDOFF: Copywriter → Editor

## Context
Landing page copy for TaskFlow. Strategy is locked (see attached brief).
Targeting eng managers who hate meetings.

## What I Did
Full landing page draft: hero, problem, solution, proof, CTA.
Three headline variants. Email capture section.

## Deliverable
Draft attached below.

## For Your Work
- Constraint: Keep under 500 words total (brief requirement)
- Priority: Hero section is most important - needs to grab in 3 seconds
- Watch for: I might be overusing "meetings" - check for repetition

## Open Questions
- Is the testimonial section too long?
- Does the CTA "Reclaim your calendar" work or too cute?

## I'm Available For
Rewrites if structural changes needed, clarifying intent on any section.
```

### Editor → Director
```
HANDOFF: Editor → Director

## Context
TaskFlow landing page, final review complete.

## What I Did
Line edit, tightened hero (cut 15 words), fixed consistency issues,
strengthened CTAs.

## Deliverable
Final copy attached. Track-changes version also included.

## For Your Work
- Constraint: None - this is ready
- Priority: Ship it
- Watch for: Optimizer should review structure before dev handoff

## Open Questions
- None. Clean to ship.

## I'm Available For
Final tweaks if stakeholder feedback requires changes.
```

## Handoff Rules

1. **No naked handoffs.** Never pass work without context.
2. **Be specific about what you did.** Don't make them guess.
3. **Flag what you're unsure about.** Better to say it than hide it.
4. **Stay available.** The handoff doesn't end your involvement.
5. **Include the artifact.** Don't just reference—attach or inline.

## When a Handoff is Rejected

Receiving agents can reject handoffs. If that happens:

```
RETURN: [Receiving Agent] → [Sending Agent]

## Why I'm Returning This
[Specific reason]

## What I Need
[What would make this ready]

## Suggestion
[How to fix it]
```

This is normal and healthy. Better to reject early than produce bad work.
