# Asset Generation Integration Guide

## Overview

HIGH ERA now includes integrated asset generation using FAL.ai's turbo models. This allows you to generate high-quality images, videos, and audio directly within the platform.

## Quick Start

### 1. Environment Setup

Add your FAL API key to the `.env` file:

```bash
FAL_KEY=your-fal-api-key-here
FAL_API_KEY=your-fal-api-key-here  # Fallback
```

### 2. Generate Assets via UI

Visit `/assess` to access the Asset Assessment Lab where you can:

1. Select asset type (Image, Video, or Audio)
2. Choose a turbo model (optimized for speed + quality)
3. Enter your creative prompt
4. Generate and review assets
5. Approve assets for integration

### 3. Generate Assets via Script

Use the command-line script for batch generation:

```bash
# Generate OG images for founders
python scripts/generate_campaign_assets.py --audience founders --type og

# Generate all ad creatives for a specific audience
python scripts/generate_campaign_assets.py --audience freelancers --type ads

# Generate all assets for all audiences
python scripts/generate_campaign_assets.py --all
```

### 4. Generate Assets via API

POST to `/api/generate-asset`:

```typescript
const response = await fetch('/api/generate-asset', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'image',
    prompt: 'Cinematic hero image for a marketing agency',
    model: 'fal-ai/flux/schnell'  // Optional, smart defaults applied
  })
});

const asset = await response.json();
console.log(asset.url);  // GCS public URL
```

## Turbo Models

### Image Generation (Fast)

**Recommended: FLUX Schnell** (`fal-ai/flux/schnell`)
- Ultra-fast generation (2-4 seconds)
- High quality photorealism
- Best for: Hero images, OG images, campaign assets

**SDXL Lightning** (`fal-ai/fast-lightning-sdxl`)
- Ultra-fast (1-2 seconds)
- Good quality
- Best for: Quick iterations, social media posts

**Fast SDXL** (`fal-ai/fast-sdxl`)
- Balanced speed/quality
- Best for: General marketing visuals

**Qwen Image 2512** (`fal-ai/qwen-image-2512`)
- Fast generation with excellent text rendering
- Best for: Logos, posters, text overlays

### Premium Image Models

**FLUX Pro 1.1** (`fal-ai/flux-pro/v1.1`)
- Premium photorealism
- Best for: Main hero images, flagship assets

**Recraft V3** (`fal-ai/recraft-v3`)
- Design and vector focus
- Best for: Brand assets, icons, patterns

### Video Generation

**LTX Video** (`fal-ai/ltx-2-19b/distilled/text-to-video`)
- Fast video generation
- Best for: Quick video assets

**Kling V2.5 Turbo Pro** (`fal-ai/kling-video/v2.5-turbo/pro/text-to-video`)
- High quality turbo video
- Best for: Marketing videos

### Audio Generation

**Stable Audio** (`fal-ai/stable-audio`)
- Music and soundscapes
- Best for: Background audio, ambient tracks

## Integration Points

### 1. Homepage Hero Image

The homepage dynamically loads hero images from GCS:

```svelte
let heroImageUrl = 'https://storage.googleapis.com/marketing-copy-assets/images/generated_[id].png';
```

Update `heroImageUrl` to use newly generated assets.

### 2. Audience Pages (OG Images)

Audience-specific landing pages can use generated OG images in their SEO config:

```typescript
// In lib/seo/config.ts
export const audienceSEO = {
  founders: {
    og: {
      image: 'https://storage.googleapis.com/.../og_founders_primary.png'
    }
  }
}
```

### 3. Assessment Lab

Visit `/assess` to:
- Generate new assets
- Review generated assets
- Approve assets for production use
- Track asset generation history

## Asset Storage

Generated assets are stored in Google Cloud Storage:

- **Images**: `gs://[bucket]/images/generated_[id].png`
- **Videos**: `gs://[bucket]/videos/generated_[id].mp4`
- **Audio**: `gs://[bucket]/audio/generated_[id].mp3`

Public URLs are returned after generation for immediate use.

## Prompt Engineering Tips

### For Hero Images
```
Technical founder at minimalist desk, laptop showing landing page wireframes,
soft morning light through window, focused expression, clean modern workspace,
photorealistic, professional photography style, warm natural lighting
```

### For Abstract Visuals
```
Abstract flowing composition of marketing elements: headlines, buttons,
form fields, all dissolving and reforming in golden light streams,
premium dark background, electric indigo and warm amber accents
```

### For Brand Assets
```
Seamless repeating pattern of abstract marketing icons,
subtle monochrome on cream background, sophisticated texture,
vintage-modern hybrid aesthetic, tileable
```

## API Reference

### Backend Endpoint

**POST** `/generate-asset`

Request:
```json
{
  "type": "image",
  "prompt": "Your detailed prompt here",
  "model": "fal-ai/flux/schnell"
}
```

Response:
```json
{
  "id": "request_id",
  "url": "https://storage.googleapis.com/.../generated_id.png",
  "gcs_path": "images/generated_id.png",
  "prompt": "Your prompt",
  "model": "fal-ai/flux/schnell"
}
```

### Smart Model Selection

If no model is specified, the backend automatically selects the best model based on prompt content:

- Contains "text", "sign", "label" → Qwen Image 2512 (text specialist)
- General content → FLUX Pro 1.1 (premium quality)

## Troubleshooting

### Network Errors

If you see `[Errno -5] No address associated with hostname`, check:
1. FAL_KEY is set correctly
2. Network connectivity to fal.ai
3. API key is valid and has credits

### Storage Errors

If assets fail to upload:
1. Check GCS credentials
2. Verify bucket permissions
3. Ensure bucket name is correct in storage config

## Next Steps

1. Generate initial hero images for each audience
2. Create OG images for all landing pages
3. Build a library of approved brand assets
4. Set up automated asset generation for campaigns
