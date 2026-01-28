<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	export let category: 'og' | 'hero' | 'social' | 'brand' | 'all' = 'all';
	export let audience: string | null = null;

	let assets: any[] = [];
	let loading = true;
	let error: string | null = null;
	let selectedAsset: any = null;

	onMount(async () => {
		await loadAssets();
	});

	async function loadAssets() {
		try {
			loading = true;
			const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
			
			let prefix = '';
			if (category !== 'all') {
				prefix = `images/${category}`;
			}
			if (audience) {
				prefix += `_${audience}`;
			}

			const response = await fetch(`${apiUrl}/assets?prefix=${prefix}`);
			if (response.ok) {
				const data = await response.json();
				assets = data.assets || [];
			}
		} catch (e) {
			error = 'Failed to load assets';
			console.error(e);
		} finally {
			loading = false;
		}
	}

	function getAssetName(path: string): string {
		return path.split('/').pop()?.split('_').slice(1, 3).join(' ') || 'Asset';
	}

	function copyUrl(url: string) {
		navigator.clipboard.writeText(url);
	}
</script>

<div class="asset-gallery">
	{#if loading}
		<div class="loading-state">
			<span class="spinner"></span>
			<p>Loading assets from library...</p>
		</div>
	{:else if error}
		<div class="error-state">
			<p>{error}</p>
		</div>
	{:else if assets.length === 0}
		<div class="empty-state">
			<p>No assets found. Generate your first asset in the <a href="/assess">Assessment Lab</a>.</p>
		</div>
	{:else}
		<div class="gallery-grid">
			{#each assets as asset}
				<button 
					class="asset-card" 
					on:click={() => selectedAsset = asset}
					transition:fade
				>
					<div class="asset-preview">
						<img 
							src={asset.url} 
							alt={getAssetName(asset.name)}
							loading="lazy"
						/>
					</div>
					<div class="asset-info">
						<span class="asset-name">{getAssetName(asset.name)}</span>
						<span class="asset-date">{new Date(asset.updated).toLocaleDateString()}</span>
					</div>
				</button>
			{/each}
		</div>
	{/if}

	{#if selectedAsset}
		<div class="asset-modal" on:click={() => selectedAsset = null} transition:fade>
			<div class="modal-content" on:click|stopPropagation>
				<button class="close-btn" on:click={() => selectedAsset = null}>&times;</button>
				<img src={selectedAsset.url} alt={getAssetName(selectedAsset.name)} />
				<div class="modal-actions">
					<button class="btn-secondary" on:click={() => copyUrl(selectedAsset.url)}>
						Copy URL
					</button>
					<a 
						href={selectedAsset.url} 
						download 
						class="btn-primary"
						target="_blank"
						rel="noopener noreferrer"
					>
						Download
					</a>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.asset-gallery {
		width: 100%;
	}

	.loading-state, .error-state, .empty-state {
		padding: 4rem 2rem;
		text-align: center;
		color: var(--color-text-muted);
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
	}

	.empty-state a {
		color: var(--color-brass);
		text-decoration: underline;
	}

	.gallery-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 1.5rem;
	}

	.asset-card {
		background: var(--color-cream);
		border: 1px solid var(--color-border);
		padding: 0;
		cursor: pointer;
		transition: all 0.2s ease;
		text-align: left;
	}

	.asset-card:hover {
		border-color: var(--color-brass);
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0,0,0,0.1);
	}

	.asset-preview {
		width: 100%;
		aspect-ratio: 16/9;
		overflow: hidden;
		background: var(--color-bg-tertiary);
	}

	.asset-preview img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.asset-info {
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.asset-name {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-navy);
		text-transform: capitalize;
	}

	.asset-date {
		font-family: var(--font-mono);
		font-size: 0.6rem;
		color: var(--color-text-muted);
	}

	.asset-modal {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0,0,0,0.9);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: 2rem;
	}

	.modal-content {
		position: relative;
		max-width: 90vw;
		max-height: 90vh;
		background: white;
		padding: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.modal-content img {
		max-width: 100%;
		max-height: 70vh;
		object-fit: contain;
	}

	.close-btn {
		position: absolute;
		top: 1rem;
		right: 1rem;
		background: none;
		border: none;
		font-size: 2rem;
		cursor: pointer;
		color: var(--color-navy);
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.modal-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
	}

	@media (max-width: 768px) {
		.gallery-grid {
			grid-template-columns: 1fr;
		}

		.modal-content {
			padding: 1rem;
		}
	}
</style>
