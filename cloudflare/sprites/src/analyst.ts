/**
 * HIGH ERA AGENCY - Competitive Research Analyst
 *
 * Tools and workflows for competitive intelligence gathering.
 * Integrates with external APIs for comprehensive market analysis.
 */

import { DurableObject } from "cloudflare:workers";
import {
  generateResearchReport,
  generateQuickScan,
  generateComparisonMatrix,
} from "./templates";
import {
  EnhancedScraper,
  IntelligenceExtractor,
  SearchEngine,
  TechDetectorFree,
} from "./free-tools";

// ============================================================================
// TYPES
// ============================================================================

export interface CompetitorProfile {
  domain: string;
  name: string;
  description?: string;
  discoveredAt: number;
}

export interface ResearchRequest {
  id: string;
  type: ResearchType;
  target: string; // Domain or company name
  competitors?: string[]; // Optional list of known competitors
  depth: "quick" | "standard" | "deep";
  focus?: ResearchFocus[];
}

export type ResearchType =
  | "competitor_landscape"
  | "seo_gap_analysis"
  | "content_audit"
  | "pricing_analysis"
  | "tech_stack"
  | "social_presence"
  | "full_intelligence";

export type ResearchFocus =
  | "seo"
  | "content"
  | "pricing"
  | "features"
  | "positioning"
  | "social"
  | "technology"
  | "traffic";

export interface ResearchResult {
  id: string;
  type: ResearchType;
  target: string;
  completedAt: number;
  data: CompetitiveIntelligence;
  insights: string[];
  recommendations: string[];
}

export interface CompetitiveIntelligence {
  target: CompanyProfile;
  competitors: CompanyProfile[];
  landscape: MarketLandscape;
  gaps: OpportunityGap[];
  threats: CompetitiveThreat[];
}

export interface CompanyProfile {
  domain: string;
  name: string;
  tagline?: string;
  positioning?: string;
  seo?: SEOProfile;
  content?: ContentProfile;
  pricing?: PricingProfile;
  social?: SocialProfile;
  technology?: TechProfile;
  traffic?: TrafficProfile;
}

export interface SEOProfile {
  domainAuthority?: number;
  organicKeywords?: number;
  organicTraffic?: number;
  topKeywords?: KeywordRanking[];
  backlinks?: number;
  referringDomains?: number;
}

export interface KeywordRanking {
  keyword: string;
  position: number;
  volume: number;
  difficulty?: number;
  url?: string;
}

export interface ContentProfile {
  blogPosts?: number;
  publishingFrequency?: string;
  topContent?: ContentPiece[];
  contentTypes?: string[];
  avgWordCount?: number;
}

export interface ContentPiece {
  title: string;
  url: string;
  estimatedTraffic?: number;
  topKeyword?: string;
}

export interface PricingProfile {
  model: "freemium" | "subscription" | "usage" | "enterprise" | "hybrid";
  tiers?: PricingTier[];
  lowestPrice?: number;
  highestPrice?: number;
  freeTrialDays?: number;
}

export interface PricingTier {
  name: string;
  price: number;
  billing: "monthly" | "annual" | "one-time";
  features?: string[];
}

export interface SocialProfile {
  twitter?: { handle: string; followers: number };
  linkedin?: { url: string; followers: number };
  youtube?: { channel: string; subscribers: number };
  totalFollowers?: number;
  engagementRate?: number;
}

export interface TechProfile {
  stack?: string[];
  analytics?: string[];
  marketing?: string[];
  infrastructure?: string[];
}

export interface TrafficProfile {
  monthlyVisits?: number;
  bounceRate?: number;
  pagesPerVisit?: number;
  avgVisitDuration?: number;
  trafficSources?: {
    direct: number;
    search: number;
    social: number;
    referral: number;
    paid: number;
  };
}

export interface MarketLandscape {
  totalCompetitors: number;
  marketLeader?: string;
  segments: MarketSegment[];
  positioningMap?: PositioningMap;
}

export interface MarketSegment {
  name: string;
  competitors: string[];
  characteristics: string[];
}

export interface PositioningMap {
  xAxis: { label: string; low: string; high: string };
  yAxis: { label: string; low: string; high: string };
  positions: { company: string; x: number; y: number }[];
}

export interface OpportunityGap {
  type: "keyword" | "content" | "feature" | "positioning" | "channel";
  description: string;
  competitors: string[];
  potentialImpact: "low" | "medium" | "high";
  effort: "low" | "medium" | "high";
}

