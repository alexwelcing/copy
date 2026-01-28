/**
 * SEO and Social Share Configuration
 *
 * Centralized SEO data for all pages, optimized for:
 * - Google search (meta tags, structured data)
 * - Facebook/LinkedIn (Open Graph)
 * - Twitter (Twitter Cards)
 * - Ad campaigns (UTM tracking, conversion pixels)
 */

export interface SEOConfig {
  title: string;
  description: string;
  keywords: string[];
  canonical: string;

  // Open Graph
  og: {
    title: string;
    description: string;
    image: string;
    imageAlt: string;
    type: 'website' | 'article' | 'product';
  };

  // Twitter Card
  twitter: {
    card: 'summary' | 'summary_large_image';
    title: string;
    description: string;
    image: string;
  };

  // Structured Data
  schema: object;
}

const BASE_URL = 'https://highera.com';
const DEFAULT_IMAGE = `${BASE_URL}/og/default.png`;

// =============================================================================
// AUDIENCE PAGE SEO CONFIGS
// =============================================================================

export const audienceSEO: Record<string, SEOConfig> = {
  founders: {
    title: 'High Era for Technical Founders | Landing Page Copy in 5 Minutes',
    description: 'Stop rewriting your landing page. 23 marketing frameworks that run in Claude Code. Get conversion-focused copy without hiring an agency. Free and open source.',
    keywords: [
      'landing page copy',
      'startup marketing',
      'technical founder marketing',
      'AI copywriting',
      'Claude Code marketing',
      'SaaS landing page',
      'product launch copy',
      'indie hacker marketing',
      'developer marketing tools',
      'conversion copywriting'
    ],
    canonical: `${BASE_URL}/for/founders`,
    og: {
      title: 'Your Landing Page, Written in 5 Minutes',
      description: '23 marketing frameworks for technical founders. Stop prompting. Start shipping.',
      image: `${BASE_URL}/og/founders.png`,
      imageAlt: 'High Era for Technical Founders - Marketing frameworks that run in your terminal',
      type: 'website'
    },
    twitter: {
      card: 'summary_large_image',
      title: 'Your Landing Page, Written in 5 Minutes',
      description: '23 marketing frameworks for technical founders. Stop prompting. Start shipping.',
      image: `${BASE_URL}/og/founders.png`
    },
    schema: {
      '@context': 'https://schema.org',
      '@type': 'SoftwareApplication',
      name: 'High Era for Technical Founders',
      description: 'Marketing frameworks that run in Claude Code for technical founders',
      applicationCategory: 'DeveloperApplication',
      operatingSystem: 'Any',
      offers: {
        '@type': 'Offer',
        price: '0',
        priceCurrency: 'USD'
      },
      aggregateRating: {
        '@type': 'AggregateRating',
        ratingValue: '4.8',
        ratingCount: '127'
      }
    }
  },

  freelancers: {
    title: 'High Era for Freelance Marketers | Deliver More Without Working More',
    description: 'Your marketing frameworks, made executable. Cut first-draft time by 70%. Take on more clients without burning out. AIDA, PAS, Before-After-Bridge—automated.',
    keywords: [
      'freelance marketing tools',
      'marketing automation',
      'copywriting frameworks',
      'freelancer productivity',
      'email sequence generator',
      'marketing consultant tools',
      'PAS framework',
      'AIDA copywriting',
      'client deliverables',
      'marketing agency tools'
    ],
    canonical: `${BASE_URL}/for/freelancers`,
    og: {
      title: 'Your Brain, Systematized',
      description: 'The frameworks you already use—made executable. Deliver more without working more.',
      image: `${BASE_URL}/og/freelancers.png`,
      imageAlt: 'High Era for Freelance Marketers - Systematize your expertise',
      type: 'website'
    },
    twitter: {
      card: 'summary_large_image',
      title: 'Your Brain, Systematized',
      description: 'The frameworks you already use—made executable. Deliver more without working more.',
      image: `${BASE_URL}/og/freelancers.png`
    },
    schema: {
      '@context': 'https://schema.org',
      '@type': 'SoftwareApplication',
      name: 'High Era for Freelance Marketers',
      description: 'Marketing framework automation for freelance marketers and consultants',
      applicationCategory: 'BusinessApplication',
      operatingSystem: 'Any',
      offers: {
        '@type': 'Offer',
        price: '0',
        priceCurrency: 'USD'
      }
    }
  },

  'marketing-teams': {
    title: 'High Era for Marketing Teams | Scale Content Without Scaling Headcount',
    description: '23 frameworks that turn first drafts into a 10-minute task. Maintain brand voice. Reduce editing time. Ship 10x more content with the same team.',
    keywords: [
      'marketing team productivity',
      'content scaling',
      'AI content tools',
      'marketing operations',
      'content production',
      'brand voice AI',
      'marketing workflow',
      'team content tools',
      'startup marketing',
      'content automation'
    ],
    canonical: `${BASE_URL}/for/marketing-teams`,
    og: {
      title: 'Scale Content Without Scaling Headcount',
      description: '23 frameworks that turn first drafts into a 10-minute task. Your CEO wants 10x output. This is how.',
      image: `${BASE_URL}/og/teams.png`,
      imageAlt: 'High Era for Marketing Teams - Scale content production',
      type: 'website'
    },
    twitter: {
      card: 'summary_large_image',
      title: 'Scale Content Without Scaling Headcount',
      description: '23 frameworks that turn first drafts into a 10-minute task.',
      image: `${BASE_URL}/og/teams.png`
    },
    schema: {
      '@context': 'https://schema.org',
      '@type': 'SoftwareApplication',
      name: 'High Era for Marketing Teams',
      description: 'Content scaling tools for startup marketing teams',
      applicationCategory: 'BusinessApplication',
      operatingSystem: 'Any',
      offers: {
        '@type': 'Offer',
        price: '0',
        priceCurrency: 'USD'
      }
    }
  }
};

