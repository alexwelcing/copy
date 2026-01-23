# Stop Prompting. Start Deploying.

**23 marketing skills. Each one a complete framework. All executable in Claude Code.**

Most people ask AI to "write some copy." They get generic, forgettable content that sounds like everyone else's generic, forgettable content.

This is different.

This is marketing expertise encoded into executable skills - the same mental models top copywriters, CRO specialists, and growth marketers use, made repeatable inside Claude Code.

---

## What This Actually Does

You load a skill. The skill contains a complete framework:
- How to gather context
- What questions to answer first
- Proven structures and formulas
- Quality checklists
- Strategic rationale for every decision

**Example**: The `copywriting` skill doesn't just write headlines. It first identifies page purpose, audience awareness stage, traffic context, and objections - then applies tested formulas like "Outcome + Timeframe" or "Eliminate Pain" - then validates against a quality checklist.

That's the difference between prompting and deploying.

---

## The Skills

### Write Things That Convert

| Skill | What It Does |
|-------|--------------|
| `copywriting` | Headlines, landing pages, CTAs - with strategic frameworks |
| `copy-editing` | Three-pass editing: clarity, then concision, then power |
| `email-sequence` | Welcome, nurture, sales, win-back - complete sequences |
| `social-content` | Platform-native content that doesn't smell like AI |

### Fix What's Broken

| Skill | What It Does |
|-------|--------------|
| `page-cro` | Systematic landing page audits with prioritized fixes |
| `form-cro` | Field-by-field conversion optimization |
| `signup-flow-cro` | Registration friction removal |
| `onboarding-cro` | Get users to their aha moment faster |
| `popup-cro` | Exit intent, timing, triggers that work |
| `paywall-upgrade-cro` | Free-to-paid conversion paths |

### Get Found

| Skill | What It Does |
|-------|--------------|
| `seo-audit` | Technical + content + competitive SEO analysis |
| `programmatic-seo` | Template-based pages at scale |
| `schema-markup` | JSON-LD that wins rich results |

### Think Bigger

| Skill | What It Does |
|-------|--------------|
| `marketing-ideas` | Structured brainstorming with prioritization |
| `marketing-psychology` | Cialdini, cognitive biases, applied persuasion |
| `pricing-strategy` | Models, anchoring, packaging |
| `launch-strategy` | Product Hunt, soft launches, hard launches |
| `competitor-alternatives` | Positioning that creates space |
| `referral-program` | Viral loops that actually loop |
| `free-tool-strategy` | Lead-gen tools worth building |

### Measure What Matters

| Skill | What It Does |
|-------|--------------|
| `ab-test-setup` | Statistical validity, test design, learning extraction |
| `analytics-tracking` | Events, funnels, attribution that tells the truth |
| `paid-ads` | Google, Meta, LinkedIn - structure and optimization |

---

## How to Use It

### Single Skill

Load a skill and use its framework:

```
Read skills/page-cro/SKILL.md

Now audit this landing page: [your page]
```

The skill guides the analysis. You get structured recommendations with strategic rationale, not just "make the button bigger."

### Full Campaigns

For complex work spanning multiple skills:

1. Fill out `templates/brief.md` with your project details
2. The Mayor agent analyzes requirements and creates a work plan
3. Specialized agents execute each skill in parallel
4. Work is tracked through convoys (task bundles)
5. Review, iterate, deliver

This orchestration system is inspired by [Gastown](https://github.com/steveyegge/gastown) - battle-tested multi-agent coordination.

---

## The System

```
copy/
├── skills/           # 23 marketing frameworks
├── agency/           # Multi-agent orchestration
│   ├── mayor/       # Coordinates complex projects
│   ├── rigs/        # Project containers with client context
│   └── convoys/     # Work tracking
├── templates/        # Briefs, deliverables, tracking
└── workflows/        # Pre-built sequences for common projects
```

### Workflows Ready to Run

- **Full-Service Campaign**: Discovery → Strategy → Content → Optimization → Delivery
- **Quick Copy**: Brief → Context → Write → Polish
- **CRO Audit**: Analyze → Deep dive → Synthesize → Prioritize
- **SEO Campaign**: Audit → Strategy → Create → Implement → Measure

---

## Why This Works

**Skills encode expertise.** A prompt is a one-shot request. A skill is a complete mental model - context gathering, frameworks, formulas, quality checks. The skill knows what questions to ask before writing a single word.

**Strategy precedes execution.** Every skill starts with understanding: Who's the audience? What's their awareness stage? What objections will they have? What proof do we need? Copy comes last.

**Compound returns.** Run a CRO audit, feed insights into copywriting, validate changes with A/B testing. The skills connect. They build on each other.

**Proof by demonstration.** We dogfooded this entire system on itself. The README you're reading was written by our copywriting skill, optimized by our page-cro skill. The quality of the output is the proof that it works.

---

## Easy Deployment (Fork & Run)

Deploy your own private instance of the agency in minutes. You bring the keys, we bring the code.

<a href="https://render.com/deploy" target="_blank">
<img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>

1. **Fork this repository** to your GitHub account.
2. **Click the button above** (or go to Render.com and select "New + -> Blueprint").
3. **Connect your forked repo.**
4. **Enter your `ANTHROPIC_API_KEY`** when prompted.

The system will deploy both the API and the Frontend, automatically connecting them.

---

## HTTP API

Run the skills as a service. Deploy to Google Cloud Run or any container platform.

### Quick Start

```bash
# Local
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python -m service.main

# Docker
docker build -t marketing-agency-api .
docker run -p 8080:8080 -e ANTHROPIC_API_KEY="your-key" marketing-agency-api

# Cloud Run
export GCP_PROJECT_ID="your-project"
./deploy/deploy.sh
```

### API Usage

```bash
# Execute any skill
curl -X POST http://localhost:8080/work \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "copywriting",
    "task": "Write a landing page headline",
    "context": {
      "product": "TaskFlow - AI project management",
      "audience": "Engineering managers",
      "benefit": "50% fewer meetings"
    }
  }'
```

Response includes structured output, alternatives, and recommendations parsed from the skill execution.

See `service/API.md` for full documentation.

---

## Get Started

### Claude Code (Interactive)

```bash
# Clone and enter
git clone [repo] && cd copy

# Load any skill and start using it
Read skills/copywriting/SKILL.md
# Then: "Write a landing page for [your product]"

# Or run a full workflow
Read workflows/cro-audit.md
# Then: "Audit [your page] following this workflow"
```

### HTTP API (Programmatic)

```bash
# Run locally
pip install -r requirements.txt
python -m service.main

# Test
curl http://localhost:8080/skills
```

---

## Built On

- Marketing frameworks adapted from [marketingskills](https://github.com/coreyhaines31/marketingskills)
- Multi-agent orchestration from [Gastown](https://github.com/steveyegge/gastown)
- [Claude Code](https://github.com/anthropics/claude-code) by Anthropic

---

*This README was written using the copywriting skill, structured using page-cro principles, and refined using copy-editing frameworks. What you're reading is the product demonstrating itself.*
