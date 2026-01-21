# Full-Service Campaign Workflow

The standard workflow for complete marketing campaigns requiring multiple skills and deliverables.

## Workflow Phases

### Phase 1: Discovery & Planning

**Mayor Actions**:
1. Receive and analyze brief
2. Identify required skills
3. Determine deliverable dependencies
4. Create convoy with beads
5. Establish timeline

**Skills Typically Needed**:
- `marketing-ideas` - Initial brainstorming
- `competitor-alternatives` - Competitive research
- `marketing-psychology` - Audience insights

**Outputs**:
- Analyzed brief with skill mapping
- Convoy created with all beads
- Dependency graph

### Phase 2: Strategy Development

**Mayor Actions**:
1. Spawn strategy-focused polecats
2. Assign strategy beads
3. Review strategic outputs
4. Approve before moving to execution

**Skills Typically Needed**:
- `pricing-strategy` - If pricing involved
- `launch-strategy` - If launching something
- `referral-program` - If growth mechanics needed

**Outputs**:
- Strategic framework
- Messaging hierarchy
- Campaign architecture

### Phase 3: Content Creation

**Mayor Actions**:
1. Spawn content polecats in parallel
2. Assign copywriting beads
3. Coordinate dependent work
4. Review for consistency

**Skills Typically Needed**:
- `copywriting` - Core copy creation
- `email-sequence` - Email campaigns
- `social-content` - Social media content

**Outputs**:
- Landing page copy
- Email sequences
- Social media content
- Ad copy

### Phase 4: Optimization

**Mayor Actions**:
1. Apply CRO skills to content
2. Review for conversion best practices
3. Suggest improvements

**Skills Typically Needed**:
- `page-cro` - Landing page optimization
- `form-cro` - Form optimization
- `copy-editing` - Polish and refine

**Outputs**:
- Optimized copy versions
- CRO recommendations
- A/B test suggestions

### Phase 5: Technical Setup

**Mayor Actions**:
1. Coordinate SEO implementation
2. Set up tracking requirements
3. Configure testing

**Skills Typically Needed**:
- `seo-audit` - SEO requirements
- `schema-markup` - Structured data
- `analytics-tracking` - Measurement setup
- `ab-test-setup` - Testing plan

**Outputs**:
- SEO specifications
- Tracking plan
- Test documentation

### Phase 6: Review & Delivery

**Mayor Actions**:
1. Compile all deliverables
2. Quality check against brief
3. Package for delivery
4. Archive convoy

**Outputs**:
- Complete deliverable package
- Implementation guide
- Measurement plan

## Parallel Execution

Many beads can run in parallel:

```
Phase 2: Strategy
    |
    v
Phase 3: Content (parallel tracks)
    |
    ├── Landing Page Copy ─────┐
    ├── Email Sequence ────────┤──> Phase 4: Optimization
    └── Social Content ────────┘
    |
    v
Phase 5: Technical
    |
    v
Phase 6: Delivery
```

## Example Convoy

```
convoy-launch-001
├── mkt-001: marketing-ideas (strategy)
├── mkt-002: competitor-alternatives (strategy)
├── mkt-003: copywriting (hero section) [depends: 001, 002]
├── mkt-004: copywriting (features section) [depends: 001]
├── mkt-005: copywriting (testimonials) [parallel]
├── mkt-006: page-cro (optimization) [depends: 003, 004, 005]
├── mkt-007: email-sequence (launch emails) [depends: 001]
├── mkt-008: social-content (launch posts) [depends: 001]
├── mkt-009: seo-audit (technical) [depends: 006]
├── mkt-010: analytics-tracking (setup) [depends: 006]
└── mkt-011: ab-test-setup (testing plan) [depends: 006]
```

## Quality Gates

### After Phase 2
- [ ] Strategy approved by stakeholder
- [ ] Messaging hierarchy confirmed
- [ ] Scope finalized

### After Phase 3
- [ ] Copy reviewed for brand voice
- [ ] All content complete
- [ ] Consistency check passed

### After Phase 4
- [ ] CRO best practices applied
- [ ] Copy polished
- [ ] Alternatives provided

### After Phase 5
- [ ] Technical specs complete
- [ ] Tracking verified
- [ ] Tests documented

### Final Delivery
- [ ] All deliverables complete
- [ ] Brief requirements met
- [ ] Documentation included
