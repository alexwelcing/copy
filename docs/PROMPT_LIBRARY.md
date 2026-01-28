# Asset Generation Prompt Library

High-quality prompts for generating marketing assets with FAL turbo models.

## Hero Images

### Professional/Corporate
```
Professional marketing team collaborating around large screen showing campaign dashboard,
modern glass-walled office, natural light, diverse team members engaged in discussion,
high-tech but human atmosphere, corporate photography style with warmth,
4K quality, shallow depth of field
```

### Technical/Founder Focus
```
Technical founder at minimalist standing desk, MacBook showing wireframes and code,
dual monitors with design and terminal, soft morning light through large windows,
focused expression, clean modern workspace with plants, professional photography style,
warm natural lighting, photorealistic detail
```

### Agency Aesthetic
```
Vintage advertising agency aesthetic meets modern tech, art deco elements,
brass accents on dark navy walls, strategic documents on leather desk,
warm golden hour lighting through venetian blinds, film photography grain,
sophisticated Mad Men meets Silicon Valley vibe
```

## Abstract/Conceptual

### Marketing Transformation
```
Abstract visualization of marketing transformation: old paper briefs dissolving
into digital streams of light, golden and electric blue particles flowing upward,
dark premium background, high-end tech aesthetic, cinema 4D rendering style,
sophisticated and minimal
```

### Data to Story
```
Flowing data visualization transforming into narrative elements: numbers becoming
words, charts becoming compelling headlines, all connected by glowing neural pathways,
deep space blue to warm amber gradient, futuristic but elegant
```

### Creative Process
```
Kinetic typography explosion: marketing words fragmenting and reassembling,
'COPY', 'STRATEGY', 'CAMPAIGN' in bold sans-serif, dynamic motion blur effect,
dark background with bright accent lighting, energy and transformation theme,
3D render, high contrast
```

## OG Images (Social Sharing)

### Founders
```
Split screen composition: left shows chaotic sticky notes and messy docs,
right shows clean polished landing page on screen, arrow of transformation between,
professional before/after marketing visual, bright clean background,
modern flat illustration style
```

### Freelancers
```
Freelance marketer in creative home office, multiple screens showing client campaigns,
coffee cup and plants visible, warm afternoon sunlight, productive organized chaos,
lifestyle photography style, authentic and relatable, not overly polished,
4K photorealistic
```

### Marketing Teams
```
Marketing war room: team around collaborative screen with metrics dashboard,
post-it notes on glass walls, diverse professional team celebrating success,
modern corporate office, warm professional lighting, aspirational team energy,
corporate photography with human warmth
```

## Social Media Assets

### Testimonial Backgrounds
```
Elegant gradient background from deep navy through electric purple to warm copper,
subtle noise texture for premium feel, soft lighting, modern app aesthetic,
space for text overlay in center, professional and distinctive,
perfect for quote cards
```

### Feature Cards
```
Isometric illustration of marketing workflow: landing page components floating
and assembling, colorful but cohesive palette (navy, brass, coral),
playful yet professional, modern SaaS illustration style, clean lines,
suitable for feature highlights
```

### Pattern Tiles
```
Seamless repeating pattern of abstract marketing icons: headlines, CTAs, forms,
analytics symbols, subtle monochrome on cream background, sophisticated texture,
vintage-modern hybrid aesthetic, tileable pattern, Art Deco influence
```

## Brand Assets

### Logo/Text Heavy
**Model Recommendation: `fal-ai/qwen-image-2512`**

```
Luxury brand monogram: intertwined letters 'HE' in art deco geometric style,
brass metallic texture, embossed effect on deep navy background,
vintage advertising meets modern minimalism, sharp crisp edges,
suitable for letterhead and branding
```

### Minimalist Hero
```
Single elegant cursor pointer on pristine white surface, small concentric ripple
effect spreading outward, representing the simplicity of starting,
ultra minimal composition, soft directional lighting, zen-like calm aesthetic,
premium product photography, Apple-style minimalism
```

