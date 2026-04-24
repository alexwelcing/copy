# Positioning Brief: Lupine

**Agent:** Strategist
**Date:** April 24, 2026
**Status:** Draft — ready for Director review

---

## Audience

**Primary:** Computational materials scientists (PhD students, postdocs, PIs) who run molecular dynamics and DFT simulations daily. They know LAMMPS intimately. They've written wrapper scripts they're ashamed of. They've lost weeks to toolchain bugs that had nothing to do with their actual research.

**Secondary:** Lab directors and national lab program managers who sign off on tool adoption and worry about license costs, foreign dependencies, and whether new postdocs can actually reproduce last year's results.

**Tertiary:** Industry R&D teams (battery, semiconductor, aerospace) where simulation cycle time directly maps to revenue timeline.

---

## Current Belief

"The tools are bad, but they're what we have. VASP works if you can afford it. LAMMPS works if you can wrangle it. Visualization means OVITO or matplotlib hacks. Every new project starts with a week of plumbing before any science happens. This is just how computational materials science works."

They've internalized the friction as a feature of the field, not a solvable problem.

---

## Desired Belief

"There's now a single platform that does what my 5-tool pipeline does — faster, in the browser, with formal verification I can trust. I can start doing science in minutes instead of days. And it's open source, so I'm not locked into another Austrian monopoly."

---

## Key Tension

**Researchers lose more time fighting their tools than doing their research.** Every simulation workflow is a brittle chain of disconnected software, proprietary licenses, and unverified scripts. The field's infrastructure hasn't kept pace with the science — ML potentials are ready, WebGPU is ready, but the toolchain is stuck in 1995.

---

## Differentiator

Lupine is the only platform that unifies DFT, ML potentials, MD simulation, and visualization in a single Rust codebase with formal verification. Everything else is either:
- A point solution (OVITO = viz only, VASP = DFT only)
- A legacy monolith (LAMMPS = 30 years of bolted-on code)
- A database, not a tool (Materials Project)

**The wedge:** Lupine View ships free today and is immediately better than OVITO for browser-based visualization. It's the Trojan horse — researchers try it for viz, discover the platform.

---

## Proof Points

| Claim | Evidence |
|-------|----------|
| Speed | 10M+ atoms at 60fps (WebGPU), 1000x vs pure DFT |
| Scientific rigor | 15 canonical laws recovered, 47 theorems proven in Lean 4 |
| Validation | R² = 1.000 (Stokes-Einstein), R² = 0.997 (Hall-Petch) |
| Integrity | Simpson's Paradox fabrication detected and flagged |
| Accessibility | Zero install — runs in browser via WASM + WebGPU |
| Trust | Apache 2.0 open source core |
| Scale | 60 papers analyzed, 38 abstracts fetched, 27 DOIs indexed |

---

## Core Message

**"One platform. Real science. No plumbing."**

Alternate framings (test these):
- "Materials science infrastructure, rebuilt from scratch"
- "From simulation to discovery — one command"
- "The toolchain researchers deserve"

---

## Tone

**Technically precise, never breathless.** These are PhD-level scientists — they can smell marketing from a mile away. The copy should sound like a brilliant colleague explaining what they built, not a startup pitching VCs.

- Specific over vague ("10M atoms at 60fps" not "blazing fast")
- Show the math, show the proof
- Dry wit is fine; enthusiasm is fine; hype is not
- Respect the reader's expertise — never explain what DFT is
- Let the benchmarks speak

---

## Avoid

- **"Revolutionary" / "game-changing" / "disruptive"** — every startup says this; researchers tune it out
- **Oversimplifying the science** — the audience knows more than you do
- **Attacking LAMMPS directly** — researchers have emotional attachment to their tools; position as "what comes next" not "LAMMPS is bad"
- **Vague speed claims** — always quantify (atoms, fps, R² values)
- **Enterprise sales language** — "unlock value", "drive outcomes", "leverage"
- **Promising what isn't shipped** — clearly delineate View (live) vs. platform (coming)

