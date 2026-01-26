# Example: Remotion-Script
**Date:** 2026-01-26
**Status:** ⚠️ Needs Polish
**Score:** 0/10

## The Brief
**Task:** Create a 15-second video script announcing the 'Twin-Engine' workflow.
**Context:** {
  "product": "High Era",
  "visual_style": "Kinetic typography, split screen"
}

---

## The Output
# Remotion Script: Twin-Engine Workflow Announcement

## 1. Script Table

| Scene | Timing | Audio (Script) | Visual (Components) |
|-------|--------|----------------|---------------------|
| **Hook** | 0-3s | "Introducing Twin-Engine: {{company_name}}'s breakthrough workflow that doubles your creative velocity." | Split screen appears with kinetic typography:<br>- LEFT: "TWIN-ENGINE" animates in (bold, staggered letters)<br>- RIGHT: Velocity meter animating from 1x → 2x<br>**Transition**: Slide in from edges with elastic easing |
| **Problem → Solution** | 3-8s | "Stop choosing between speed and quality. Now your team runs both simultaneously—creative on one side, execution on the other." | Split screen demonstration:<br>- LEFT: "CREATIVE" with brain icon, flowing organic shapes<br>- RIGHT: "EXECUTION" with gear icon, geometric precision<br>- CENTER: Lightning bolt connecting both sides<br>**Animation**: Particles flowing between engines<br>**Transition**: Synchronized pulse effect |
| **Value Proof** | 8-12s | "High Era clients ship {{percentage}}% faster while maintaining premium standards. Two engines. One unstoppable output." | Kinetic data visualization:<br>- Speed metrics animating upward<br>- Quality checkmarks cascading<br>- Split screen merges into unified "HIGH ERA" wordmark<br>**Animation**: Counter numbers rolling up<br>**Transition**: Convergence effect (screens merge) |
| **CTA** | 12-15s | "Ready to ignite your workflow? Discover Twin-Engine at {{website_url}}" | Full screen call-to-action:<br>- "DISCOVER TWIN-ENGINE" in bold kinetic type<br>- URL appears below with subtle pulse<br>- Brand colors (assume: gradient background)<br>**Animation**: CTA text explodes in from center<br>**Transition**: Scale + fade with anticipation easing |

---

## 2. Variable Map

### Required Dynamic Variables
```javascript
{
  company_name: String,        // Client's company name
  percentage: Number,          // Performance improvement metric (suggest: 40-60)
  website_url: String,         // Landing page URL
}
```

### Optional Enhancement Variables
```javascript
{
  client_logo: String (URL),   // For personalized versions
  industry: String,            // For industry-specific copy variants
  user_name: String,           // For hyper-personalized versions
}
```

---

## 3. Remotion Context

### Key Props Structure
```typescript
interface TwinEngineVideoProps {
  // Dynamic content
  companyName: string;
  percentage: number;
  websiteUrl: string;
  
  // Visual configuration
  primaryColor: string;      // Default: "#FF6B35"
  secondaryColor: string;    // Default: "#004E89"
  accentColor: string;       // Default: "#F7B801"
  
  // Timing controls
  fps: number;               // Recommended: 30
  durationInFrames: number;  // 450 frames @ 30fps = 15s
}
```

### State Management Recommendations

**Scene Composition Architecture:**
```
<Composition>
  <Sequence from={0} durationInFrames={90}>
    <HookScene /> {/* 0-3s */}
  </Sequence>
  
  <Sequence from={90} durationInFrames={150}>
    <ProblemSolutionScene /> {/* 3-8s */}
  </Sequence>
  
  <Sequence from={240} durationInFrames={120}>
    <ValueProofScene /> {/* 8-12s */}
  </Sequence>
  
  <Sequence from={360} durationInFrames={90}>
    <CTAScene /> {/* 12-15s */}
  </Sequence>
</Composition>
```

### Animation Recommendations

**Kinetic Typography Settings:**
- Font: Bold sans-serif (Montserrat Bold, Inter Black, or custom brand font)
- Letter stagger delay: 0.05s per character
- Entry animation: `spring({ fps: 30, config: { damping: 200, stiffness: 90 } })`

