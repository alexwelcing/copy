# High Era: Marketing Agency

A living marketing agency powered by specialized AI agents.

## Quick Start

**Talk to an agent:**
```
Read agency/agents/director.md
"I need a landing page for [product]"
```

**Or use a quick-start pattern:**
```
Read agency/spawn/write.md
Read agency/agents/copywriter.md
"Write a hero section for [product]"
```

## The Team

| Agent | Role | Spawn |
|-------|------|-------|
| **Director** | Orchestrates projects, assigns work, ensures delivery | `agency/agents/director.md` |
| **Strategist** | Positioning, psychology, competitive analysis | `agency/agents/strategist.md` |
| **Copywriter** | Headlines, pages, emails, ads | `agency/agents/copywriter.md` |
| **Editor** | Polish, consistency, quality gate | `agency/agents/editor.md` |
| **Optimizer** | CRO, page structure, conversion | `agency/agents/optimizer.md` |
| **Analyst** | Measurement, tracking, data | `agency/agents/analyst.md` |

## Entry Points

| Need | Pattern | What to Load |
|------|---------|--------------|
| Full project | Brief mode | `spawn/brief.md` + `agents/director.md` |
| Fast copy | Write mode | `spawn/write.md` + `agents/copywriter.md` |
| Analyze something | Audit mode | `spawn/audit.md` + `agents/optimizer.md` |
| Fix something | Optimize mode | `spawn/optimize.md` + `agents/optimizer.md` |
| Figure out positioning | Strategy mode | `spawn/strategy.md` + `agents/strategist.md` |

## Skills Library

Agents draw from 23 specialized skills:

**Writing:** `copywriting` `copy-editing` `email-sequence` `social-content`

**CRO:** `page-cro` `form-cro` `signup-flow-cro` `onboarding-cro` `popup-cro` `paywall-upgrade-cro`

**SEO:** `seo-audit` `programmatic-seo` `schema-markup`

**Strategy:** `marketing-ideas` `marketing-psychology` `pricing-strategy` `launch-strategy` `competitor-alternatives` `referral-program` `free-tool-strategy`

**Measurement:** `ab-test-setup` `analytics-tracking` `paid-ads`

Load skills directly when needed: `skills/[skill-name]/SKILL.md`

## How Agents Work Together

Agents communicate through protocols:
- **Handoffs** - Work transfers with context (`protocols/handoff.md`)
- **Reviews** - Feedback requests (`protocols/review.md`)
- **Escalations** - Blockers and conflicts (`protocols/escalate.md`)
- **Syncs** - Status updates (`protocols/sync.md`)

The **Board** tracks live state:
- `agency/board/status.json` - Agent availability
- `agency/board/active.json` - Current projects
- `agency/board/inbox.json` - Pending requests

## Key Principle

**Strategy precedes execution.**

Every project starts with understanding:
- Who is the audience?
- What do they believe now?
- What do we need them to believe?
- What proof do we have?

Copy comes last. Thinking comes first.
