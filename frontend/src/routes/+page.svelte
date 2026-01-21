<script lang="ts">
	import { executeWork, SKILL_CATEGORIES, type WorkResult, ApiError } from '$lib/api';

	// Form state
	let selectedCategory = 'writing';
	let selectedSkill = 'copywriting';
	let task = '';
	let content = '';
	let contextFields: { key: string; value: string }[] = [
		{ key: 'product', value: '' },
		{ key: 'audience', value: '' }
	];

	// Execution state
	let loading = false;
	let error: string | null = null;
	let result: WorkResult | null = null;

	// Get skills for selected category
	$: categorySkills = SKILL_CATEGORIES[selectedCategory as keyof typeof SKILL_CATEGORIES]?.skills || {};

	// Reset skill when category changes
	$: {
		const skills = Object.keys(categorySkills);
		if (skills.length > 0 && !skills.includes(selectedSkill)) {
			selectedSkill = skills[0];
		}
	}

	function addContextField() {
		contextFields = [...contextFields, { key: '', value: '' }];
	}

	function removeContextField(index: number) {
		contextFields = contextFields.filter((_, i) => i !== index);
	}

	async function handleSubmit() {
		if (!task.trim()) {
			error = 'Please enter a task';
			return;
		}

		loading = true;
		error = null;
		result = null;

		// Build context object
		const context: Record<string, string> = {};
		for (const field of contextFields) {
			if (field.key.trim() && field.value.trim()) {
				context[field.key.trim()] = field.value.trim();
			}
		}

		try {
			result = await executeWork({
				skill: selectedSkill,
				task: task.trim(),
				context: Object.keys(context).length > 0 ? context : undefined,
				content: content.trim() || undefined
			});
		} catch (e) {
			if (e instanceof ApiError) {
				error = e.detail;
			} else {
				error = 'Failed to execute skill. Is the API running?';
			}
		} finally {
			loading = false;
		}
	}

	function clearResults() {
		result = null;
		error = null;
	}
</script>

<svelte:head>
	<title>Execute Skill | Marketing Agency</title>
</svelte:head>

