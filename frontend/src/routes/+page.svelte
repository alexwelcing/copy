<script lang="ts">
	import { executeWork, SKILL_CATEGORIES, type WorkResult, ApiError } from '$lib/api';
	import { getPresetsForSkill, type Preset } from '$lib/presets';
    import { onMount } from 'svelte';

	// Toggle State for Dogfooding demonstration
	let showOptimized = false;

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
	let showPresets = false;
	let showAdvanced = false;
	let showAllPresets = false;

	$: currentStep = task.trim() ? 2 : 1;
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

	function clearResults() {
		result = null;
		error = null;
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
	<title>{showOptimized ? 'Marketing Skills, Automated | Agency AI' : 'AI Marketing Agency'}</title>
</svelte:head>

<!-- Global Mode Toggle -->
<div class="mode-toggle-wrapper container">
    <div class="mode-toggle glass">
        <button class:active={!showOptimized} on:click={() => showOptimized = false}>Original View</button>
        <div class="toggle-divider"></div>
        <button class:active={showOptimized} on:click={() => showOptimized = true}>✨ Optimized View</button>
    </div>
</div>

{#if !showOptimized}
    <!-- ORIGINAL HOMEPAGE -->
    <div class="container fade-in">
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

        <div class="progress-steps glass">
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
            <div class="panel glass">
                <form on:submit|preventDefault={handleSubmit}>
                    <!-- Skill Selection -->
                    <div class="form-section">
                        <h3>1. Choose Skill</h3>
                        <div class="skill-selector">
                            <div class="category-tabs">
                                {#each Object.entries(SKILL_CATEGORIES) as [key, cat]}
                                    <button type="button" class="category-tab" class:active={selectedCategory === key} on:click={() => selectedCategory = key}>{cat.label}</button>
                                {/each}
                            </div>
                            <div class="skill-grid">
                                {#each Object.entries(categorySkills) as [skillKey, description]}
                                    <button type="button" class="skill-card" class:active={selectedSkill === skillKey} on:click={() => selectedSkill = skillKey}>
                                        <span class="skill-name">{skillKey}</span>
                                        <span class="skill-desc">{description}</span>
                                    </button>
                                {/each}
                            </div>
                        </div>
                    </div>

                    <!-- Model Selection -->
                    <div class="form-section">
                        <h3>2. Select Intelligence</h3>
                        <div class="model-selector">
                            <label class="model-card" class:active={selectedModel.includes('sonnet')}>
                                <input type="radio" name="model" value="claude-sonnet-4-5-20250929" bind:group={selectedModel}>
                                <div class="model-info">
                                    <span class="model-name">Power (Claude 3.5)</span>
                                    <span class="model-desc">Best for complex audits and strategy</span>
                                </div>
                            </label>
                            <label class="model-card" class:active={selectedModel.includes('MiniMax')}>
                                <input type="radio" name="model" value="MiniMax-M2.1" bind:group={selectedModel}>
                                <div class="model-info">
                                    <span class="model-name">Speed (MiniMax M2.1)</span>
                                    <span class="model-desc">Ultra-fast execution for copy and video scripts</span>
                                </div>
                            </label>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>3. Describe Task</h3>
                        {#if skillPresets.length > 0}
                            <div class="quick-start">
                                <label class="quick-start-label" for="task">⚡ Quick Start</label>
                                <div class="presets-list-compact">
                                    {#each (showAllPresets ? skillPresets : skillPresets.slice(0, 3)) as preset}
                                        <button type="button" class="preset-pill" on:click={() => loadPreset(preset)}>{preset.name}</button>
                                    {/each}
                                </div>
                            </div>
                        {/if}
                        <textarea id="task" bind:value={task} placeholder="Describe what you need..." rows="4"></textarea>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn-primary" disabled={!isReadyToExecute || loading}>
                            {#if loading}<span class="spinner"></span> Generating...{:else}Execute Skill →{/if}
                        </button>
                    </div>
                </form>
            </div>

            <!-- Results Panel -->
            <div class="panel glass">
                <div class="results-header"><h3>Results</h3></div>
                {#if result}
                    <div class="result-content">
                        <div class="output-content">{@html formatOutput(result.output)}</div>
                    </div>
                {:else}
                    <div class="empty-state">
                        <div class="empty-icon">✨</div>
                        <p>Results appear here in seconds.</p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{:else}
    <!-- OPTIMIZED HOMEPAGE (Based on CRO Audit & Programmatic Strategy) -->
    <div class="optimized-home fade-in">
        <!-- Hero Section -->
        <section class="hero">
            <div class="container">
                <div class="hero-grid">
                    <div class="hero-content">
                        <div class="badge neon-badge">LAUNCHING SOON</div>
                        <h1>Marketing Skills, <span class="text-indigo">Automated.</span></h1>
                        <p class="hero-sub">
                            Execute expert marketing strategies in seconds, not hours. Access 25+ specialized skills through an intuitive UI or integrate via API.
                        </p>
                        <div class="hero-actions">
                            <button class="btn-primary btn-xl" on:click={() => showOptimized = false}>Try the Interface ↓</button>
                            <button class="btn-secondary btn-xl">View API Docs</button>
                        </div>
                        <div class="hero-trust">
                            <div class="trust-avatars">
                                <div class="avatar"></div><div class="avatar"></div><div class="avatar"></div>
                            </div>
                            <span>Joined by 500+ Early Access Marketers</span>
                        </div>
                    </div>
                    <div class="hero-visual">
                        <div class="visual-card glass">
                            <div class="card-header">
                                <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                                <div class="card-title">remotion-script.v1</div>
                            </div>
                            <div class="card-body">
                                <div class="code-line"><code>const</code> script = AI.generate(&#123;</div>
                                <div class="code-line indent">skill: <span class="text-mint">'remotion-script'</span>,</div>
                                <div class="code-line indent">target: <span class="text-mint">'SaaS Founders'</span></div>
                                <div class="code-line">&#125;);</div>
                                <div class="progress-pulse"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Use Cases / Skills Section -->
        <section class="skills-showcase">
            <div class="container">
                <div class="section-header-centered">
                    <h2>Expert Frameworks, <span class="text-mint">Instant Execution.</span></h2>
                    <p>Stop searching for frameworks. Our AI is pre-trained on agency-grade methodologies.</p>
                </div>
                
                <div class="skills-grid-optimized">
                    <div class="skill-box glass">
                        <div class="icon">🔍</div>
                        <h3>SEO & Content</h3>
                        <ul>
                            <li>SEO Audits</li>
                            <li>Programmatic SEO</li>
                            <li>Schema Markup</li>
                        </ul>
                    </div>
                    <div class="skill-box glass">
                        <div class="icon">📈</div>
                        <h3>CRO & Growth</h3>
                        <ul>
                            <li>Landing Page Audits</li>
                            <li>Form Optimization</li>
                            <li>Pricing Strategy</li>
                        </ul>
                    </div>
                    <div class="skill-box glass">
                        <div class="icon">🎬</div>
                        <h3>Programmatic Video</h3>
                        <ul>
                            <li>Remotion Scripting</li>
                            <li>Visual Layouts</li>
                            <li>Automated Ads</li>
                        </ul>
                    </div>
                    <div class="skill-box glass">
                        <div class="icon">✍️</div>
                        <h3>Copy & Strategy</h3>
                        <ul>
                            <li>Email Sequences</li>
                            <li>Competitor Analysis</li>
                            <li>Market Positioning</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- Pricing Section (CRO Recommended) -->
        <section class="pricing-optimized">
            <div class="container">
                <div class="pricing-grid">
                    <div class="price-card glass">
                        <div class="price-header">
                            <h4>Starter</h4>
                            <div class="price">$49<span>/mo</span></div>
                        </div>
                        <ul class="price-features">
                            <li>50 skill executions</li>
                            <li>All 25+ skills</li>
                            <li>UI Access</li>
                        </ul>
                        <button class="btn-secondary">Start 14-Day Trial</button>
                    </div>
                    <div class="price-card glass featured">
                        <div class="featured-badge">MOST POPULAR</div>
                        <div class="price-header">
                            <h4>Professional</h4>
                            <div class="price">$199<span>/mo</span></div>
                        </div>
                        <ul class="price-features">
                            <li>250 skill executions</li>
                            <li>UI + API Access</li>
                            <li>Priority Support</li>
                        </ul>
                        <button class="btn-primary">Get Early Access</button>
                    </div>
                </div>
            </div>
        </section>
    </div>
{/if}

<style>
    /* Mode Toggle */
    .mode-toggle-wrapper {
        display: flex;
        justify-content: center;
        margin: 2rem auto;
    }

    .mode-toggle {
        display: flex;
        padding: 0.25rem;
        border-radius: 40px;
        background: rgba(15, 23, 42, 0.8);
    }

    .mode-toggle button {
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-size: 0.875rem;
        background: transparent;
        color: var(--color-text-secondary);
        transition: all 0.3s ease;
    }

    .mode-toggle button.active {
        background: var(--color-indigo);
        color: white;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }

    .toggle-divider {
        width: 1px;
        background: var(--color-border);
        margin: 0.5rem 0.25rem;
    }

    /* Original View Styles */
    .page-header { margin-bottom: 3rem; text-align: center; }
    .page-header h1 { font-size: 3rem; margin-bottom: 1rem; }
    .value-prop { font-size: 1.25rem; max-width: 800px; margin: 0 auto 2rem; }
    .trust-indicators { justify-content: center; }
    
    .layout { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
    .panel { min-height: 600px; border-radius: var(--radius-xl); padding: 2rem; }
    
    /* Optimized View Styles */
    .optimized-home {
        padding-bottom: 5rem;
    }

    .hero {
        padding: 4rem 0 6rem;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 4rem;
        align-items: center;
    }

    .hero-content h1 {
        font-size: 4.5rem;
        margin: 1.5rem 0;
        line-height: 1;
    }

    .text-indigo { color: var(--color-indigo); }
    .text-mint { color: var(--color-mint); }

    .hero-sub {
        font-size: 1.25rem;
        margin-bottom: 2.5rem;
        max-width: 540px;
    }

    .hero-actions {
        display: flex;
        gap: 1rem;
        margin-bottom: 3rem;
    }

    .btn-xl {
        padding: 1rem 2rem;
        font-size: 1.125rem;
    }

    .neon-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        background: rgba(16, 185, 129, 0.1);
        color: var(--color-mint);
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        border: 1px solid var(--color-mint);
    }

    .hero-trust {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-size: 0.875rem;
        color: var(--color-text-muted);
    }

    .trust-avatars {
        display: flex;
    }

    .avatar { width: 32px; height: 32px; border-radius: 50%; background: #334155; border: 2px solid var(--color-bg); margin-left: -8px; }
    .avatar:first-child { margin-left: 0; }

    .visual-card {
        border-radius: var(--radius-xl);
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    .card-header {
        padding: 1rem;
        background: rgba(255,255,255,0.03);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid var(--color-border);
    }

    .dot { width: 10px; height: 10px; border-radius: 50%; background: #334155; }
    .card-title { font-family: var(--font-mono); font-size: 0.75rem; margin-left: 0.5rem; color: var(--color-text-muted); }

    .card-body {
        padding: 2rem;
        font-family: var(--font-mono);
        font-size: 1rem;
    }

    .indent { padding-left: 1.5rem; }

    .progress-pulse {
        height: 4px;
        background: var(--color-indigo);
        width: 60%;
        margin-top: 2rem;
        border-radius: 2px;
        box-shadow: 0 0 15px var(--color-indigo);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.5; width: 10%; }
        50% { opacity: 1; width: 80%; }
        100% { opacity: 0.5; width: 10%; }
    }

    .skills-showcase {
        padding: 6rem 0;
        background: rgba(0,0,0,0.2);
    }

    .section-header-centered {
        text-align: center;
        margin-bottom: 4rem;
    }

    .section-header-centered h2 {
        margin-bottom: 1rem;
    }

    .skills-grid-optimized {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
    }

    .skill-box {
        padding: 2rem;
        border-radius: var(--radius-lg);
        transition: transform 0.3s ease;
    }

    .skill-box:hover {
        transform: translateY(-5px);
        border-color: var(--color-indigo);
    }

    .skill-box .icon { font-size: 2rem; margin-bottom: 1.5rem; }
    .skill-box h3 { font-size: 1.25rem; margin-bottom: 1rem; }
    .skill-box ul { list-style: none; padding: 0; }
    .skill-box li { color: var(--color-text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem; }

    .pricing-optimized { padding: 6rem 0; }
    .pricing-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; max-width: 800px; margin: 0 auto; }
    
    .price-card { padding: 3rem; border-radius: var(--radius-xl); text-align: center; position: relative; }
    .price-card.featured { border: 2px solid var(--color-indigo); transform: scale(1.05); }
    
    .featured-badge {
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--color-indigo);
        color: white;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .price-header h4 { margin-bottom: 1rem; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.1em; }
    .price { font-size: 3rem; font-weight: 800; margin-bottom: 2rem; }
    .price span { font-size: 1rem; color: var(--color-text-muted); font-weight: 400; }
    
    .price-features { list-style: none; padding: 0; margin-bottom: 2.5rem; text-align: left; }
    .price-features li { margin-bottom: 1rem; color: var(--color-text-secondary); display: flex; align-items: center; gap: 0.5rem; }
    .price-features li::before { content: '✓'; color: var(--color-mint); font-weight: 700; }

    /* Reuse existing component styles */
    .form-section { margin-bottom: 1.5rem; }
    .category-tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; }
    .category-tab { background: rgba(255,255,255,0.05); border: 1px solid var(--color-border); padding: 0.5rem 1rem; font-size: 0.8rem; border-radius: 4px; }
    .category-tab.active { background: var(--color-indigo); color: white; border-color: var(--color-indigo); }
    
    .skill-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }
    .skill-card { background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); padding: 1rem; text-align: left; border-radius: 8px; }
    .skill-card.active { border-color: var(--color-indigo); background: rgba(79, 70, 229, 0.1); }
    .skill-name { display: block; font-weight: 600; margin-bottom: 0.25rem; }
    .skill-desc { font-size: 0.75rem; color: var(--color-text-muted); }

    .model-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .model-card { border: 1px solid var(--color-border); padding: 1rem; border-radius: 8px; display: flex; gap: 1rem; cursor: pointer; }
    .model-card.active { border-color: var(--color-indigo); background: rgba(79, 70, 229, 0.05); }
    .model-name { font-weight: 600; display: block; }
    .model-desc { font-size: 0.75rem; color: var(--color-text-muted); }

    textarea { width: 100%; background: rgba(0,0,0,0.2); border: 1px solid var(--color-border); border-radius: 8px; padding: 1rem; color: white; }
    .form-actions { margin-top: 1.5rem; }
    .form-actions button { width: 100%; padding: 1rem; font-size: 1rem; }

    @media (max-width: 1024px) {
        .hero-grid { grid-template-columns: 1fr; text-align: center; }
        .hero-content h1 { font-size: 3rem; }
        .hero-sub { margin: 0 auto 2rem; }
        .hero-actions { justify-content: center; }
        .hero-trust { justify-content: center; }
        .skills-grid-optimized { grid-template-columns: 1fr 1fr; }
        .pricing-grid { grid-template-columns: 1fr; }
    }
</style>