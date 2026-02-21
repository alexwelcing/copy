#!/usr/bin/env python3
"""
HIGH ERA AGENCY - Competitive Intelligence Analyzer

Local Python implementation of the Cloudflare analyst.
Runs competitive research using free tools + Claude.

Usage:
    python analyze_competitor.py law.com
    python analyze_competitor.py law.com --competitors law360.com reuters.com/legal
    python analyze_competitor.py law.com --output report.md
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin, urlparse
import ssl

# Disable SSL verification for scraping (some sites have issues)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class PageData:
    url: str
    html: str
    text: str
    title: Optional[str] = None
    description: Optional[str] = None
    headings: list = field(default_factory=list)


@dataclass
class TechStack:
    frameworks: list = field(default_factory=list)
    analytics: list = field(default_factory=list)
    marketing: list = field(default_factory=list)
    hosting: list = field(default_factory=list)


@dataclass
class Intelligence:
    positioning: str = ""
    target_audience: list = field(default_factory=list)
    value_propositions: list = field(default_factory=list)
    key_features: list = field(default_factory=list)
    differentiators: list = field(default_factory=list)
    pricing_signals: list = field(default_factory=list)
    content_topics: list = field(default_factory=list)


@dataclass
class CompanyProfile:
    domain: str
    name: str
    tagline: Optional[str] = None
    positioning: Optional[str] = None
    tech_stack: TechStack = field(default_factory=TechStack)
    intelligence: Intelligence = field(default_factory=Intelligence)
    seo_estimate: dict = field(default_factory=dict)


@dataclass
class SWOT:
    strengths: list = field(default_factory=list)
    weaknesses: list = field(default_factory=list)
    opportunities: list = field(default_factory=list)
    threats: list = field(default_factory=list)


@dataclass
class CompetitiveReport:
    target: CompanyProfile
    competitors: list
    swot: SWOT
    insights: list
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================================
# SCRAPER
# ============================================================================

class Scraper:
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    ]

    def fetch(self, url: str) -> Optional[PageData]:
        """Fetch and parse a single page."""
        try:
            req = Request(url, headers={
                "User-Agent": self.USER_AGENTS[0],
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            })

            with urlopen(req, timeout=15, context=ssl_context) as response:
                html = response.read().decode("utf-8", errors="ignore")

            return PageData(
                url=url,
                html=html,
                text=self._extract_text(html),
                title=self._extract_title(html),
                description=self._extract_meta(html, "description"),
                headings=self._extract_headings(html),
            )
        except Exception as e:
            print(f"  [!] Failed to fetch {url}: {e}")
            return None

    def fetch_multiple(self, domain: str) -> list:
        """Fetch multiple pages from a domain."""
        paths = ["/", "/pricing", "/about", "/blog", "/features", "/product", "/solutions"]
        pages = []

        for path in paths:
            url = f"https://{domain}{path}"
            print(f"  Fetching {url}...")
            page = self.fetch(url)
            if page:
                pages.append(page)

        # Also try www subdomain if no pages found
        if not pages:
            for path in paths[:3]:
                url = f"https://www.{domain}{path}"
                print(f"  Fetching {url}...")
                page = self.fetch(url)
                if page:
                    pages.append(page)

        return pages

    def _extract_text(self, html: str) -> str:
        """Extract readable text from HTML."""
        # Remove scripts and styles
        text = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
        text = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', text, flags=re.IGNORECASE)
        text = re.sub(r'<nav[^>]*>[\s\S]*?</nav>', '', text, flags=re.IGNORECASE)
        text = re.sub(r'<footer[^>]*>[\s\S]*?</footer>', '', text, flags=re.IGNORECASE)
        # Remove tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _extract_title(self, html: str) -> Optional[str]:
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_meta(self, html: str, name: str) -> Optional[str]:
        patterns = [
            rf'<meta[^>]*name=["\']?{name}["\']?[^>]*content=["\']([^"\']+)["\']',
            rf'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']?{name}["\']?',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_headings(self, html: str) -> list:
        headings = []
        for match in re.finditer(r'<h[1-3][^>]*>([^<]+)</h[1-3]>', html, re.IGNORECASE):
            text = match.group(1).strip()
            if len(text) > 3:
                headings.append(text)
        return headings


# ============================================================================
# TECH DETECTOR
# ============================================================================

class TechDetector:
    def detect(self, pages: list) -> TechStack:
        """Detect technologies from HTML content."""
        combined_html = "\n".join(p.html for p in pages)

        frameworks = []
        analytics = []
        marketing = []
        hosting = []

        # Frameworks
        if "__NEXT_DATA__" in combined_html or "/_next/" in combined_html:
            frameworks.append("Next.js")
        if "__NUXT__" in combined_html:
            frameworks.append("Nuxt.js")
        if "ng-version" in combined_html:
            frameworks.append("Angular")
        if "data-reactroot" in combined_html or "__REACT" in combined_html:
            frameworks.append("React")
        if "wp-content" in combined_html:
            frameworks.append("WordPress")
        if "Webflow" in combined_html:
            frameworks.append("Webflow")
        if "Shopify" in combined_html:
            frameworks.append("Shopify")
        if "squarespace" in combined_html.lower():
            frameworks.append("Squarespace")

        # Analytics
        if "gtag" in combined_html or "google-analytics" in combined_html:
            analytics.append("Google Analytics")
        if "segment.com" in combined_html or "analytics.js" in combined_html:
            analytics.append("Segment")
        if "mixpanel" in combined_html:
            analytics.append("Mixpanel")
        if "amplitude" in combined_html:
            analytics.append("Amplitude")
        if "hotjar" in combined_html:
            analytics.append("Hotjar")
        if "fullstory" in combined_html:
            analytics.append("FullStory")
        if "posthog" in combined_html:
            analytics.append("PostHog")

        # Marketing
        if "hubspot" in combined_html.lower():
            marketing.append("HubSpot")
        if "intercom" in combined_html.lower():
            marketing.append("Intercom")
        if "drift" in combined_html.lower():
            marketing.append("Drift")
        if "mailchimp" in combined_html.lower():
            marketing.append("Mailchimp")
        if "fbq" in combined_html or "facebook.com/tr" in combined_html:
            marketing.append("Meta Pixel")
        if "googleads" in combined_html or "ads/ga-audiences" in combined_html:
            marketing.append("Google Ads")
        if "linkedin.com/px" in combined_html:
            marketing.append("LinkedIn Pixel")
        if "marketo" in combined_html.lower():
            marketing.append("Marketo")
        if "pardot" in combined_html.lower():
            marketing.append("Pardot")

        # Hosting
        if "vercel" in combined_html.lower():
            hosting.append("Vercel")
        if "netlify" in combined_html.lower():
            hosting.append("Netlify")
        if "cloudflare" in combined_html.lower():
            hosting.append("Cloudflare")
        if "amazonaws" in combined_html:
            hosting.append("AWS")
        if "akamai" in combined_html.lower():
            hosting.append("Akamai")

        return TechStack(
            frameworks=list(set(frameworks)),
            analytics=list(set(analytics)),
            marketing=list(set(marketing)),
            hosting=list(set(hosting)),
        )


# ============================================================================
# CLAUDE INTELLIGENCE EXTRACTOR
# ============================================================================

class IntelligenceExtractor:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _call_claude(self, system: str, user: str, max_tokens: int = 1024) -> str:
        """Call Claude API."""
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }).encode("utf-8")

        req = Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )

        with urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["content"][0]["text"]

    def extract_intelligence(self, pages: list) -> Intelligence:
        """Extract competitive intelligence from pages using Claude."""
        combined = "\n\n".join(
            f"--- {p.url} ---\n{p.text[:3000]}" for p in pages
        )

        system = """You are a competitive intelligence analyst. Extract structured insights from website content.

