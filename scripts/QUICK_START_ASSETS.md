# Quick Asset Generation Guide

This guide helps you quickly generate campaign assets using FAL turbo models.

## Setup (One-Time)

1. Add your FAL API key to `.env`:
   ```bash
   echo "FAL_KEY=your-key-here" >> .env
   echo "FAL_API_KEY=your-key-here" >> .env
   ```

2. Install Python dependencies (if not already done):
   ```bash
   pip install fal-client httpx python-dotenv
   ```

## Generate Assets

### Method 1: Web UI (Easiest)

1. Start the application:
   ```bash
   # Terminal 1: Backend
   python3 -m uvicorn service.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

2. Visit http://localhost:3000/assess

3. Generate assets interactively:
   - Select type (image/video/audio)
   - Choose model (defaults are good)
   - Enter creative prompt
   - Click "Initiate Generation"

### Method 2: Command Line Script

Generate all campaign assets in batch:

```bash
# Set API key for this session
export FAL_KEY="your-key-here"

# Generate everything
python scripts/generate_campaign_assets.py --all

# Or generate specific assets
python scripts/generate_campaign_assets.py --audience founders --type og
python scripts/generate_campaign_assets.py --audience freelancers --type ads
python scripts/generate_campaign_assets.py --type brand
```

Assets are saved to `generated_assets/` directory with a manifest file.

### Method 3: Direct API Call

```bash
curl -X POST http://localhost:8000/generate-asset \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "prompt": "Professional marketing agency workspace, cinematic lighting",
    "model": "fal-ai/flux/schnell"
  }'
```

## Recommended Prompts

### Hero Images
```
Technical founder at minimalist desk, laptop showing landing page wireframes,
soft morning light through window, focused expression, code editor visible,
clean modern workspace, photorealistic, professional photography style
```

### Abstract Brand Assets
```
Abstract flowing composition of marketing elements: headlines, buttons, forms,
all dissolving and reforming in golden light streams, premium dark background,
electric indigo and warm amber accents, high-end tech aesthetic
```

### Social Media Backgrounds
```
Soft gradient from deep navy to warm copper, subtle geometric patterns,
professional and premium feel, modern marketing aesthetic, space for text overlay
```

## Model Recommendations

| Use Case | Recommended Model | Speed | Quality |
|----------|------------------|--------|---------|
| Hero images | `fal-ai/flux-pro/v1.1` | Moderate | Premium |
| OG images | `fal-ai/flux/schnell` | Ultra-fast | High |
| Quick iteration | `fal-ai/fast-lightning-sdxl` | Ultra-fast | Good |
| Text/logos | `fal-ai/qwen-image-2512` | Fast | High |
| Brand assets | `fal-ai/recraft-v3` | Fast | High |

## Troubleshooting

### "No address associated with hostname"
- Check internet connection
- Verify FAL_KEY is valid
- Ensure fal.ai is accessible from your network

### "Failed to generate asset"
- Check FAL API key has credits
- Try a different model
- Simplify the prompt

### Assets not appearing in UI
- Check `generated_assets/manifest.json`
- Verify GCS bucket permissions (if using cloud storage)
- Check browser console for errors

## Next Steps

1. Generate initial assets for all audiences
2. Review generated assets in `/assess`
3. Approve best assets for production use
4. Copy approved assets to `frontend/static/`
5. Update SEO config with asset URLs

## Learn More

- Full documentation: [docs/ASSET_GENERATION.md](../docs/ASSET_GENERATION.md)
- Model configuration: [frontend/src/lib/config/models.ts](../frontend/src/lib/config/models.ts)
- FAL guide: [fal-guide.md](../fal-guide.md)
