# Escalation Protocol

When agents are blocked, unclear, or facing decisions above their authority, they escalate to the Director.

## When to Escalate

- **Blocked**: Can't proceed without information or decision
- **Conflict**: Disagree with another agent's direction
- **Scope change**: The work is different than originally briefed
- **Quality concern**: Something fundamental is wrong
- **Resource need**: Need a different agent involved

## Escalation Format

```
ESCALATE: [Agent] → Director

## Issue Type
[Blocked / Conflict / Scope Change / Quality Concern / Resource Need]

## What's Happening
[Clear description of the situation]

## What I've Tried
[Steps taken before escalating]

## What I Need
[Specific decision or action required]

## Impact If Unresolved
[What happens if this isn't addressed]

## My Recommendation
[What you think we should do]
```

## Example Escalations

### Blocked
```
ESCALATE: Copywriter → Director

## Issue Type
Blocked

## What's Happening
I'm writing the social proof section but we have no customer testimonials.
Can't write believable proof without actual quotes.

## What I've Tried
- Checked brand assets folder
- Asked Strategist if they found any in research
- Looked for case studies

## What I Need
Either real testimonials or a decision to skip this section.

## Impact If Unresolved
Landing page ships without social proof = lower conversion.

## My Recommendation
Can we reach out to 2-3 customers for quick quotes? Or use data
("500 teams use TaskFlow") instead of testimonials?
```

### Conflict
```
ESCALATE: Editor → Director

## Issue Type
Conflict

## What's Happening
Strategist wants the hero to lead with "AI-powered productivity."
I think our audience is skeptical of AI claims and this will hurt trust.
We've gone back and forth twice and aren't aligned.

## What I've Tried
- Explained my reasoning
- Proposed alternatives ("Intelligent" instead of "AI-powered")
- Asked for data supporting AI messaging

## What I Need
A decision on whether to include "AI" in the hero.

## Impact If Unresolved
We're burning time debating instead of shipping.

## My Recommendation
Test it. Run two variants and let data decide.
```

### Quality Concern
```
ESCALATE: Optimizer → Director

## Issue Type
Quality Concern

## What's Happening
The landing page has 4 different CTAs above the fold. This is
a conversion killer. Every CRO principle says focus on one action.

## What I've Tried
- Flagged in my audit
- Explained impact to Copywriter
- Proposed reduced CTA structure

## What I Need
Authority to require a single primary CTA.

## Impact If Unresolved
We ship a page that will underperform. We'll spend the next month
"optimizing" something that was broken from the start.

## My Recommendation
One primary CTA above the fold. Secondary actions below.
```

## Director Response Format

```
DIRECTOR RESPONSE: → [Agent]

## Decision
[What we're doing]

## Reasoning
[Why]

## Next Steps
[Who does what now]

## For the Record
[Anything to note for the project]
```

## Escalation Norms

1. **Escalate early.** Don't spin for hours before raising a flag.
2. **Come with a recommendation.** Don't just present problems.
3. **Document what you tried.** Show you attempted to resolve it.
4. **Accept the decision.** Once Director calls it, execute.
5. **No surprises.** If something's off, say it before it's a crisis.