<div class="container">
	<div class="page-header">
		<h1>Execute a Skill</h1>
		<p>Select a skill, describe your task, and get structured output.</p>
	</div>

	<div class="layout">
		<!-- Input Panel -->
		<div class="panel input-panel">
			<form on:submit|preventDefault={handleSubmit}>
				<!-- Skill Selection -->
				<div class="form-section">
					<h3>1. Choose Skill</h3>

					<div class="skill-selector">
						<div class="category-tabs">
							{#each Object.entries(SKILL_CATEGORIES) as [key, cat]}
								<button
									type="button"
									class="category-tab"
									class:active={selectedCategory === key}
									on:click={() => selectedCategory = key}
								>
									{cat.label}
								</button>
							{/each}
						</div>

						<div class="skill-grid">
							{#each Object.entries(categorySkills) as [skillKey, description]}
								<button
									type="button"
									class="skill-card"
									class:active={selectedSkill === skillKey}
									on:click={() => selectedSkill = skillKey}
								>
									<span class="skill-name">{skillKey}</span>
									<span class="skill-desc">{description}</span>
								</button>
							{/each}
						</div>
					</div>
				</div>

				<!-- Task Input -->
				<div class="form-section">
					<h3>2. Describe Task</h3>
					<label for="task">What do you want the skill to do?</label>
					<textarea
						id="task"
						bind:value={task}
						placeholder="e.g., Write a landing page headline for a project management tool targeting engineering managers"
						rows="4"
					></textarea>
				</div>

				<!-- Context -->
				<div class="form-section">
					<h3>3. Add Context <span class="optional">(optional)</span></h3>
					<p class="text-secondary mb-2">Additional context improves output quality.</p>

					<div class="context-fields">
						{#each contextFields as field, i}
							<div class="context-field">
								<input
									type="text"
									placeholder="Key (e.g., product)"
									bind:value={field.key}
								/>
								<input
									type="text"
									placeholder="Value"
									bind:value={field.value}
								/>
								<button
									type="button"
									class="btn-icon"
									on:click={() => removeContextField(i)}
									title="Remove field"
								>
									×
								</button>
							</div>
						{/each}
					</div>
					<button type="button" class="btn-secondary btn-sm" on:click={addContextField}>
						+ Add Field
					</button>
				</div>

				<!-- Content to Analyze -->
				<div class="form-section">
					<h3>4. Content to Analyze <span class="optional">(optional)</span></h3>
					<label for="content">For audits and editing, paste content here</label>
					<textarea
						id="content"
						bind:value={content}
						placeholder="Paste landing page HTML, existing copy, or other content to analyze..."
						rows="6"
					></textarea>
				</div>

				<!-- Submit -->
				<div class="form-actions">
					<button type="submit" class="btn-primary btn-lg" disabled={loading || !task.trim()}>
						{#if loading}
							<span class="spinner"></span>
							Executing...
						{:else}
							Execute Skill
						{/if}
					</button>
				</div>
			</form>
		</div>

		<!-- Results Panel -->
		<div class="panel results-panel">
			<div class="results-header">
				<h3>Results</h3>
				{#if result}
					<button class="btn-secondary btn-sm" on:click={clearResults}>Clear</button>
				{/if}
			</div>

			{#if error}
				<div class="error-box fade-in">
					<strong>Error:</strong> {error}
				</div>
			{:else if loading}
				<div class="loading-state">
					<div class="spinner"></div>
					<p>Executing <code>{selectedSkill}</code> skill...</p>
					<p class="text-muted">This may take 10-30 seconds</p>
				</div>
			{:else if result}
				<div class="result-content fade-in">
					<!-- Metadata -->
					<div class="result-meta">
						<span class="skill-badge">{result.skill}</span>
						{#if result.metadata}
							<span class="text-muted">
								{result.metadata.input_tokens + result.metadata.output_tokens} tokens
							</span>
						{/if}
					</div>

					<!-- Main Output -->
					<div class="result-section">
						<h4>Output</h4>
						<div class="output-content">
							{@html formatOutput(result.output)}
						</div>
					</div>

					<!-- Alternatives -->
					{#if result.alternatives && result.alternatives.length > 0}
						<div class="result-section">
							<h4>Alternatives</h4>
							<ul class="alternatives-list">
								{#each result.alternatives as alt}
									<li>{alt}</li>
								{/each}
							</ul>
						</div>
					{/if}

					<!-- Recommendations -->
					{#if result.recommendations && result.recommendations.length > 0}
						<div class="result-section">
							<h4>Recommendations</h4>
							<ul class="recommendations-list">
								{#each result.recommendations as rec}
									<li>{rec}</li>
								{/each}
							</ul>
						</div>
					{/if}
				</div>
			{:else}
				<div class="empty-state">
					<p>Results will appear here after execution.</p>
					<p class="text-muted">Select a skill and describe your task to get started.</p>
				</div>
			{/if}
		</div>
	</div>
</div>

<script context="module" lang="ts">
	function formatOutput(text: string): string {
		// Basic markdown-like formatting
		return text
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/^### (.+)$/gm, '<h5>$1</h5>')
			.replace(/^## (.+)$/gm, '<h4>$1</h4>')
			.replace(/^# (.+)$/gm, '<h3>$1</h3>')
			.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
			.replace(/`([^`]+)`/g, '<code>$1</code>')
			.replace(/^- (.+)$/gm, '<li>$1</li>')
			.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
			.replace(/\n\n/g, '</p><p>')
			.replace(/\n/g, '<br>')
			.replace(/^/, '<p>')
			.replace(/$/, '</p>');
	}
</script>

<style>
	.page-header {
		margin-bottom: 2rem;
	}

	.page-header h1 {
		margin-bottom: 0.5rem;
	}

	.layout {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
	}

	@media (max-width: 1024px) {
		.layout {
			grid-template-columns: 1fr;
		}
	}

	.panel {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: 1.5rem;
	}

	.form-section {
		margin-bottom: 1.5rem;
	}

	.form-section h3 {
		font-size: 1rem;
		margin-bottom: 1rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.optional {
		font-weight: 400;
		color: var(--color-text-muted);
		font-size: 0.875rem;
	}

	/* Category Tabs */
	.category-tabs {
		display: flex;
		gap: 0.5rem;
		margin-bottom: 1rem;
		flex-wrap: wrap;
	}

	.category-tab {
		background: var(--color-bg-tertiary);
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
		padding: 0.5rem 0.75rem;
		font-size: 0.8125rem;
	}

	.category-tab.active {
		background: var(--color-accent);
		color: white;
		border-color: var(--color-accent);
	}

	.category-tab:hover:not(.active) {
		border-color: var(--color-border-hover);
	}

	/* Skill Grid */
	.skill-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
		gap: 0.75rem;
	}

	.skill-card {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		text-align: left;
		background: var(--color-bg-tertiary);
		border: 1px solid var(--color-border);
		padding: 0.75rem;
	}

	.skill-card.active {
		border-color: var(--color-accent);
		background: rgba(59, 130, 246, 0.1);
	}

	.skill-card:hover:not(.active) {
		border-color: var(--color-border-hover);
	}

	.skill-name {
		font-family: var(--font-mono);
		font-size: 0.8125rem;
		color: var(--color-text);
		margin-bottom: 0.25rem;
	}

	.skill-desc {
		font-size: 0.75rem;
		color: var(--color-text-muted);
	}

	/* Context Fields */
	.context-fields {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.context-field {
		display: flex;
		gap: 0.5rem;
	}

	.context-field input:first-child {
		flex: 0 0 120px;
	}

	.context-field input:nth-child(2) {
		flex: 1;
	}

	.btn-icon {
		background: var(--color-bg-tertiary);
		color: var(--color-text-muted);
		border: 1px solid var(--color-border);
		width: 36px;
		height: 36px;
		padding: 0;
		font-size: 1.25rem;
		line-height: 1;
	}

	.btn-icon:hover {
		color: var(--color-error);
		border-color: var(--color-error);
	}

	.btn-sm {
		padding: 0.375rem 0.75rem;
		font-size: 0.8125rem;
	}

	.btn-lg {
		padding: 0.875rem 1.5rem;
		font-size: 1rem;
	}

	.form-actions {
		margin-top: 2rem;
	}

	.form-actions button {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
	}

	/* Results Panel */
	.results-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
		padding-bottom: 0.75rem;
		border-bottom: 1px solid var(--color-border);
	}

	.results-header h3 {
		margin: 0;
	}

	.error-box {
		background: rgba(239, 68, 68, 0.1);
		border: 1px solid var(--color-error);
		border-radius: var(--radius);
		padding: 1rem;
		color: var(--color-error);
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 3rem 1rem;
		text-align: center;
	}

	.loading-state .spinner {
		width: 32px;
		height: 32px;
		margin-bottom: 1rem;
	}

	.empty-state {
		text-align: center;
		padding: 3rem 1rem;
		color: var(--color-text-muted);
	}

	/* Result Content */
	.result-meta {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.skill-badge {
		background: var(--color-accent);
		color: white;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-family: var(--font-mono);
		font-size: 0.75rem;
	}

	.result-section {
		margin-bottom: 1.5rem;
	}

	.result-section h4 {
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		margin-bottom: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.output-content {
		background: var(--color-bg-tertiary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1rem;
		max-height: 500px;
		overflow-y: auto;
		font-size: 0.9375rem;
		line-height: 1.7;
	}

	.output-content :global(h3),
	.output-content :global(h4),
	.output-content :global(h5) {
		margin-top: 1.5rem;
		margin-bottom: 0.75rem;
	}

	.output-content :global(h3:first-child),
	.output-content :global(h4:first-child),
	.output-content :global(h5:first-child) {
		margin-top: 0;
	}

	.output-content :global(code) {
		background: var(--color-bg-secondary);
	}

	.output-content :global(ul) {
		margin: 0.5rem 0;
		padding-left: 1.5rem;
	}

	.output-content :global(li) {
		margin: 0.25rem 0;
	}

	.alternatives-list,
	.recommendations-list {
		background: var(--color-bg-tertiary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1rem 1rem 1rem 2rem;
		margin: 0;
	}

	.alternatives-list li,
	.recommendations-list li {
		margin: 0.5rem 0;
	}
</style>