Return JSON only:
{
  "positioning": "One sentence describing how they position themselves",
  "target_audience": ["audience segment 1", "audience segment 2"],
  "value_propositions": ["value prop 1", "value prop 2"],
  "key_features": ["feature 1", "feature 2"],
  "differentiators": ["what makes them unique"],
  "pricing_signals": ["any pricing info, free trial mentions, etc"],
  "content_topics": ["main topics they write about"]
}"""

        try:
            result = self._call_claude(system, f"Analyze:\n\n{combined}")
            data = json.loads(result)
            return Intelligence(**data)
        except Exception as e:
            print(f"  [!] Intelligence extraction failed: {e}")
            return Intelligence()

    def find_competitors(self, pages: list, industry: str = "") -> list:
        """Find competitors using Claude."""
        combined = "\n".join(f"{p.title}: {p.text[:1500]}" for p in pages[:3])

        system = """You are a market research analyst. Based on a company's website content, identify their likely competitors.

Return a JSON array of competitor domain names only. Example: ["competitor1.com", "competitor2.com"]
Focus on direct competitors in the same market segment. Return 5-8 competitors."""

        try:
            result = self._call_claude(
                system,
                f"Find competitors for this company{f' in {industry}' if industry else ''}:\n\n{combined}"
            )
            return json.loads(result)
        except:
            return []

    def generate_swot(self, target: Intelligence, competitors: list) -> SWOT:
        """Generate SWOT analysis."""
        system = """You are a strategic analyst. Generate a SWOT analysis comparing a target company against its competitors.

