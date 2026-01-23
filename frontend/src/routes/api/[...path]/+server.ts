import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

// Get config from runtime environment
const API_URL = env.VITE_API_URL || 'http://localhost:8080';
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

	try {
		const response = await fetch(url, {
			method: request.method,
			headers,
			body: request.body,
			// @ts-ignore - duplex is needed for some node environments with streaming bodies
			duplex: 'half'
		});

		return new Response(response.body, {
			status: response.status,
			statusText: response.statusText,
			headers: response.headers
		});
	} catch (e) {
		console.error('Proxy error:', e);
		throw error(502, 'Bad Gateway: Could not reach backend API');
	}
}

export const GET: RequestHandler = ({ request, params }) => {
	return proxy(request, params.path || '');
};

export const POST: RequestHandler = ({ request, params }) => {
	return proxy(request, params.path || '');
};
