/**
 * Example presets for common marketing tasks
 */

export interface Preset {
	skill: string;
	name: string;
	task: string;
	context?: Record<string, string>;
	content?: string;
}

export const PRESETS: Preset[] = [
	// Copywriting
	{
		skill: 'copywriting',
		name: 'Landing Page Headlines',
		task: 'Write 5 headline options for a landing page. Include a primary headline, subheadline, and 3 alternatives with different angles (outcome-focused, pain-focused, curiosity-driven).',
		context: {
			product: 'Your product name',
			audience: 'Target audience',
			main_benefit: 'Primary benefit',
			tone: 'Professional but approachable'
		}
	},
	{
		skill: 'copywriting',
		name: 'Product Description',
		task: 'Write a compelling product description for the homepage hero section. Include headline, subheadline, 3-4 bullet points, and primary CTA.',
		context: {
			product: 'Your product name',
			audience: 'Target audience',
			key_features: 'Feature 1, Feature 2, Feature 3',
			differentiator: 'What makes this different'
		}
	},
	{
		skill: 'copywriting',
		name: 'CTA Button Copy',
		task: 'Generate 10 CTA button variations for a signup flow. Include primary action CTAs, friction reducers, and urgency variants where appropriate.',
		context: {
			action: 'Sign up for free trial',
			audience: 'SaaS buyers',
			page_context: 'Pricing page'
		}
	},

	// Page CRO
	{
		skill: 'page-cro',
		name: 'Landing Page Audit',
		task: 'Perform a comprehensive CRO audit of this landing page. Identify quick wins, high-impact changes, and A/B test ideas. Prioritize recommendations by expected impact.',
		context: {
			conversion_goal: 'Free trial signup',
			traffic_source: 'Google Ads',
			current_conversion_rate: 'Unknown'
		},
		content: 'Paste your landing page HTML or content here...'
	},
	{
		skill: 'page-cro',
		name: 'Pricing Page Review',
		task: 'Analyze this pricing page for conversion optimization. Focus on reducing decision friction, highlighting value, and addressing common objections.',
		context: {
			pricing_model: 'Freemium with Pro tier',
			target_tier: 'Pro ($X/month)',
			main_objection: 'Price sensitivity'
		},
		content: 'Paste your pricing page content here...'
	},

	// Email Sequence
	{
		skill: 'email-sequence',
		name: 'Welcome Sequence',
		task: 'Create a 5-email welcome sequence for new signups. Focus on getting users to their first success (activation event). Include subject lines, preview text, and full email copy.',
		context: {
			product: 'Your product',
			activation_event: 'First project created',
			audience: 'New signups',
			tone: 'Helpful, not pushy'
		}
	},
	{
		skill: 'email-sequence',
		name: 'Re-engagement Campaign',
		task: 'Design a 3-email re-engagement sequence for users who signed up but never activated. Win them back or get feedback on why they left.',
		context: {
			product: 'Your product',
			days_inactive: '14+',
			incentive: 'Extended trial or discount (optional)'
		}
	},

	// Marketing Psychology
	{
		skill: 'marketing-psychology',
		name: 'Persuasion Audit',
		task: 'Analyze this page through the lens of Cialdini\'s principles. Identify which principles are being used, which are missing, and provide specific recommendations for each.',
		context: {
			page_type: 'Landing page',
			goal: 'Increase signups'
		},
		content: 'Paste your page content here...'
	},
	{
		skill: 'marketing-psychology',
		name: 'Pricing Psychology',
		task: 'Recommend psychological principles to apply to our pricing page. Include specific tactics for anchoring, framing, and reducing price sensitivity.',
		context: {
			pricing_tiers: 'Free, Pro ($X), Team ($Y)',
			target_tier: 'Pro',
			audience: 'SMB decision makers'
		}
	},

	// Launch Strategy
	{
		skill: 'launch-strategy',
		name: 'Product Hunt Launch',
		task: 'Create a complete Product Hunt launch plan including pre-launch preparation (2 weeks), launch day timeline (hour by hour), and post-launch follow-up. Include copy for tagline, description, and first comment.',
		context: {
			product: 'Your product',
			category: 'Productivity',
			existing_audience: 'Email list size, Twitter followers',
			launch_date: 'Target date'
		}
	},
	{
		skill: 'launch-strategy',
		name: 'Feature Launch',
		task: 'Plan an internal feature launch to existing users. Include announcement email, in-app messaging, and social media content.',
		context: {
			feature: 'New feature name',
			benefit: 'Main user benefit',
			availability: 'All users / Pro only'
		}
	},

	// SEO
	{
		skill: 'seo-audit',
		name: 'Quick SEO Check',
		task: 'Perform a quick SEO audit focusing on the most impactful issues. Check title tags, meta descriptions, headings, and content quality. Prioritize fixes.',
		context: {
			page_url: 'URL to audit',
			target_keyword: 'Primary keyword',
			competitors: 'Top 2-3 competitor URLs'
		},
		content: 'Paste page HTML or describe the page...'
	},

	// Competitor Analysis
	{
		skill: 'competitor-alternatives',
		name: 'Positioning Analysis',
		task: 'Analyze our positioning against these competitors. Identify gaps, opportunities, and recommend messaging that creates differentiation.',
		context: {
			our_product: 'Your product',
			competitors: 'Competitor 1, Competitor 2, Competitor 3',
			our_strengths: 'What we do best',
			target_audience: 'Who we serve'
		}
	},

	// A/B Testing
	{
		skill: 'ab-test-setup',
		name: 'Test Hypothesis',
		task: 'Design an A/B test for this hypothesis. Include test setup, success metrics, sample size requirements, and expected duration.',
		context: {
			hypothesis: 'If we [change], then [metric] will [improve] because [reason]',
			current_baseline: 'Current conversion rate',
			minimum_detectable_effect: '10-20%'
		}
	}
];

export function getPresetsForSkill(skill: string): Preset[] {
	return PRESETS.filter(p => p.skill === skill);
}

export function getPresetsByCategory(): Record<string, Preset[]> {
	const categories: Record<string, Preset[]> = {};
	for (const preset of PRESETS) {
		if (!categories[preset.skill]) {
			categories[preset.skill] = [];
		}
		categories[preset.skill].push(preset);
	}
	return categories;
}
