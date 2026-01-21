# Marketing Agency API

HTTP service for executing marketing skills.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Run server
python -m service.main
```

Server runs at `http://localhost:8080`

### Docker

```bash
# Build
docker build -t marketing-agency-api .

# Run
docker run -p 8080:8080 -e ANTHROPIC_API_KEY="your-key" marketing-agency-api
```

### Cloud Run Deployment

```bash
# Set project
export GCP_PROJECT_ID="your-project"
export ANTHROPIC_API_KEY="your-key"

# Deploy
./deploy/deploy.sh
```

## API Reference

### Health Check

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "skills_available": 23
}
```

### List Skills

```
GET /skills
```

Returns all available skills organized by category.

### Execute Skill

```
POST /work
Content-Type: application/json
```

Request body:
```json
{
  "skill": "copywriting",
  "task": "Write a headline for...",
  "context": {
    "product": "Your product",
    "audience": "Target audience"
  },
  "content": "Optional content to analyze"
}
```

Response:
```json
{
  "skill": "copywriting",
  "output": "Full output from the skill...",
  "sections": {
    "Headlines": "...",
    "Subheadlines": "..."
  },
  "alternatives": ["Option 1", "Option 2"],
  "recommendations": ["Do this", "Try that"],
  "metadata": {
    "model": "claude-sonnet-4-20250514",
    "input_tokens": 1234,
    "output_tokens": 567
  }
}
```

### Shortcut Endpoints

For common skills:

```
POST /copywriting
POST /page-cro
POST /email-sequence
```

## Available Skills

### Writing
- `copywriting` - Conversion-focused copy
- `copy-editing` - Polish existing content
- `email-sequence` - Email campaigns
- `social-content` - Social media content

### CRO
- `page-cro` - Landing page optimization
- `form-cro` - Form optimization
- `signup-flow-cro` - Registration flows
- `onboarding-cro` - User onboarding
- `popup-cro` - Popup optimization
- `paywall-upgrade-cro` - Upgrade flows

### SEO
- `seo-audit` - Site audits
- `programmatic-seo` - Scalable SEO
- `schema-markup` - Structured data

### Strategy
- `marketing-ideas` - Brainstorming
- `marketing-psychology` - Persuasion
- `pricing-strategy` - Pricing
- `launch-strategy` - Launches
- `competitor-alternatives` - Positioning
- `referral-program` - Viral growth
- `free-tool-strategy` - Lead gen tools

### Measurement
- `ab-test-setup` - A/B testing
- `analytics-tracking` - Analytics
- `paid-ads` - Paid advertising

## Examples

### Generate Landing Page Copy

```bash
curl -X POST http://localhost:8080/work \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "copywriting",
    "task": "Write landing page copy for our product",
    "context": {
      "product": "TaskFlow - AI project management",
      "audience": "Engineering managers",
      "main_benefit": "50% fewer meetings",
      "tone": "Professional, confident"
    }
  }'
```

### Audit a Landing Page

```bash
curl -X POST http://localhost:8080/work \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "page-cro",
    "task": "Audit this page for conversion issues",
    "content": "<html>...your page HTML...</html>",
    "context": {
      "conversion_goal": "Free trial signup",
      "traffic_source": "Paid search"
    }
  }'
```

### Create Email Sequence

```bash
curl -X POST http://localhost:8080/work \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "email-sequence",
    "task": "Create a 5-email welcome sequence",
    "context": {
      "product": "SaaS tool",
      "activation_event": "First project created",
      "tone": "Friendly, helpful"
    }
  }'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | API key for Claude | Required |
| `CLAUDE_MODEL` | Model to use | claude-sonnet-4-20250514 |
| `PORT` | Server port | 8080 |
| `CORS_ORIGINS` | Allowed origins | * |
| `DEBUG` | Enable debug mode | false |

## Error Handling

Errors return JSON:

```json
{
  "error": "Error type",
  "detail": "Details if DEBUG=true",
  "skill": "skill-name if relevant"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad request (invalid input)
- `404` - Skill not found
- `500` - Server error

## Rate Limits

The API inherits rate limits from the Anthropic API. For high-volume usage, implement client-side rate limiting or use batch processing.
