<script lang="ts">
	import { SKILL_CATEGORIES } from '$lib/api';
</script>

<svelte:head>
	<title>Strategic Framework Index | HIGH ERA</title>
</svelte:head>

<div class="skills-directory fade-in">
    <header class="directory-hero">
        <nav class="manual-nav mb-4" style="position: absolute; top: 2rem; left: 0; width: 100%;">
            <div class="container">
                <a href="/" style="text-decoration: none; color: var(--color-brass); font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold;">← TERMINAL</a>
            </div>
        </nav>
        <div class="container">
            <div class="badge-classic">ESTABLISHED 2026</div>
            <h1>The Strategic <span class="text-italic">Framework</span> Index.</h1>
            <p class="lead">A curated repository of 25+ agency-grade specialized skills built on the timeless principles of Madison Avenue.</p>
        </div>
    </header>

    <section class="directory-body">
        <div class="container">
            <div class="directory-grid">
                {#each Object.entries(SKILL_CATEGORIES) as [id, cat]}
                    <div class="framework-category paper-card">
                        <div class="category-header">
                            <span class="category-id">DEPT: {id.toUpperCase()}</span>
                            <h3>{cat.label}</h3>
                            <p class="category-desc">{cat.description}</p>
                        </div>
                        
                        <div class="framework-list">
                            {#each Object.entries(cat.skills) as [skillId, desc]}
                                <a href="/skills/{skillId}" class="framework-item">
                                    <div class="framework-info">
                                        <span class="framework-name">{skillId.replace(/-/g, ' ')}</span>
                                        <span class="framework-desc">{desc}</span>
                                    </div>
                                    <span class="framework-arrow">→</span>
                                </a>
                            {/each}
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </section>
</div>

<style>
    .skills-directory { padding-bottom: 8rem; background: var(--color-bg); }
    
    .directory-hero { padding: 6rem 0; border-bottom: 1px solid var(--color-border); text-align: center; }
    .directory-hero h1 { font-size: 4rem; margin-bottom: 1.5rem; }
    .lead { font-size: 1.25rem; color: var(--color-smoke); max-width: 800px; margin: 0 auto; line-height: 1.8; }

    .directory-body { padding: 6rem 0; }
    .directory-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 3rem; }

    .framework-category { padding: 3rem; min-height: auto; display: flex; flex-direction: column; }
    .category-header { border-bottom: 1px solid var(--color-border); padding-bottom: 1.5rem; margin-bottom: 2rem; }
    .category-id { font-family: var(--font-mono); font-size: 0.65rem; color: var(--color-brass); letter-spacing: 0.1em; display: block; margin-bottom: 0.5rem; }
    .category-desc { font-size: 0.9rem; color: var(--color-smoke); margin-top: 0.5rem; font-style: italic; }

    .framework-list { display: flex; flex-direction: column; gap: 0.5rem; }
    .framework-item {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem; border-radius: var(--radius);
        text-decoration: none; color: inherit;
        transition: all 0.2s ease; border: 1px solid transparent;
    }
    .framework-item:hover {
        background: var(--color-bg-tertiary);
        border-color: var(--color-border);
        transform: translateX(5px);
    }

    .framework-name { display: block; font-family: var(--font-sans); font-weight: 800; font-size: 0.8rem; text-transform: uppercase; color: var(--color-navy); letter-spacing: 0.05em; }
    .framework-desc { display: block; font-size: 0.75rem; color: var(--color-smoke); margin-top: 0.2rem; }
    .framework-arrow { color: var(--color-brass); font-weight: bold; opacity: 0; transition: opacity 0.2s; }
    .framework-item:hover .framework-arrow { opacity: 1; }

    @media (max-width: 1024px) {
        .directory-grid { grid-template-columns: 1fr; }
        .directory-hero h1 { font-size: 3rem; }
    }
</style>
