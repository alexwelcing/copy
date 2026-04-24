# Competitive Positioning Analysis: Lupine

**Agent:** Strategist (with `competitor-alternatives` skill)
**Date:** April 24, 2026
**Status:** Draft

---

## Competitive Landscape Map

```
                        Proprietary
                            │
                   VASP ●   │
                            │
         Paid ──────────────┼──────────────── Free/OSS
                            │
              OVITO Pro ●   │          ● Lupine (target position)
                            │     ● LAMMPS
                            │  ● Materials Project
                        Open Source
```

**Lupine's target quadrant:** Open source + unified platform (currently unoccupied)

---

## Competitor Battle Cards

### VASP (Vienna Ab initio Simulation Package)

| Dimension | Detail |
|-----------|--------|
| **What it does** | DFT calculations — the gold standard for quantum-level accuracy |
| **Strength** | 30+ years of validated results, massive citation base, trusted by reviewers |
| **Weakness** | $4,500/license, proprietary, Austrian-held (sovereignty risk), DFT only (no MD, no viz) |
| **Their users say** | "It's expensive but I trust the results" / "My reviewer expects VASP" |
| **Our angle** | "DFT-accuracy at MD speed, formally verified, no license fee, no foreign dependency" |
| **Objection** | "Can Lupine reproduce VASP results?" → Show benchmark parity with R² values |
| **SEO keywords** | "VASP alternative", "VASP free alternative", "VASP license cost", "open source DFT" |

### LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator)

| Dimension | Detail |
|-----------|--------|
| **What it does** | Molecular dynamics simulation engine — most widely used MD code |
| **Strength** | Free, open source, 50K+ users, massive ecosystem of potentials and scripts |
| **Weakness** | 1995 codebase, fragmented GPU support, no built-in visualization, steep learning curve, reproducibility issues |
| **Their users say** | "I've spent years learning it" / "The documentation is a maze but I know my way" |
| **Our angle** | NOT "LAMMPS is bad" — instead: "Lupine reads your LAMMPS files. Start there." Respect the relationship. |
| **Objection** | "I have years of LAMMPS scripts" → "Drag your dump files into Lupine View right now. Zero migration needed for viz." |
| **SEO keywords** | "LAMMPS visualization", "LAMMPS alternatives", "LAMMPS WebGPU", "molecular dynamics visualization" |

### OVITO (Open Visualization Tool)

| Dimension | Detail |
|-----------|--------|
| **What it does** | Molecular visualization and analysis — the standard viz tool for MD researchers |
| **Strength** | Purpose-built for materials science viz, good analysis plugins |
| **Weakness** | Pro version is paid, desktop-only, no browser support, can't handle 10M+ atoms smoothly |
| **Their users say** | "It works but I wish I could share visualizations without making everyone install it" |
| **Our angle** | "Lupine View: 10M atoms at 60fps in your browser. Free. Drag and drop." Direct feature superiority. |
| **Objection** | "OVITO has analysis features Lupine doesn't" → "View is the visualization layer. The full platform does analysis too." |
| **SEO keywords** | "OVITO alternative", "OVITO free alternative", "molecular visualization browser", "WebGPU molecular visualization" |

### Materials Project

| Dimension | Detail |
|-----------|--------|
| **What it does** | Materials property database — lookup, not simulation |
| **Strength** | Huge curated database, DOE-backed, widely cited |
| **Weakness** | Read-only — can't run simulations, can't customize, not a workflow tool |
| **Their users say** | "Great for looking up properties but I still need my own simulations" |
| **Our angle** | Complementary, not competitive. "Start with Materials Project data, simulate in Lupine." |
| **SEO keywords** | "materials simulation platform", "computational materials science tools" |

### Custom Scripts / DIY Pipelines

| Dimension | Detail |
|-----------|--------|
| **What it does** | Researcher-built Python/Bash glue connecting VASP + LAMMPS + OVITO + matplotlib |
| **Strength** | Fully customized to the researcher's workflow |
| **Weakness** | Fragile, non-reproducible, non-shareable, breaks when people leave the lab |
| **Their users say** | "It works on my machine" / "Don't touch the pipeline, nobody knows how it works" |
| **Our angle** | "Stop maintaining your Frankenstein pipeline. One platform, reproducible, shareable." |
| **Objection** | "My pipeline does exactly what I need" → "How long does it take a new student to use it?" |

---

## Comparison Page Strategy

Build these pages (high-intent SEO + direct conversion):

### Page 1: "Lupine vs VASP"
- **URL:** `/compare/vasp`
- **Angle:** Cost, openness, sovereignty, speed
- **Key table:** License cost, source availability, formal verification, browser access
- **CTA:** "Try Lupine View free — see the difference in your browser"

### Page 2: "Lupine vs OVITO"
- **URL:** `/compare/ovito`
- **Angle:** Browser-native, free, performance at scale
- **Key table:** Atom count rendering, browser support, price, file format support
- **CTA:** "Drag your LAMMPS file into Lupine View right now"

### Page 3: "LAMMPS Visualization Tools" (not "vs LAMMPS")
- **URL:** `/guides/lammps-visualization`
- **Angle:** Helpful guide that positions Lupine View as the best option
- **Key table:** Feature comparison of viz options for LAMMPS users
- **CTA:** "Visualize your LAMMPS data in 2 seconds"

### Page 4: "Open Source Materials Science Software"
- **URL:** `/guides/open-source-materials-science`
- **Angle:** Category ownership — become the definitive resource
- **Key table:** Full landscape of open source tools with Lupine's position
- **CTA:** "Lupine: the open-source platform that ties it all together"

### Page 5: "Best Molecular Dynamics Software [2026]"
- **URL:** `/guides/molecular-dynamics-software`
- **Angle:** Comprehensive comparison that ranks Lupine highly
- **Key table:** All major MD tools compared on features, price, platform
- **CTA:** "Start with Lupine View — free, no install"

---

## Positioning Statement

> For computational materials scientists who lose weeks to fragmented toolchains, Lupine is the unified simulation platform that combines DFT, ML potentials, MD, and visualization in one formally verified, open-source codebase. Unlike VASP, it's free and open. Unlike LAMMPS, it's modern and integrated. Unlike OVITO, it runs in your browser at 10M+ atoms.

---

## Win/Loss Themes

**We win when:**
- Researcher is frustrated with tool fragmentation
- Lab is onboarding new students/postdocs
- Cost of VASP licenses is a budget conversation
- Sovereignty or security is a procurement factor
- Researcher wants to share visualizations without install requirements

**We lose when:**
- Researcher has deep VASP expertise and reviewers expect VASP citations
- Lab has existing infrastructure investment they can't abandon mid-project
- Features needed aren't yet shipped (platform beyond View)
- Researcher needs a specific LAMMPS potential that isn't yet supported

**We respond to "we lose" scenarios:**
- VASP citations → publish benchmark papers showing parity
- Existing infrastructure → LAMMPS file compatibility as bridge
- Features not shipped → "Start with View today, platform is coming"
- Missing potentials → community contribution roadmap (Apache 2.0)