export interface CompetitiveThreat {
  competitor: string;
  threat: string;
  severity: "low" | "medium" | "high";
  timeframe: "immediate" | "short-term" | "long-term";
}

// ============================================================================
// RESEARCH TOOLS
// ============================================================================

export interface Env {
  ANTHROPIC_API_KEY: string;
  // Optional external API keys
  AHREFS_API_KEY?: string;
  SEMRUSH_API_KEY?: string;
  SIMILARWEB_API_KEY?: string;
  BUILTWITH_API_KEY?: string;
}

/**
 * Web Fetcher - Fetches and extracts content from URLs
 */
export class WebFetcher {
  async fetch(url: string): Promise<{ html: string; text: string }> {
    const response = await fetch(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (compatible; HighEraBot/1.0; +https://highera.dev)",
        Accept: "text/html,application/xhtml+xml",
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}: ${response.status}`);
    }

    const html = await response.text();
    const text = this.extractText(html);

    return { html, text };
  }

  private extractText(html: string): string {
    // Remove scripts, styles, and HTML tags
    return html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  async fetchMetadata(
    url: string
  ): Promise<{ title?: string; description?: string; ogImage?: string }> {
    const { html } = await this.fetch(url);

    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const descMatch = html.match(
      /<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i
    );
    const ogImageMatch = html.match(
      /<meta[^>]*property=["']og:image["'][^>]*content=["']([^"']+)["']/i
    );

    return {
      title: titleMatch?.[1]?.trim(),
      description: descMatch?.[1]?.trim(),
      ogImage: ogImageMatch?.[1]?.trim(),
    };
  }
}

/**
 * SEO Research Tool
 */
export class SEOResearcher {
  constructor(
    private env: Env,
    private fetcher: WebFetcher
  ) {}

  async analyzeKeywords(domain: string): Promise<Partial<SEOProfile>> {
    // If we have Ahrefs API key, use it
    if (this.env.AHREFS_API_KEY) {
      return this.fetchAhrefsData(domain);
    }

    // Otherwise, do basic analysis from page content
    return this.basicSEOAnalysis(domain);
  }

  private async fetchAhrefsData(domain: string): Promise<Partial<SEOProfile>> {
    const response = await fetch(
      `https://api.ahrefs.com/v3/site-explorer/overview?target=${domain}&mode=domain`,
      {
        headers: {
          Authorization: `Bearer ${this.env.AHREFS_API_KEY}`,
        },
      }
    );

    if (!response.ok) {
      console.error(`Ahrefs API error: ${response.status}`);
      return this.basicSEOAnalysis(domain);
    }

    const data = (await response.json()) as {
      domain_rating?: number;
      organic_keywords?: number;
      organic_traffic?: number;
      backlinks?: number;
      referring_domains?: number;
    };

    return {
      domainAuthority: data.domain_rating,
      organicKeywords: data.organic_keywords,
      organicTraffic: data.organic_traffic,
      backlinks: data.backlinks,
      referringDomains: data.referring_domains,
    };
  }

  private async basicSEOAnalysis(domain: string): Promise<Partial<SEOProfile>> {
    // Basic analysis without API - check homepage
    try {
      const { html } = await this.fetcher.fetch(`https://${domain}`);

      // Count meta tags, headings, etc.
      const h1Count = (html.match(/<h1/gi) || []).length;
      const h2Count = (html.match(/<h2/gi) || []).length;
      const hasMetaDesc = /<meta[^>]*name=["']description["']/i.test(html);
      const hasOgTags = /<meta[^>]*property=["']og:/i.test(html);

      return {
        // Can't get real metrics without API, but can note structure
        topKeywords: [], // Would need API
      };
    } catch {
      return {};
    }
  }
}

/**
 * Pricing Research Tool
 */
export class PricingResearcher {
  constructor(
    private env: Env,
    private fetcher: WebFetcher
  ) {}

  async analyzePricing(domain: string): Promise<Partial<PricingProfile>> {
    // Try common pricing page URLs
    const pricingUrls = [
      `https://${domain}/pricing`,
      `https://${domain}/plans`,
      `https://${domain}/price`,
      `https://www.${domain}/pricing`,
    ];

    for (const url of pricingUrls) {
      try {
        const { text } = await this.fetcher.fetch(url);

        // Extract pricing information using Claude
        return this.extractPricingWithAI(text, url);
      } catch {
        continue;
      }
    }

    return {};
  }

  private async extractPricingWithAI(
    pageText: string,
    url: string
  ): Promise<Partial<PricingProfile>> {
    // Use Claude to extract structured pricing data
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
        system: `You are a pricing analyst. Extract structured pricing information from webpage text.
Return JSON only, no explanation. Format:
{
  "model": "freemium|subscription|usage|enterprise|hybrid",
  "tiers": [{"name": "...", "price": 0, "billing": "monthly|annual", "features": ["..."]}],
  "lowestPrice": 0,
  "highestPrice": 0,
  "freeTrialDays": 0
}
If information is not available, omit the field.`,
        messages: [
          {
            role: "user",
            content: `Extract pricing from this page (${url}):\n\n${pageText.slice(0, 8000)}`,
          },
        ],
      }),
    });

    if (!response.ok) {
      return {};
    }

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = data.content.find((c) => c.type === "text")?.text || "{}";
      return JSON.parse(text);
    } catch {
      return {};
    }
  }
}

