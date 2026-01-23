import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

// Get config from runtime environment
let rawApiUrl = env.VITE_API_URL || 'http://localhost:8080';

// Sanitize API_URL: ensure protocol and port (fixes Render env var issues)
if (!rawApiUrl.startsWith('http://') && !rawApiUrl.startsWith('https://')) {
	console.log(`[Proxy] API_URL '${rawApiUrl}' missing protocol. Prepending http://`);
	rawApiUrl = `http://${rawApiUrl}`;
}

// If it's the internal service name without port, add 8080
if (rawApiUrl === 'http://marketing-agency-api') {
	console.log(`[Proxy] API_URL '${rawApiUrl}' missing port. Appending :8080`);
	rawApiUrl = `${rawApiUrl}:8080`;
}

const API_URL = rawApiUrl;
const API_SECRET = env.API_SECRET;

async function proxy(request: Request, path: string) {
	const url = `${API_URL.replace(/\/$/, '')}/${path}`;
	
	const headers = new Headers(request.headers);
	headers.delete('host');
	headers.delete('connection');
	
	// Add authentication if secret is configured
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

			// If backend is waking up (502/503/504), throw to trigger retry
			if ([502, 503, 504].includes(response.status) && i < maxRetries - 1) {
				throw new Error(`Backend unavailable (Status ${response.status})`);
			}

			return new Response(response.body, {
				status: response.status,
				statusText: response.statusText,
				headers: response.headers
			});
		} catch (e) {
			console.log(`Proxy attempt ${i + 1} failed:`, e);
			
			// If this was the last try, throw the error
			if (i === maxRetries - 1) {
				console.error('All proxy attempts failed');
				throw error(502, 'Bad Gateway: Backend is waking up or unreachable. Please try again in a moment.');
			}

			// Wait before retrying (exponential backoff: 1s, 2s, 4s...)
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
