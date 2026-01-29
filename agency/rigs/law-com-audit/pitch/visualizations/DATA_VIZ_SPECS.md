# Data Visualization Specifications

## Executive Pitch Deck Charts

---

## Chart 1: Market Preference Gap

**Type:** Horizontal Bar Chart
**Slide:** 3

**Data:**
```
Law360:     52%  ████████████████████████████
Bloomberg:  15%  ████████
ALM/Law.com: 17% █████████
Other:      16%  ████████
```

**Design:**
- Law360 bar: Bold gold (#C9A227)
- Others: Muted gray (#4A5568)
- No gridlines
- Values displayed at end of bars
- Dark background (#0A1628)

**Key Callout:** "3x preference gap"

---

## Chart 2: Conversion Funnel

**Type:** Funnel Visualization
**Slide:** 4

**Data:**
```
Stage               Count     Rate
─────────────────────────────────
Visitors           1,200,000   100%
Paywall Encounters   400,000    33%
Registrations         12,000     3%
Trial Starts           8,000    67%
Paid Subscribers       1,600    20%
```

**Design:**
- Gradient from wide (gold) to narrow (muted)
- Leak indicators at each stage
- Percentage dropoff displayed
- Dark background

**Key Callout:** "0.13% overall conversion"

---

## Chart 3: Keyword Rankings Gap

**Type:** Comparison Table with Visual Bars
**Slide:** 12

**Data:**
```
Keyword              Law.com   Law360   Gap
─────────────────────────────────────────────
"biglaw news"           15        1     -14
"legal industry trends" 22        3     -19
"partner compensation"  12        2     -10
"law firm mergers"       6        1      -5
```

**Design:**
- Two columns with mini bar visualization
- Red indicators for large gaps
- Green for close races
- Dark background

**Key Callout:** "Winning where we have authority"

---

## Chart 4: Revenue Impact Waterfall

**Type:** Waterfall Chart
**Slide:** 13

**Data:**
```
Initiative           Revenue Impact
───────────────────────────────────
Paywall Messaging      +$240,000
Registration Flow      +$360,000
Pricing Page           +$300,000
Trial Onboarding       +$180,000
Enterprise Flow        +$600,000
───────────────────────────────────
TOTAL                +$1,680,000
```

**Design:**
- Stacked ascending bars
- Each segment in gradient gold
- Running total line
- Final bar emphasized
- Dark background

**Key Callout:** "+$1.68M annual revenue opportunity"

---

## Chart 5: 90-Day Roadmap

**Type:** Timeline/Gantt
**Slide:** 15

**Data:**
```
Week  1  2  3  4  5  6  7  8  9 10 11 12
─────────────────────────────────────────
Quick Wins    ████
Registration       ████████
Pricing                  ████████
SEO                          ████████████
Campaign                              ████
Measurement  M1──────M2──────────M3──────
```

**Design:**
- Horizontal timeline
- Gold bars for activities
- Milestone markers (M1, M2, M3)
- Clean, minimal
- Dark background

---

## Chart 6: ROI Calculation

**Type:** Simple Equation Visual
**Slide:** 17

**Data:**
```
Investment:     $145,000
÷
Revenue Lift: $1,680,000
=
ROI:              11.6x
```

**Design:**
- Large typography
- Investment in muted color
- Revenue in gold
- ROI in large bold gold
- Simple and impactful

**Key Callout:** "Payback in 5-6 weeks"

---

## Chart 7: Risk Timeline

**Type:** Declining Line with Markers
**Slide:** 18

**Data:**
```
Month   Position    Event
─────────────────────────────────
0       Inflection  Now
6       Declining   Market share erosion
12      Critical    Position unrecoverable
24      Terminal    Irrelevance
```

**Design:**
- Descending curve
- Warning markers at 6, 12, 24 months
- Color gradient from gold to red
- Urgency-inducing visual
- Dark background

---

## Chart 8: Investment Breakdown

**Type:** Donut Chart
**Slide:** 16

**Data:**
```
Component          Amount    Pct
────────────────────────────────
Strategy           $25,000    17%
CRO Implementation $45,000    31%
SEO Technical      $35,000    24%
Campaign Creative  $40,000    28%
────────────────────────────────
Total             $145,000   100%
```

**Design:**
- Donut with gold segments
- Total in center
- Legend to the right
- Clean, minimal
- Dark background

---

## Animation Specifications

For presentation software (Keynote/PowerPoint):

### Funnel Chart
1. Full funnel appears
2. Leak particles animate out at each stage
3. Final conversion number pulses

### Waterfall Chart
1. Bars build up sequentially
2. Running total line draws
3. Final total emphasizes

### ROI Calculation
1. Investment appears
2. Pause
3. Revenue lift appears
4. Pause
5. ROI result reveals with emphasis

### Risk Timeline
1. Line draws from left to right
2. Warning markers pulse as timeline reaches them
3. Final state holds with subtle pulse on "24 months"

---

## Export Specifications

**Format:** PNG with transparency
**Resolution:** 2x (retina)
**Color Profile:** sRGB
**Background:** Dark navy (#0A1628) or transparent

**Naming Convention:**
- `chart-[number]-[name]-[version].png`
- Example: `chart-02-funnel-v1.png`

---

## Tools Recommended

**For Production:**
- Figma (design)
- D3.js (interactive)
- Observable (notebooks)
- Flourish (no-code)

**For Quick Mockups:**
- Excalidraw
- Whimsical
- Miro

**For Animation:**
- After Effects
- Keynote Magic Move
- PowerPoint Morph
