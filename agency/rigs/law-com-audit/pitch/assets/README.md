# Pitch Deck Asset Generation

Premium visual assets for the Law.com Executive Pitch Deck.

## Quick Start

```bash
cd agency/rigs/law-com-audit/pitch/assets

# Set your Fal API key
export FAL_KEY='your-key-here'

# Verify setup
make setup

# Generate all assets
make generate
```

## Commands

| Command | Description |
|---------|-------------|
| `make setup` | Verify environment and dependencies |
| `make verify` | Test API key validity |
| `make preview` | Generate single test asset |
| `make generate` | Generate all 14 premium assets |
| `make clean` | Remove generated assets |

## Scripts

### Premium Generator (Recommended)
```bash
python generate_premium.py
```
- Uses **Flux Pro 1.1** for highest quality
- 14 assets with carefully crafted prompts
- James Turrell / Bloomberg aesthetic
- Outputs to `./generated_assets/`

### Fast Generator
```bash
./generate_all_assets.sh
```
- Uses **Flux Schnell** for speed
- Same 14 assets, simpler prompts
- Lower quality but faster

## Output

Generated assets are saved to `./generated_assets/`:

```
generated_assets/
├── cover.png           # Slide 1 - Title background
├── inflection.png      # Slide 2 - Convergence moment
├── dominance.png       # Slide 3 - Market gap (3x)
├── leaking_value.png   # Slide 4 - Conversion funnel
├── three_assets.png    # Slide 5 - Exclusive assets
├── repositioning.png   # Slide 6 - Strategy journey
├── foundation.png      # Slide 7 - Three pillars
├── fortress.png        # Slide 10 - Competitive moat
├── transformation.png  # Slide 11 - Before/after
├── growth.png          # Slide 17 - ROI curve
├── decline.png         # Slide 18 - Risk trajectory
├── section_break.png   # Section dividers
├── intelligence.png    # Hero - Platform concept
├── rankings.png        # Hero - Benchmarking
└── manifest.json       # Generation metadata
```

## API Key

Get a Fal API key at: https://fal.ai/dashboard/keys

The key format is: `key_id:key_secret`

Flux Pro 1.1 costs approximately $0.05 per image.
Full generation: ~$0.70 total.

## Design System

All assets follow the pitch deck design language:

- **Navy**: `#0A1628` - Deep backgrounds
- **Gold**: `#C9A227` - Accent elements
- **Cream**: `#F8F6F1` - Highlights

Visual style: Minimal, contemplative, premium consulting aesthetic.
Inspired by James Turrell light installations and Bloomberg terminal design.

## Troubleshooting

**"FAL_KEY not set"**
```bash
export FAL_KEY='your-key-here'
```

**"HTTP 401: Unauthorized"**
- Your API key is invalid or expired
- Get a new one at https://fal.ai/dashboard/keys

**"HTTP 402: Payment Required"**
- Insufficient credits
- Add credits at https://fal.ai/dashboard/billing

**Connection timeout**
- Flux Pro 1.1 can take 30-60s per image
- Script has 180s timeout, should be sufficient