**Split Screen Management:**
```javascript
// Use interpolate for smooth transitions
const splitPosition = interpolate(
  frame,
  [0, 30, 330, 360],
  [100, 50, 50, 0], // Percentage from center
  { extrapolateRight: 'clamp' }
);
```

**Color Pulse Effect:**
```javascript
const pulseOpacity = interpolate(
  frame % 30, // Repeat every second
  [0, 15, 30],
  [0.6, 1, 0.6],
  { easing: Easing.inOut(Easing.ease) }
);
```

### Component-Specific Notes

**Scene 1 (Hook):**
- Use `@remotion/motion-blur` for the sliding text
- Implement `continueRender()` / `delayRender()` if loading custom fonts
- Z-index: Typography layer (z:20) above meter animation (z:10)

**Scene 2 (Problem→Solution):**
- Particle system: Use `<AbsoluteFill>` with randomized `<div>` elements
- Implement collision detection boundaries at split line
- Icon animations: Rotate + scale combined (creative = organic rotation, execution = precise 90° snaps)

**Scene 3 (Value Proof):**
- Counter animation: Use `Math.floor()` with interpolate for rolling numbers
- Checkmark SVG animations: Stagger by 0.1s intervals
- Merge effect: Use clip-path transition from two rects to one

**Scene 4 (CTA):**
- Text explosion: Use radial origin with individual letter trajectories
- Add subtle motion to URL (prevent static feel)
- Consider adding a glowing border animation around CTA area

---

## 4. Quality Checklist Results

- [x] **Dynamic variables clearly identified**: `{{company_name}}`, `{{percentage}}`, `{{website_url}}`
- [x] **Timing specified**: All scenes have precise second markers (0-3s, 3-8s, 8-12s, 12-15s)
- [x] **Script under 150 words**: Current count: 67 words
- [x] **Z-pattern consideration**: Visual flow moves LEFT → RIGHT → CENTER → FULL SCREEN
- [x] **Remotion developer instructions**: Comprehensive transitions, easing functions, and component architecture provided

---

## 5. Alternative Versions

### A/B Testing Variants

**Variant A: Metric-Forward Hook**
```
"{{company_name}} teams are shipping {{percentage}}% faster with Twin-Engine..."
```
*Use when: Targeting data-driven decision makers*

**Variant B: Question Hook**
```
"What if {{company_name}} could double output without doubling headcount?"
```
*Use when: Targeting cost-conscious executives*

**Variant C: Direct Challenge**
```
"{{company_name}}: Your creative process is single-threaded. Here's the parallel solution."
```
*Use when: Targeting technical/engineering-minded audiences*

---

## 6. Technical Optimization Notes

### Performance Recommendations
- **Render strategy**: Use `<OffthreadVideo>` for any background video assets
- **Font loading**: Preload fonts using Remotion's `staticFile()` API
- **Export settings**: H.264, 1080p @ 30fps, CRF 18 for social media distribution
- **File size target**: <5MB for optimal loading (use two-pass encoding if needed)

### Accessibility Considerations
- Add captions as a separate `<Sequence>` layer with high contrast
- Ensure color contrast ratio of 4.5:1 minimum for all text
- Provide alt text props for any iconography
- Consider adding an audio description track variant

---

## 7. Implementation Priority

**Phase 1 (MVP):**
1. Build basic split-screen layout with static content
2. Implement kinetic typography for main headlines
3. Add percentage counter animation

**Phase 2 (Enhancement):**
1. Add particle flow system between engines
2. Implement spring physics for transitions
3. Polish timing with easing curves

**Phase 3 (Scale):**
1. Create variable injection system for bulk rendering
2. Build template variants for A/B testing
3. Implement dynamic color theming based on brand input

---

**Estimated Development Time**: 8-12 hours for full implementation
**Recommended Testing**: Render 5 variants with different data to verify variable injection system

---

## Quality Assurance
**Critique:** Failed to parse evaluation.