## Video Prompts

### Explainer Animation
**Model: `fal-ai/kling-video/v2.5-turbo/pro/text-to-video`**

```
Camera slowly zooms through floating marketing elements in 3D space:
landing page components, email templates, social posts, all orbiting
a central glowing 'brief' document, smooth cinematic motion,
dark premium environment with golden accent lighting
```

### Logo Reveal
```
Brass metallic letters 'HIGH ERA' assembling from scattered particles,
each letter snaps into place with subtle impact, final frame holds with
soft glow, dark background, luxury brand reveal style, 5 seconds
```

## Audio Prompts

### Background Music
**Model: `fal-ai/stable-audio`**

```
Sophisticated background music for marketing video: blend of vintage jazz piano
with modern electronic beats, confident and professional mood, medium tempo,
30 seconds loop, suitable for corporate presentation
```

### Ambient Soundscape
```
Creative workspace ambience: soft keyboard typing, gentle paper shuffling,
distant coffee shop atmosphere, warm and focused mood, lo-fi aesthetic,
perfect for deep work or briefing sessions
```

## Prompt Engineering Tips

### For Best Results:
1. **Be Specific About Style**: "professional photography" vs "3D render" vs "illustration"
2. **Lighting Matters**: "soft morning light", "golden hour", "dramatic spotlight"
3. **Include Technical Details**: "4K", "shallow depth of field", "photorealistic"
4. **Set the Mood**: "professional", "sophisticated", "energetic", "calm"
5. **Composition**: "split screen", "center frame", "rule of thirds", "isometric view"

### What to Avoid:
- Vague descriptions: "nice image" → too general
- Too many concepts: Pick 1-2 main themes
- Contradictions: "minimalist" + "complex detailed"
- Generic AI slop words: "breathtaking", "stunning", "masterpiece"

### Model Selection:
- **Text in image?** → Use `fal-ai/qwen-image-2512`
- **Need it fast?** → Use `fal-ai/flux/schnell` or `fal-ai/fast-lightning-sdxl`
- **Premium quality?** → Use `fal-ai/flux-pro/v1.1`
- **Design/vector feel?** → Use `fal-ai/recraft-v3`

## Testing Your Prompts

1. Start with a turbo model for speed
2. Generate 3-4 variations
3. Note what works and doesn't work
4. Refine the prompt
5. Try premium model for final version

## Prompt Templates

### Template: Hero Image
```
[Subject] in [environment], [specific details], [lighting], 
[mood/emotion], [photography style], [technical specs]
```

### Template: Abstract Concept
```
Abstract visualization of [concept]: [visual metaphor], 
[color scheme], [style reference], [rendering type], [mood]
```

### Template: Social Share
```
[Composition type]: [left side], [right side], [connecting element],
[style], [background], [intended platform]
```

## Real Examples from Our Library

These prompts generated actual assets used in production:

**Homepage Hero** (FLUX Schnell):
```
Vintage advertising agency desk with modern laptop, brass desk lamp illuminating 
strategic documents, art deco wallpaper background, warm golden hour light,
sophisticated Mad Men aesthetic meets Silicon Valley, film photography grain,
professional high-end marketing mood
```

**Founder OG Image** (FLUX Pro 1.1):
```
Technical founder reviewing polished pitch deck on iPad, confident expression,
modern minimalist office backdrop, warm natural lighting, business casual attire,
aspirational but approachable, LinkedIn-style professional photography,
shallow depth of field, 4K quality
```

**Brand Pattern** (Recraft V3):
```
Seamless geometric pattern: marketing icons as art deco motifs, brass on navy,
subtle texture, vintage advertising meets modern design system, tileable,
sophisticated brand asset, vector-style precision
```

## Share Your Prompts

Found a great prompt? Add it to this library via PR or share in Discussions!
