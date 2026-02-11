/**
 * HIGH ERA AGENCY - Free Research Tools
 *
 * No paid APIs required. Uses web scraping + Claude analysis
 * to extract competitive intelligence.
 */

// ============================================================================
// TYPES
// ============================================================================

export interface Env {
  ANTHROPIC_API_KEY: string;
}

export interface ScrapedPage {
  url: string;
  html: string;
  text: string;
  metadata: PageMetadata;
  links: string[];
  headings: string[];
}

export interface PageMetadata {
  title?: string;
  description?: string;
  ogImage?: string;
  canonical?: string;
  robots?: string;
  author?: string;
  publishedDate?: string;
}

export interface ExtractedIntelligence {
  positioning: string;
  targetAudience: string[];
  valuePropositions: string[];
  keyFeatures: string[];
  differentiators: string[];
  callsToAction: string[];
  socialProof: string[];
  pricingSignals: string[];
  contentTopics: string[];
  estimatedTrafficTier: "low" | "medium" | "high" | "very-high";
  techSignals: string[];
}

// ============================================================================
// ENHANCED WEB SCRAPER
// ============================================================================

export class EnhancedScraper {
  private userAgents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (compatible; HighEraBot/1.0; +https://highera.dev)",
  ];

  async scrapePage(url: string): Promise<ScrapedPage> {
    const response = await fetch(url, {
      headers: {
        "User-Agent": this.userAgents[Math.floor(Math.random() * this.userAgents.length)],
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
      },
      redirect: "follow",
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}: ${response.status}`);
    }

    const html = await response.text();

    return {
      url,
      html,
      text: this.extractText(html),
      metadata: this.extractMetadata(html),
      links: this.extractLinks(html, url),
      headings: this.extractHeadings(html),
    };
  }

  async scrapeMultiplePages(
    domain: string,
    paths: string[] = ["/", "/pricing", "/about", "/blog", "/features", "/product"]
  ): Promise<ScrapedPage[]> {
    const pages: ScrapedPage[] = [];

    for (const path of paths) {
      try {
        const page = await this.scrapePage(`https://${domain}${path}`);
        pages.push(page);
      } catch {
        // Page doesn't exist or blocked, continue
      }
    }

    return pages;
  }

  private extractText(html: string): string {
    return html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
      .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, "")
      .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, "")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  private extractMetadata(html: string): PageMetadata {
    return {
      title: this.extractTag(html, /<title[^>]*>([^<]+)<\/title>/i),
      description: this.extractMeta(html, "description"),
      ogImage: this.extractMeta(html, "og:image", "property"),
      canonical: this.extractLink(html, "canonical"),
      robots: this.extractMeta(html, "robots"),
      author: this.extractMeta(html, "author"),
      publishedDate: this.extractMeta(html, "article:published_time", "property"),
    };
  }

  private extractTag(html: string, regex: RegExp): string | undefined {
    const match = html.match(regex);
    return match?.[1]?.trim();
  }

  private extractMeta(html: string, name: string, attr: string = "name"): string | undefined {
    const regex = new RegExp(
      `<meta[^>]*${attr}=["']${name}["'][^>]*content=["']([^"']+)["']`,
      "i"
    );
    const match = html.match(regex);
    if (match) return match[1]?.trim();

    // Try reverse order
    const regex2 = new RegExp(
      `<meta[^>]*content=["']([^"']+)["'][^>]*${attr}=["']${name}["']`,
      "i"
    );
    const match2 = html.match(regex2);
    return match2?.[1]?.trim();
  }

  private extractLink(html: string, rel: string): string | undefined {
    const regex = new RegExp(`<link[^>]*rel=["']${rel}["'][^>]*href=["']([^"']+)["']`, "i");
    const match = html.match(regex);
    return match?.[1]?.trim();
  }

  private extractLinks(html: string, baseUrl: string): string[] {
    const links: string[] = [];
    const regex = /<a[^>]*href=["']([^"'#]+)["']/gi;
    let match;

    while ((match = regex.exec(html)) !== null) {
      let href = match[1];
      if (href.startsWith("/")) {
        href = new URL(href, baseUrl).href;
      }
      if (href.startsWith("http")) {
        links.push(href);
      }
    }

    return [...new Set(links)];
  }

  private extractHeadings(html: string): string[] {
    const headings: string[] = [];
    const regex = /<h[1-3][^>]*>([^<]+)<\/h[1-3]>/gi;
    let match;

    while ((match = regex.exec(html)) !== null) {
      const text = match[1].trim();
      if (text.length > 3) {
        headings.push(text);
      }
    }

    return headings;
  }
}

