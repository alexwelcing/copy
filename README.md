# Copy & Marketing Agency

An AI-powered full-service copy and marketing asset generation system built on Claude Code. This system combines specialized marketing skills with multi-agent orchestration for complex campaign work.

## Overview

This repository provides a complete Claude Code ecosystem for generating marketing content, optimizing conversions, and running comprehensive marketing campaigns. It features:

- **23 specialized marketing skills** covering content creation, CRO, SEO, growth, and measurement
- **Multi-agent orchestration** inspired by [Gastown](https://github.com/steveyegge/gastown) for complex projects
- **Structured workflows** for campaigns, audits, and content creation
- **Templates** for briefs, work tracking, and deliverables

## Quick Start

### Single Task

For individual marketing tasks, invoke a skill directly:

```
# Generate landing page copy
Load the copywriting skill and create copy for...

# Audit a page for conversion optimization
Load the page-cro skill and analyze...

# Create an email sequence
Load the email-sequence skill and design...
```

### Full Campaign

For complex projects requiring multiple skills:

```
# Review the brief template
Read templates/brief.md

# Fill out your brief, then have the Mayor analyze it
The Mayor will create a convoy and coordinate work across multiple agents
```

## Available Skills

### Content Creation
| Skill | Description |
|-------|-------------|
| `copywriting` | Conversion-focused web copy |
| `copy-editing` | Polish and refine existing content |
| `social-content` | Social media content strategy |
| `email-sequence` | Email marketing campaigns |

### Conversion Optimization (CRO)
| Skill | Description |
|-------|-------------|
| `page-cro` | Landing page optimization |
| `form-cro` | Form conversion optimization |
| `signup-flow-cro` | Registration flow optimization |
| `onboarding-cro` | User onboarding optimization |
| `popup-cro` | Popup effectiveness |
| `paywall-upgrade-cro` | Subscription conversion |

### SEO & Discovery
| Skill | Description |
|-------|-------------|
| `seo-audit` | Comprehensive site audits |
| `programmatic-seo` | Scalable SEO automation |
| `schema-markup` | Structured data implementation |

### Strategy & Growth
| Skill | Description |
|-------|-------------|
| `marketing-ideas` | Brainstorming and ideation |
| `marketing-psychology` | Psychological principles |
| `pricing-strategy` | Pricing optimization |
| `launch-strategy` | Product launch planning |
| `competitor-alternatives` | Competitive positioning |
| `referral-program` | Word-of-mouth growth |
| `free-tool-strategy` | Lead generation tools |

### Measurement
| Skill | Description |
|-------|-------------|
| `ab-test-setup` | A/B testing methodology |
| `analytics-tracking` | Analytics implementation |
| `paid-ads` | Paid advertising management |

## Agency System

The agency uses a multi-agent orchestration system inspired by Gastown:

### Components

- **Mayor**: Central coordinator that analyzes briefs, assigns work, and manages delivery
- **Polecats**: Ephemeral worker agents specialized in specific skills
- **Convoys**: Work tracking units that bundle related tasks
- **Rigs**: Project containers with client context and brand guidelines
- **Hooks**: Persistent state storage for work continuity

### Workflow

```
Brief → Mayor Analysis → Convoy Creation → Polecat Assignment → Execution → Review → Delivery
                                    ↓
                            Parallel Work Tracks
                            ├── Content Creation
                            ├── CRO Optimization
                            └── Technical Setup
```

## Directory Structure

```
copy/
├── .claude/                 # Claude Code configuration
│   ├── commands/           # Custom commands
│   ├── hooks/              # Event hooks
│   ├── settings.json       # Agency settings
│   └── CLAUDE.md           # System instructions
├── skills/                  # Marketing skill definitions
│   ├── copywriting/
│   ├── page-cro/
│   ├── email-sequence/
│   └── ... (23 total skills)
├── agency/                  # Orchestration system
│   ├── mayor/              # Mayor agent configuration
│   ├── rigs/               # Project containers
│   ├── crews/              # Agent workspaces
│   └── convoys/            # Work tracking
├── templates/               # Reusable templates
│   ├── brief.md            # Creative brief template
│   ├── convoy.md           # Convoy tracking template
│   └── deliverable.md      # Deliverable template
├── workflows/               # Predefined workflows
│   ├── full-service.md     # Complete campaign workflow
│   ├── quick-copy.md       # Fast copy workflow
│   ├── cro-audit.md        # CRO audit workflow
│   └── seo-campaign.md     # SEO campaign workflow
└── README.md
```

## Workflows

### Full-Service Campaign
Complete marketing campaigns with multiple deliverables:
1. Discovery & Planning
2. Strategy Development
3. Content Creation
4. Optimization
5. Technical Setup
6. Review & Delivery

### Quick Copy
Streamlined workflow for standalone copy requests:
1. Brief Analysis
2. Context Gathering
3. Copy Creation
4. Optional Polish
5. Delivery

### CRO Audit
Systematic conversion optimization analysis:
1. Page Analysis
2. Deep Dive Audits
3. Technical Analysis
4. Synthesis & Recommendations

### SEO Campaign
Comprehensive SEO-focused initiatives:
1. Audit & Research
2. Strategy Development
3. Content Creation
4. Technical Implementation
5. Measurement Setup

## Usage Examples

### Generate Landing Page Copy

```
I need copy for a landing page for a project management tool.

Target audience: Engineering managers at mid-size tech companies
Main benefit: Reduce meeting time by 50%
Tone: Professional but approachable
```

### Run a CRO Audit

```
Please audit this landing page for conversion optimization:
[provide URL or page content]

Focus on:
- Above the fold effectiveness
- CTA placement and copy
- Trust signals
- Mobile experience
```

### Plan a Product Launch

```
We're launching a new feature next month. Help me plan the launch:

Product: AI-powered scheduling assistant
Target: Current users + prospects
Goal: 1000 new signups in first week
Budget: $5000 for ads
```

## Templates

### Creative Brief (`templates/brief.md`)
Comprehensive template for project requirements including:
- Project overview and objectives
- Target audience details
- Messaging framework
- Deliverables list
- Timeline and constraints

### Convoy (`templates/convoy.md`)
Work tracking template with:
- Bead (task) management
- Progress visualization
- Dependency tracking
- Status updates

### Deliverable (`templates/deliverable.md`)
Output format template including:
- Content delivery
- Strategic rationale
- Alternatives
- Review process

## Best Practices

1. **Start with a brief**: Clear requirements lead to better outputs
2. **Use appropriate skills**: Match the skill to the specific task
3. **Review and iterate**: Quality control through the review workflow
4. **Track everything**: Use convoys for visibility into complex projects
5. **Leverage templates**: Consistent format improves communication

## Credits

This system is built on:
- Marketing skill frameworks adapted from [marketingskills](https://github.com/coreyhaines31/marketingskills)
- Multi-agent orchestration concepts from [Gastown](https://github.com/steveyegge/gastown)
- Claude Code by Anthropic

## License

MIT License - See LICENSE file for details