/**
 * Technology Stack Detector
 */
export class TechDetector {
  constructor(
    private env: Env,
    private fetcher: WebFetcher
  ) {}

  async detectStack(domain: string): Promise<Partial<TechProfile>> {
    // If we have BuiltWith API key
    if (this.env.BUILTWITH_API_KEY) {
      return this.fetchBuiltWithData(domain);
    }

    // Otherwise, basic detection from headers and HTML
    return this.basicTechDetection(domain);
  }

  private async fetchBuiltWithData(
    domain: string
  ): Promise<Partial<TechProfile>> {
    const response = await fetch(
      `https://api.builtwith.com/v21/api.json?KEY=${this.env.BUILTWITH_API_KEY}&LOOKUP=${domain}`,
      {}
    );

    if (!response.ok) {
      return this.basicTechDetection(domain);
    }

    const data = (await response.json()) as {
      Results?: Array<{
        Result?: {
          Paths?: Array<{
            Technologies?: Array<{ Name: string; Categories?: string[] }>;
          }>;
        };
      }>;
    };

    const techs =
      data.Results?.[0]?.Result?.Paths?.[0]?.Technologies?.map(
        (t) => t.Name
      ) || [];

    return {
      stack: techs,
    };
  }

  private async basicTechDetection(
    domain: string
  ): Promise<Partial<TechProfile>> {
    try {
      const response = await fetch(`https://${domain}`, {
        headers: { "User-Agent": "Mozilla/5.0" },
      });

      const html = await response.text();
      const headers = Object.fromEntries(response.headers.entries());

      const stack: string[] = [];
      const analytics: string[] = [];
      const marketing: string[] = [];

      // Detect from HTML
      if (html.includes("react") || html.includes("__NEXT_DATA__"))
        stack.push("React");
      if (html.includes("__NUXT__")) stack.push("Vue/Nuxt");
      if (html.includes("ng-version")) stack.push("Angular");
      if (html.includes("Webflow")) stack.push("Webflow");
      if (html.includes("wp-content")) stack.push("WordPress");
      if (html.includes("Shopify")) stack.push("Shopify");

      // Analytics
      if (html.includes("gtag") || html.includes("google-analytics"))
        analytics.push("Google Analytics");
      if (html.includes("segment")) analytics.push("Segment");
      if (html.includes("mixpanel")) analytics.push("Mixpanel");
      if (html.includes("amplitude")) analytics.push("Amplitude");
      if (html.includes("hotjar")) analytics.push("Hotjar");

      // Marketing
      if (html.includes("hubspot")) marketing.push("HubSpot");
      if (html.includes("intercom")) marketing.push("Intercom");
      if (html.includes("drift")) marketing.push("Drift");
      if (html.includes("mailchimp")) marketing.push("Mailchimp");

      // From headers
      if (headers["x-powered-by"]) stack.push(headers["x-powered-by"]);
      if (headers["server"]) stack.push(headers["server"]);

      return {
        stack: [...new Set(stack)],
        analytics: [...new Set(analytics)],
        marketing: [...new Set(marketing)],
      };
    } catch {
      return {};
    }
  }
}

/**
 * Content Analyzer
 */
export class ContentAnalyzer {
  constructor(
    private env: Env,
    private fetcher: WebFetcher
  ) {}

