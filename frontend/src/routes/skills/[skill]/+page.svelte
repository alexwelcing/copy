<script lang="ts">
    import { page } from '$app/stores';
    import { SKILL_CATEGORIES } from '$lib/api';
    import { onMount } from 'svelte';

    $: skillId = $page.params.skill;
    
    // Find skill info
    $: skillInfo = Object.values(SKILL_CATEGORIES)
        .flatMap(cat => Object.entries(cat.skills))
        .find(([id]) => id === skillId);

    $: category = Object.entries(SKILL_CATEGORIES).find(([_, cat]) => 
        Object.keys(cat.skills).includes(skillId)
    );

    let showOptimized = false;
</script>

<svelte:head>
    <title>{skillId} | AI Marketing Agency</title>
    <meta name="description" content="Automate your {skillId} with expert AI marketing skills." />
</svelte:head>

<div class="mode-toggle-wrapper container">
    <div class="mode-toggle glass">
        <button class:active={!showOptimized} on:click={() => showOptimized = false}>Standard Template</button>
        <div class="toggle-divider"></div>
        <button class:active={showOptimized} on:click={() => showOptimized = true}>✨ Programmatic SEO View</button>
    </div>
</div>

<div class="container fade-in">
    {#if !showOptimized}
        <!-- STANDARD VIEW -->
        <div class="standard-view">
            <header class="skill-header">
                <div class="badge">{category ? category[1].label : 'Skill'}</div>
                <h1>{skillId}</h1>
                <p class="lead">{skillInfo ? skillInfo[1] : 'Expert marketing execution.'}</p>
                <a href="/?skill={skillId}" class="btn-primary mt-4">Execute this Skill →</a>
            </header>

            <section class="mt-4">
                <h3>How it works</h3>
                <p>Select this skill from our library, provide your product context, and receive agency-grade output in 30 seconds.</p>
            </section>
        </div>
    {:else}
        <!-- PROGRAMMATIC SEO OPTIMIZED VIEW -->
        <div class="optimized-skill-view">
            <header class="hero-mini">
                <div class="badge neon-badge">{category ? category[1].label.toUpperCase() : 'MARKETING SKILL'}</div>
                <h1>Automated <span class="text-indigo">{skillId.replace('-', ' ')}</span> for Marketers</h1>
                <p class="lead">Execute expert {skillId.replace('-', ' ')} strategies through UI or API access. Built on proven agency frameworks.</p>
                
                <div class="hero-actions mt-4">
                    <a href="/?skill={skillId}" class="btn-primary btn-lg">Start Free Trial</a>
                    <button class="btn-secondary btn-lg">View API Docs</button>
                </div>
            </header>

            <div class="pseo-grid mt-4">
                <div class="pseo-main">
                    <section class="glass p-8 rounded-xl mb-8">
                        <h2>What is <span class="text-indigo">{skillId.replace('-', ' ')}</span>?</h2>
                        <p class="mt-4 text-lg">
                            {skillId.replace('-', ' ')} is a specialized, AI-powered capability that executes complex marketing tasks with expert-level precision. 
                            Our {skillId} skill follows proven methodologies used by top-tier marketing agencies to ensure consistent, high-quality results.
                        </p>
                        
                        <div class="features-list mt-8">
                            <div class="feature-item">
                                <span class="check">✓</span>
                                <div>
                                    <strong>Expert Frameworks</strong>
                                    <p>Pre-trained on industry-standard best practices.</p>
                                </div>
                            </div>
                            <div class="feature-item">
                                <span class="check">✓</span>
                                <div>
                                    <strong>Instant Execution</strong>
                                    <p>Go from task to deliverable in under 30 seconds.</p>
                                </div>
                            </div>
                            <div class="feature-item">
                                <span class="check">✓</span>
                                <div>
                                    <strong>API Ready</strong>
                                    <p>Integrate {skillId} directly into your product or workflow.</p>
                                </div>
                            </div>
                        </div>
                    </section>

                    <section class="glass p-8 rounded-xl">
                        <h2>When to use <span class="text-indigo">{skillId.replace('-', ' ')}</span></h2>
                        <div class="use-cases-grid mt-6">
                            <div class="use-case-card">
                                <h4>Solo Marketers</h4>
                                <p>Execute enterprise-level {skillId} without the agency overhead.</p>
                            </div>
                            <div class="use-case-card">
                                <h4>SaaS Teams</h4>
                                <p>Automate repetitive marketing tasks and scale your growth experiment.</p>
                            </div>
                        </div>
                    </section>
                </div>

                <div class="pseo-sidebar">
                    <div class="sidebar-box glass">
                        <h4>Skill Specs</h4>
                        <div class="spec-item">
                            <span>Latency</span>
                            <strong>12-18s</strong>
                        </div>
                        <div class="spec-item">
                            <span>Intelligence</span>
                            <strong>Claude 3.5 / MiniMax</strong>
                        </div>
                        <div class="spec-item">
                            <span>Output Type</span>
                            <strong>Structured JSON/MD</strong>
                        </div>
                    </div>

                    <div class="sidebar-box glass mt-4">
                        <h4>Related Skills</h4>
                        <div class="related-list">
                            {#if category}
                                {#each Object.keys(category[1].skills).filter(s => s !== skillId).slice(0, 3) as related}
                                    <a href="/skills/{related}" class="related-link">{related}</a>
                                {/each}
                            {/if}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .mode-toggle-wrapper { display: flex; justify-content: center; margin: 2rem auto; }
    .mode-toggle { display: flex; padding: 0.25rem; border-radius: 40px; background: rgba(15, 23, 42, 0.8); }
    .mode-toggle button { padding: 0.5rem 1.5rem; border-radius: 30px; font-size: 0.875rem; background: transparent; color: var(--color-text-secondary); }
    .mode-toggle button.active { background: var(--color-indigo); color: white; }
    .toggle-divider { width: 1px; background: var(--color-border); margin: 0.5rem 0.25rem; }

    .skill-header { padding: 4rem 0; text-align: center; }
    .lead { font-size: 1.25rem; color: var(--color-text-secondary); margin-top: 1rem; }
    .badge { display: inline-block; padding: 0.25rem 0.75rem; background: var(--color-bg-secondary); border-radius: 20px; font-size: 0.75rem; color: var(--color-indigo); font-weight: 600; margin-bottom: 1rem; }
    .neon-badge { border: 1px solid var(--color-mint); color: var(--color-mint); background: rgba(16, 185, 129, 0.05); }

    .pseo-grid { display: grid; grid-template-columns: 1fr 300px; gap: 2rem; }
    .sidebar-box { padding: 1.5rem; border-radius: 16px; }
    .sidebar-box h4 { font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-text-muted); margin-bottom: 1rem; }
    .spec-item { display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.875rem; }
    .related-link { display: block; padding: 0.5rem 0; color: var(--color-indigo); font-size: 0.9375rem; }
    
    .feature-item { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    .check { color: var(--color-mint); font-weight: 800; }
    .use-cases-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .use-case-card { padding: 1.25rem; background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); border-radius: 12px; }
    .use-case-card h4 { font-size: 1rem; margin-bottom: 0.5rem; }
    .use-case-card p { font-size: 0.875rem; }

    .p-8 { padding: 2rem; }
    .rounded-xl { border-radius: 1.25rem; }
    .text-indigo { color: var(--color-indigo); }
    .text-lg { font-size: 1.125rem; }

    @media (max-width: 768px) {
        .pseo-grid { grid-template-columns: 1fr; }
    }
</style>