Return JSON only:
{
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "opportunities": ["opportunity 1", "opportunity 2"],
  "threats": ["threat 1", "threat 2"]
}

Be specific and actionable. 4-6 items per category."""

        try:
            result = self._call_claude(
                system,
                f"Generate SWOT analysis.\n\nTarget: {json.dumps(asdict(target))}\n\nCompetitors: {json.dumps([asdict(c) for c in competitors])}"
            )
            data = json.loads(result)
            return SWOT(**data)
        except Exception as e:
            print(f"  [!] SWOT generation failed: {e}")
            return SWOT()

    def generate_insights(self, target: CompanyProfile, competitors: list) -> list:
        """Generate strategic insights."""
        system = """You are a competitive analyst. Generate 5-7 actionable insights based on competitive data.
Return a JSON array of strings only. Each insight should be specific and actionable."""

        try:
            result = self._call_claude(
                system,
                f"Generate insights for {target.name} vs {', '.join(c.name for c in competitors)}.\n\nTarget: {json.dumps(asdict(target), default=str)}\n\nCompetitors: {json.dumps([asdict(c) for c in competitors], default=str)}"
            )
            return json.loads(result)
        except:
            return []


# ============================================================================
# COMPETITIVE ANALYZER
# ============================================================================

class CompetitiveAnalyzer:
    def __init__(self, api_key: str):
        self.scraper = Scraper()
        self.tech_detector = TechDetector()
        self.extractor = IntelligenceExtractor(api_key)

    def analyze_company(self, domain: str) -> CompanyProfile:
        """Analyze a single company."""
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

        print(f"\n[*] Analyzing {domain}...")

        # Scrape pages
        pages = self.scraper.fetch_multiple(domain)
        if not pages:
            print(f"  [!] Could not scrape {domain}")
            return CompanyProfile(domain=domain, name=domain)

        # Detect tech
        print("  Detecting technology stack...")
        tech_stack = self.tech_detector.detect(pages)

        # Extract intelligence with Claude
        print("  Extracting intelligence with Claude...")
        intelligence = self.extractor.extract_intelligence(pages)

        # Build profile
        homepage = pages[0] if pages else None
        name = domain
        if homepage and homepage.title:
            name = homepage.title.split("|")[0].split("-")[0].strip()

        # Estimate SEO
        seo_estimate = {
            "estimated_authority": "high" if len(pages) > 3 else "medium",
            "content_depth": "deep" if any(len(p.text) > 5000 for p in pages) else "moderate",
            "headings_found": sum(len(p.headings) for p in pages),
        }

        return CompanyProfile(
            domain=domain,
            name=name,
            tagline=homepage.description if homepage else None,
            positioning=intelligence.positioning,
            tech_stack=tech_stack,
            intelligence=intelligence,
            seo_estimate=seo_estimate,
        )

    def run_analysis(
        self,
        target_domain: str,
        competitor_domains: list = None,
        industry: str = "",
    ) -> CompetitiveReport:
        """Run full competitive analysis."""

        # Analyze target
        target = self.analyze_company(target_domain)

        # Find or use provided competitors
        if not competitor_domains:
            print("\n[*] Finding competitors with Claude...")
            pages = self.scraper.fetch_multiple(target_domain)
            competitor_domains = self.extractor.find_competitors(pages, industry)
            print(f"  Found: {', '.join(competitor_domains)}")

        # Analyze competitors
        competitors = []
        for domain in competitor_domains[:5]:
            try:
                profile = self.analyze_company(domain)
                competitors.append(profile)
            except Exception as e:
                print(f"  [!] Failed to analyze {domain}: {e}")

        # Generate SWOT
        print("\n[*] Generating SWOT analysis...")
        competitor_intels = [c.intelligence for c in competitors if c.intelligence]
        swot = self.extractor.generate_swot(target.intelligence, competitor_intels)

        # Generate insights
        print("[*] Generating strategic insights...")
        insights = self.extractor.generate_insights(target, competitors)

        return CompetitiveReport(
            target=target,
            competitors=competitors,
            swot=swot,
            insights=insights,
        )


# ============================================================================
# REPORT GENERATOR
# ============================================================================

def generate_markdown_report(report: CompetitiveReport) -> str:
    """Generate markdown report from analysis."""

    md = f"""# Competitive Intelligence Report
