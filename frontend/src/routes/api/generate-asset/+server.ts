import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

// API endpoint for generating assets using FAL turbo models
export const POST: RequestHandler = async ({ request, fetch }) => {
	try {
		const { type, prompt, model } = await request.json();

		if (!prompt) {
			return json({ error: 'Missing prompt' }, { status: 400 });
		}

		// Forward request to Python backend API
		const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
		const response = await fetch(`${apiUrl}/generate-asset`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				type: type || 'image',
				prompt,
				model: model || undefined // Let backend choose smart default
			})
		});

		if (!response.ok) {
			const error = await response.text();
			return json({ error }, { status: response.status });
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Asset generation error:', error);
		return json(
			{ error: 'Failed to generate asset' },
			{ status: 500 }
		);
	}
};
