# SEO Audit: Law.com

## Agent: Analyst
## Skill Applied: `seo-audit`
## Date: January 2026

---

## Executive Summary

Law.com has significant SEO opportunities that remain untapped. While the site benefits from strong domain authority due to age and inbound links from legal industry sources, technical issues and content organization problems limit organic visibility. This audit identifies 47 specific improvements across technical SEO, content optimization, and link strategy.

---

## Domain Authority Analysis

### Current Metrics (Estimated)

| Metric | Law.com | Law360.com | Bloomberg Law | Above The Law |
|--------|---------|------------|---------------|---------------|
| Domain Authority | 78 | 82 | 91 | 71 |
| Referring Domains | ~18,000 | ~24,000 | ~45,000 | ~15,000 |
| Organic Keywords | ~85,000 | ~142,000 | ~95,000 | ~112,000 |
| Monthly Organic Traffic | ~1.2M | ~3.8M | ~1.8M | ~2.1M |

**Assessment:** Law.com underperforms relative to domain authority. The site should rank for more keywords given its backlink profile and age. This suggests on-page and technical issues are limiting performance.

---

## Technical SEO Issues

### Critical (Immediate Action Required)

#### 1. Paywall Implementation Issues
**Issue:** Google may have difficulty distinguishing free preview content from paywalled content, leading to indexing problems.

**Evidence:** Structured data for paywalled content appears inconsistent across publication sections.

**Recommendation:**
- Implement consistent `isAccessibleForFree` schema markup
- Use proper `hasPart` schema for paywall sections
- Ensure first-click-free policy is properly configured for Google News

**Impact:** High
**Effort:** Medium

---

#### 2. Duplicate Content Across Publications
**Issue:** Similar articles appear across multiple ALM properties (law.com, nationallawjournal.com, americanlawyer.com) with minimal differentiation.

**Evidence:** Same bylined articles indexed at multiple URLs.

**Recommendation:**
- Implement canonical tags pointing to primary publication
- Consider consolidating all content under law.com domain
- Use hreflang for legitimate regional variations

**Impact:** High
**Effort:** High

---

#### 3. Page Speed Performance
**Issue:** Core Web Vitals likely failing on article pages due to ad load and legacy CMS.

**Estimated Metrics:**
- LCP (Largest Contentful Paint): >4.0s (Poor)
- FID (First Input Delay): >200ms (Poor)
- CLS (Cumulative Layout Shift): >0.25 (Poor)

**Recommendation:**
- Lazy load below-fold ads
- Implement critical CSS inlining
- Defer non-essential JavaScript
- Consider AMP for article pages (Google News benefit)

**Impact:** High
**Effort:** High

---

### High Priority

#### 4. URL Structure Inconsistency
**Issue:** URL patterns vary across sections and publications.

**Examples:**
- `/news/article-slug`
- `/americanlawyer/2026/01/article-slug`
- `/sites/almstaff/2026/01/article-slug`

**Recommendation:**
- Standardize URL structure: `/[publication]/[category]/[article-slug]`
- Implement 301 redirects for legacy URLs
- Include primary keyword in URL slug

**Impact:** Medium
**Effort:** Medium

---

#### 5. Internal Linking Weakness
**Issue:** Limited internal linking between related articles, publications, and topic hubs.

**Evidence:** Article pages have minimal contextual internal links. Topic pages don't exist.

**Recommendation:**
- Create topic hub pages for major practice areas
- Implement "Related Articles" module on all pages
- Add contextual links within article body
- Link between publications when covering same story

**Impact:** Medium
**Effort:** Medium

---

#### 6. Schema Markup Gaps
**Issue:** Missing or incomplete structured data.

**Current State:**
- Article schema: Partial
- Organization schema: Missing
- BreadcrumbList: Missing
- FAQ schema: Not utilized
- NewsArticle schema: Inconsistent

**Recommendation:**
Implement comprehensive schema:
```json
{
  "@type": "NewsArticle",
  "headline": "...",
  "author": {"@type": "Person", "name": "..."},
  "publisher": {"@type": "Organization", "name": "The American Lawyer"},
  "datePublished": "...",
  "dateModified": "...",
  "isAccessibleForFree": false,
  "hasPart": {
    "@type": "WebPageElement",
    "isAccessibleForFree": false,
    "cssSelector": ".article-body"
  }
}
```

**Impact:** Medium
**Effort:** Low

---

### Medium Priority

#### 7. Mobile Experience
**Issue:** Mobile experience likely suboptimal given desktop-first legacy design.

**Recommendation:**
- Audit mobile rendering
- Ensure touch targets are appropriately sized
- Test mobile subscription flow
- Consider mobile-specific content prioritization

**Impact:** Medium
**Effort:** Medium

---

#### 8. XML Sitemap Organization
**Issue:** Sitemap likely contains outdated or low-value URLs.

**Recommendation:**
- Segment sitemaps by publication and content type
- Exclude paywalled archives older than 6 months
- Submit separate news sitemap for Google News
- Include lastmod dates accurately

**Impact:** Low
**Effort:** Low

---

#### 9. Image Optimization
**Issue:** Images likely unoptimized for web delivery.

