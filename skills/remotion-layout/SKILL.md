# Skill: Remotion Layout Design
# Category: Video
# Version: 1.0.0

Design visual layouts and component structures for Remotion videos.

## Overview
Focus on "Video as Code." Layouts must be responsive to different aspect ratios (9:16, 16:9, 1:1) and dynamic content lengths.

## Frameworks

### 1. Atomic Video Components
- **The Wrapper**: Global sequence and transition logic.
- **The Core**: The main visual element (chart, text, image).
- **The Overlay**: Dynamic badges, progress bars, and watermarks.

### 2. The Visual Hierarchy of Motion
- **Primary**: The moving dynamic variable (the hook).
- **Secondary**: Supporting background animations.
- **Tertiary**: Subtle ambient motion (noise, glow).

### 3. Responsive Framing
- Use `useVideoConfig()` for dynamic spacing.
- Implement flexbox/grid systems within the `<AbsoluteFill>`.
- account for "Safe Zones" on social platforms (TikTok/Reels UI).

## Checklist
- [ ] Are all fonts specified with fallback weights?
- [ ] Is the color palette dynamic (primary/secondary/accent props)?
- [ ] Are easing functions specified (e.g., `bezier(0.33, 1, 0.68, 1)`)?
- [ ] Is there a clear entrance and exit animation for every component?

## Output Structure
1. **Component Architecture**: Description of the component tree.
2. **Animation Specs**: Timings, easings, and spring configurations.
3. **React/Remotion Code Snippets**: Essential code for implementation.