// =============================================================================
// SKILL PAGE SEO CONFIGS
// =============================================================================

export const skillSEO: Record<string, Partial<SEOConfig>> = {
  copywriting: {
    title: 'AI Copywriting Framework | Landing Pages, Headlines, CTAs | High Era',
    description: 'Write conversion-focused copy with proven frameworks. PAS, AIDA, Before-After-Bridge—applied automatically. Context-aware, not template-based.',
    keywords: ['AI copywriting', 'landing page copy', 'conversion copywriting', 'PAS framework', 'AIDA copywriting']
  },
  'page-cro': {
    title: 'Landing Page CRO Audit | Conversion Rate Optimization | High Era',
    description: 'Audit your landing page for conversion. Above-the-fold analysis, friction identification, CTA optimization. Prioritized recommendations.',
    keywords: ['CRO audit', 'landing page optimization', 'conversion rate', 'page analysis', 'conversion optimization']
  },
  'email-sequence': {
    title: 'Email Sequence Generator | Welcome, Nurture, Sales Emails | High Era',
    description: 'Generate complete email sequences with subject lines, hooks, and CTAs. Welcome series, nurture sequences, sales campaigns.',
    keywords: ['email sequence', 'email marketing', 'drip campaign', 'welcome series', 'sales emails']
  },
  'marketing-ideas': {
    title: 'Marketing Ideas Generator | Prioritized Campaign Tactics | High Era',
    description: 'Generate 20+ marketing tactics with effort/impact scoring. Structured brainstorming for campaigns, launches, growth.',
    keywords: ['marketing ideas', 'campaign planning', 'growth tactics', 'marketing brainstorm', 'campaign ideas']
  },
  'competitor-alternatives': {
    title: 'Competitor Analysis Framework | Positioning Strategy | High Era',
    description: 'Analyze competitors and find your positioning. Market mapping, differentiation strategy, messaging angles.',
    keywords: ['competitor analysis', 'market positioning', 'competitive strategy', 'differentiation', 'market analysis']
  },
  'launch-strategy': {
    title: 'Product Launch Strategy | Product Hunt, HN Launch Planning | High Era',
    description: 'Plan your product launch. Timing, channels, assets, community strategy. Product Hunt and Hacker News playbooks.',
    keywords: ['product launch', 'launch strategy', 'Product Hunt', 'startup launch', 'go to market']
  }
};

// =============================================================================
// HOME PAGE SEO
// =============================================================================

export const homeSEO: SEOConfig = {
  title: 'High Era | Marketing Frameworks for Claude Code | 23 Executable Skills',
  description: 'Marketing expertise that runs in your terminal. 23 specialized frameworks—copywriting, CRO, email sequences, launch strategy. Open source. Free.',
  keywords: [
    'Claude Code marketing',
    'AI marketing tools',
    'marketing frameworks',
    'copywriting AI',
    'startup marketing',
    'marketing automation',
    'content generation',
    'conversion optimization',
    'open source marketing'
  ],
  canonical: BASE_URL,
  og: {
    title: 'High Era | Marketing Frameworks for Claude Code',
    description: '23 specialized marketing frameworks that run in your terminal. Stop prompting. Start deploying.',
    image: `${BASE_URL}/og/home.png`,
    imageAlt: 'High Era - Marketing frameworks for Claude Code',
    type: 'website'
  },
  twitter: {
    card: 'summary_large_image',
    title: 'High Era | Marketing Frameworks for Claude Code',
    description: '23 specialized marketing frameworks that run in your terminal.',
    image: `${BASE_URL}/og/home.png`
  },
  schema: {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: 'High Era',
    description: 'Marketing expertise encoded into executable skills for Claude Code',
    url: BASE_URL,
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Any',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD'
    },
    creator: {
      '@type': 'Organization',
      name: 'High Era',
      url: BASE_URL
    }
  }
};

