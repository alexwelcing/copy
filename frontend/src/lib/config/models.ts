/**
 * FAL.ai Turbo Model Configuration
 * Fast, high-quality models optimized for production use
 */

export const TURBO_MODELS = {
	image: {
		// Fastest turbo models for campaign generation
		'fal-ai/flux/schnell': {
			name: 'FLUX Schnell',
			description: 'Fast + high quality (recommended)',
			speed: 'ultra-fast',
			quality: 'high'
		},
		'fal-ai/fast-lightning-sdxl': {
			name: 'SDXL Lightning',
			description: 'Ultra fast generation',
			speed: 'ultra-fast',
			quality: 'good'
		},
		'fal-ai/fast-sdxl': {
			name: 'Fast SDXL',
			description: 'Balanced speed/quality',
			speed: 'fast',
			quality: 'high'
		},
		'fal-ai/flux/dev': {
			name: 'FLUX Dev',
			description: 'Quality focus',
			speed: 'moderate',
			quality: 'very-high'
		},
		'fal-ai/recraft-v3': {
			name: 'Recraft V3',
			description: 'Design/vector focus',
			speed: 'fast',
			quality: 'high'
		},
		// Premium models for hero images
		'fal-ai/flux-pro/v1.1': {
			name: 'FLUX Pro 1.1',
			description: 'Premium photorealism',
			speed: 'moderate',
			quality: 'premium'
		},
		'fal-ai/flux-realism': {
			name: 'FLUX Realism',
			description: 'Photorealistic images',
			speed: 'moderate',
			quality: 'premium'
		},
		// Text specialists
		'fal-ai/qwen-image-2512': {
			name: 'Qwen Image 2512',
			description: 'Best for text in images',
			speed: 'fast',
			quality: 'high',
			specialty: 'text'
		},
		'fal-ai/longcat-image': {
			name: 'LongCat Image',
			description: 'Multilingual text',
			speed: 'fast',
			quality: 'high',
			specialty: 'text'
		}
	},
	video: {
		'fal-ai/ltx-2-19b/distilled/text-to-video': {
			name: 'LTX Video (Fast)',
			description: 'Fast video generation',
			speed: 'fast',
			quality: 'good'
		},
		'fal-ai/kling-video/v2.5-turbo/pro/text-to-video': {
			name: 'Kling V2.5 Turbo Pro',
			description: 'High quality turbo',
			speed: 'fast',
			quality: 'high'
		},
		'fal-ai/minimax/hailuo-2.3/pro/image-to-video': {
			name: 'MiniMax Hailuo Pro',
			description: 'Image to video',
			speed: 'moderate',
			quality: 'high'
		}
	},
	audio: {
		'fal-ai/stable-audio': {
			name: 'Stable Audio',
			description: 'Music and soundscapes',
			speed: 'fast',
			quality: 'high'
		}
	}
} as const;

// Default recommendations by use case
export const MODEL_RECOMMENDATIONS = {
	'hero-image': 'fal-ai/flux-pro/v1.1',
	'og-image': 'fal-ai/flux/schnell',
	'social-post': 'fal-ai/fast-sdxl',
	'text-overlay': 'fal-ai/qwen-image-2512',
	'brand-asset': 'fal-ai/recraft-v3',
	'quick-iteration': 'fal-ai/fast-lightning-sdxl'
};

// Helper to get model list by type
export function getModelsByType(type: 'image' | 'video' | 'audio'): Record<string, any> {
	return TURBO_MODELS[type];
}

// Helper to get recommended model for use case
export function getRecommendedModel(useCase: keyof typeof MODEL_RECOMMENDATIONS): string {
	return MODEL_RECOMMENDATIONS[useCase];
}
