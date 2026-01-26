<script lang="ts">
    import { page } from '$app/stores';
    import { SKILL_CATEGORIES } from '$lib/api';

    $: skillId = $page.params.skill;
    
    // Find skill info
    $: skillInfo = Object.values(SKILL_CATEGORIES)
        .flatMap(cat => Object.entries(cat.skills))
        .find(([id]) => id === skillId);

    $: category = Object.entries(SKILL_CATEGORIES).find(([_, cat]) => 
        Object.keys(cat.skills).includes(skillId)
    );
</script>

<svelte:head>
    <title>{skillId} | Agency AI</title>
</svelte:head>

<div class="skill-manual fade-in">
    <div class="container">
        <!-- Navigation Breadcrumb -->
        <nav class="manual-nav">
            <a href="/skills">← INDEX</a>
            <span class="divider">/</span>
            <span class="current">{category ? category[0].toUpperCase() : 'DEPT'}</span>
        </nav>

        <div class="manual-grid">
            <!-- Left: Strategic Context -->
            <div class="manual-content paper-card">
                <header class="manual-header">
                    <div class="meta-row">
                        <span class="ref-code">REF: {skillId.toUpperCase().slice(0, 3)}-{Math.floor(Math.random() * 900) + 100}</span>
                        <span class="status-badge">STATUS: ACTIVE</span>
                    </div>
                    <h1>{skillId.replace(/-/g, ' ')}</h1>
                    <p class="lead">{skillInfo ? skillInfo[1] : 'Expert marketing execution capability.'}</p>
                    
                    <div class="action-row">
                        <a href="/?skill={skillId}" class="btn-primary">Initialize Protocol →</a>
                    </div>
                </header>

                <section class="manual-section">
                    <h3>Operational Framework</h3>
                    <p class="typewriter-text">
                        The <strong>{skillId.replace(/-/g, ' ')}</strong> framework leverages agency-grade methodology to execute high-value marketing tasks. 
                        By systematizing the creative process, we ensure consistent, high-fidelity outputs that respect the intelligence of the audience.
                    </p>
                </section>

                <section class="manual-section">
                    <h3>Execution Parameters</h3>
                    <ul class="checklist">
                        <li><strong>Input:</strong> Contextual briefing via terminal.</li>
                        <li><strong>Process:</strong> Multi-step reasoning (Chain-of-Thought).</li>
                        <li><strong>Output:</strong> Structured, ready-to-deploy assets.</li>
                    </ul>
                </section>
            </div>

            <!-- Right: Technical Specs -->
            <aside class="manual-sidebar">
                <div class="spec-card paper-card">
                    <h4>Technical Specifications</h4>
                    <div class="spec-grid">
                        <div class="spec-item">
                            <span class="label">LATENCY</span>
                            <span class="value">12-18s</span>
                        </div>
                        <div class="spec-item">
                            <span class="label">INTELLIGENCE</span>
                            <span class="value">CLAUDE 3.5</span>
                        </div>
                        <div class="spec-item">
                            <span class="label">FORMAT</span>
                            <span class="value">JSON / MARKDOWN</span>
                        </div>
                    </div>
                </div>

                <div class="related-card paper-card mt-4">
                    <h4>Related Frameworks</h4>
                    <div class="related-list">
                        {#if category}
                            {#each Object.keys(category[1].skills).filter(s => s !== skillId).slice(0, 4) as related}
                                <a href="/skills/{related}" class="related-link">
                                    <span class="arrow">→</span> {related.replace(/-/g, ' ')}
                                </a>
                            {/each}
                        {/if}
                    </div>
                </div>
            </aside>
        </div>
    </div>
</div>

<style>
    .skill-manual { padding: 4rem 0 8rem; background: var(--color-bg); min-height: 100vh; }
    
    .manual-nav { margin-bottom: 2rem; font-family: var(--font-mono); font-size: 0.8rem; }
    .manual-nav a { text-decoration: none; color: var(--color-brass); font-weight: bold; }
    .manual-nav .divider { margin: 0 0.5rem; color: var(--color-border); }
    .manual-nav .current { color: var(--color-smoke); }

    .manual-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 3rem; align-items: start; }

    .manual-header { border-bottom: 1px solid var(--color-border); padding-bottom: 2rem; margin-bottom: 2rem; }
    .meta-row { display: flex; justify-content: space-between; margin-bottom: 1rem; font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-text-muted); }
    .status-badge { border: 1px solid var(--color-success); color: var(--color-success); padding: 0.1rem 0.4rem; }

    h1 { font-size: 3rem; text-transform: capitalize; margin-bottom: 1rem; }
    .lead { font-size: 1.2rem; color: var(--color-smoke); margin-bottom: 2rem; font-style: italic; }

    .manual-section { margin-bottom: 3rem; }
    .manual-section h3 { font-size: 1.2rem; margin-bottom: 1rem; font-family: var(--font-sans); text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid var(--color-navy); display: inline-block; padding-bottom: 0.25rem; }
    
    .typewriter-text { font-family: var(--font-mono); font-size: 0.95rem; line-height: 1.8; color: var(--color-ink); }
    
    .checklist { list-style: none; }
    .checklist li { margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative; font-family: var(--font-mono); font-size: 0.9rem; }
    .checklist li::before { content: "✓"; position: absolute; left: 0; color: var(--color-brass); font-weight: bold; }

    .spec-card h4, .related-card h4 { font-size: 0.8rem; font-family: var(--font-sans); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.5rem; color: var(--color-navy); border-bottom: 1px solid var(--color-border); padding-bottom: 0.5rem; }
    
    .spec-grid { display: grid; gap: 1rem; }
    .spec-item { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--color-border); padding-bottom: 0.5rem; }
    .spec-item .label { font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-smoke); }
    .spec-item .value { font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold; color: var(--color-navy); }

    .related-list { display: flex; flex-direction: column; gap: 0.75rem; }
    .related-link { text-decoration: none; color: var(--color-text); font-size: 0.9rem; font-family: var(--font-sans); font-weight: 600; text-transform: capitalize; transition: color 0.2s; }
    .related-link:hover { color: var(--color-brass); }
    .related-link .arrow { color: var(--color-brass); margin-right: 0.5rem; }

    @media (max-width: 1024px) {
        .manual-grid { grid-template-columns: 1fr; }
    }
</style>