// ============================================================================
// CLAUDE-POWERED INTELLIGENCE EXTRACTION
// ============================================================================

export class IntelligenceExtractor {
  constructor(private env: Env) {}

  /**
   * Extract competitive intelligence from scraped pages using Claude
   */
  async extractIntelligence(pages: ScrapedPage[]): Promise<ExtractedIntelligence> {
    // Combine page content
    const combinedContent = pages
      .map((p) => `--- ${p.url} ---\n${p.text.slice(0, 3000)}`)
      .join("\n\n");

    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 2048,
        system: `You are a competitive intelligence analyst. Extract structured insights from website content.

Return JSON only:
{
  "positioning": "One sentence describing how they position themselves",
  "targetAudience": ["audience segment 1", "audience segment 2"],
  "valuePropositions": ["value prop 1", "value prop 2"],
  "keyFeatures": ["feature 1", "feature 2"],
  "differentiators": ["what makes them unique"],
  "callsToAction": ["main CTAs on site"],
  "socialProof": ["customer logos, testimonials, stats mentioned"],
  "pricingSignals": ["any pricing info, free trial mentions, etc"],
  "contentTopics": ["main topics they write about"],
  "estimatedTrafficTier": "low|medium|high|very-high based on content depth and site sophistication",
  "techSignals": ["technologies detected from content"]
}`,
        messages: [
          {
            role: "user",
            content: `Analyze this website content and extract competitive intelligence:\n\n${combinedContent}`,
          },
        ],
      }),
    });

    if (!response.ok) {
      throw new Error(`Claude API error: ${response.status}`);
    }

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = data.content.find((c) => c.type === "text")?.text || "{}";
      return JSON.parse(text);
    } catch {
      return {
        positioning: "Unknown",
        targetAudience: [],
        valuePropositions: [],
        keyFeatures: [],
        differentiators: [],
        callsToAction: [],
        socialProof: [],
        pricingSignals: [],
        contentTopics: [],
        estimatedTrafficTier: "medium",
        techSignals: [],
      };
    }
  }

  /**
   * Extract detailed pricing from pricing page
   */
  async extractPricing(
    pricingPage: ScrapedPage
  ): Promise<{
    model: string;
    tiers: Array<{ name: string; price: string; features: string[] }>;
    freeTrial: boolean;
    freeTrialDays?: number;
  }> {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        system: `Extract pricing information from this pricing page.

Return JSON only:
{
  "model": "freemium|subscription|usage-based|enterprise|hybrid",
  "tiers": [
    {"name": "Tier Name", "price": "$X/mo or Custom", "features": ["feature1", "feature2"]}
  ],
  "freeTrial": true/false,
  "freeTrialDays": number or null
}`,
        messages: [
          {
            role: "user",
            content: `Extract pricing from:\n\n${pricingPage.text.slice(0, 6000)}`,
          },
        ],
      }),
    });

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = data.content.find((c) => c.type === "text")?.text || "{}";
      return JSON.parse(text);
    } catch {
      return { model: "unknown", tiers: [], freeTrial: false };
    }
  }

  /**
   * Analyze content strategy from blog
   */
  async analyzeContentStrategy(
    blogPage: ScrapedPage
  ): Promise<{
    publishingFrequency: string;
    topicClusters: string[];
    contentFormats: string[];
    estimatedBlogPosts: number;
    contentQuality: "low" | "medium" | "high";
  }> {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        system: `Analyze this blog/content page and assess their content strategy.

Return JSON only:
{
  "publishingFrequency": "daily|weekly|monthly|irregular",
  "topicClusters": ["topic1", "topic2"],
  "contentFormats": ["blog posts", "case studies", "guides", etc],
  "estimatedBlogPosts": number estimate,
  "contentQuality": "low|medium|high based on depth and professionalism"
}`,
        messages: [
          {
            role: "user",
            content: `Analyze content strategy from:\n\nHeadings: ${blogPage.headings.join(", ")}\n\nContent: ${blogPage.text.slice(0, 5000)}`,
          },
        ],
      }),
    });

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = data.content.find((c) => c.type === "text")?.text || "{}";
      return JSON.parse(text);
    } catch {
      return {
        publishingFrequency: "unknown",
        topicClusters: [],
        contentFormats: [],
        estimatedBlogPosts: 0,
        contentQuality: "medium",
      };
    }
  }

  /**
   * Find competitors using Claude
   */
  async findCompetitors(
    pages: ScrapedPage[],
    industry?: string
  ): Promise<string[]> {
    const combinedContent = pages
      .map((p) => `${p.metadata.title}: ${p.text.slice(0, 2000)}`)
      .join("\n\n");

    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        system: `You are a market research analyst. Based on a company's website content, identify their likely competitors.

Return a JSON array of competitor domain names only. Example: ["competitor1.com", "competitor2.com"]

Focus on:
1. Direct competitors (same product category)
2. Similar target market
3. Well-known players in the space

Return 5-10 competitors, most relevant first.`,
        messages: [
          {
            role: "user",
            content: `Find competitors for this company${industry ? ` in the ${industry} industry` : ""}:\n\n${combinedContent}`,
          },
        ],
      }),
    });

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = data.content.find((c) => c.type === "text")?.text || "[]";
      const parsed = JSON.parse(text);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }

  /**
   * Generate SWOT analysis
   */
  async generateSWOT(
    targetIntel: ExtractedIntelligence,
    competitorIntel: ExtractedIntelligence[]
  ): Promise<{
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  }> {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        system: `You are a strategic analyst. Generate a SWOT analysis comparing a target company against its competitors.

Return JSON only:
{
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "opportunities": ["opportunity 1", "opportunity 2"],
  "threats": ["threat 1", "threat 2"]
}

Be specific and actionable.`,
        messages: [
          {
            role: "user",
            content: `Generate SWOT analysis.

Target company:
${JSON.stringify(targetIntel, null, 2)}

Competitors:
${JSON.stringify(competitorIntel, null, 2)}`,
          },
        ],
      }),
    });

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = data.content.find((c) => c.type === "text")?.text || "{}";
      return JSON.parse(text);
    } catch {
      return { strengths: [], weaknesses: [], opportunities: [], threats: [] };
    }
  }

  /**
   * Estimate SEO metrics from content signals
   */
  async estimateSEOMetrics(
    pages: ScrapedPage[]
  ): Promise<{
    estimatedDomainAuthority: "low" | "medium" | "high" | "very-high";
    contentDepth: "shallow" | "moderate" | "deep";
    technicalSEOSignals: string[];
    keywordTargeting: string[];
    estimatedOrganicKeywords: string;
  }> {
    // Count content signals
    const totalHeadings = pages.reduce((sum, p) => sum + p.headings.length, 0);
    const totalLinks = pages.reduce((sum, p) => sum + p.links.length, 0);
    const hasCanonical = pages.some((p) => p.metadata.canonical);
    const hasOgImage = pages.some((p) => p.metadata.ogImage);
    const avgTextLength = pages.reduce((sum, p) => sum + p.text.length, 0) / pages.length;

    // Technical SEO signals
    const technicalSEOSignals: string[] = [];
    if (hasCanonical) technicalSEOSignals.push("Canonical tags");
    if (hasOgImage) technicalSEOSignals.push("Open Graph tags");
    if (pages.some((p) => p.metadata.robots)) technicalSEOSignals.push("Robots meta");
    if (pages.some((p) => p.html.includes("schema.org"))) technicalSEOSignals.push("Schema markup");
    if (pages.some((p) => p.html.includes("hreflang"))) technicalSEOSignals.push("Hreflang tags");

    // Estimate DA based on signals
    let daEstimate: "low" | "medium" | "high" | "very-high" = "low";
    const signals = technicalSEOSignals.length + (avgTextLength > 3000 ? 2 : 0) + (totalHeadings > 20 ? 1 : 0);
    if (signals >= 5) daEstimate = "very-high";
    else if (signals >= 3) daEstimate = "high";
    else if (signals >= 2) daEstimate = "medium";

    // Content depth
    let contentDepth: "shallow" | "moderate" | "deep" = "shallow";
    if (avgTextLength > 5000) contentDepth = "deep";
    else if (avgTextLength > 2000) contentDepth = "moderate";

    // Extract keyword targeting from headings and titles
    const keywordTargeting = pages
      .flatMap((p) => [...p.headings, p.metadata.title || ""])
      .filter((h) => h.length > 5)
      .slice(0, 10);

    // Rough keyword estimate
    let estimatedOrganicKeywords = "<1,000";
    if (daEstimate === "very-high") estimatedOrganicKeywords = "10,000+";
    else if (daEstimate === "high") estimatedOrganicKeywords = "5,000-10,000";
    else if (daEstimate === "medium") estimatedOrganicKeywords = "1,000-5,000";

    return {
      estimatedDomainAuthority: daEstimate,
      contentDepth,
      technicalSEOSignals,
      keywordTargeting,
      estimatedOrganicKeywords,
    };
  }
}

