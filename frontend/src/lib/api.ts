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

export interface Brief {
    id?: string;
    title: string;
    product: string;
    audience: string;
    value: string;
    context?: Record<string, string>;
    description?: string;
    created_at?: string;
    updated_at?: string;
}

export interface BriefList {
    briefs: Brief[];
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
	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...options?.headers
	};

    // 1. Anonymous ID (Always present)
    let anonId = typeof localStorage !== 'undefined' ? localStorage.getItem('agency_anon_id') : null;
    if (!anonId && typeof crypto !== 'undefined') {
        anonId = crypto.randomUUID();
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem('agency_anon_id', anonId);
        }
    }
    if (anonId) {
        headers['X-Anonymous-ID'] = anonId;
    }

    // 2. User Token (If signed in)
    // We'll assume the token is stored in localStorage by the Auth component
    const token = typeof localStorage !== 'undefined' ? localStorage.getItem('agency_user_token') : null;
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

	const response = await fetch(`${API_BASE}${endpoint}`, {
		...options,
		headers
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

export interface Lead {
    email: string;
    role?: string;
    company?: string;
    source?: string;
    intent?: string;
}

export async function saveLead(lead: Lead): Promise<void> {
    await request('/leads', {
        method: 'POST',
        body: JSON.stringify(lead)
    });
}

export async function saveBrief(brief: Brief): Promise<Brief> {
    return request('/briefs', {
        method: 'POST',
        body: JSON.stringify(brief)
    });
}

export async function listBriefs(limit: number = 20): Promise<BriefList> {
    return request(`/briefs?limit=${limit}`);
}

export async function getBrief(id: string): Promise<Brief> {
    return request(`/briefs/${id}`);
}

// Skill metadata for UI
export const SKILL_CATEGORIES = {
	writing: {
		label: 'Write Things That Convert',
		description: 'Create conversion-focused content',
		skills: {
			copywriting: 'Headlines, landing pages, CTAs',
			'copy-editing': 'Polish and refine content',
			'email-sequence': 'Welcome, nurture, sales sequences',
			'social-content': 'Platform-native social content'
		}
	},
	cro: {
		label: "Fix What's Broken",
		description: 'Fix conversion leaks',
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
		label: 'Get Found',
		description: 'Technical and content SEO',
		skills: {
			'seo-audit': 'Technical + content SEO',
			'programmatic-seo': 'Template-based pages',
			'schema-markup': 'Structured data'
		}
	},
	strategy: {
		label: 'Think Bigger',
		description: 'Strategic growth planning',
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
		label: 'Measure What Matters',
		description: 'Analytics and testing',
		skills: {
			'ab-test-setup': 'A/B testing',
			'analytics-tracking': 'Analytics setup',
			'paid-ads': 'Paid advertising'
		}
	},
	video: {
		label: 'Programmatic Video',
		description: 'Remotion and dynamic video content',
		skills: {
			'remotion-script': 'Dynamic video scripts',
			'remotion-layout': 'Video component design',
			'manim-composer': 'Mathematical animations',
			'manim-best-practices': 'Manim optimization'
		}
	}
} as const;