---

## Psychology Triggers (Ranked by Audience Fit)

| Trigger | Application | Priority |
|---------|-------------|----------|
| **Authority** | Lean 4 proofs, recovered canonical laws, R² values — this audience trusts math, not testimonials | Highest |
| **Loss aversion** | "How many weeks have you lost to pipeline debugging this year?" | High |
| **Social proof** | Community adoption metrics once available; for now, LAMMPS user count (50K+) as addressable peer group | Medium |
| **Reciprocity** | Lupine View is free — give value before asking for anything | High |
| **Scarcity (authentic)** | Sovereignty angle — "How long before your VASP license becomes a geopolitical liability?" | Medium (for gov/lab segment) |
| **Commitment** | Free viz tool → try simulation → adopt platform (graduated commitment ladder) | High |

---

## Segment-Specific Messaging

### Grad Students / Postdocs
- **Lead with:** Zero install, free, works in browser
- **Hook:** "Drag your LAMMPS dump file into a browser tab. That's it."
- **Objection to address:** "Is this actually production-quality?"
- **Proof:** Show the Lean 4 verification — "more formally verified than the tool you're using now"

### PIs / Lab Directors
- **Lead with:** Reproducibility, student onboarding time, license cost elimination
- **Hook:** "New postdoc, productive on day one — not day fourteen"
- **Objection to address:** "We can't switch mid-project"
- **Proof:** LAMMPS file compatibility, Apache 2.0 (no lock-in)

### National Labs / Sovereign Buyers
- **Lead with:** Apache 2.0, Rust (auditable, memory-safe), no foreign dependency
- **Hook:** "Open-source materials infrastructure your nation controls"
- **Objection to address:** "Can this actually replace VASP for our workflows?"
- **Proof:** DFT + ML potential benchmark parity

### Industry R&D
- **Lead with:** Speed (1000x), unified pipeline, collaboration
- **Hook:** "Simulation to results in hours, not months"
- **Objection to address:** "We need enterprise support"
- **Proof:** Formal verification as quality guarantee

---

## Strategic Recommendations

1. **Lead with Lupine View as the wedge.** It's free, it's shipping, it's immediately better than OVITO for browser viz. Every researcher who drops a LAMMPS file into View is a future platform user. This is the reciprocity play.

2. **Build comparison pages for each competitor.** "Lupine vs VASP", "Lupine vs OVITO", "LAMMPS alternatives" — these are high-intent SEO keywords with low competition in scientific computing.

3. **Publish benchmark papers, not blog posts.** This audience trusts arXiv preprints and reproducible benchmarks over marketing content. A paper showing Lean 4 verification of simulation results would be the most powerful marketing asset possible.

4. **Sovereignty is a channel, not the headline.** For most researchers, "it works better and it's free" is enough. The sovereignty angle is a sales conversation for gov/lab procurement, not website hero copy.

5. **Don't launch on Product Hunt.** This audience isn't there. Launch on Hacker News (Show HN), the LAMMPS mailing list, and relevant arXiv discussion channels. A well-written Show HN with benchmarks will travel further than any launch day playbook.

---

HANDOFF: Strategist → Copywriter

## Strategy Complete

**Audience**: Computational materials scientists running MD/DFT daily
**Core message**: One platform. Real science. No plumbing.
**Differentiator**: Only unified DFT + ML + MD + viz platform, formally verified, open source
**Proof points**: Lean 4 theorems, R² benchmarks, 10M atom rendering, Apache 2.0
**Tone**: Technically precise, benchmark-driven, zero hype

## For Copy Development

Priority deliverable: Homepage / hero section rewrite with segment-specific landing pages
Key constraint: Never talk down to the audience — they are the experts
Reference: Current site at lupine.science; use their existing proof points but tighten framing

I'll be available for questions. Flag anything that feels off.
