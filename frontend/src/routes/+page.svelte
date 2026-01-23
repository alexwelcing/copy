<script lang="ts">
	import { executeWork, SKILL_CATEGORIES, type WorkResult, ApiError } from '$lib/api';
	import { getPresetsForSkill, type Preset } from '$lib/presets';

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

	

		// UI State

		let showPresets = false;

		let showAdvanced = false;

		let showAllPresets = false;

	

		$: currentStep = task.trim() ? 2 : 1;

		$: isReadyToExecute = selectedSkill && task.trim();

		

		// Presets

		$: skillPresets = getPresetsForSkill(selectedSkill);

	

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

	

		function loadPreset(preset: Preset) {

			task = preset.task;

			content = preset.content || '';

	

			// Load context fields

			if (preset.context) {

				contextFields = Object.entries(preset.context).map(([key, value]) => ({ key, value }));

			} else {

				contextFields = [

					{ key: 'product', value: '' },

					{ key: 'audience', value: '' }

				];

			}

	

			showPresets = false;

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

			}

			finally {

				loading = false;

			}

		}

	

		function clearResults() {

			result = null;

			error = null;

		}

	

		function copyOutput() {

			if (result?.output) {

				navigator.clipboard.writeText(result.output);

			}

		}

	</script>

	

	<svelte:head>

		<title>AI Marketing Agency | Execute Expert Skills</title>

	</svelte:head>

	

	<div class="container">

		<div class="page-header">

			<h1>AI Marketing Skills That Actually Work</h1>

			<p class="value-prop">

				Get expert-level copy, audits, and strategy in 30 seconds. 

				No prompt engineering required—just describe what you need.

			</p>

			<div class="trust-indicators">

				<div class="stat"><strong>23</strong> specialized skills</div>

				<div class="stat"><strong>10-30s</strong> average execution</div>

				<div class="stat"><strong>Zero</strong> AI expertise needed</div>

			</div>

		</div>

	

		<div class="progress-steps">

			<div class="step" class:complete={currentStep >= 1}>

				<span class="step-number">1</span>

				<span class="step-label">Choose Skill</span>

			</div>

			<div class="step-line" class:complete={currentStep >= 2}></div>

			<div class="step" class:complete={currentStep >= 2}>

				<span class="step-number">2</span>

				<span class="step-label">Describe Task</span>

			</div>

			<div class="step-line" class:complete={currentStep >= 3}></div>

			<div class="step" class:complete={currentStep >= 3}>

				<span class="step-number">3</span>

				<span class="step-label">Get Results</span>

			</div>

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
					<div class="section-header">
						<h3>2. Describe Task</h3>
					</div>

					{#if skillPresets.length > 0}
						<div class="quick-start">
							<label class="quick-start-label" for="task">
								⚡ Quick Start (click to use)
							</label>
							<div class="presets-list-compact">
								{#each (showAllPresets ? skillPresets : skillPresets.slice(0, 3)) as preset}
									<button
										type="button"
										class="preset-pill"
										on:click={() => loadPreset(preset)}
									>
										{preset.name}
									</button>
								{/each}
								{#if skillPresets.length > 3}
									<button 
										type="button" 
										class="preset-pill preset-more"
										on:click={() => showAllPresets = !showAllPresets}
									>
										{showAllPresets ? 'Show Less' : `+${skillPresets.length - 3} more`}
									</button>
								{/if}
							</div>
						</div>
					{/if}

					<label for="task">Or describe what you need in your own words</label>
					<textarea
						id="task"
						bind:value={task}
						placeholder="e.g., Write a landing page headline for a project management tool targeting engineering managers"
						rows="4"
					></textarea>
				</div>

				<!-- Advanced Options Toggle -->
				<div class="advanced-toggle-wrapper">
					<button 
						type="button" 
						class="btn-text-toggle" 
						on:click={() => showAdvanced = !showAdvanced}
					>
						<span>{showAdvanced ? '− Hide' : '+ Show'} Advanced Options</span>
						<span class="text-muted-sm">(context & content analysis)</span>
					</button>
				</div>

				{#if showAdvanced}
					<div class="advanced-options fade-in">
						<!-- Context -->
						<div class="form-section">
							<h3>3. Add Context <span class="optional">(optional)</span></h3>
							<p class="text-secondary mb-2">Details about your product or audience improve output quality.</p>

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
							<label for="content">For audits and editing, paste existing content here</label>
							<textarea
								id="content"
								bind:value={content}
								placeholder="Paste landing page HTML, existing copy, or other content to analyze..."
								rows="6"
							></textarea>
						</div>
					</div>
				{/if}

				<!-- Submit -->
				<div class="form-actions">
					<button type="submit" class="btn-primary btn-lg" disabled={!isReadyToExecute || loading}>
						{#if loading}
							<span class="spinner"></span>
							Generating {selectedSkill}...
						{:else}
							{task.trim() ? `Generate ${selectedSkill} →` : 'Enter a Task to Continue'}
						{/if}
					</button>
				</div>
			</form>
		</div>

		<!-- Results Panel -->
		<div class="panel results-panel">
			<div class="results-header">
				<h3>Results</h3>
				<div class="results-actions">
					{#if result}
						<button class="btn-secondary btn-sm" on:click={copyOutput} title="Copy output">
							Copy
						</button>
						<button class="btn-secondary btn-sm" on:click={clearResults}>
							Clear
						</button>
					{/if}
				</div>
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
					<div class="empty-icon">✨</div>
					<h4>Ready to Execute</h4>
					<p>Your results will appear here in 10-30 seconds.</p>
					
					<div class="empty-benefits">
						<div class="benefit-item">
							<span class="benefit-icon">⚡</span>
							<span>Instant expert-level output</span>
						</div>
						<div class="benefit-item">
							<span class="benefit-icon">🎯</span>
							<span>Structured & actionable</span>
						</div>
						<div class="benefit-item">
							<span class="benefit-icon">🔄</span>
							<span>Iterate until perfect</span>
						</div>
					</div>

					{#if skillPresets.length > 0}
						<div class="empty-cta">
							<p class="text-muted text-sm">First time? Try an example →</p>
						</div>
					{/if}
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

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.section-header h3 {
		margin: 0;
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

	/* Presets */
	.presets-list {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: 0.75rem;
		margin-bottom: 1rem;
		padding: 1rem;
		background: var(--color-bg-tertiary);
		border-radius: var(--radius);
		border: 1px solid var(--color-border);
	}

	.preset-card {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		text-align: left;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		padding: 0.75rem;
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.preset-card:hover {
		border-color: var(--color-accent);
		background: rgba(59, 130, 246, 0.05);
	}

	.preset-name {
		font-weight: 500;
		font-size: 0.875rem;
		color: var(--color-text);
		margin-bottom: 0.25rem;
	}

	.preset-desc {
		font-size: 0.75rem;
		color: var(--color-text-muted);
		line-height: 1.4;
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

	.results-actions {
		display: flex;
		gap: 0.5rem;
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

	/* NEW STYLES FROM AUDIT */
	.value-prop {
		font-size: 1.125rem;
		color: var(--color-text-secondary);
		max-width: 600px;
		margin-bottom: 1.5rem;
	}

	.trust-indicators {
		display: flex;
		gap: 2rem;
		margin-top: 1.5rem;
		flex-wrap: wrap;
	}

	.stat {
		font-size: 0.8125rem;
		color: var(--color-text-muted);
		line-height: 1.4;
	}

	.stat strong {
		color: var(--color-accent);
		font-size: 1.25rem;
		display: block;
		margin-bottom: 0.25rem;
	}

	.progress-steps {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 2.5rem;
		padding: 1.25rem;
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
	}

	.step {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		opacity: 0.3;
		transition: all 0.3s ease;
	}

	.step.complete {
		opacity: 1;
	}

	.step-number {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		background: var(--color-bg-tertiary);
		border: 2px solid var(--color-border);
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 600;
		font-size: 0.875rem;
		transition: all 0.3s ease;
	}

	.step.complete .step-number {
		background: var(--color-accent);
		border-color: var(--color-accent);
		color: white;
		box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
	}

	.step-label {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-text-muted);
	}

	.step-line {
		flex: 0 0 60px;
		height: 2px;
		background: var(--color-border);
		margin: 0 1rem;
		margin-bottom: 1.25rem;
		transition: background 0.3s ease;
	}

	@media (max-width: 640px) {
		.step-line {
			flex: 0 0 30px;
		}
	}

	.step-line.complete {
		background: var(--color-accent);
	}

	.quick-start {
		background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
		border: 1px solid var(--color-border);
		border-radius: var(--radius);
		padding: 1rem;
		margin-bottom: 1.25rem;
	}

	.quick-start-label {
		display: block;
		font-size: 0.8125rem;
		font-weight: 600;
		margin-bottom: 0.75rem;
		color: var(--color-text);
		cursor: pointer;
	}

	.presets-list-compact {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.preset-pill {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		padding: 0.4rem 0.8rem;
		font-size: 0.8125rem;
		border-radius: 20px;
		white-space: nowrap;
		transition: all 0.15s ease;
		color: var(--color-text-secondary);
	}

	.preset-pill:hover {
		border-color: var(--color-accent);
		background: rgba(59, 130, 246, 0.1);
		color: var(--color-text);
		transform: translateY(-1px);
	}

	.preset-more {
		background: var(--color-bg-tertiary);
		color: var(--color-text-muted);
	}

	.advanced-toggle-wrapper {
		margin: 1.5rem 0;
		display: flex;
		justify-content: center;
	}

	.btn-text-toggle {
		background: none;
		border: none;
		color: var(--color-accent);
		padding: 0.5rem 1rem;
		font-size: 0.875rem;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.25rem;
		transition: all 0.2s ease;
	}

	.btn-text-toggle:hover {
		color: var(--color-accent-hover);
		background: rgba(59, 130, 246, 0.05);
		border-radius: var(--radius);
	}

	.text-muted-sm {
		font-size: 0.75rem;
		color: var(--color-text-muted);
	}

	.advanced-options {
		border-top: 1px dashed var(--color-border);
		margin-top: 0.5rem;
		padding-top: 1.5rem;
	}

	/* Enhanced Empty State */
	.empty-state {
		text-align: center;
		padding: 4rem 1.5rem;
	}

	.empty-icon {
		font-size: 3.5rem;
		margin-bottom: 1.5rem;
		filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.2));
	}

	.empty-state h4 {
		margin-bottom: 0.75rem;
		color: var(--color-text);
		font-size: 1.25rem;
	}

	.empty-benefits {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin: 2rem auto;
		padding: 1.5rem;
		background: var(--color-bg-tertiary);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		max-width: 320px;
		text-align: left;
	}

	.benefit-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		font-size: 0.9375rem;
		color: var(--color-text-secondary);
	}

	.benefit-icon {
		font-size: 1.25rem;
		flex-shrink: 0;
	}

	.empty-cta {
		margin-top: 2rem;
		padding-top: 2rem;
		border-top: 1px solid var(--color-border);
	}

	.text-sm {
		font-size: 0.875rem;
	}
</style>