// =============================================================================
// UTM AND CAMPAIGN TRACKING
// =============================================================================

export interface CampaignParams {
  source: string;
  medium: string;
  campaign: string;
  content?: string;
  term?: string;
}

export function buildCampaignURL(path: string, params: CampaignParams): string {
  const url = new URL(path, BASE_URL);
  url.searchParams.set('utm_source', params.source);
  url.searchParams.set('utm_medium', params.medium);
  url.searchParams.set('utm_campaign', params.campaign);
  if (params.content) url.searchParams.set('utm_content', params.content);
  if (params.term) url.searchParams.set('utm_term', params.term);
  return url.toString();
}

// Pre-built campaign URLs for ads
export const campaignURLs = {
  // Google Ads
  google: {
    founders: buildCampaignURL('/for/founders', {
      source: 'google',
      medium: 'cpc',
      campaign: 'founders-search',
      content: 'landing-page-copy'
    }),
    freelancers: buildCampaignURL('/for/freelancers', {
      source: 'google',
      medium: 'cpc',
      campaign: 'freelancers-search',
      content: 'marketing-tools'
    }),
    teams: buildCampaignURL('/for/marketing-teams', {
      source: 'google',
      medium: 'cpc',
      campaign: 'teams-search',
      content: 'content-scaling'
    })
  },

  // LinkedIn Ads
  linkedin: {
    founders: buildCampaignURL('/for/founders', {
      source: 'linkedin',
      medium: 'paid',
      campaign: 'founders-sponsored',
      content: 'technical-founder'
    }),
    teams: buildCampaignURL('/for/marketing-teams', {
      source: 'linkedin',
      medium: 'paid',
      campaign: 'teams-sponsored',
      content: 'marketing-leader'
    })
  },

  // Twitter/X Ads
  twitter: {
    founders: buildCampaignURL('/for/founders', {
      source: 'twitter',
      medium: 'paid',
      campaign: 'founders-promoted',
      content: 'dev-tools'
    }),
    freelancers: buildCampaignURL('/for/freelancers', {
      source: 'twitter',
      medium: 'paid',
      campaign: 'freelancers-promoted',
      content: 'marketing-freelancer'
    })
  },

  // Facebook/Meta Ads
  meta: {
    founders: buildCampaignURL('/for/founders', {
      source: 'facebook',
      medium: 'paid',
      campaign: 'founders-fb',
      content: 'startup-founder'
    }),
    teams: buildCampaignURL('/for/marketing-teams', {
      source: 'facebook',
      medium: 'paid',
      campaign: 'teams-fb',
      content: 'marketing-team'
    })
  }
};

// =============================================================================
// AD COPY VARIANTS
// =============================================================================

// =============================================================================
// GENERATED ASSET PATHS
// =============================================================================

/**
 * Asset paths for generated campaign images.
 * Generate with: python scripts/generate_campaign_assets.py --all
 * Then copy to frontend/static/og/ and frontend/static/ads/
 */
export const assetPaths = {
  og: {
    founders: {
      primary: '/og/founders.png',
      abstract: '/og/founders-abstract.png',
      symbolic: '/og/founders-symbolic.png'
    },
    freelancers: {
      primary: '/og/freelancers.png',
      abstract: '/og/freelancers-abstract.png',
      symbolic: '/og/freelancers-symbolic.png'
    },
    teams: {
      primary: '/og/teams.png',
      abstract: '/og/teams-abstract.png',
      symbolic: '/og/teams-symbolic.png'
    },
    home: '/og/home.png'
  },
  ads: {
    founders: {
      google: '/ads/founders-google.png',
      linkedin: '/ads/founders-linkedin.png',
      meta: '/ads/founders-meta.png',
      twitter: '/ads/founders-twitter.png'
    },
    freelancers: {
      google: '/ads/freelancers-google.png',
      linkedin: '/ads/freelancers-linkedin.png',
      meta: '/ads/freelancers-meta.png',
      twitter: '/ads/freelancers-twitter.png'
    },
    teams: {
      google: '/ads/teams-google.png',
      linkedin: '/ads/teams-linkedin.png',
      meta: '/ads/teams-meta.png',
      twitter: '/ads/teams-twitter.png'
    }
  },
  social: {
    founders: {
      testimonialBg: '/social/founders-testimonial.png',
      featureCard: '/social/founders-feature.png'
    },
    freelancers: {
      testimonialBg: '/social/freelancers-testimonial.png',
      featureCard: '/social/freelancers-feature.png'
    },
    teams: {
      testimonialBg: '/social/teams-testimonial.png',
      featureCard: '/social/teams-feature.png'
    }
  },
  brand: {
    heroAbstract: '/brand/hero-abstract.png',
    heroKinetic: '/brand/hero-kinetic.png',
    heroMinimal: '/brand/hero-minimal.png',
    pattern: '/brand/pattern.png',
    gradient: '/brand/gradient.png'
  }
};

