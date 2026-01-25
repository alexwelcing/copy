# Brand Visual Guide: Remotion Vision Persona
# Version 1.0.0

This guide defines the visual identity for the "Remotion Vision" expansion of the Marketing Agency platform. It reflects a shift from static copy to dynamic, programmatic video intelligence.

## 1. Core Concept: "The Kinetic Pulse"
The brand identity is built on the concept of **Kinetic Intelligence**—the intersection of programmatic precision and cinematic motion.

## 2. Color Palette

### Primary: Electric Indigo
- **HEX**: `#4F46E5`
- **Purpose**: Brand primary, action buttons, dynamic variable highlights.
- **Vibe**: High-energy, professional, digital-first.

### Secondary: Cyber Mint
- **HEX**: `#10B981`
- **Purpose**: Success states, growth metrics, data-driven overlays.
- **Vibe**: Performance, precision.

### Accent: Neon Pulse (Glow)
- **HEX**: `#F472B6`
- **Purpose**: Motion paths, highlights in video, attention-grabbing elements.
- **Vibe**: Creativity, human-touch AI.

### Neutral: Deep Space
- **HEX**: `#0F172A` (Backgrounds)
- **HEX**: `#1E293B` (Panels)
- **HEX**: `#94A3B8` (Muted text)

## 3. Typography
- **Primary Font**: `Inter` (Sans-serif) - Clean, readable, programmatic.
- **Monospace Font**: `JetBrains Mono` - Used for dynamic variables and code-as-video snippets.
- **Hierarchy**:
  - H1: 2.5rem, SemiBold, Tight tracking.
  - H2: 1.5rem, Medium.
  - Body: 1rem, Regular, Open leading (1.6).

## 4. Visual Elements

### Motion Blur Icons
Icons should have a subtle horizontal motion blur effect to represent speed and progression.

### Glassmorphism
Panels use `backdrop-filter: blur(12px)` with a subtle white border (`rgba(255,255,255,0.1)`) to feel layered and modern.

### The "Dynamic Brackets"
Use `{{ }}` as a visual motif in the UI to highlight where the AI is injecting programmatic intelligence into the video.

## 5. Tone of Voice
- **Direct**: No fluff.
- **Fast**: Emphasize "30 seconds" and "100 TPS".
- **Empowering**: "You are the director, the AI is the crew."

## 6. Remotion Component Strategy
When generating Remotion code, the "Persona" should follow these rules:
- **Duration**: Default to 15-30 seconds.
- **FPS**: 30 or 60.
- **Easings**: Use `spring()` for UI elements and `bezier(0.33, 1, 0.68, 1)` for text.
- **Personalization**: Always include at least 3 props for dynamic injection.