// ============================================================================
// GOOGLE SEARCH (NO API KEY NEEDED)
// ============================================================================

export class SearchEngine {
  /**
   * Find competitors using DuckDuckGo (no API key needed)
   */
  async searchCompetitors(query: string): Promise<string[]> {
    // DuckDuckGo HTML search (no API key required)
    const searchUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query + " competitors alternatives")}`;

    try {
      const response = await fetch(searchUrl, {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible)",
        },
      });

      const html = await response.text();

      // Extract domains from search results
      const domains: string[] = [];
      const regex = /href="https?:\/\/([^/"]+)/g;
      let match;

      while ((match = regex.exec(html)) !== null) {
        const domain = match[1].replace("www.", "");
        if (
          !domain.includes("duckduckgo") &&
          !domain.includes("google") &&
          !domain.includes("bing") &&
          !domains.includes(domain)
        ) {
          domains.push(domain);
        }
      }

      return domains.slice(0, 10);
    } catch {
      return [];
    }
  }

  /**
   * Search for industry news and trends
   */
  async searchNews(query: string): Promise<Array<{ title: string; url: string }>> {
    const searchUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query + " news")}`;

    try {
      const response = await fetch(searchUrl, {
        headers: { "User-Agent": "Mozilla/5.0 (compatible)" },
      });

      const html = await response.text();
      const results: Array<{ title: string; url: string }> = [];

      // Extract result links
      const regex = /<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</g;
      let match;

      while ((match = regex.exec(html)) !== null) {
        results.push({
          url: match[1],
          title: match[2].trim(),
        });
      }

      return results.slice(0, 10);
    } catch {
      return [];
    }
  }
}

