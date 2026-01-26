import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

// Helper to get env var from Node process or SvelteKit dynamic env
const getEnv = (key: string) => {
    // @ts-ignore
    if (typeof process !== 'undefined' && process.env && process.env[key]) {
        // @ts-ignore
        return process.env[key];
    }
    // @ts-ignore
    return env[key];
}

let rawApiUrl = getEnv('VITE_API_URL') || 'http://localhost:8080';

// Sanitize API_URL
if (!rawApiUrl.startsWith('http://') && !rawApiUrl.startsWith('https://')) {
	console.log(`[Proxy] API_URL '${rawApiUrl}' missing protocol. Prepending http://`);
	rawApiUrl = `http://${rawApiUrl}`;
}

if (rawApiUrl === 'http://marketing-agency-api') {
	console.log(`[Proxy] API_URL '${rawApiUrl}' missing port. Appending :8080`);
	rawApiUrl = `${rawApiUrl}:8080`;
}

const API_URL = rawApiUrl;
const API_SECRET = getEnv('API_SECRET');

console.log(`[Proxy] Configured to forward to: ${API_URL}`);

async function proxy(request: Request, path: string) {
	const url = `${API_URL.replace(/\/$/, '')}/${path}`;
	
	console.log(`[Proxy] Forwarding ${request.method} request to: ${url}`);

	const headers = new Headers(request.headers);
	headers.delete('host');
	headers.delete('connection');
	
	if (API_SECRET) {
		headers.set('Authorization', `Bearer ${API_SECRET}`);
	}

	const maxRetries = 3;
	const baseDelay = 1000;

	for (let i = 0; i < maxRetries; i++) {
		try {
			const response = await fetch(url, {
				method: request.method,
				headers,
				body: request.body,
				// @ts-ignore
				duplex: 'half'
			});

			if (!response.ok) {
				console.log(`[Proxy] Backend returned ${response.status} ${response.statusText}`);
			}

			// If backend is waking up (502/503/504), throw to trigger retry
			if ([502, 503, 504].includes(response.status) && i < maxRetries - 1) {
				throw new Error(`Backend unavailable (Status ${response.status})`);
			}

			return new Response(response.body, {
				status: response.status,
				statusText: response.statusText,
				headers: response.headers
			});
		} catch (e: any) {
			console.log(`[Proxy] Attempt ${i + 1} failed:`, e.message);
			
			if (i === maxRetries - 1) {
				console.error('[Proxy] All attempts failed');
				// Return JSON error so client can see it
				return new Response(JSON.stringify({ error: 'Backend Unreachable', details: e.message }), { 
                    status: 502,
                    headers: { 'Content-Type': 'application/json' }
                });
			}

			const delay = baseDelay * Math.pow(2, i);
			await new Promise(r => setTimeout(r, delay));
		}
	}
	
	throw error(502, 'Unreachable');
}

export const GET: RequestHandler = ({ request, params }) => {
	return proxy(request, params.path || '');
};

export const POST: RequestHandler = ({ request, params }) => {
	return proxy(request, params.path || '');
};