## {report.target.name}

**Domain:** {report.target.domain}
**Generated:** {report.generated_at}

---

## Executive Summary

{report.target.positioning or "No positioning detected."}

---

## Target Company Profile

### {report.target.name}

**Tagline:** {report.target.tagline or "N/A"}

**Positioning:** {report.target.positioning or "N/A"}

### Technology Stack

| Category | Technologies |
|----------|--------------|
| Frameworks | {", ".join(report.target.tech_stack.frameworks) or "Not detected"} |
| Analytics | {", ".join(report.target.tech_stack.analytics) or "Not detected"} |
| Marketing | {", ".join(report.target.tech_stack.marketing) or "Not detected"} |
| Hosting | {", ".join(report.target.tech_stack.hosting) or "Not detected"} |

### Value Propositions

{chr(10).join(f"- {vp}" for vp in report.target.intelligence.value_propositions) or "- None detected"}

### Key Features

{chr(10).join(f"- {f}" for f in report.target.intelligence.key_features) or "- None detected"}

### Target Audience

{chr(10).join(f"- {a}" for a in report.target.intelligence.target_audience) or "- Not identified"}

### Differentiators

{chr(10).join(f"- {d}" for d in report.target.intelligence.differentiators) or "- None detected"}

---

## Competitors ({len(report.competitors)} analyzed)

"""

    for comp in report.competitors:
        md += f"""### {comp.name}

**Domain:** {comp.domain}

**Positioning:** {comp.positioning or "N/A"}

**Tech Stack:** {", ".join(comp.tech_stack.frameworks + comp.tech_stack.analytics[:2]) or "Not detected"}

**Value Props:** {"; ".join(comp.intelligence.value_propositions[:3]) or "N/A"}

---

"""

    md += f"""## SWOT Analysis

### Strengths
{chr(10).join(f"- {s}" for s in report.swot.strengths) or "- None identified"}

### Weaknesses
{chr(10).join(f"- {w}" for w in report.swot.weaknesses) or "- None identified"}

### Opportunities
{chr(10).join(f"- {o}" for o in report.swot.opportunities) or "- None identified"}

### Threats
{chr(10).join(f"- {t}" for t in report.swot.threats) or "- None identified"}

---

## Strategic Insights

{chr(10).join(f"{i+1}. {insight}" for i, insight in enumerate(report.insights)) or "No insights generated."}

---

## Recommendations

Based on the competitive analysis:

"""

    # Generate recommendations from insights
    for i, insight in enumerate(report.insights[:5], 1):
        md += f"{i}. **Action:** {insight}\n\n"

    md += """---

*Report generated by High Era Agency Competitive Analyst*
"""

    return md


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Competitive Intelligence Analyzer")
    parser.add_argument("domain", help="Target domain to analyze")
    parser.add_argument("--competitors", nargs="*", help="Competitor domains (auto-detected if not provided)")
    parser.add_argument("--industry", default="", help="Industry context for better competitor detection")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of markdown")

    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable required")
        print("Run: export ANTHROPIC_API_KEY='your-key'")
        sys.exit(1)

    # Run analysis
    print("=" * 60)
    print("HIGH ERA AGENCY - Competitive Intelligence")
    print("=" * 60)

    analyzer = CompetitiveAnalyzer(api_key)
    report = analyzer.run_analysis(
        args.domain,
        args.competitors,
        args.industry,
    )

    # Generate output
    if args.json:
        output = json.dumps(asdict(report), indent=2, default=str)
    else:
        output = generate_markdown_report(report)

    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"\n[*] Report saved to {args.output}")
    else:
        print("\n" + "=" * 60)
        print(output)


if __name__ == "__main__":
    main()