// ============================================================================
// FREE TECH DETECTION
// ============================================================================

export class TechDetectorFree {
  /**
   * Detect tech stack from HTML source (no API needed)
   */
  detectFromHTML(html: string): {
    frameworks: string[];
    analytics: string[];
    marketing: string[];
    hosting: string[];
    other: string[];
  } {
    const frameworks: string[] = [];
    const analytics: string[] = [];
    const marketing: string[] = [];
    const hosting: string[] = [];
    const other: string[] = [];

    // Frameworks
    if (html.includes("__NEXT_DATA__") || html.includes("/_next/")) frameworks.push("Next.js");
    if (html.includes("__NUXT__") || html.includes("/_nuxt/")) frameworks.push("Nuxt.js");
    if (html.includes("ng-version") || html.includes("ng-app")) frameworks.push("Angular");
    if (html.includes("data-reactroot") || html.includes("__REACT")) frameworks.push("React");
    if (html.includes("data-v-") || html.includes("Vue.js")) frameworks.push("Vue.js");
    if (html.includes("Webflow")) frameworks.push("Webflow");
    if (html.includes("wp-content") || html.includes("WordPress")) frameworks.push("WordPress");
    if (html.includes("Shopify")) frameworks.push("Shopify");
    if (html.includes("squarespace")) frameworks.push("Squarespace");
    if (html.includes("wix.com")) frameworks.push("Wix");
    if (html.includes("framer")) frameworks.push("Framer");
    if (html.includes("gatsby")) frameworks.push("Gatsby");
    if (html.includes("astro")) frameworks.push("Astro");

    // Analytics
    if (html.includes("gtag") || html.includes("google-analytics") || html.includes("GA4")) {
      analytics.push("Google Analytics");
    }
    if (html.includes("segment.com") || html.includes("analytics.js")) analytics.push("Segment");
    if (html.includes("mixpanel")) analytics.push("Mixpanel");
    if (html.includes("amplitude")) analytics.push("Amplitude");
    if (html.includes("hotjar")) analytics.push("Hotjar");
    if (html.includes("fullstory")) analytics.push("FullStory");
    if (html.includes("heap")) analytics.push("Heap");
    if (html.includes("posthog")) analytics.push("PostHog");
    if (html.includes("plausible")) analytics.push("Plausible");
    if (html.includes("fathom")) analytics.push("Fathom");

    // Marketing
    if (html.includes("hubspot")) marketing.push("HubSpot");
    if (html.includes("intercom")) marketing.push("Intercom");
    if (html.includes("drift")) marketing.push("Drift");
    if (html.includes("crisp")) marketing.push("Crisp");
    if (html.includes("zendesk")) marketing.push("Zendesk");
    if (html.includes("mailchimp")) marketing.push("Mailchimp");
    if (html.includes("klaviyo")) marketing.push("Klaviyo");
    if (html.includes("convertkit")) marketing.push("ConvertKit");
    if (html.includes("fbq") || html.includes("facebook.com/tr")) marketing.push("Meta Pixel");
    if (html.includes("ads/ga-audiences") || html.includes("googleads")) marketing.push("Google Ads");
    if (html.includes("linkedin.com/px")) marketing.push("LinkedIn Pixel");
    if (html.includes("twitter.com/i/adsct")) marketing.push("Twitter Pixel");

    // Hosting signals
    if (html.includes("vercel")) hosting.push("Vercel");
    if (html.includes("netlify")) hosting.push("Netlify");
    if (html.includes("cloudflare")) hosting.push("Cloudflare");
    if (html.includes("fastly")) hosting.push("Fastly");
    if (html.includes("amazonaws")) hosting.push("AWS");
    if (html.includes("azure")) hosting.push("Azure");
    if (html.includes("heroku")) hosting.push("Heroku");

    // Other tools
    if (html.includes("stripe")) other.push("Stripe");
    if (html.includes("paypal")) other.push("PayPal");
    if (html.includes("recaptcha")) other.push("reCAPTCHA");
    if (html.includes("sentry")) other.push("Sentry");
    if (html.includes("datadog")) other.push("Datadog");
    if (html.includes("launchdarkly")) other.push("LaunchDarkly");

    return {
      frameworks: [...new Set(frameworks)],
      analytics: [...new Set(analytics)],
      marketing: [...new Set(marketing)],
      hosting: [...new Set(hosting)],
      other: [...new Set(other)],
    };
  }

  /**
   * Detect from HTTP headers
   */
  detectFromHeaders(headers: Headers): string[] {
    const detected: string[] = [];

    const server = headers.get("server");
    if (server) {
      if (server.includes("cloudflare")) detected.push("Cloudflare");
      if (server.includes("nginx")) detected.push("Nginx");
      if (server.includes("apache")) detected.push("Apache");
      if (server.includes("vercel")) detected.push("Vercel");
    }

    const poweredBy = headers.get("x-powered-by");
    if (poweredBy) {
      detected.push(poweredBy);
    }

    if (headers.get("x-vercel-id")) detected.push("Vercel");
    if (headers.get("cf-ray")) detected.push("Cloudflare");
    if (headers.get("x-netlify-request-id")) detected.push("Netlify");

    return [...new Set(detected)];
  }
}
