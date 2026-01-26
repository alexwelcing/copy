<script lang="ts">
	import { executeWork, SKILL_CATEGORIES, type WorkResult, ApiError } from '$lib/api';
	import { getPresetsForSkill, type Preset } from '$lib/presets';
    import { onMount } from 'svelte';

	let heroImageUrl = 'https://storage.googleapis.com/marketing-copy-assets/images/generated_c46bed9c-bf11-44f3-8aba-6dcf6d121b8e.png';

	// Form state
	let selectedCategory = 'writing';
	let selectedSkill = 'copywriting';
	let selectedModel = 'claude-sonnet-4-5-20250929';
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
	$: isReadyToExecute = selectedSkill && task.trim();
	$: skillPresets = getPresetsForSkill(selectedSkill);
	$: categorySkills = SKILL_CATEGORIES[selectedCategory as keyof typeof SKILL_CATEGORIES]?.skills || {};

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
		if (preset.context) {
			contextFields = Object.entries(preset.context).map(([key, value]) => ({ key, value }));
		} else {
			contextFields = [
				{ key: 'product', value: '' },
				{ key: 'audience', value: '' }
			];
		}
	}

	async function handleSubmit() {
		if (!task.trim()) {
			error = 'Please enter a task';
			return;
		}

		loading = true;
		error = null;
		result = null;

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
				content: content.trim() || undefined,
				model: selectedModel
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

	function copyOutput() {
		if (result?.output) {
			navigator.clipboard.writeText(result.output);
		}
	}

    function formatOutput(text: string): string {
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

<svelte:head>
	<title>Strategic Marketing Automation | HIGH ERA</title>
</svelte:head>

<div class="optimized-home fade-in">
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-grid">
                <div class="hero-content">
                    <div class="badge-classic">ESTABLISHED 2026</div>
                    <h1>The <span class="text-italic">Human</span> Side of Automation.</h1>
                    <p class="hero-sub">
                        Expert marketing strategies executed with mid-century precision. 25+ specialized skills built on the timeless frameworks of Madison Avenue.
                    </p>
                    <div class="hero-actions">
                        <a href="#terminal" class="btn-primary btn-hero-terminal">Open Briefing Terminal</a>
                        <button class="btn-secondary">Request API Credentials</button>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="frame-classic">
                        {#if heroImageUrl}
                            <img src={heroImageUrl} alt="High Era Marketing Realism" class="hero-image-styled" />
                        {:else}
                            <div class="placeholder-classic">
                                <span>Developing Cinematic Asset...</span>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Briefing Terminal (The Tool) -->
    <section id="terminal" class="terminal-section">
        <div class="container">
            <div class="terminal-grid">
                <!-- Left: Input Brief -->
                <div class="brief-panel paper-card">
                    <div class="brief-header">
                        <span class="form-id">FORM 22-B: STRATEGIC BRIEF</span>
                        <h2>Define the Objective</h2>
                    </div>
                    
                    <form on:submit|preventDefault={handleSubmit} class="brief-form">
                        <!-- Skill Selection -->
                        <div class="brief-section">
                            <label class="brief-label">1. DEPARTMENT & SPECIALIZATION</label>
                            <div class="brief-selectors">
                                <select bind:value={selectedCategory} class="classic-select">
                                    {#each Object.entries(SKILL_CATEGORIES) as [key, cat]}
                                        <option value={key}>{cat.label}</option>
                                    {/each}
                                </select>
                                <select bind:value={selectedSkill} class="classic-select">
                                    {#each Object.entries(categorySkills) as [skillKey, _]}
                                        <option value={skillKey}>{skillKey.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>

                        <!-- Task Input -->
                        <div class="brief-section">
                            <label class="brief-label" for="opt-task">2. PROJECT DESCRIPTION</label>
                            {#if skillPresets.length > 0}
                                <div class="brief-presets">
                                    {#each skillPresets.slice(0, 3) as preset}
                                        <button type="button" class="preset-pill-classic" on:click={() => loadPreset(preset)}>{preset.name}</button>
                                    {/each}
                                </div>
                            {/if}
                            <textarea 
                                id="opt-task" 
                                bind:value={task} 
                                placeholder="Type your strategic requirements here..." 
                                rows="6"
                                class="typewriter-textarea"
                            ></textarea>
                        </div>

                        <!-- Context Fields -->
                        <div class="brief-section">
                            <div class="flex justify-between items-center mb-2">
                                <label class="brief-label">3. KEY CONTEXT</label>
                                <button type="button" class="text-btn" on:click={addContextField}>+ Add Field</button>
                            </div>
                            <div class="context-stack">
                                {#each contextFields as field, i}
                                    <div class="context-row">
                                        <input type="text" bind:value={field.key} placeholder="Key" class="context-input key" />
                                        <input type="text" bind:value={field.value} placeholder="Value" class="context-input" />
                                        <button type="button" class="remove-btn" on:click={() => removeContextField(i)}>&times;</button>
                                    </div>
                                {/each}
                            </div>
                        </div>

                        <div class="brief-actions">
                            <button type="submit" class="btn-primary w-full" disabled={!isReadyToExecute || loading}>
                                {#if loading}
                                    <span class="spinner"></span> TRANSMITTING...
                                {:else}
                                    EXECUTE STRATEGY →
                                {/if}
                            </button>
                        </div>
                    </form>
                </div>

                                    <!-- Right: Output Memo -->
                                    <div class="memo-panel paper-card">
                                        <div class="memo-header">
                                            <div class="agency-seal">HIGH ERA</div>
                                            <div class="memo-meta">
                                                <span>TO: PROJECT MANAGER</span>
                                                <span>RE: {selectedSkill.toUpperCase()} OUTPUT</span>
                                                <span>DATE: {new Date().toLocaleDateString()}</span>
                                            </div>
                                        </div>
                    <div class="memo-content">
                        {#if result}
                            <div class="memo-body typewriter">
                                {@html formatOutput(result.output)}
                            </div>
                            <div class="memo-footer">
                                <button class="btn-secondary btn-sm" on:click={copyOutput}>Copy to Clipboard</button>
                                <span class="serial">SN: {result.id.slice(0,8)}</span>
                            </div>
                        {:else if loading}
                            <div class="memo-loading">
                                <div class="typewriter-cursor"></div>
                                <p>Processing strategy... Intelligence is being applied.</p>
                            </div>
                        {:else}
                            <div class="memo-empty">
                                <div class="watermark">DRAFT</div>
                                <p>Awaiting briefing input...</p>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- The Value Section -->
    <section class="philosophy">
        <div class="container">
            <div class="philosophy-grid">
                <div class="phil-item">
                    <h3>Tactile Precision</h3>
                    <p>We believe in the weight of words. Our AI doesn't just predict; it constructs using the same strategic rigor as the legends of advertising.</p>
                </div>
                <div class="phil-item">
                    <h3>Human Realism</h3>
                    <p>No neon. No cliches. Just high-fidelity execution that respects the intelligence of your audience and the humanity of your brand.</p>
                </div>
            </div>
        </div>
    </section>
</div>

<style>
    /* Page Specific Layout */
    .optimized-home { padding-bottom: 8rem; background: var(--color-bg); }
    .hero { padding: 6rem 0; }
    .hero-grid { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 5rem; align-items: center; }
    .hero-content h1 { font-size: 5rem; margin-bottom: 2rem; color: var(--color-navy); }
    .hero-sub { font-size: 1.25rem; margin-bottom: 3rem; line-height: 1.8; color: var(--color-smoke); }
    .hero-actions { display: flex; gap: 1.5rem; }
    .btn-hero-terminal { padding: 1.25rem 3rem; font-size: 0.85rem; border-width: 2px; }
    .hero-image-styled { width: 100%; display: block; filter: sepia(0.1) contrast(1.1); }

    .terminal-section { padding: 4rem 0; border-top: 1px solid var(--color-border); scroll-margin-top: 100px; }
    .terminal-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: start; }
    
    .brief-header, .memo-header { border-bottom: 2px solid var(--color-navy); margin-bottom: 2rem; padding-bottom: 1.5rem; }
    .form-id { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-smoke); display: block; margin-bottom: 0.5rem; }
    .brief-section { margin-bottom: 2.5rem; }
    .brief-selectors { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }

    .brief-presets { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
    .preset-pill-classic {
        background: transparent; border: 1px solid var(--color-border);
        padding: 0.4rem 0.8rem; font-size: 0.65rem; color: var(--color-smoke);
        text-transform: none; letter-spacing: 0; cursor: pointer;
    }
    .preset-pill-classic:hover { background: var(--color-navy); color: white; }

    .context-stack { display: flex; flex-direction: column; gap: 0.5rem; }
    .context-row { display: flex; gap: 0.5rem; align-items: center; }
    .context-input { flex: 1; padding: 0.5rem; border: 1px solid var(--color-border); font-size: 0.8rem; font-family: var(--font-mono); }
    .context-input.key { flex: 0 0 100px; background: #f8f8f8; }
    .remove-btn { background: none; border: none; font-size: 1.2rem; color: var(--color-smoke); cursor: pointer; padding: 0 0.5rem; }
    .text-btn { background: none; border: none; color: var(--color-brass); font-family: var(--font-mono); font-size: 0.7rem; cursor: pointer; text-transform: uppercase; }

    /* Memo Specifics */
    .memo-meta { display: flex; flex-direction: column; gap: 0.25rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--color-navy); }
    .agency-seal { position: absolute; top: 3rem; right: 3rem; font-family: var(--font-serif); font-weight: 900; opacity: 0.1; font-size: 1.5rem; transform: rotate(-15deg); border: 2px solid currentColor; padding: 0.5rem; }
    .memo-body :global(p) { margin-bottom: 1.5rem; }
    .memo-body :global(h5), .memo-body :global(h4), .memo-body :global(h3) { font-family: var(--font-serif); margin: 2rem 0 1rem; color: var(--color-navy); }
    
    .memo-footer { border-top: 1px solid var(--color-border); margin-top: 3rem; padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; }
    .serial { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-text-muted); }
    .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg); font-family: var(--font-serif); font-size: 8rem; font-weight: 900; color: rgba(0,0,0,0.03); pointer-events: none; }
    .memo-empty { height: 400px; display: flex; align-items: center; justify-content: center; color: var(--color-text-muted); }
    .memo-loading { height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1rem; color: var(--color-smoke); font-family: var(--font-mono); font-size: 0.8rem; }

    .typewriter-cursor { width: 10px; height: 1.2em; background: var(--color-brass); display: inline-block; animation: blink 1s infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    .philosophy { border-top: 1px solid var(--color-border); padding: 6rem 0; }
    .philosophy-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; }
    .phil-item h3 { margin-bottom: 1rem; font-family: var(--font-serif); }

    @media (max-width: 1024px) {
        .hero-grid, .terminal-grid { grid-template-columns: 1fr; }
        .hero-content h1 { font-size: 3.5rem; }
        .philosophy-grid { grid-template-columns: 1fr; }
        .paper-card { padding: 2rem; min-height: auto; }
    }
</style>