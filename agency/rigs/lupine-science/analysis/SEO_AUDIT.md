# SEO Audit & Strategy: Lupine

**Agent:** Optimizer (with `seo-audit` + `programmatic-seo` skills)
**Date:** April 24, 2026
**Status:** Draft

---

## Executive Summary

Lupine has strong technical content and legitimate proof points, but the site is currently structured as an investor pitch, not a search acquisition funnel. The highest-impact moves are: (1) add comparison/alternative pages targeting high-intent keywords, (2) implement schema markup, (3) restructure for topic authority around "computational materials science" as a category, and (4) build a programmatic SEO engine around LAMMPS potentials/file formats.

**Overall SEO Health: Early Stage (40/100)**
- Technical: 50/100 (functional but no schema, unclear meta)
- On-Page: 45/100 (decent headings, missing meta descriptions, no keyword targeting)
- Content: 35/100 (strong depth, but written for investors not searchers)
- Off-Page: 20/100 (new domain, no backlink profile yet)

---

## Technical SEO Issues

### Critical

| Issue | Impact | Fix |
|-------|--------|-----|
| No structured data / schema markup | Missing rich snippets, no SoftwareApplication schema | Add JSON-LD: SoftwareApplication, Organization, Article for each page |
| No meta descriptions visible | Google generates its own (usually poorly) | Write unique meta description per page, 150-160 chars |
| No robots.txt / sitemap.xml (likely) | Crawl efficiency | Generate and submit to Google Search Console |

### High

| Issue | Impact | Fix |
|-------|--------|-----|
| Title tag is branding-heavy | "Lupine Materials Science — The Future of..." wastes keyword space | Rewrite: "Lupine — Open Source Materials Simulation Platform \| DFT + MD + ML" |
| No canonical tags visible | Potential duplicate content | Add canonical tags to all pages |
| Static HTML pages (.html extensions) | Not inherently bad but limits dynamic SEO | Consider removing .html extensions for cleaner URLs |

### Medium

| Issue | Impact | Fix |
|-------|--------|-----|
| Image alt text likely missing/generic | Lost image search traffic | Add descriptive alt text: "WebGPU molecular visualization of 10 million atoms in Lupine View" |
| No Open Graph / Twitter Card meta | Poor social sharing previews | Add OG tags with compelling descriptions and preview images |
| Internal linking is navigation-only | No contextual cross-linking | Add in-content links between related pages |

---

## On-Page SEO Analysis

### Current Page Titles (Assessed)

| Page | Current Title (Estimated) | Recommended Title |
|------|--------------------------|-------------------|
| Homepage | "Lupine Materials Science — The Future of Computational Materials" | "Lupine — Open Source Computational Materials Science Platform" |
| Research Manifesto | Likely generic | "Why Materials Science Needs New Infrastructure \| Lupine Research" |
| Platform Architecture | Likely generic | "Unified DFT + MD + ML Platform Architecture \| Lupine" |
| ML Potentials Guide | Likely generic | "Machine-Learned Interatomic Potentials Guide \| MACE, NequIP \| Lupine" |
| Formal Verification | Likely generic | "Formally Verified Materials Simulation with Lean 4 \| Lupine" |
| Battery Case Study | Likely generic | "Battery Materials Discovery with ML Potentials \| Lupine Case Study" |
| Superalloys Case Study | Likely generic | "Superalloy Simulation at Scale \| Lupine Case Study" |

### Heading Structure Assessment

**Good:** H1 is clear and benefit-oriented. H2s create logical sections.
**Issue:** H1 ("Discover New Materials Before They Exist") is poetic but not keyword-rich. Consider adding a keyword-rich subtitle.
**Fix:** Keep the H1 for humans, add a visible subtitle: "The open-source platform unifying DFT, molecular dynamics, and ML potentials"

---

## Keyword Strategy

### Tier 1: High Intent, Low Competition (Target Now)

These are searches by people actively looking for solutions. Scientific computing has dramatically lower SEO competition than consumer markets.

