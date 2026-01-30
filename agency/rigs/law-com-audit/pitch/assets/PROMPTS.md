# Pitch Deck Asset Prompts

## Agency-Crafted Prompts for Executive Presentation

All prompts optimized for Fal Flux Schnell or Flux Pro models.
Generate at: https://fal.ai/models/fal-ai/flux/schnell/playground

---

### Base Style (append to all prompts)

```
premium executive presentation aesthetic, dark navy (#0A1628) background,
golden amber (#C9A227) accents, sophisticated consulting style,
McKinsey meets Bloomberg visual language, photorealistic, extremely clean minimal
```

---

## Cover & Section Assets

### 1. Cover Background
**ID:** `cover`
**Use:** Slide 1 - Title slide background

```
Abstract premium executive presentation background for legal intelligence company,
deep navy blue gradient with elegant gold accent lines suggesting data streams
and intelligence networks flowing diagonally across the frame,
minimalist geometric patterns, extremely sophisticated corporate luxury aesthetic
```

### 2. Section Divider - Strategy
**ID:** `divider_strategy`
**Use:** Section break slides

```
Minimalist premium section divider background,
deep navy with single elegant gold geometric accent positioned off-center,
extremely clean with large negative space for text overlay,
sophisticated consulting presentation aesthetic
```

---

## Data Visualization Assets

### 3. Timeline Convergence
**ID:** `timeline`
**Use:** Slide 2 - Inflection point

```
Abstract visualization of converging timelines representing critical business moment,
five thin golden lines converging from edges toward a bright central focal point,
suggesting urgency and pivotal decision point, elegant data visualization
```

### 4. Market Gap Comparison
**ID:** `market_gap`
**Use:** Slide 3 - Competitive gap (3x preference)

```
Minimalist bar chart abstract visualization showing dramatic competitive gap,
two vertical bars - one dramatically tall golden amber bar on left,
one much shorter muted gray bar on right, approximately 3:1 ratio,
clean geometric data visualization suggesting market dominance
```

### 5. Conversion Funnel Leak
**ID:** `funnel`
**Use:** Slide 4 - Conversion problems

```
Dramatic visualization of a business conversion funnel with leaks,
wide golden opening at top tapering severely to narrow bottom,
golden light particles and value escaping through fractures along walls,
abstract representation of lost revenue and conversion friction
```

### 6. ROI Growth Arrow
**ID:** `roi`
**Use:** Slide 17 - Return on investment

```
Dramatic exponential growth arrow visualization for investment return,
golden arrow starting small at bottom left, expanding and curving
dynamically upward to large impressive finish at top right,
premium data visualization suggesting massive ROI, aspirational
```

### 7. Risk Decline Warning
**ID:** `risk`
**Use:** Slide 18 - Risk of inaction

```
Descending trend line visualization with warning markers,
line starting high on left declining steeply to right,
three amber/red warning indicator points along the decline,
suggesting business risk and negative trajectory without action,
urgent but professional data visualization
```

---

## Strategic Concept Assets

### 8. Exclusive Assets Pillars
**ID:** `pillars`
**Use:** Slide 5 - Unique defensible assets

```
Three elegant golden pillar or trophy icons arranged horizontally,
premium minimalist 3D rendering, each pillar with subtle glow,
representing valuable exclusive business assets and competitive moats,
architectural sophistication, museum quality presentation
```

### 9. Positioning Map
**ID:** `positioning`
**Use:** Slide 6 - Strategic repositioning

```
Strategic quadrant positioning visualization for business strategy,
subtle grid with four quadrants, elegant golden curved arrow
moving from bottom-left commodity quadrant to top-right premium quadrant,
suggesting strategic transformation and repositioning journey
```

### 10. Strategy Pillars Architecture
**ID:** `strategy`
**Use:** Slide 7 - Three-pillar strategy

```
Three classical Greek columns supporting a triangular pediment structure,
rendered in elegant golden tones, architectural visualization,
suggesting strategic strength and foundational business framework,
neoclassical minimalist style, premium sophisticated aesthetic
```

### 11. Competitive Moat
**ID:** `moat`
**Use:** Slide 10 - Defensive positioning

```
Abstract geometric visualization of a fortress with protective moat,
golden wireframe castle structure surrounded by flowing defensive barrier,
suggesting competitive defense and barriers to entry,
premium architectural diagram style, strategic business visual
```

### 12. Transformation Split
**ID:** `transformation`
**Use:** Slide 11 - Before/after vision

```
Split-screen business transformation visualization,
left half shows chaotic scattered geometric fragments suggesting disorder,
right half shows organized elegant dashboard with clean aligned elements,
dramatic before and after contrast, digital transformation narrative
```

---

## Hero Images

### 13. Intelligence Platform Hero
**ID:** `hero_intel`
**Use:** Feature highlight / marketing

```
Abstract visualization of legal intelligence platform concept,
network of connected nodes suggesting data insights and knowledge,
central glowing hub radiating golden connections outward,
represents transformation from news aggregation to intelligence platform,
futuristic but grounded premium technology aesthetic
```

### 14. Benchmarking Hero
**ID:** `hero_bench`
**Use:** Data/rankings highlight

```
Abstract visualization of benchmarking and competitive rankings,
elegant tiered podium or ranking visualization with golden accents,
suggests market leadership and competitive positioning intelligence,
premium business data visualization aesthetic
```

---

## Generation Instructions

### Option 1: Fal Playground (Manual)
1. Go to https://fal.ai/models/fal-ai/flux/schnell/playground
2. Paste prompt + style base
3. Set size to 16:9 Landscape
4. Generate and download

### Option 2: Shell Script (Automated)
```bash
export FAL_KEY="your-key-here"
./generate_all_assets.sh
```

### Option 3: Python Script
```bash
export FAL_KEY="your-key-here"
python generate_direct.py
```

---

## Asset Mapping to Slides

| Asset ID | Slide | Purpose |
|----------|-------|---------|
| cover | 1 | Title background |
| timeline | 2 | Inflection point |
| market_gap | 3 | 3x competitive gap |
| funnel | 4 | Conversion leak |
| pillars | 5 | Exclusive assets |
| positioning | 6 | Repositioning map |
| strategy | 7 | Three pillars |
| moat | 10 | Competitive defense |
| transformation | 11 | Before/after |
| roi | 17 | ROI visualization |
| risk | 18 | Risk of inaction |
| divider_strategy | Sections | Section breaks |
| hero_intel | Marketing | Intelligence hero |
| hero_bench | Marketing | Rankings hero |
