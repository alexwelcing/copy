<script lang="ts">
	import { executeWork, SKILL_CATEGORIES, type WorkResult, ApiError, saveBrief, listBriefs, type Brief } from '$lib/api';
	import { getPresetsForSkill, type Preset } from '$lib/presets';
    import MadLib from '$lib/components/MadLib.svelte';
    import ErrorBoundary from '$lib/components/ErrorBoundary.svelte';
    import LoadingSkeleton from '$lib/components/LoadingSkeleton.svelte';
    import { toasts } from '$lib/stores/toast';
    import { onMount } from 'svelte';
    import { fade, slide } from 'svelte/transition';

    // ASSET MAP (Neo-Madison Collection)
    const SKILL_IMAGES: Record<string, string> = {
        'copywriting': 'https://storage.googleapis.com/marketing-copy-assets/images/generated_68947224-4217-4070-b3be-c011f0f45085.png',
        'page-cro': 'https://storage.googleapis.com/marketing-copy-assets/images/generated_e21500bf-66a2-40cf-a3ab-081068a5486c.png',
        'marketing-ideas': 'https://storage.googleapis.com/marketing-copy-assets/images/generated_28c3106a-835a-4f55-960f-ed828a2e7113.png',
        'remotion-script': 'https://storage.googleapis.com/marketing-copy-assets/images/generated_95fee53a-08cd-4ad6-a597-2a685a93a747.png',
        'default': 'https://storage.googleapis.com/marketing-copy-assets/images/generated_c46bed9c-bf11-44f3-8aba-6dcf6d121b8e.png'
    };

	// Form state
	let selectedCategory = 'writing';
	let selectedSkill = 'copywriting';
	let selectedModel = 'claude-sonnet-4-5-20250929';
	let task = '';
	let content = '';
    
    // Reactive Hero Image
    $: heroImageUrl = SKILL_IMAGES[selectedSkill] || SKILL_IMAGES['default'];
    
    // MadLib state
    let product = '';
    let audience = '';
    let coreValue = '';
    
    // Persistence state
    let savedBriefs: Brief[] = [];
    let currentBriefId: string | undefined = undefined;
    let isSaving = false;
    let showDossier = false;
    let briefsLoading = true;
    let briefsError: string | null = null;

	let contextFields: { key: string; value: string }[] = [];

	// Execution state
	let loading = false;
	let error: string | null = null;
	let result: WorkResult | null = null;

	// UI State
	$: isReadyToExecute = selectedSkill && task.trim() && product.trim() && audience.trim();
	$: skillPresets = getPresetsForSkill(selectedSkill);
	$: categorySkills = SKILL_CATEGORIES[selectedCategory as keyof typeof SKILL_CATEGORIES]?.skills || {};

    // Ghost Writer Logic
    $: ghostTitle = task ? (task.length > 30 ? task.slice(0, 30) + '...' : task) : 'UNNAMED STRATEGY';
    $: ghostContext = product || audience ? `FOR ${product.toUpperCase()} targeting ${audience.toUpperCase()}` : 'AWAITING CONTEXT';

    async function loadBriefs() {
        briefsLoading = true;
        briefsError = null;
        try {
            const res = await listBriefs();
            savedBriefs = res.briefs;
        } catch (e) {
            console.error("Failed to load briefs", e);
            briefsError = "Failed to load saved briefs";
        } finally {
            briefsLoading = false;
        }
    }

    onMount(() => {
        loadBriefs();
    });

	$: {
		const skills = Object.keys(categorySkills);
		if (skills.length > 0 && !skills.includes(selectedSkill)) {
			selectedSkill = skills[0];
		}
	}

    async function handleSave() {
        if (!product || !audience || !task) return;
        
        isSaving = true;
        try {
            const context: Record<string, string> = {};
            for (const field of contextFields) {
                if (field.key.trim() && field.value.trim()) {
                    context[field.key.trim()] = field.value.trim();
                }
            }

            const brief: Brief = {
                id: currentBriefId,
                title: ghostTitle,
                product,
                audience,
                value: coreValue,
                description: task,
                context
            };

            const saved = await saveBrief(brief);
            currentBriefId = saved.id;
            
            // Refresh list
            const res = await listBriefs();
            savedBriefs = res.briefs;
            toasts.success('Brief saved to dossier');
        } catch (e) {
            const errorMsg = e instanceof ApiError ? e.detail : 'Failed to save to dossier';
            toasts.error(errorMsg);
            error = errorMsg;
        } finally {
            isSaving = false;
        }
    }

    function loadSavedBrief(brief: Brief) {
        currentBriefId = brief.id;
        product = brief.product;
        audience = brief.audience;
        coreValue = brief.value;
        task = brief.description || '';
        if (brief.context) {
             contextFields = Object.entries(brief.context).map(([key, value]) => ({ key, value }));
        }
        showDossier = false;
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
            product = preset.context.product || '';
            audience = preset.context.audience || '';
            coreValue = preset.context.value || '';
            
            // Filter out the main mad-lib fields from the extra context fields
			contextFields = Object.entries(preset.context)
                .filter(([key]) => !['product', 'audience', 'value'].includes(key))
                .map(([key, value]) => ({ key, value }));
		} else {
            product = '';
            audience = '';
            coreValue = '';
			contextFields = [];
		}
	}

	async function handleSubmit() {
		if (!task.trim()) {
			toasts.warning('Please enter a task description');
			error = 'Please enter a task';
			return;
		}

		loading = true;
		error = null;
		result = null;

		const context: Record<string, string> = {
            product,
            audience,
            value: coreValue
        };

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
			toasts.success('Strategy generated successfully');
		} catch (e) {
			let errorMessage: string;
			if (e instanceof ApiError) {
				// Handle specific error codes
				if (e.status === 429) {
					errorMessage = 'Daily limit reached. Sign in for more requests or try again tomorrow.';
				} else if (e.status === 503 || e.status === 502) {
					errorMessage = 'Service temporarily unavailable. Please try again in a moment.';
				} else {
					errorMessage = e.detail;
				}
			} else {
				errorMessage = 'Failed to execute skill. Is the API running?';
			}
			error = errorMessage;
			toasts.error(errorMessage);
		} finally {
			loading = false;
		}
	}

	function copyOutput() {
		if (result?.output) {
			navigator.clipboard.writeText(result.output);
			toasts.success('Copied to clipboard');
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
    <section class="hero neo-hero">
        <div class="container">
            <div class="hero-grid">
                <div class="hero-content">
                    <div class="badge-classic">ESTABLISHED 2026</div>
                    <h1>The Agency That <span class="text-italic">Remembers</span>.</h1>
                    <p class="hero-sub">
                        Your brand context, saved forever. Your strategy, executed instantly.
                        <br>The briefing infrastructure for leaders who refuse to repeat themselves.
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
                    <div class="caption-classic">
                        FIG 1. THE TWIN-ENGINE WORKFLOW
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Briefing Terminal (The Tool) -->
    <section id="terminal" class="terminal-section">
        <div class="container">
            <div class="terminal-stack">
                
                <!-- 1. The Dossier (Horizontal Reel) -->
                <div class="dossier-bar">
                    <div class="dossier-header">
                        <span class="badge-classic-small">ARCHIVES</span>
                        <button class="text-btn" on:click={() => { currentBriefId = undefined; task = ''; product = ''; audience = ''; coreValue = ''; contextFields = []; }}>+ NEW BRIEF</button>
                    </div>

                    
                    {#if savedBriefs.length === 0}
                        <div class="empty-reel">Your project library is empty.</div>
                    {:else}
                        <div class="brief-reel">
                            {#each savedBriefs.slice(0, 6) as brief}
                                <button class="brief-reel-card" class:active={currentBriefId === brief.id} on:click={() => loadSavedBrief(brief)}>
                                    <span class="reel-title">{brief.title}</span>
                                    <span class="reel-date">{new Date(brief.updated_at || '').toLocaleDateString()}</span>
                                </button>
                            {/each}
                            {#if savedBriefs.length > 6}
                                <div class="reel-more">+{savedBriefs.length - 6}</div>
                            {/if}
                        </div>
                    {/if}
                </div>

                <!-- 2. The Briefing Room (Input) -->
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

                        <!-- Context FIRST (Flip) -->
                        {#if selectedSkill}
                            <div class="brief-section" transition:slide>
                                <label class="brief-label">2. KEY CONTEXT</label>
                                <MadLib bind:product bind:audience bind:value={coreValue} />
                            </div>
                        {/if}
                            </div>
                        {/if}

                        <!-- Description SECOND -->
                        {#if product.trim() && audience.trim()}
                            <div class="brief-section" transition:slide>
                                <label class="brief-label" for="opt-task">3. PROJECT DESCRIPTION</label>
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
                                    rows="4"
                                    class="typewriter-textarea"
                                ></textarea>
                            </div>

                            <div class="brief-section" transition:slide>
                                <div class="flex justify-between items-center mb-2">
                                    <label class="brief-label">4. ADDITIONAL DATA (OPTIONAL)</label>
                                    <button type="button" class="text-btn" on:click={addContextField}>+ Add Field</button>
                                </div>
                                <div class="context-stack">
                                    {#each contextFields as field, i}
                                        <div class="context-row" transition:slide|local>
                                            <input type="text" bind:value={field.key} placeholder="Key" class="context-input key" />
                                            <input type="text" bind:value={field.value} placeholder="Value" class="context-input" />
                                            <button type="button" class="remove-btn" on:click={() => removeContextField(i)}>&times;</button>
                                        </div>
                                    {/each}
                                </div>
                            </div>
                        {/if}

                        <div class="brief-actions grid grid-cols-2 gap-4">
                            <button type="button" class="btn-secondary" on:click={handleSave} disabled={isSaving || !ghostTitle}>
                                {isSaving ? 'SAVING...' : 'SAVE DRAFT'}
                            </button>
                            <button type="submit" class="btn-primary" disabled={!isReadyToExecute || loading}>
                                {#if loading}
                                    <span class="spinner"></span> TRANSMITTING...
                                {:else}
                                    EXECUTE STRATEGY →
                                {/if}
                            </button>
                        </div>
                    </form>
                </div>

                <!-- 3. Output Memo (Result) -->
                <div class="memo-panel paper-card">
                    <div class="memo-header">
                        <div class="agency-seal">HIGH ERA</div>
                        <div class="memo-meta">
                            <div class="flex justify-between items-start">
                                <div>
                                    <span>TO: PROJECT MANAGER</span>
                                    <span>RE: {selectedSkill.toUpperCase()} OUTPUT</span>
                                    <span>DATE: {new Date().toLocaleDateString()}</span>
                                </div>
                                <div class="twin-engine-badge">
                                    <span class="pulse"></span> TWIN-ENGINE
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="memo-content">
                        {#if result}
                            <div class="memo-body typewriter" in:fade>
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
                            <div class="memo-ghost" in:fade>
                                <div class="watermark" class:active={isReadyToExecute}>
                                    {isReadyToExecute ? 'READY' : 'DRAFT'}
                                </div>
                                <div class="ghost-content">
                                    <h4 class="ghost-title">{ghostTitle}</h4>
                                    <p class="ghost-meta">{ghostContext}</p>
                                    <div class="ghost-lines">
                                        <div class="line" style="width: 100%"></div>
                                        <div class="line" style="width: 90%"></div>
                                        <div class="line" style="width: 95%"></div>
                                        <div class="line" style="width: 40%"></div>
                                    </div>
                                    {#if !isReadyToExecute}
                                        <p class="ghost-hint">Complete the briefing to generate strategy.</p>
                                    {/if}
                                </div>
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

    <!-- Asset Generation Section -->
    <section class="asset-generation">
        <div class="container">
            <div class="section-header">
                <div class="badge-classic">TURBO GENERATION</div>
                <h2>Cinematic Assets at <span class="text-italic">Speed</span></h2>
                <p class="section-intro">
                    Generate high-quality images, videos, and audio using state-of-the-art turbo models.
                    From hero images to campaign assets, all optimized for speed without sacrificing quality.
                </p>
            </div>

            <div class="turbo-models-grid">
                <div class="model-card">
                    <div class="model-icon">🎨</div>
                    <h4>FLUX Schnell</h4>
                    <p>Ultra-fast image generation (2-4s) with photorealistic quality. Perfect for hero images and OG graphics.</p>
                    <div class="model-meta">
                        <span class="speed-badge">ultra-fast</span>
                        <span class="quality-badge">high</span>
                    </div>
                </div>

                <div class="model-card">
                    <div class="model-icon">⚡</div>
                    <h4>SDXL Lightning</h4>
                    <p>Lightning-fast generation (1-2s) for rapid iteration. Ideal for social media and quick concepts.</p>
                    <div class="model-meta">
                        <span class="speed-badge">ultra-fast</span>
                        <span class="quality-badge">good</span>
                    </div>
                </div>

                <div class="model-card">
                    <div class="model-icon">🎬</div>
                    <h4>Kling Video Turbo</h4>
                    <p>High-quality video generation with turbo speed. Create engaging motion graphics and explainers.</p>
                    <div class="model-meta">
                        <span class="speed-badge">fast</span>
                        <span class="quality-badge">high</span>
                    </div>
                </div>

                <div class="model-card">
                    <div class="model-icon">✍️</div>
                    <h4>Qwen Text Specialist</h4>
                    <p>Exceptional text rendering in images. Best for logos, posters, and typography-heavy designs.</p>
                    <div class="model-meta">
                        <span class="speed-badge">fast</span>
                        <span class="quality-badge">high</span>
                        <span class="specialty-badge">text</span>
                    </div>
                </div>
            </div>

            <div class="cta-center">
                <a href="/assess" class="btn-primary">Try Asset Generation Lab →</a>
            </div>
        </div>
    </section>
</div>

<style>
    .optimized-home { padding-bottom: 8rem; background: var(--color-bg); }
    .hero { padding: 6rem 0; }
    .hero-grid { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 5rem; align-items: center; }
    .hero-content h1 { font-size: 5rem; margin-bottom: 2rem; color: var(--color-navy); }
    .hero-sub { font-size: 1.25rem; margin-bottom: 3rem; line-height: 1.8; color: var(--color-smoke); }
    .hero-actions { display: flex; gap: 1.5rem; }
    .btn-hero-terminal { padding: 1.25rem 3rem; font-size: 0.85rem; border-width: 2px; }
    .hero-image-styled { width: 100%; display: block; filter: sepia(0.1) contrast(1.1); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }

    .terminal-section { padding: 4rem 0; border-top: 1px solid var(--color-border); scroll-margin-top: 100px; }
    
    /* TERMINAL STACK LAYOUT */
    .terminal-stack { display: flex; flex-direction: column; gap: 3rem; max-width: 850px; margin: 0 auto; }
    
    /* Dossier Reel (Horizontal) */
    .dossier-bar { width: 100%; }
    .dossier-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--color-border); padding-bottom: 0.5rem; }
    .brief-reel { display: flex; gap: 1rem; overflow-x: auto; padding-bottom: 1rem; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; }
    .brief-reel::-webkit-scrollbar { height: 6px; }
    .brief-reel::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 3px; }
    
    .brief-reel-card { 
        flex: 0 0 220px; padding: 1.25rem; border: 1px solid var(--color-border); background: white; 
        text-align: left; cursor: pointer; transition: all 0.2s ease; scroll-snap-align: start;
        display: flex; flex-direction: column; justify-content: space-between; height: 100px;
    }
    .brief-reel-card:hover { border-color: var(--color-navy); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .brief-reel-card.active { border-top: 4px solid var(--color-brass); background: #fffcf5; }
    
    .reel-title { font-family: var(--font-serif); font-weight: 700; font-size: 0.85rem; color: var(--color-navy); line-height: 1.2; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .reel-date { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-text-muted); margin-top: auto; }
    .reel-more { flex: 0 0 60px; display: flex; align-items: center; justify-content: center; background: var(--color-bg-tertiary); border: 1px solid var(--color-border); font-family: var(--font-mono); color: var(--color-text-muted); cursor: pointer; }
    .empty-reel { padding: 2rem; text-align: center; color: var(--color-text-muted); font-style: italic; border: 1px dashed var(--color-border); border-radius: 4px; }

    .badge-classic-small { font-family: var(--font-sans); font-weight: 800; font-size: 0.65rem; letter-spacing: 0.15em; color: var(--color-navy); text-transform: uppercase; }

    /* Briefing Room */
    .briefing-room { width: 100%; margin-bottom: 2rem; }
    
    /* Removed old grid/sidebar styles */
    .terminal-layout, .terminal-grid-main, .dossier-sidebar { display: none; }


    .brief-header, .memo-header { border-bottom: 2px solid var(--color-navy); margin-bottom: 2rem; padding-bottom: 1.5rem; }
    .form-id { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-smoke); display: block; margin-bottom: 0.5rem; text-transform: uppercase; }
    .brief-section { margin-bottom: 3rem; } /* Increased from 2.5rem */
    .brief-selectors { display: flex; flex-wrap: wrap; gap: 1.5rem; } 
    
    .classic-select {
        flex: 1 1 auto;
        min-width: 200px;
        /* Maintain other global styles */
    }

    .brief-presets { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.5rem; }
    .preset-pill-classic {
        background: transparent; border: 1px solid var(--color-border);
        padding: 0.5rem 1rem; font-size: 0.7rem; color: var(--color-smoke); /* Increased padding */
        text-transform: none; letter-spacing: 0; cursor: pointer;
    }
    .preset-pill-classic:hover { background: var(--color-navy); color: white; }

    .context-stack { display: flex; flex-direction: column; gap: 1rem; } /* Increased gap */
    .context-row { display: flex; gap: 1rem; align-items: center; }
    .context-input { flex: 1; padding: 0.75rem; border: 1px solid var(--color-border); font-size: 0.9rem; font-family: var(--font-mono); }
    .context-input.key { flex: 0 0 120px; background: #f8f8f8; }
    .remove-btn { background: none; border: none; font-size: 1.2rem; color: var(--color-smoke); cursor: pointer; padding: 0 0.5rem; }
    .text-btn { background: none; border: none; color: var(--color-brass); font-family: var(--font-mono); font-size: 0.7rem; cursor: pointer; text-transform: uppercase; }

    /* TWIN ENGINE BADGE */
    .twin-engine-badge {
        display: flex; align-items: center; gap: 0.5rem; background: var(--color-navy);
        color: white; padding: 0.4rem 0.8rem; font-family: var(--font-mono); font-size: 0.6rem;
        letter-spacing: 0.1em; border-radius: 20px;
    }
    .pulse { width: 6px; height: 6px; background: #10b981; border-radius: 50%; animation: pulse-green 2s infinite; }
    @keyframes pulse-green { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); } 70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }

    /* Memo Specifics */
    .memo-meta { display: flex; flex-direction: column; gap: 0.25rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--color-navy); }
    .agency-seal { position: absolute; top: 3rem; right: 3rem; font-family: var(--font-serif); font-weight: 900; opacity: 0.1; font-size: 1.5rem; transform: rotate(-15deg); border: 2px solid currentColor; padding: 0.5rem; }
    .memo-body :global(p) { margin-bottom: 1.5rem; }
    .memo-body :global(h5), .memo-body :global(h4), .memo-body :global(h3) { font-family: var(--font-serif); margin: 2rem 0 1rem; color: var(--color-navy); }
    
    .memo-footer { border-top: 1px solid var(--color-border); margin-top: 3rem; padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; }
    .serial { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-text-muted); }
    .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg); font-family: var(--font-serif); font-size: 8rem; font-weight: 900; color: rgba(0,0,0,0.03); pointer-events: none; transition: color 0.5s ease; }
    .watermark.active { color: rgba(180, 83, 9, 0.05); }

    .memo-ghost { height: 400px; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; position: relative; padding: 2rem; }
    .ghost-content { width: 100%; z-index: 1; }
    .ghost-title { font-family: var(--font-serif); color: var(--color-navy); opacity: 0.4; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.1em; }
    .ghost-meta { font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-brass); opacity: 0.5; margin-bottom: 2rem; }
    .ghost-lines { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem; width: 100%; }
    .line { height: 8px; background: var(--color-border); border-radius: 4px; opacity: 0.5; }
    .ghost-hint { font-family: var(--font-mono); font-size: 0.75rem; color: var(--color-text-muted); font-style: italic; }

    .memo-loading { height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1rem; color: var(--color-smoke); font-family: var(--font-mono); font-size: 0.8rem; }

    .typewriter-cursor { width: 10px; height: 1.2em; background: var(--color-brass); display: inline-block; animation: blink 1s infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    .philosophy { border-top: 1px solid var(--color-border); padding: 6rem 0; }
    .philosophy-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; }
    .phil-item h3 { margin-bottom: 1rem; font-family: var(--font-serif); }

    /* Asset Generation Section */
    .asset-generation { background: var(--color-cream); padding: 6rem 0; border-top: 1px solid var(--color-border); }
    .section-header { text-align: center; max-width: 700px; margin: 0 auto 4rem; }
    .section-header h2 { font-size: 3rem; margin: 1rem 0; color: var(--color-navy); }
    .section-intro { font-size: 1.1rem; color: var(--color-smoke); line-height: 1.8; }
    
    .turbo-models-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 3rem; }
    
    .model-card {
        background: white; padding: 2rem; border: 1px solid var(--color-border);
        transition: all 0.3s ease;
    }
    .model-card:hover { border-color: var(--color-brass); transform: translateY(-4px); box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    
    .model-icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .model-card h4 { font-family: var(--font-mono); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-navy); margin-bottom: 0.75rem; }
    .model-card p { font-size: 0.9rem; color: var(--color-smoke); line-height: 1.6; margin-bottom: 1rem; }
    
    .model-meta { display: flex; flex-wrap: wrap; gap: 0.5rem; }
    .speed-badge, .quality-badge, .specialty-badge { 
        font-family: var(--font-mono); font-size: 0.6rem; text-transform: uppercase;
        padding: 0.2rem 0.6rem; border-radius: 2px;
    }
    .speed-badge { background: var(--color-bg-tertiary); color: var(--color-text-muted); }
    .quality-badge { background: var(--color-brass); color: white; }
    .specialty-badge { background: var(--color-navy); color: white; }
    
    .cta-center { text-align: center; margin-top: 3rem; }

    @media (max-width: 1200px) {
        .terminal-layout { grid-template-columns: 1fr; }
        .dossier-sidebar { min-height: auto; margin-bottom: 2rem; }
    }

        /* NEO-MADISON THEME */
    .neo-hero {
        background-color: var(--color-bg);
        border-bottom: 1px solid var(--color-border);
    }
    
    .neo-madison-section {
        background-color: #f8f8f8;
        border-top: 1px solid var(--color-border);
        padding: 8rem 0;
    }

    .section-header-center {
        text-align: center;
        margin-bottom: 5rem;
    }
    
    .section-header-center h2 {
        font-size: 3rem;
        color: var(--color-navy);
        margin-bottom: 1rem;
    }

    .phil-item {
        border-left: 1px solid var(--color-border);
        padding-left: 2rem;
        position: relative;
    }
    
    .phil-number {
        font-family: var(--font-mono);
        color: var(--color-brass);
        font-size: 0.8rem;
        margin-bottom: 1rem;
        letter-spacing: 0.1em;
    }

    @media (max-width: 1024px) {

            .hero-grid { grid-template-columns: 1fr; }

            .terminal-grid-main { grid-template-columns: 1fr; }

            .hero-content h1 { font-size: 3.5rem; }

            .philosophy-grid { grid-template-columns: 1fr; }

            .paper-card { padding: 2rem; min-height: auto; }

            .brief-selectors { grid-template-columns: 1fr; } /* Stack selectors on mobile */

        }

    </style>