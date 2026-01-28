/**
 * Audience-specific landing page content
 *
 * Each audience has tailored messaging, pain points, and CTAs
 * designed to convert their specific situation.
 */

export interface AudiencePage {
  slug: string;
  audience: string;
  headline: string;
  subheadline: string;
  painPoints: {
    hook: string;
    points: Array<{
      problem: string;
      agitation: string;
    }>;
  };
  solution: {
    intro: string;
    points: Array<{
      title: string;
      description: string;
    }>;
  };
  proof: {
    type: 'demo' | 'testimonial' | 'dogfood';
    content: string;
  };
  cta: {
    primary: string;
    secondary: string;
    action: string;
  };
  objections: Array<{
    objection: string;
    response: string;
  }>;
  skills: string[]; // Recommended skills for this audience
}

export const audiences: AudiencePage[] = [
  // ==========================================================================
  // AUDIENCE 1: TECHNICAL FOUNDERS
  // ==========================================================================
  {
    slug: 'founders',
    audience: 'Technical Founders',
    headline: 'Your landing page, written in 5 minutes. Not 5 days.',
    subheadline: '23 marketing frameworks that run in Claude Code. Stop prompting. Start shipping.',
    painPoints: {
      hook: 'You know the pattern.',
      points: [
        {
          problem: "You've rewritten your landing page twenty times.",
          agitation: "Each version sounds either too technical or too generic. You know the product is good. You just can't explain it."
        },
        {
          problem: "ChatGPT output sounds like ChatGPT.",
          agitation: "Hollow. Corporate. The exact opposite of how you'd describe your product to a friend."
        },
        {
          problem: "Agencies want $15k for a landing page.",
          agitation: "You're pre-revenue. That's your runway for the next three months."
        },
        {
          problem: "Marketing feels like a foreign language.",
          agitation: "You can architect a distributed system. But 'above the fold' and 'awareness stages' might as well be Klingon."
        }
      ]
    },
    solution: {
      intro: "This is different. Not another AI writing tool. A complete marketing methodology that runs in your terminal.",
      points: [
        {
          title: "Skills, not prompts",
          description: "Each skill is a 2000-word framework—context questions, psychological principles, proven structures, quality checks. The same mental models top marketers use, made executable."
        },
        {
          title: "Strategy before words",
          description: "Every skill asks the right questions first. Who's the audience? What's their awareness stage? What objections will they have? Copy comes last."
        },
        {
          title: "Specificity in, specificity out",
          description: "Generic inputs get generic outputs. That's true everywhere. The skill forces you to get specific—and then delivers copy that matches."
        },
        {
          title: "Works in Claude Code",
          description: "No new tool to learn. Load a skill file. Tell it what you need. Ship."
        }
      ]
    },
    proof: {
      type: 'dogfood',
      content: "This entire page was written using the copywriting skill. The email sequence uses the email-sequence skill. We eat our own cooking."
    },
    cta: {
      primary: "Write your landing page →",
      secondary: "See the 23 skills",
      action: "copywriting"
    },
    objections: [
      {
        objection: "I can prompt Claude myself",
        response: "You can. But the skill knows to ask about awareness stages, apply loss aversion correctly, and check against 15 quality criteria. You'd have to hold all that in your head."
      },
      {
        objection: "This is just prompt engineering",
        response: "Open the skill file. It's not a template—it's a complete methodology. Context gathering, psychological principles, structural formulas, quality checklists. That's not a prompt."
      },
      {
        objection: "AI copy always sounds artificial",
        response: "Only if you give it artificial inputs. 'Write me a landing page' gets garbage. 'Here's my product, audience, key objection, and proof points' gets something you'd actually ship."
      }
    ],
    skills: ['copywriting', 'page-cro', 'launch-strategy', 'competitor-alternatives']
  },

  // ==========================================================================
  // AUDIENCE 2: FREELANCE MARKETERS
  // ==========================================================================
  {
    slug: 'freelancers',
    audience: 'Freelance Marketers',
    headline: 'Your brain, systematized.',
    subheadline: 'The frameworks you already use—AIDA, PAS, Before-After-Bridge—made executable. Deliver more without working more.',
    painPoints: {
      hook: "You're selling hours. And you're running out of them.",
      points: [
        {
          problem: "Every first draft takes 3 hours.",
          agitation: "You know the framework. You've used it a hundred times. But you still start from blank every time."
        },
        {
          problem: "Clients expect instant turnaround.",
          agitation: "The AI era has reset expectations. 'Can you have this by end of day?' used to be unreasonable. Now it's Tuesday."
        },
        {
          problem: "Junior freelancers are undercutting your rates.",
          agitation: "They're charging $50/hour because AI does the writing. But their output is garbage. Yours isn't. But the price pressure is real."
        },
        {
          problem: "You keep reinventing the same deliverables.",
          agitation: "Email sequence. Landing page. Ad copy. You've done each one fifty times. Still starting from scratch."
        }
      ]
    },
    solution: {
      intro: "This isn't an AI writing tool. It's your expertise, encoded into executable frameworks.",
      points: [
        {
          title: "Your frameworks, running automatically",
          description: "PAS. AIDA. Before-After-Bridge. The skill applies them correctly every time. You focus on strategy, not structure."
        },
        {
          title: "First drafts in minutes, not hours",
          description: "Load the skill. Input the brief. Get a draft that's 80% there. Spend your time on the 20% that makes it great."
        },
        {
          title: "Systemize without losing the craft",
          description: "The skill handles the formula. You add the insight. Clients get better work, faster. You get your evenings back."
        },
        {
          title: "Transparent methodology",
          description: "Every skill shows its work. Context questions, psychological principles, quality checks. Steal the frameworks. Improve them. Make them yours."
        }
      ]
    },
    proof: {
      type: 'demo',
      content: "Load the email-sequence skill. Input a client brief. Get a complete 5-email sequence with subject lines, hooks, and CTAs—structured exactly like you'd do it, in 5 minutes instead of 5 hours."
    },
    cta: {
      primary: "Try on a client project →",
      secondary: "See the frameworks",
      action: "email-sequence"
    },
    objections: [
      {
        objection: "My clients pay for my expertise, not AI",
        response: "They pay for results. The expertise is in choosing the right approach, refining the output, and knowing what good looks like. This just makes execution faster."
      },
      {
        objection: "What if clients find out I use AI?",
        response: "They probably already assume it. The question is whether the work is good. If the output is excellent, the method is irrelevant."
      },
      {
        objection: "I have my own processes",
        response: "Good. Use these as inputs to your process. Or steal the frameworks and build your own skills. It's all open source."
      }
    ],
    skills: ['email-sequence', 'copywriting', 'page-cro', 'marketing-psychology']
  },

  // ==========================================================================
  // AUDIENCE 3: STARTUP MARKETING TEAMS
  // ==========================================================================
  {
    slug: 'marketing-teams',
    audience: 'Startup Marketing Teams',
    headline: 'Scale content without scaling headcount.',
    subheadline: '23 frameworks that turn first drafts into a 10-minute task. Your CEO wants 10x output. This is how.',
    painPoints: {
      hook: "Your CEO saw a TikTok about AI and now expects miracles.",
      points: [
        {
          problem: "You need to produce 10x more content with the same team.",
          agitation: "The board deck said 'AI-powered content engine.' You're the one who has to build it."
        },
        {
          problem: "Every AI tool you've tried produces the same garbage.",
          agitation: "Jasper. Copy.ai. Writesonic. Same hollow corporate-speak. Same need to rewrite everything."
        },
        {
          problem: "Junior writers need constant editing.",
          agitation: "You're spending more time editing than it would take to write it yourself. But you don't have time to write it yourself."
        },
        {
          problem: "First drafts take 3 hours each.",
          agitation: "That's 15 hours a week on drafts alone. Multiply by your team. That's where your bandwidth goes."
        }
      ]
    },
    solution: {
      intro: "This isn't about replacing your team. It's about making first drafts a 10-minute task.",
      points: [
        {
          title: "First drafts that don't need a rewrite",
          description: "Each skill applies proven frameworks—the same ones your senior writers use. Junior writers get structured output. You get less editing."
        },
        {
          title: "Brand voice built in",
          description: "The skill asks about voice and tone before writing. Input your brand guide once. Get consistent output across the team."
        },
        {
          title: "Strategy frameworks, not just copy",
          description: "Competitor analysis. Marketing psychology. Launch strategy. The thinking skills, not just the writing skills."
        },
        {
          title: "Open and customizable",
          description: "Every skill is a markdown file. Edit them. Add your brand guidelines. Build custom skills for your specific needs."
        }
      ]
    },
    proof: {
      type: 'demo',
      content: "Run the marketing-ideas skill with your next campaign brief. Get a prioritized list of 20 tactics with effort/impact scoring—the kind of brainstorm that usually takes a half-day offsite."
    },
    cta: {
      primary: "See the 23 skills →",
      secondary: "Start with one skill",
      action: "skills"
    },
    objections: [
      {
        objection: "We already have a content workflow",
        response: "This slots into your workflow. Use it for first drafts. Keep your editing and approval process. The input is faster; the quality bar is yours."
      },
      {
        objection: "AI can't match our brand voice",
        response: "It can if you give it the right inputs. Every skill asks about voice and tone. Input your brand guide and it adapts."
      },
      {
        objection: "My team won't use command-line tools",
        response: "If they can use Slack, they can use Claude Code. It's a chat interface. Type what you need. Get what you asked for."
      }
    ],
    skills: ['marketing-ideas', 'copywriting', 'email-sequence', 'competitor-alternatives', 'copy-editing']
  }
];

// Utility to get audience by slug
export function getAudience(slug: string): AudiencePage | undefined {
  return audiences.find(a => a.slug === slug);
}

// Get all audience slugs for routing
export function getAudienceSlugs(): string[] {
  return audiences.map(a => a.slug);
}
