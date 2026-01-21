# Copy & Marketing Agency

This is an AI-powered full-service copy and marketing asset generation system built on Claude Code.

## System Architecture

This system combines:
- **Marketing Skills**: Specialized prompts and frameworks for 23+ marketing disciplines
- **Agency Orchestration**: Multi-agent coordination inspired by Gastown for complex projects
- **Persistent Workflows**: Git-backed state tracking for long-running campaigns

## Quick Start

### Single Task
For individual marketing tasks, invoke a skill directly:
```
/copywriting - Generate conversion-focused copy
/page-cro - Analyze and optimize landing pages
/seo-audit - Comprehensive SEO analysis
/email-sequence - Design email campaigns
```

### Full Campaign
For complex projects requiring multiple skills:
```
/agency brief "Campaign Name"
```

The Mayor agent will analyze requirements and coordinate specialized agents.

## Available Skills

### Content Creation
- `copywriting` - Conversion-focused web copy
- `copy-editing` - Polish and refine existing content
- `social-content` - Social media content strategy
- `email-sequence` - Email marketing campaigns

### Conversion Optimization
- `page-cro` - Landing page optimization
- `form-cro` - Form conversion optimization
- `signup-flow-cro` - Registration flow optimization
- `onboarding-cro` - User onboarding optimization
- `popup-cro` - Popup effectiveness
- `paywall-upgrade-cro` - Subscription conversion

### SEO & Discovery
- `seo-audit` - Comprehensive site audits
- `programmatic-seo` - Scalable SEO automation
- `schema-markup` - Structured data implementation

### Strategy & Growth
- `marketing-ideas` - Brainstorming and ideation
- `marketing-psychology` - Psychological principles
- `pricing-strategy` - Pricing optimization
- `launch-strategy` - Product launch planning
- `competitor-alternatives` - Competitive positioning
- `referral-program` - Word-of-mouth growth
- `free-tool-strategy` - Lead generation tools

### Measurement
- `ab-test-setup` - A/B testing methodology
- `analytics-tracking` - Analytics implementation
- `paid-ads` - Paid advertising management

## Agency Workflow

The agency uses a convoy-based workflow:

1. **Brief Creation**: Define project goals, audience, and deliverables
2. **Work Breakdown**: Mayor creates convoy with individual beads (work units)
3. **Agent Assignment**: Specialized polecats spawn for each skill
4. **Execution**: Agents work in parallel, persisting state through hooks
5. **Review**: Creative review and iteration
6. **Delivery**: Final assets compiled and presented

## Directory Structure

```
copy/
├── .claude/           # Claude Code configuration
│   ├── commands/      # Custom commands
│   └── hooks/         # Event hooks
├── skills/            # Marketing skill definitions
├── agency/            # Orchestration system
│   ├── mayor/         # Mayor agent configuration
│   ├── rigs/          # Project containers
│   ├── crews/         # Agent workspaces
│   └── convoys/       # Work tracking
├── templates/         # Reusable templates
└── workflows/         # Predefined workflows
```

## Best Practices

1. **Start with a brief**: Always define clear objectives before generating assets
2. **Use appropriate skills**: Match the skill to the task for best results
3. **Review and iterate**: Use the review workflow for quality control
4. **Track everything**: Leverage convoys for visibility into complex projects
5. **Persist state**: Use hooks to ensure work survives interruptions