  async analyzeContent(domain: string): Promise<Partial<ContentProfile>> {
    // Try to find blog/resources
    const contentUrls = [
      `https://${domain}/blog`,
      `https://${domain}/resources`,
      `https://${domain}/articles`,
      `https://blog.${domain}`,
    ];

    for (const url of contentUrls) {
      try {
        const { html, text } = await this.fetcher.fetch(url);

        // Count articles on page
        const articleLinks = html.match(/<a[^>]*href=["'][^"']*\/blog\/[^"']+["']/gi) || [];
        const h2Tags = html.match(/<h2[^>]*>([^<]+)<\/h2>/gi) || [];

        return {
          blogPosts: Math.max(articleLinks.length, h2Tags.length),
          contentTypes: this.detectContentTypes(html),
        };
      } catch {
        continue;
      }
    }

    return {};
  }

  private detectContentTypes(html: string): string[] {
    const types: string[] = [];

    if (/blog|article|post/i.test(html)) types.push("Blog Posts");
    if (/case.?study/i.test(html)) types.push("Case Studies");
    if (/whitepaper|ebook|guide/i.test(html)) types.push("Whitepapers");
    if (/webinar|video/i.test(html)) types.push("Videos");
    if (/podcast/i.test(html)) types.push("Podcasts");
    if (/template|toolkit/i.test(html)) types.push("Templates");

    return types;
  }
}

// ============================================================================
// RESEARCH ANALYST DURABLE OBJECT
// ============================================================================

/**
 * Competitive Research Analyst
 *
 * Orchestrates research tools and AI analysis for competitive intelligence.
 */
export class CompetitiveAnalyst extends DurableObject<Env> {
  // Original tools (use paid APIs if available)
  private fetcher: WebFetcher;
  private seoResearcher: SEOResearcher;
  private pricingResearcher: PricingResearcher;
  private techDetector: TechDetector;
  private contentAnalyzer: ContentAnalyzer;

  // Free tools (no API keys required)
  private scraper: EnhancedScraper;
  private extractor: IntelligenceExtractor;
  private searchEngine: SearchEngine;
  private freeTechDetector: TechDetectorFree;

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    // Original tools
    this.fetcher = new WebFetcher();
    this.seoResearcher = new SEOResearcher(env, this.fetcher);
    this.pricingResearcher = new PricingResearcher(env, this.fetcher);
    this.techDetector = new TechDetector(env, this.fetcher);
    this.contentAnalyzer = new ContentAnalyzer(env, this.fetcher);

    // Free tools
    this.scraper = new EnhancedScraper();
    this.extractor = new IntelligenceExtractor(env);
    this.searchEngine = new SearchEngine();
    this.freeTechDetector = new TechDetectorFree();
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const format = url.searchParams.get("format") || "json";

    // Full competitive research
    if (url.pathname === "/research" && request.method === "POST") {
      const req = (await request.json()) as ResearchRequest;
      const result = await this.runResearch(req);

      if (format === "markdown") {
        const report = generateResearchReport(result);
        return new Response(report, {
          headers: { "Content-Type": "text/markdown" },
        });
      }

      return Response.json(result);
    }

    // Quick competitor scan
    if (url.pathname === "/scan" && request.method === "POST") {
      const { domain } = (await request.json()) as { domain: string };
      const profile = await this.scanCompetitor(domain);

      if (format === "markdown") {
        const report = generateQuickScan(profile);
        return new Response(report, {
          headers: { "Content-Type": "text/markdown" },
        });
      }

      return Response.json(profile);
    }

    // Find competitors
    if (url.pathname === "/find-competitors" && request.method === "POST") {
      const { domain, industry } = (await request.json()) as {
        domain: string;
        industry?: string;
      };
      const competitors = await this.findCompetitors(domain, industry);
      return Response.json({ competitors });
    }

    // SEO gap analysis
    if (url.pathname === "/seo-gap" && request.method === "POST") {
      const { target, competitors } = (await request.json()) as {
        target: string;
        competitors: string[];
      };
      const gaps = await this.analyzeSEOGaps(target, competitors);
      return Response.json({ gaps });
    }

    // Comparison matrix
    if (url.pathname === "/compare" && request.method === "POST") {
      const { target, competitors } = (await request.json()) as {
        target: string;
        competitors: string[];
      };

      const [targetProfile, ...competitorProfiles] = await Promise.all([
        this.scanCompetitor(target),
        ...competitors.map((c) => this.scanCompetitor(c)),
      ]);

      if (format === "markdown") {
        const report = generateComparisonMatrix(targetProfile, competitorProfiles);
        return new Response(report, {
          headers: { "Content-Type": "text/markdown" },
        });
      }

      return Response.json({ target: targetProfile, competitors: competitorProfiles });
    }

    // Deep scan using free tools (no API keys needed)
    if (url.pathname === "/deep-scan" && request.method === "POST") {
      const { domain } = (await request.json()) as { domain: string };
      const result = await this.deepScan(domain);
      return Response.json(result);
    }

    // Full intelligence using free tools
    if (url.pathname === "/intelligence" && request.method === "POST") {
      const { domain, industry } = (await request.json()) as {
        domain: string;
        industry?: string;
      };
      const result = await this.gatherIntelligence(domain, industry);

      if (format === "markdown") {
        return new Response(this.formatIntelligenceReport(result), {
          headers: { "Content-Type": "text/markdown" },
        });
      }

      return Response.json(result);
    }

    // SWOT analysis
    if (url.pathname === "/swot" && request.method === "POST") {
      const { target, competitors } = (await request.json()) as {
        target: string;
        competitors: string[];
      };
      const swot = await this.generateSWOTAnalysis(target, competitors);
      return Response.json(swot);
    }

    return new Response("Not found", { status: 404 });
  }

  /**
   * Deep scan using free tools - no API keys required
   */
  async deepScan(domain: string): Promise<{
    profile: CompanyProfile;
    intelligence: {
      positioning: string;
      targetAudience: string[];
      valuePropositions: string[];
      keyFeatures: string[];
      differentiators: string[];
      pricingSignals: string[];
      techStack: {
        frameworks: string[];
        analytics: string[];
        marketing: string[];
        hosting: string[];
      };
      seoEstimate: {
        estimatedAuthority: string;
        contentDepth: string;
        keywordTargeting: string[];
      };
    };
  }> {
    // Clean domain
    domain = domain.replace(/^https?:\/\//, "").replace(/^www\./, "").split("/")[0];

    // Scrape multiple pages
    const pages = await this.scraper.scrapeMultiplePages(domain);

    if (pages.length === 0) {
      throw new Error(`Could not scrape ${domain}`);
    }

    // Extract intelligence using Claude
    const intelligence = await this.extractor.extractIntelligence(pages);

    // Detect tech from HTML
    const techFromHTML = this.freeTechDetector.detectFromHTML(
      pages.map((p) => p.html).join("\n")
    );

    // Estimate SEO metrics
    const seoEstimate = await this.extractor.estimateSEOMetrics(pages);

    // Extract pricing if pricing page exists
    const pricingPage = pages.find(
      (p) => p.url.includes("/pricing") || p.url.includes("/plans")
    );
    let pricing;
    if (pricingPage) {
      pricing = await this.extractor.extractPricing(pricingPage);
    }

    // Build profile
    const homepage = pages.find((p) => p.url.endsWith(domain) || p.url.endsWith(domain + "/"));
    const profile: CompanyProfile = {
      domain,
      name: homepage?.metadata.title?.split("|")[0]?.split("-")[0]?.trim() || domain,
      tagline: homepage?.metadata.description,
      positioning: intelligence.positioning,
      technology: {
        stack: techFromHTML.frameworks,
        analytics: techFromHTML.analytics,
        marketing: techFromHTML.marketing,
      },
      pricing: pricing ? {
        model: pricing.model as "freemium" | "subscription" | "usage" | "enterprise" | "hybrid",
        tiers: pricing.tiers?.map(t => ({
          name: t.name,
          price: parseInt(t.price.replace(/\D/g, "")) || 0,
          billing: "monthly" as const,
          features: t.features,
        })),
        freeTrialDays: pricing.freeTrialDays,
      } : undefined,
    };

    return {
      profile,
      intelligence: {
        positioning: intelligence.positioning,
        targetAudience: intelligence.targetAudience,
        valuePropositions: intelligence.valuePropositions,
        keyFeatures: intelligence.keyFeatures,
        differentiators: intelligence.differentiators,
        pricingSignals: intelligence.pricingSignals,
        techStack: techFromHTML,
        seoEstimate: {
          estimatedAuthority: seoEstimate.estimatedDomainAuthority,
          contentDepth: seoEstimate.contentDepth,
          keywordTargeting: seoEstimate.keywordTargeting,
        },
      },
    };
  }

  /**
   * Full competitive intelligence using free tools
   */
  async gatherIntelligence(
    domain: string,
    industry?: string
  ): Promise<{
    target: CompanyProfile;
    competitors: CompanyProfile[];
    swot: {
      strengths: string[];
      weaknesses: string[];
      opportunities: string[];
      threats: string[];
    };
    insights: string[];
  }> {
    // Deep scan target
    const targetScan = await this.deepScan(domain);

    // Find competitors using search
    const searchCompetitors = await this.searchEngine.searchCompetitors(
      `${domain} competitors alternatives ${industry || ""}`
    );

    // Also use Claude to find competitors
    const pages = await this.scraper.scrapeMultiplePages(domain);
    const aiCompetitors = await this.extractor.findCompetitors(pages, industry);

    // Combine and dedupe
    const allCompetitors = [...new Set([...searchCompetitors, ...aiCompetitors])]
      .filter((c) => c !== domain && !c.includes(domain))
      .slice(0, 5);

    // Scan top competitors
    const competitorScans = await Promise.all(
      allCompetitors.map(async (comp) => {
        try {
          const scan = await this.deepScan(comp);
          return scan.profile;
        } catch {
          return null;
        }
      })
    );

    const validCompetitors = competitorScans.filter((c): c is CompanyProfile => c !== null);

    // Generate SWOT using Claude
    const targetIntel = await this.extractor.extractIntelligence(pages);
    const competitorIntels = await Promise.all(
      validCompetitors.slice(0, 3).map(async (comp) => {
        const compPages = await this.scraper.scrapeMultiplePages(comp.domain);
        return this.extractor.extractIntelligence(compPages);
      })
    );

    const swot = await this.extractor.generateSWOT(targetIntel, competitorIntels);

    // Generate insights
    const insights = await this.generateAIInsights(targetScan.profile, validCompetitors);

    return {
      target: targetScan.profile,
      competitors: validCompetitors,
      swot,
      insights,
    };
  }

  /**
   * Generate SWOT analysis
   */
  async generateSWOTAnalysis(
    target: string,
    competitors: string[]
  ): Promise<{
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  }> {
    const targetPages = await this.scraper.scrapeMultiplePages(target);
    const targetIntel = await this.extractor.extractIntelligence(targetPages);

    const competitorIntels = await Promise.all(
      competitors.slice(0, 3).map(async (comp) => {
        const pages = await this.scraper.scrapeMultiplePages(comp);
        return this.extractor.extractIntelligence(pages);
      })
    );

    return this.extractor.generateSWOT(targetIntel, competitorIntels);
  }

  /**
   * Generate AI insights from profiles
   */
  private async generateAIInsights(
    target: CompanyProfile,
    competitors: CompanyProfile[]
  ): Promise<string[]> {
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
        system: `You are a competitive analyst. Generate 5-7 actionable insights based on competitive data.
Return a JSON array of strings only.`,
        messages: [
          {
            role: "user",
            content: `Generate insights for ${target.name} vs competitors: ${competitors.map(c => c.name).join(", ")}\n\nTarget: ${JSON.stringify(target)}\n\nCompetitors: ${JSON.stringify(competitors)}`,
          },
        ],
      }),
    });

    const data = (await response.json()) as { content: Array<{ type: string; text: string }> };
    try {
      const text = data.content.find((c) => c.type === "text")?.text || "[]";
      return JSON.parse(text);
    } catch {
      return [];
    }
  }

  /**
   * Format intelligence report as markdown
   */
  private formatIntelligenceReport(intel: {
    target: CompanyProfile;
    competitors: CompanyProfile[];
    swot: { strengths: string[]; weaknesses: string[]; opportunities: string[]; threats: string[] };
    insights: string[];
  }): string {
    return `# Competitive Intelligence Report
## ${intel.target.name}

**Generated:** ${new Date().toLocaleDateString()}

---

## Target Profile

**Domain:** ${intel.target.domain}
**Positioning:** ${intel.target.positioning || "N/A"}
**Tagline:** ${intel.target.tagline || "N/A"}

### Technology Stack
${intel.target.technology?.stack?.join(", ") || "Not detected"}

### Analytics & Marketing
- Analytics: ${intel.target.technology?.analytics?.join(", ") || "Not detected"}
- Marketing: ${intel.target.technology?.marketing?.join(", ") || "Not detected"}

---

## Competitors (${intel.competitors.length} found)

${intel.competitors.map((c) => `### ${c.name}
**Domain:** ${c.domain}
**Positioning:** ${c.positioning || "N/A"}
**Tech:** ${c.technology?.stack?.join(", ") || "N/A"}
`).join("\n")}

---

## SWOT Analysis

### Strengths
${intel.swot.strengths.map((s) => `- ${s}`).join("\n")}

### Weaknesses
${intel.swot.weaknesses.map((w) => `- ${w}`).join("\n")}

### Opportunities
${intel.swot.opportunities.map((o) => `- ${o}`).join("\n")}

### Threats
${intel.swot.threats.map((t) => `- ${t}`).join("\n")}

---

## Key Insights

${intel.insights.map((i, idx) => `${idx + 1}. ${i}`).join("\n\n")}

---

*Generated by High Era Agency (Free Tools)*
`;
  }

  /**
   * Run full competitive research
   */
  async runResearch(request: ResearchRequest): Promise<ResearchResult> {
    const startTime = Date.now();

    // 1. Scan target
    const targetProfile = await this.scanCompetitor(request.target);

    // 2. Find or use provided competitors
    const competitorDomains =
      request.competitors ||
      (await this.findCompetitors(request.target)).slice(0, 5);

    // 3. Scan competitors in parallel
    const competitorProfiles = await Promise.all(
      competitorDomains.map((domain) => this.scanCompetitor(domain))
    );

    // 4. Analyze landscape
    const landscape = await this.analyzeMarketLandscape(
      targetProfile,
      competitorProfiles
    );

    // 5. Identify gaps and threats
    const gaps = await this.identifyGaps(targetProfile, competitorProfiles);
    const threats = await this.identifyThreats(
      targetProfile,
      competitorProfiles
    );

    // 6. Generate insights with AI
    const { insights, recommendations } = await this.generateInsights({
      target: targetProfile,
      competitors: competitorProfiles,
      landscape,
      gaps,
      threats,
    });

    return {
      id: request.id,
      type: request.type,
      target: request.target,
      completedAt: Date.now(),
      data: {
        target: targetProfile,
        competitors: competitorProfiles,
        landscape,
        gaps,
        threats,
      },
      insights,
      recommendations,
    };
  }

  /**
   * Scan a single competitor
   */
  async scanCompetitor(domain: string): Promise<CompanyProfile> {
    // Clean domain
    domain = domain.replace(/^https?:\/\//, "").replace(/^www\./, "").split("/")[0];

    // Fetch in parallel
    const [metadata, seo, pricing, tech, content] = await Promise.all([
      this.fetcher.fetchMetadata(`https://${domain}`).catch(() => ({})),
      this.seoResearcher.analyzeKeywords(domain).catch(() => ({})),
      this.pricingResearcher.analyzePricing(domain).catch(() => ({})),
      this.techDetector.detectStack(domain).catch(() => ({})),
      this.contentAnalyzer.analyzeContent(domain).catch(() => ({})),
    ]);

    return {
      domain,
      name: metadata.title?.split("|")[0]?.split("-")[0]?.trim() || domain,
      tagline: metadata.description,
      seo,
      pricing,
      technology: tech,
      content,
    };
  }

  /**
   * Find competitors for a domain
   */
  async findCompetitors(
    domain: string,
    industry?: string
  ): Promise<string[]> {
    // Use Claude to identify competitors
    const { text } = await this.fetcher.fetch(`https://${domain}`);

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
        system: `You are a competitive intelligence analyst. Given a company's website content, identify their likely competitors.
Return a JSON array of competitor domains only, no explanation. Example: ["competitor1.com", "competitor2.com"]
Focus on direct competitors in the same market segment.`,
        messages: [
          {
            role: "user",
            content: `Identify competitors for ${domain}${industry ? ` in the ${industry} industry` : ""}.

Website content:
${text.slice(0, 6000)}`,
          },
        ],
      }),
    });

    if (!response.ok) {
      return [];
    }

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
   * Analyze market landscape
   */
  async analyzeMarketLandscape(
    target: CompanyProfile,
    competitors: CompanyProfile[]
  ): Promise<MarketLandscape> {
    // Find market leader (highest traffic/authority)
    const allCompanies = [target, ...competitors];
    const leader = allCompanies.reduce((best, company) => {
      const score = (company.seo?.organicTraffic || 0) + (company.seo?.domainAuthority || 0) * 1000;
      const bestScore = (best.seo?.organicTraffic || 0) + (best.seo?.domainAuthority || 0) * 1000;
      return score > bestScore ? company : best;
    });

    return {
      totalCompetitors: competitors.length,
      marketLeader: leader.domain,
      segments: [], // Would need more analysis
    };
  }

  /**
   * Identify opportunity gaps
   */
  async identifyGaps(
    target: CompanyProfile,
    competitors: CompanyProfile[]
  ): Promise<OpportunityGap[]> {
    const gaps: OpportunityGap[] = [];

    // Content gaps
    const competitorContentTypes = new Set(
      competitors.flatMap((c) => c.content?.contentTypes || [])
    );
    const targetContentTypes = new Set(target.content?.contentTypes || []);

    for (const type of competitorContentTypes) {
      if (!targetContentTypes.has(type)) {
        gaps.push({
          type: "content",
          description: `Competitors have ${type} but you don't`,
          competitors: competitors
            .filter((c) => c.content?.contentTypes?.includes(type))
            .map((c) => c.domain),
          potentialImpact: "medium",
          effort: "medium",
        });
      }
    }

    // Pricing gaps
    const competitorPricing = competitors.filter((c) => c.pricing?.lowestPrice);
    if (competitorPricing.length > 0 && target.pricing?.lowestPrice) {
      const avgPrice =
        competitorPricing.reduce((sum, c) => sum + (c.pricing?.lowestPrice || 0), 0) /
        competitorPricing.length;

      if (target.pricing.lowestPrice > avgPrice * 1.3) {
        gaps.push({
          type: "pricing",
          description: `Your entry price is 30%+ higher than competitor average`,
          competitors: competitorPricing.map((c) => c.domain),
          potentialImpact: "high",
          effort: "low",
        });
      }
    }

    return gaps;
  }

  /**
   * Identify competitive threats
   */
  async identifyThreats(
    target: CompanyProfile,
    competitors: CompanyProfile[]
  ): Promise<CompetitiveThreat[]> {
    const threats: CompetitiveThreat[] = [];

    // SEO threat - competitor with much higher authority
    for (const competitor of competitors) {
      if (
        competitor.seo?.domainAuthority &&
        target.seo?.domainAuthority &&
        competitor.seo.domainAuthority > target.seo.domainAuthority * 1.5
      ) {
        threats.push({
          competitor: competitor.domain,
          threat: `Significantly higher domain authority (${competitor.seo.domainAuthority} vs ${target.seo.domainAuthority})`,
          severity: "high",
          timeframe: "long-term",
        });
      }
    }

    // Content threat - competitor publishing more
    for (const competitor of competitors) {
      if (
        competitor.content?.blogPosts &&
        target.content?.blogPosts &&
        competitor.content.blogPosts > target.content.blogPosts * 2
      ) {
        threats.push({
          competitor: competitor.domain,
          threat: `Publishing significantly more content`,
          severity: "medium",
          timeframe: "short-term",
        });
      }
    }

    return threats;
  }

  /**
   * Analyze SEO gaps between target and competitors
   */
  async analyzeSEOGaps(
    target: string,
    competitors: string[]
  ): Promise<OpportunityGap[]> {
    // Would use Ahrefs/SEMrush API for keyword gap analysis
    // For now, return structural analysis
    return [];
  }

  /**
   * Generate AI insights from research data
   */
  async generateInsights(data: CompetitiveIntelligence): Promise<{
    insights: string[];
    recommendations: string[];
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
        max_tokens: 2048,
        system: `You are a competitive intelligence analyst. Analyze the research data and provide:
1. Key insights about the competitive landscape
2. Actionable recommendations

Return JSON only:
{
  "insights": ["insight 1", "insight 2", ...],
  "recommendations": ["recommendation 1", "recommendation 2", ...]
}

Be specific and actionable. Reference specific competitors and data points.`,
        messages: [
          {
            role: "user",
            content: `Analyze this competitive intelligence data:\n\n${JSON.stringify(data, null, 2)}`,
          },
        ],
      }),
    });

    if (!response.ok) {
      return { insights: [], recommendations: [] };
    }

    const result = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
    };

    try {
      const text = result.content.find((c) => c.type === "text")?.text || "{}";
      return JSON.parse(text);
    } catch {
      return { insights: [], recommendations: [] };
    }
  }
}