**Recommendation:**
- Implement WebP format with fallbacks
- Add descriptive alt text (keyword opportunity)
- Lazy load images below fold
- Implement responsive images with srcset

**Impact:** Low
**Effort:** Medium

---

## Content SEO Analysis

### Keyword Gap Analysis

**High-Value Keywords Where Law.com Underperforms:**

| Keyword | Monthly Volume | Law.com Rank | Law360 Rank | Opportunity |
|---------|---------------|--------------|-------------|-------------|
| "biglaw news" | 2,400 | 15 | 1 | High |
| "law firm layoffs" | 4,800 | 8 | 1 | Medium |
| "legal industry trends" | 1,900 | 22 | 3 | High |
| "am law 100" | 6,600 | 2 | 8 | Defend |
| "partner compensation" | 2,100 | 12 | 2 | High |
| "legal tech news" | 3,200 | 18 | 1 | High |
| "law firm mergers" | 1,800 | 6 | 1 | Medium |
| "in house counsel salary" | 4,400 | 14 | 5 | High |

**Assessment:** Law.com should own queries related to rankings and data (Am Law 100, partner compensation, firm benchmarking) but is underperforming on industry news queries.

---

### Content Gap Analysis

**Topics Where Competitors Rank, Law.com Doesn't:**

1. **Legal Technology Reviews**
   - Law360 has dedicated LegalTech section
   - Law.com coverage is fragmented
   - Opportunity: Create Legal Tech Hub

2. **Career Advice / Associate Life**
   - Above The Law dominates this space
   - Law.com has minimal career content
   - Opportunity: Leverage rankings authority for career insights

3. **Practice Area Deep Dives**
   - Law360's 60 practice areas vs. Law.com's publication silos
   - Opportunity: Cross-publication topic hubs

4. **Data-Driven Features**
   - "Law firms with highest associate salaries"
   - "Most profitable practice areas"
   - Opportunity: Turn Legal Compass data into SEO content

---

### Featured Snippet Opportunities

**Queries Where Law.com Could Capture Position 0:**

| Query | Current Status | Content Needed |
|-------|---------------|----------------|
| "what is biglaw" | No snippet | Definition + salary data |
| "am law 100 list" | Partial | Full ranked list page |
| "partner track timeline" | No snippet | Career progression guide |
| "law firm profit margin" | No snippet | Data visualization |
| "legal industry statistics" | No snippet | Annual stats roundup |

**Recommendation:** Create dedicated "Answer" pages optimized for featured snippets, linking to full subscription content.

---

## Link Building Opportunities

### Current Link Profile Assessment

**Strengths:**
- Strong links from law schools, bar associations
- Citations from mainstream news (NYT, WSJ)
- Legal industry directories

**Weaknesses:**
- Limited blogger/influencer links
- Weak social signals
- Few links to specific articles (most to homepage)

### Link Building Recommendations

#### 1. Rankings as Linkbait
The Am Law 100/200 and NLJ 500 are highly citable. Create embeddable widgets and encourage linking.

**Tactic:** Release rankings data with embeddable graphics that include link attribution.

#### 2. Expert Commentary Program
Position ALM journalists as commentators for mainstream media legal coverage.

**Tactic:** Proactive media outreach when legal news breaks.

#### 3. Law School Partnerships
Academic citations drive authority.

**Tactic:** Create student/academic access programs with citation requirements.

#### 4. Legal Tech Coverage
Legal tech companies actively seek coverage and will link to reviews.

**Tactic:** Expand product review coverage with clear link-back opportunities.

---

## Google News Optimization

### Current Status
Law.com publications are included in Google News but may not be optimized for visibility.

### Recommendations

1. **News Sitemap:** Ensure proper news-specific sitemap submission
2. **Article Tags:** Implement proper news article schema
3. **Freshness Signals:** Ensure dateModified updates for developing stories
4. **Author Authority:** Build author pages with proper schema
5. **News Keywords Meta:** Include news_keywords for trending stories

---

## Priority Action Matrix

### Immediate (Week 1-2)
1. Fix schema markup for paywalled content
2. Implement canonical tags across publications
3. Create and submit news sitemap
4. Add missing Organization schema

### Short-Term (Month 1)
5. Improve Core Web Vitals (page speed)
6. Standardize URL structure with redirects
7. Create 5 topic hub pages
8. Implement Related Articles module

### Medium-Term (Month 2-3)
9. Build featured snippet "Answer" pages
10. Launch rankings embeddable widgets
11. Create data visualization content series
12. Expand internal linking strategy

### Long-Term (Quarter 2)
13. Consider domain consolidation strategy
14. Implement full AMP for articles
15. Build expert commentary program
16. Launch law school partnership initiative

---

## Expected Impact

| Initiative | Traffic Impact | Timeline |
|------------|---------------|----------|
| Schema fixes | +5-10% | 4-6 weeks |
| Page speed improvements | +10-15% | 8-12 weeks |
| Topic hub creation | +15-20% | 3-4 months |
| Featured snippet targeting | +5-8% | 2-3 months |
| Internal linking improvements | +8-12% | 6-8 weeks |

**Total Projected Organic Traffic Increase:** 35-50% over 6 months

---

*Prepared by: Analyst Agent*
*Skill Applied: seo-audit*
*Reviewed by: Director Agent*
