# Pitch Asset Generation Setup

## Prerequisites

### 1. Fal.ai API Key

Get your API key from [fal.ai](https://fal.ai/dashboard/keys)

Set in environment:
```bash
export FAL_KEY=your_key_here
```

Or create `.env` file in project root:
```
FAL_KEY=your_key_here
```

### 2. Python Dependencies

```bash
pip install fal-client httpx
```

## Generate Assets

### Quick Generation (Flux Schnell - Fast)
```bash
cd /home/user/copy
python agency/rigs/law-com-audit/pitch/assets/generate_direct.py
```

### Output

Generated assets will have Fal CDN URLs in `generated_manifest.json`:
```json
{
  "generated_at": "2026-01-29T...",
  "model": "fal-ai/flux/schnell",
  "assets": [
    {
      "id": "cover",
      "url": "https://fal.media/files/...",
      "request_id": "..."
    }
  ]
}
```

## Assets Generated

| ID | Description | Use |
|----|-------------|-----|
| cover | Navy/gold abstract background | Slide 1 cover |
| timeline | Converging lines visualization | Slide 2 inflection |
| market_gap | Bar chart comparison | Slide 3 competitive gap |
| funnel | Leaking funnel | Slide 4 conversion |
| pillars | Three trophy pillars | Slide 5 exclusive assets |
| positioning | Quadrant with arrow | Slide 6 repositioning |
| strategy | Greek columns | Slide 7 strategy pillars |
| moat | Fortress with moat | Slide 10 competitive defense |
| transformation | Before/after split | Slide 11 transformation |
| roi | Growth arrow | Slide 17 ROI |
| risk | Declining trend | Slide 18 risk |
| divider | Section divider | Between sections |
| hero_intel | Intelligence network | Hero image option |
| hero_bench | Rankings podium | Hero image option |

## Using Generated Assets

### In Pitch Deck

Reference URLs directly in presentation software or download for embedding:

```bash
# Download all assets
cat generated_manifest.json | jq -r '.assets[].url' | xargs -I {} wget {}
```

### In Markdown/Documentation

```markdown
![Cover](https://fal.media/files/xxx/cover.png)
```

## Regenerating

To regenerate with different prompts, edit `generate_direct.py` and re-run.

For higher quality (slower), change model to:
```python
MODEL = "fal-ai/flux-pro/v1.1"
```

## Troubleshooting

### "No credentials found"
- Ensure FAL_KEY is exported in current shell
- Check: `echo $FAL_KEY`

### Rate limits
- Flux Schnell: ~10 concurrent requests
- Add delays if needed: `time.sleep(2)` between requests

### Image not generating
- Check Fal dashboard for errors
- Try simpler prompt first
- Verify model is available
