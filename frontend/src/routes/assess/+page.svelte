<script lang="ts">
    import { onMount } from 'svelte';
    import { listSkills } from '$lib/api';

    let assessmentLog: any[] = [];
    let loading = false;
    let error: string | null = null;

    onMount(() => {
        const saved = localStorage.getItem('highEra_assessmentLog');
        if (saved) {
            try {
                assessmentLog = JSON.parse(saved);
            } catch (e) {
                console.error('Failed to load history');
            }
        }
    });

    function saveLog(log: any[]) {
        assessmentLog = log;
        localStorage.setItem('highEra_assessmentLog', JSON.stringify(log));
    }

    // Asset Generation State
    type AssetType = keyof typeof MODELS;
    let assetType: AssetType = 'image';
    let prompt = '';
    let selectedModel = 'fal-ai/flux-2';
    
    const MODELS = {
        image: ['fal-ai/flux-2', 'fal-ai/flux-2-pro', 'bria/text-to-image/3.2'],
        video: ['fal-ai/ltx-2-19b/distilled/text-to-video', 'fal-ai/kling-video/v2.5-turbo/pro/text-to-video', 'fal-ai/minimax/hailuo-2.3/pro/image-to-video'],
        audio: ['fal-ai/stable-audio']
    };

    $: availableModels = MODELS[assetType];

    async function handleGenerate() {
        loading = true;
        error = null;
        
        try {
            const res = await fetch('/api/generate-asset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: assetType, prompt, model: selectedModel })
            });
            
            if (!res.ok) throw new Error('Generation failed');
            
            const asset = await res.json();
            
            const newLog = [{
                timestamp: new Date().toISOString(),
                type: assetType,
                model: selectedModel,
                prompt,
                url: asset.url,
                status: 'Needs Review'
            }, ...assessmentLog];
            
            saveLog(newLog);
            
            prompt = '';
        } catch (e: any) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

    function approveAsset(index: number) {
        const newLog = [...assessmentLog];
        newLog[index].status = 'Approved';
        saveLog(newLog);
    }

    function rejectAsset(index: number) {
        const newLog = [...assessmentLog];
        newLog[index].status = 'Rejected';
        saveLog(newLog);
    }
</script>

<div class="assess-lab fade-in">
    <header class="lab-hero">
        <div class="container">
            <nav class="manual-nav mb-4" style="position: absolute; top: 2rem;">
                <a href="/">← TERMINAL</a>
            </nav>
            <div class="badge-classic">INTERNAL LABORATORY</div>
            <h1>Asset <span class="text-italic">Assessment</span> Lab.</h1>
            <p class="lead">Decide, Design, and Assess cinematic assets for the Remotion Vision platform.</p>
        </div>
    </header>

    <div class="container py-12">
        <div class="lab-grid">
            <!-- Control Panel -->
            <div class="paper-card lab-control">
                <div class="brief-header">
                    <span class="form-id">FORM 9-X: GENERATION REQUEST</span>
                    <h2>Creative Direction</h2>
                </div>

                <div class="brief-section">
                    <label class="brief-label">1. ASSET CLASSIFICATION</label>
                    <select bind:value={assetType} class="classic-select">
                        <option value="image">Cinematic Image (Hero)</option>
                        <option value="video">Motion Background (Video)</option>
                        <option value="audio">Soundscape (Audio)</option>
                    </select>
                </div>

                <div class="brief-section">
                    <label class="brief-label">2. INTELLIGENCE MODEL</label>
                    <select bind:value={selectedModel} class="classic-select">
                        {#each availableModels as model}
                            <option value={model}>{model}</option>
                        {/each}
                    </select>
                </div>

                <div class="brief-section">
                    <label class="brief-label" for="prompt">3. ARTISTIC PROMPT</label>
                    <textarea id="prompt" bind:value={prompt} placeholder="Enter unique differentiating prompt..." rows="4" class="typewriter-textarea"></textarea>
                </div>

                <button class="btn-primary w-full mt-4" on:click={handleGenerate} disabled={loading || !prompt}>
                    {#if loading}<span class="spinner"></span> PROCESSING...{:else}INITIATE GENERATION →{/if}
                </button>
            </div>

            <!-- Assessment Log -->
            <div class="assessment-column">
                <div class="column-header">
                    <span class="form-id">REPORTS: VERIFICATION LOG</span>
                    <h3>Active Observations</h3>
                </div>

                {#if assessmentLog.length === 0}
                    <div class="empty-memo paper-card">
                        <div class="watermark">VOID</div>
                        <p>No assets currently in review cycle.</p>
                    </div>
                {:else}
                    <div class="log-stack">
                        {#each assessmentLog as entry, i}
                            <div class="report-entry paper-card">
                                <div class="report-meta">
                                    <span class="status-badge" class:approved={entry.status === 'Approved'}>{entry.status}</span>
                                    <span class="report-id">REF: {new Date(entry.timestamp).getTime().toString().slice(-6)}</span>
                                </div>
                                
                                <div class="report-visual">
                                    <div class="frame-classic">
                                        {#if entry.type === 'image'}
                                            <img src={entry.url} alt="Assessment Visual" class="report-media" />
                                        {:else if entry.type === 'video'}
                                            <video src={entry.url} controls class="report-media"></video>
                                        {:else}
                                            <audio src={entry.url} controls class="w-full"></audio>
                                        {/if}
                                    </div>
                                    <div class="caption-classic">
                                        {entry.model.toUpperCase()} Output
                                    </div>
                                </div>

                                <div class="report-details typewriter mt-4">
                                    <p><strong>Prompt:</strong> <em>"{entry.prompt}"</em></p>
                                </div>

                                {#if entry.status === 'Needs Review'}
                                    <div class="report-actions mt-6">
                                        <button class="btn-primary flex-1 btn-sm" on:click={() => approveAsset(i)}>Approve & Integrate</button>
                                        <button class="btn-secondary flex-1 btn-sm" on:click={() => rejectAsset(i)}>Reject & Iterate</button>
                                    </div>
                                {/if}
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .assess-lab { background: var(--color-bg); min-height: 100vh; padding-bottom: 8rem; }
    .lab-hero { padding: 6rem 0; border-bottom: 1px solid var(--color-border); text-align: center; }
    .py-12 { padding-top: 3rem; padding-bottom: 3rem; }

    .lab-grid { display: grid; grid-template-columns: 400px 1fr; gap: 3rem; align-items: start; }
    
    .lab-control { padding: 2.5rem; position: sticky; top: 100px; }
    
    .column-header { margin-bottom: 2rem; border-bottom: 2px solid var(--color-navy); padding-bottom: 1rem; }
    
    .log-stack { display: flex; flex-direction: column; gap: 2rem; }
    
    .report-entry { padding: 2rem; }
    .report-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
    
    .status-badge {
        font-family: var(--font-mono); font-size: 0.6rem; font-weight: bold;
        padding: 0.2rem 0.6rem; border: 1px solid currentColor;
    }
    .status-badge.approved { background: var(--color-navy); color: white; border-color: var(--color-navy); }
    
    .report-id { font-family: var(--font-mono); font-size: 0.6rem; color: var(--color-text-muted); }
    
    .report-media { width: 100%; border-radius: 2px; }
    
    .report-actions { display: flex; gap: 1rem; border-top: 1px solid var(--color-border); padding-top: 1.5rem; }
    
    .empty-memo { height: 300px; display: flex; align-items: center; justify-content: center; color: var(--color-text-muted); }

    @media (max-width: 1024px) {
        .lab-grid { grid-template-columns: 1fr; }
        .lab-control { position: static; }
    }
</style>