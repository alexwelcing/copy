/**
 * Marketing Agency API Client
 */

// Use local proxy which forwards to backend with auth
const API_BASE = '/api';

export interface WorkRequest {
	skill: string;
	task: string;
	context?: Record<string, string | string[]>;
	content?: string;
}

export interface WorkResult {
	skill: string;
	output: string;
	sections?: Record<string, string>;
	alternatives?: string[];
	recommendations?: string[];
	metadata?: {
		model: string;
		input_tokens: number;
		output_tokens: number;
	};
}

export interface HealthResponse {
	status: string;
	version: string;
	skills_available: number;
}

export interface SkillsResponse {
	skills: Record<string, Record<string, string>>;
	total: number;
}

export class ApiError extends Error {
	constructor(
		public status: number,
		public detail: string
	) {
		super(detail);
		this.name = 'ApiError';
	}
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
	const response = await fetch(`${API_BASE}${endpoint}`, {
		...options,
		headers: {
			'Content-Type': 'application/json',
			...options?.headers
		}
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
		throw new ApiError(response.status, error.detail || error.error || 'Request failed');
	}

	return response.json();
}

export async function health(): Promise<HealthResponse> {
	return request('/health');
}

export async function listSkills(): Promise<SkillsResponse> {
	return request('/skills');
}

export async function executeWork(req: WorkRequest): Promise<WorkResult> {
	return request('/work', {
		method: 'POST',
		body: JSON.stringify(req)
	});
}

// Skill metadata for UI
export const SKILL_CATEGORIES = {
	writing: {
		label: 'Writing',
		description: 'Create conversion-focused content',
		skills: {
			copywriting: 'Headlines, landing pages, CTAs',
			'copy-editing': 'Polish and refine content',
			'email-sequence': 'Welcome, nurture, sales sequences',
			'social-content': 'Platform-native social content'
		}
	},
	cro: {
		label: 'Conversion Optimization',
		description: 'Fix what\'s broken',
		skills: {
			'page-cro': 'Landing page audits',
			'form-cro': 'Form optimization',
			'signup-flow-cro': 'Registration flows',
			'onboarding-cro': 'User onboarding',
			'popup-cro': 'Popup optimization',
			'paywall-upgrade-cro': 'Upgrade flows'
		}
	},
	seo: {
		label: 'SEO',
		description: 'Get found',
		skills: {
			'seo-audit': 'Technical + content SEO',
			'programmatic-seo': 'Template-based pages',
			'schema-markup': 'Structured data'
		}
	},
	strategy: {
		label: 'Strategy',
		description: 'Think bigger',
		skills: {
			'marketing-ideas': 'Brainstorming',
			'marketing-psychology': 'Persuasion principles',
			'pricing-strategy': 'Pricing optimization',
			'launch-strategy': 'Product launches',
			'competitor-alternatives': 'Competitive positioning',
			'referral-program': 'Viral growth',
			'free-tool-strategy': 'Lead gen tools'
		}
	},
	measurement: {
		label: 'Measurement',
		description: 'Measure what matters',
		skills: {
			'ab-test-setup': 'A/B testing',
			'analytics-tracking': 'Analytics setup',
			'paid-ads': 'Paid advertising'
		}
	}
} as const;