| Keyword Cluster | Est. Monthly Volume | Competition | Page to Target |
|----------------|---------------------|-------------|----------------|
| "VASP alternative" / "VASP free alternative" | 200-500 | Low | /compare/vasp |
| "OVITO alternative" / "OVITO free" | 100-300 | Very Low | /compare/ovito |
| "LAMMPS visualization" / "LAMMPS visualize" | 500-1000 | Low | /guides/lammps-visualization |
| "molecular dynamics visualization" | 300-600 | Low-Med | /guides/lammps-visualization |
| "open source DFT software" | 200-400 | Low | /compare/vasp |
| "WebGPU molecular visualization" | 50-100 | Very Low | Homepage / View page |

### Tier 2: Category Ownership (Build Authority)

| Keyword Cluster | Est. Monthly Volume | Competition | Page to Target |
|----------------|---------------------|-------------|----------------|
| "computational materials science software" | 300-600 | Low | /guides/open-source-materials-science |
| "molecular dynamics software" / "best MD software" | 500-1000 | Low-Med | /guides/molecular-dynamics-software |
| "materials simulation platform" | 200-400 | Low | Homepage |
| "machine learned interatomic potentials" | 200-500 | Low | /ml-potentials-guide |
| "DFT vs molecular dynamics" | 100-300 | Very Low | Educational content |

### Tier 3: Long-Tail / Programmatic (Scale Later)

| Keyword Pattern | Volume per Query | Total Addressable | Page Type |
|----------------|------------------|-------------------|-----------|
| "[LAMMPS potential name] tutorial" | 10-50 each | 5K+ aggregate | pSEO template |
| "[file format] to [file format] converter" | 20-100 each | 2K+ aggregate | Free tool pages |
| "[material type] molecular dynamics" | 20-100 each | 3K+ aggregate | pSEO template |
| "how to simulate [material] in LAMMPS" | 10-50 each | 5K+ aggregate | pSEO template |

---

## Programmatic SEO Plan

### Opportunity: LAMMPS Potential Reference Pages

**The play:** There are hundreds of interatomic potentials used in LAMMPS. Each one has researchers searching for documentation, parameters, and usage examples. Build a templated page for each potential that's better than the LAMMPS docs.

**Template structure:**
```
/potentials/[potential-name]/

H1: [Potential Name] — Parameters, Usage & Visualization
Meta: Complete guide to [potential name] for molecular dynamics. Parameters, LAMMPS syntax, visualization with Lupine View.

Sections:
1. Overview (what this potential models)
2. Parameters (formatted table)
3. LAMMPS syntax example (code block)
4. Applicable materials (list with links)
5. Visualization (embed Lupine View demo)
6. Related potentials (internal links)
7. References (academic citations)

Schema: TechArticle + BreadcrumbList
CTA: "Visualize your [potential] simulation in Lupine View →"
```

**Scale:** 200+ pages targeting long-tail queries
**Effort:** Template once, populate from LAMMPS documentation data
**Defensibility:** Lupine View embed makes each page uniquely useful

### Opportunity: Material-Specific Simulation Guides

**Template structure:**
```
/materials/[material-name]/

H1: [Material Name] Simulation Guide — MD & DFT Approaches
Meta: How to simulate [material] using molecular dynamics and DFT. Potentials, parameters, and visualization.

Sections:
1. Material properties overview
2. Recommended simulation approach (DFT vs MD vs ML)
3. Recommended potentials (with links to /potentials/ pages)
4. Example workflow
5. Visualization gallery
6. Published results (literature references)

Schema: TechArticle + BreadcrumbList
CTA: "Simulate [material] in Lupine →"
```

**Scale:** 100+ pages (metals, ceramics, polymers, battery materials, semiconductors)
**Cross-linking:** Each material page links to relevant potential pages and vice versa

### Opportunity: File Format Converter Tools

**The play:** Researchers constantly convert between file formats (POSCAR, CIF, XYZ, LAMMPS data files). Build free browser-based converters.