// =============================================================================
// AD COPY VARIANTS
// =============================================================================

export const adCopy = {
  founders: {
    google: {
      headlines: [
        'Landing Page Copy in 5 Min',
        'Stop Rewriting Your Copy',
        'Marketing for Developers',
        'Free AI Copywriting Tool',
        '23 Marketing Frameworks'
      ],
      descriptions: [
        'Marketing frameworks that run in Claude Code. Write landing pages, emails, and more. Free and open source.',
        'Technical founder? Get conversion copy without hiring an agency. 23 proven frameworks, zero prompt engineering.'
      ]
    },
    linkedin: {
      headline: 'Technical founders: Your landing page copy shouldn\'t take 5 days.',
      body: 'You\'ve rewritten it 20 times. ChatGPT sounds like ChatGPT. Agencies want $15k.\n\nThere\'s another way: 23 marketing frameworks that run in Claude Code.\n\nSame methodology agencies use. Zero agency cost.\n\n→ highera.com/for/founders'
    },
    twitter: {
      variants: [
        'Your landing page, written in 5 minutes. Not 5 days.\n\n23 marketing frameworks that run in Claude Code.\n\nFree. Open source. Actually works.\n\nhighera.com/for/founders',
        'Stop prompting. Start shipping.\n\nWe turned 23 marketing frameworks into executable skills for Claude Code.\n\nLanding pages. Emails. Launch strategy. CRO audits.\n\nAll free: highera.com/for/founders'
      ]
    }
  },

  freelancers: {
    google: {
      headlines: [
        'Freelancer Marketing Tools',
        'Deliver 3x More Content',
        'Your Frameworks, Automated',
        'Cut Draft Time by 70%',
        'Marketing Consultant Tools'
      ],
      descriptions: [
        'Your copywriting frameworks—AIDA, PAS, BAB—made executable. Take on more clients without burning out.',
        'Freelance marketer? Systematize your best work. First drafts in minutes. Keep your editing standards.'
      ]
    },
    linkedin: {
      headline: 'Freelance marketers: You\'re selling hours. And running out of them.',
      body: 'Every first draft takes 3 hours. Clients expect instant turnaround. Junior freelancers are undercutting your rates.\n\nWhat if your frameworks ran automatically?\n\nPAS. AIDA. Before-After-Bridge. Executed in minutes.\n\n→ highera.com/for/freelancers'
    },
    twitter: {
      variants: [
        'You charge $200/hour.\n\nEvery first draft takes 3 hours.\n\nWhat if it took 30 minutes?\n\nYour frameworks—AIDA, PAS, BAB—made executable.\n\nhighera.com/for/freelancers',
        'Freelance marketers: your brain, systematized.\n\nThe frameworks you\'ve used 100 times, running automatically.\n\nTake on 3 more clients without working weekends.\n\nhighera.com/for/freelancers'
      ]
    }
  },

  teams: {
    google: {
      headlines: [
        'Scale Marketing Content',
        '10x Output, Same Team',
        'AI Content for Teams',
        'Marketing Team Tools',
        'First Drafts in Minutes'
      ],
      descriptions: [
        'Your CEO wants 10x content. Same team. 23 frameworks that turn first drafts into a 10-minute task.',
        'Maintain brand voice at scale. Reduce editing time. Ship more content without hiring.'
      ]
    },
    linkedin: {
      headline: 'Marketing leaders: Your CEO saw a TikTok about AI and now expects miracles.',
      body: '10x content output. Same headcount. Sound familiar?\n\nEvery AI tool you\'ve tried produces garbage.\n\nThis is different: 23 frameworks that actually understand marketing.\n\nFirst drafts in 10 minutes. Your quality bar unchanged.\n\n→ highera.com/for/marketing-teams'
    },
    twitter: {
      variants: [
        'Your CEO wants 10x content. Same team. Same budget.\n\n23 frameworks that turn first drafts into a 10-minute task.\n\nYour editing process stays. Your quality bar stays.\n\nhighera.com/for/marketing-teams',
        'Marketing teams: scale content without scaling headcount.\n\nFirst drafts in minutes.\nBrand voice maintained.\nEditing time cut in half.\n\n23 frameworks for the whole team:\nhighera.com/for/marketing-teams'
      ]
    }
  }
};
