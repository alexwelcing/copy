<script lang="ts">
	import { executeWork, SKILL_CATEGORIES, type WorkResult, ApiError, saveBrief, listBriefs, type Brief } from '$lib/api';
	import { getPresetsForSkill, type Preset } from '$lib/presets';
    import MadLib from '$lib/components/MadLib.svelte';
    import { onMount } from 'svelte';
    import { fade, slide } from 'svelte/transition';

	let heroImageUrl = 'https://storage.googleapis.com/marketing-copy-assets/images/generated_c46bed9c-bf11-44f3-8aba-6dcf6d121b8e.png';

	// Form state
	let selectedCategory = 'writing';
	let selectedSkill = 'copywriting';
	let selectedModel = 'claude-sonnet-4-5-20250929';
	let task = '';
	let content = '';
    
    // MadLib state
    let product = '';
    let audience = '';
    let coreValue = '';
    
    // Persistence state
    let savedBriefs: Brief[] = [];
    let currentBriefId: string | undefined = undefined;
    let isSaving = false;
    let showDossier = false;

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

    onMount(async () => {
        try {
            const res = await listBriefs();
            savedBriefs = res.briefs;
        } catch (e) {
            console.error("Failed to load briefs", e);
        }
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
        } catch (e) {
            error = "Failed to save to dossier";
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
                    <h1>Build Once. <span class="text-italic">Brief</span> Forever.</h1>
                    <p class="hero-sub">
                        Save your strategic context to the Dossier. Reuse proven frameworks endlessly. 
                        Expert marketing automation built on the timeless principles of Madison Avenue.
                    </p>
                    <div class="hero-actions">
                        <a href="#terminal" class="btn-primary btn-hero-terminal">Enter the Briefing Room</a>
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
            <div class="terminal-layout">
                <!-- Left: Sidebar Dossier -->
                <aside class="dossier-sidebar paper-card">
                    <div class="sidebar-header">
                        <h3>THE DOSSIER</h3>
                        <button class="text-btn" on:click={() => { currentBriefId = undefined; task = ''; product = ''; audience = ''; coreValue = ''; contextFields = []; }}>+ NEW BRIEF</button>
                    </div>
                    <div class="sidebar-content">
                        <span class="form-id">RECENT ARCHIVES</span>
                        {#if savedBriefs.length === 0}
                            <p class="empty-hint">Your library is currently empty.</p>
                        {:else}
                            <div class="brief-stack">
                                {#each savedBriefs.slice(0, 10) as brief}
                                    <button class="brief-mini-card" class:active={currentBriefId === brief.id} on:click={() => loadSavedBrief(brief)}>
                                        <span class="brief-mini-title">{brief.title}</span>
                                        <span class="brief-mini-meta">{brief.product} • {new Date(brief.updated_at || '').toLocaleDateString()}</span>
                                    </button>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </aside>

                <div class="terminal-grid-main">
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

                            <!-- Context FIRST (Flip) -->
                            {#if selectedSkill}
                                <div class="brief-section" transition:slide>
                                    <label class="brief-label">2. KEY CONTEXT</label>
                                    <MadLib bind:product bind:audience bind:value={coreValue} />
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

                <!-- Right: Output Memo (Ghost Writer) -->
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

                <!-- Right: Output Memo (Ghost Writer) -->
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
</div>

<style>
    .optimized-home { padding-bottom: 8rem; background: var(--color-bg); }
    .hero { padding: 6rem 0; }
    .hero-grid { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 5rem; align-items: center; }
    .hero-content h1 { font-size: 5rem; margin-bottom: 2rem; color: var(--color-navy); }
    .hero-sub { font-size: 1.25rem; margin-bottom: 3rem; line-height: 1.8; color: var(--color-smoke); }
    .hero-actions { display: flex; gap: 1.5rem; }
    .btn-hero-terminal { padding: 1.25rem 3rem; font-size: 0.85rem; border-width: 2px; }
    .hero-image-styled { width: 100%; display: block; filter: sepia(0.1) contrast(1.1); }

    .terminal-section { padding: 4rem 0; border-top: 1px solid var(--color-border); scroll-margin-top: 100px; }
    
    /* NEW GRID LAYOUT */
    .terminal-layout { display: grid; grid-template-columns: 280px 1fr; gap: 2rem; align-items: start; }
    .terminal-grid-main { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start; }

    /* DOSSIER SIDEBAR */
    .dossier-sidebar { min-height: 600px; padding: 2rem; display: flex; flex-direction: column; background: #fafafa; }
    .sidebar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--color-navy); }
    .sidebar-header h3 { font-size: 0.9rem; letter-spacing: 0.1em; margin: 0; }
    .empty-hint { font-size: 0.75rem; color: var(--color-text-muted); font-style: italic; margin-top: 2rem; }
    
    .brief-stack { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem; }
    .brief-mini-card { 
        display: flex; flex-direction: column; text-align: left; padding: 1rem; 
        background: white; border: 1px solid var(--color-border); cursor: pointer;
        transition: all 0.2s ease;
    }
    .brief-mini-card:hover { border-color: var(--color-navy); transform: translateX(4px); }
    .brief-mini-card.active { border-left: 4px solid var(--color-brass); background: var(--color-bg-tertiary); }
    .brief-mini-title { font-family: var(--font-serif); font-weight: 700; font-size: 0.8rem; color: var(--color-navy); margin-bottom: 0.25rem; }
    .brief-mini-meta { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-text-muted); }

    .brief-header, .memo-header { border-bottom: 2px solid var(--color-navy); margin-bottom: 2rem; padding-bottom: 1.5rem; }
    .form-id { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-smoke); display: block; margin-bottom: 0.5rem; text-transform: uppercase; }
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

    @media (max-width: 1200px) {
        .terminal-layout { grid-template-columns: 1fr; }
        .dossier-sidebar { min-height: auto; margin-bottom: 2rem; }
    }

    @media (max-width: 1024px) {
        .hero-grid { grid-template-columns: 1fr; }
        .terminal-grid-main { grid-template-columns: 1fr; }
        .hero-content h1 { font-size: 3.5rem; }
        .philosophy-grid { grid-template-columns: 1fr; }
        .paper-card { padding: 2rem; min-height: auto; }
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
    .ghost-hint { font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-text-muted); font-style: italic; }

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