```
/tools/convert/[format-a]-to-[format-b]/

H1: Convert [Format A] to [Format B] Online — Free
Meta: Free online converter for [format A] to [format B] files. No install required. Drag and drop.

Sections:
1. Converter tool (embedded, WASM-based)
2. About these formats
3. When to use each format
4. Related tools

Schema: SoftwareApplication + HowTo
CTA: "Need more than conversion? Try Lupine View →"
```

**Scale:** 20-30 format pairs
**SEO value:** High intent, tool pages earn backlinks naturally
**Strategic value:** Demonstrates Lupine's format support, captures researcher emails

---

## Content Gap Analysis

### Content Lupine Should Create (Priority Order)

| Content | Type | Keyword Target | Priority |
|---------|------|---------------|----------|
| "Lupine vs VASP" comparison | Comparison page | "VASP alternative" | P0 |
| "Lupine vs OVITO" comparison | Comparison page | "OVITO alternative" | P0 |
| LAMMPS visualization guide | Educational guide | "LAMMPS visualization" | P0 |
| ML potentials comparison (MACE vs NequIP vs...) | Guide | "machine learned potentials comparison" | P1 |
| "Best molecular dynamics software 2026" | Listicle | "molecular dynamics software" | P1 |
| "Open source materials science tools" | Roundup | "open source materials science" | P1 |
| Formal verification in simulation (Lean 4) | Technical deep-dive | "formal verification scientific computing" | P1 |
| Battery materials simulation guide | Case study / guide | "battery materials simulation" | P2 |
| WebGPU for scientific computing | Technical deep-dive | "WebGPU scientific visualization" | P2 |
| LAMMPS to Lupine migration guide | Migration | "LAMMPS migration" | P2 |

---

## Schema Markup Recommendations

### Homepage
```json
{
  "@type": "SoftwareApplication",
  "name": "Lupine",
  "applicationCategory": "Scientific Software",
  "operatingSystem": "Web Browser",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "description": "Open-source computational materials science platform..."
}
```

### Each Guide/Article Page
```json
{
  "@type": "TechArticle",
  "headline": "...",
  "author": { "@type": "Organization", "name": "Lupine" },
  "proficiencyLevel": "Expert"
}
```

### Comparison Pages
```json
{
  "@type": "WebPage",
  "speakable": { "@type": "SpeakableSpecification", "cssSelector": [".comparison-table"] }
}
```

---

## Action Plan (Priority Matrix)

### P0 — Do This Week (High Impact, Low Effort)

- [ ] Add meta descriptions to all existing pages
- [ ] Rewrite title tags with keyword targeting
- [ ] Add JSON-LD schema markup (SoftwareApplication for homepage)
- [ ] Create and submit sitemap.xml
- [ ] Set up Google Search Console
- [ ] Add Open Graph and Twitter Card meta tags

### P1 — Do This Month (High Impact, Medium Effort)

- [ ] Build "Lupine vs VASP" comparison page
- [ ] Build "Lupine vs OVITO" comparison page
- [ ] Build "LAMMPS Visualization" guide
- [ ] Add image alt text to all images
- [ ] Add internal cross-links between existing pages
- [ ] Set up basic analytics (page views, View tool usage, CTA clicks)

### P2 — Do This Quarter (High Impact, High Effort)

- [ ] Build programmatic SEO template for LAMMPS potentials (200+ pages)
- [ ] Build material-specific simulation guides (100+ pages)
- [ ] Build file format converter tools (20+ pages)
- [ ] Create "Best MD Software 2026" listicle
- [ ] Create "Open Source Materials Science" roundup
- [ ] Publish Lean 4 verification deep-dive (arXiv cross-post)

### P3 — Ongoing

- [ ] Monitor Search Console for emerging queries
- [ ] Build backlinks through academic citations and tool roundups
- [ ] A/B test title tags and meta descriptions
- [ ] Expand pSEO pages based on search data
