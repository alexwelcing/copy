# Vision & Asset Strategy: The "High Era" Identity

## 1. Core Visual Identity
**Concept**: "High Era" / "Madison Avenue 2026"
**Vibe**: Tactile, Cinematic, Mid-Century Modern meets Hard Sci-Fi.
**Key Elements**:
- **Texture**: Film grain, paper stock, ink bleed, dust particles.
- **Lighting**: Soft sunlight, "Golden Hour" office lighting, cinematic rim lighting.
- **Typography**: Swiss Style (Helvetica/Akzidenz), Typewriter monospaced, Elegant Serif (Caslon/Baskerville).
- **Palette**: Navy, Brass, Cream, Charcoal, muted Electric Indigo (for the AI accent).

## 2. Asset Strategy Plan

We will leverage specific FAL.ai models to generate assets that strictly adhere to this identity.

### A. Hero Imagery (The "Hook")
**Goal**: Establish the "Human Side of Automation" metaphor immediately.
**Subject**: A fusion of vintage office tools (typewriters, rolodexes) with subtle futuristic elements (holographic interfaces, floating data).
**Model Protocol**: `FLUX_PRO_1_1` (fal-ai/flux-pro/v1.1)
- **Why**: Best-in-class photorealism and composition adherence.
- **Prompt Strategy**: "Cinematic 35mm film shot, depth of field, Kodak Portra 400..."

### B. UI/UX Elements (The "Interface")
**Goal**: Make the tool feel like a physical artifact.
**Assets**:
- **Icons**: Hand-drawn or "stamped" style icons.
- **Diagrams**: Technical schematics on blueprint or graph paper.
**Model Protocol**: `RECRAFT_V3` (fal-ai/recraft-v3) or `FLUX_PRO` with style transfer.
- **Why**: Recraft excels at vector/illustration styles consistent with brand guidelines.

### C. Motion Backgrounds (The "Atmosphere")
**Goal**: Subtle movement to keep the page alive without distraction.
**Subject**: Slow pans over textures (paper, leather, wood) or dust motes dancing in light.
**Model Protocol**: `KLING_V1_STANDARD` (fal-ai/kling-video/v1/standard/text-to-video) or `LTX_VIDEO_DISTILLED`.
- **Why**: High fidelity motion, capable of "subtle" movement which is hard for many models.

### D. Typography & Textures
**Goal**: Headlines that look printed, not rendered.
**Model Protocol**: `QWEN_IMAGE_2512`
- **Why**: Industry leader in rendering legible text within images.

## 3. Implementation Roadmap

### Phase 1: The "Dogfood" Loop (Current)
- Use `scripts/dogfood.py` to iteratively generate and refined Hero candidates.
- Store best assets in `frontend/static/assets/`.

### Phase 2: Dynamic Injection
- Update `frontend/src/routes/+page.svelte` to pull "Approved" assets dynamically from a manifest or CMS (simulated via JSON).

### Phase 3: Personalized Assets
- Allow users to generate their own "Brand Assets" using the same pipelines (e.g., "Generate a logo in High Era style").

## 4. Model Registry (From Lexicon)

| Asset Type | Primary Model | Backup Model |
| :--- | :--- | :--- |
| **Hero Photo** | `fal-ai/flux-pro/v1.1` | `fal-ai/flux/dev` |
| **Vector/Icon** | `fal-ai/recraft-v3` | `fal-ai/flux-pro` (w/ LoRA) |
| **Motion/Video** | `fal-ai/kling-video/v1/standard` | `fal-ai/ltx-2-19b/distilled` |
| **Text/Layout** | `fal-ai/qwen-image-2512` | `fal-ai/ideogram` |
| **Editing** | `fal-ai/nano-banana-pro/edit` | `fal-ai/flux-pro/v1.1-fill` |

---
*Drafted by Agency AI - January 25, 2026*
