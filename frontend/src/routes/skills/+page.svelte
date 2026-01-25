<script lang="ts">
	import { SKILL_CATEGORIES } from '$lib/api';

	let showOptimized = false;
</script>

<svelte:head>
	<title>All Marketing Skills | AI Marketing Agency</title>
</svelte:head>

<div class="mode-toggle-wrapper container">
    <div class="mode-toggle glass">
        <button class:active={!showOptimized} on:click={() => showOptimized = false}>Simple List</button>
        <div class="toggle-divider"></div>
        <button class:active={showOptimized} on:click={() => showOptimized = true}>✨ Skill Directory View</button>
    </div>
</div>

<div class="container fade-in">
	{#if !showOptimized}
		<div class="standard-view">
			<h1>All Marketing Skills</h1>
			<p class="lead">Explore our 25+ specialized AI marketing capabilities.</p>

			<div class="category-list mt-4">
				{#each Object.entries(SKILL_CATEGORIES) as [id, cat]}
					<div class="category-section mb-4">
						<h2>{cat.label}</h2>
						<div class="skills-simple-grid">
							{#each Object.entries(cat.skills) as [skillId, desc]}
								<a href="/skills/{skillId}" class="skill-link glass">
									<strong>{skillId}</strong>
									<p>{desc}</p>
								</a>
							{/each}
						</div>
					</div>
				{/each}
			</div>
		</div>
	{:else}
		<div class="directory-view">
			<header class="section-header-centered">
				<div class="badge neon-badge">SKILL LIBRARY</div>
				<h1>The Marketing <span class="text-indigo">Framework</span> Index</h1>
				<p>Access 25+ agency-grade skills built on proven marketing methodologies.</p>
			</header>

			<div class="directory-grid">
				{#each Object.entries(SKILL_CATEGORIES) as [id, cat]}
					<div class="directory-category glass">
						<div class="cat-header">
							<h3>{cat.label}</h3>
							<p>{cat.description}</p>
						</div>
						<div class="cat-skills">
							{#each Object.entries(cat.skills) as [skillId, desc]}
								<a href="/skills/{skillId}" class="skill-item">
									<div class="skill-item-info">
										<span class="skill-name-label">{skillId.replace('-', ' ')}</span>
										<span class="skill-short-desc">{desc}</span>
									</div>
									<span class="arrow">→</span>
								</a>
							{/each}
						</div>
					</div>
				{/each}
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

	.lead { font-size: 1.25rem; color: var(--color-text-secondary); margin-bottom: 2rem; }
	.skills-simple-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem; }
	.skill-link { padding: 1.5rem; border-radius: 12px; display: block; }
	.skill-link strong { display: block; margin-bottom: 0.5rem; font-family: var(--font-mono); color: var(--color-indigo); }

	.section-header-centered { text-align: center; margin-bottom: 4rem; }
	.directory-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem; }
	.directory-category { border-radius: 20px; overflow: hidden; display: flex; flex-direction: column; }
	.cat-header { padding: 2rem; background: rgba(255,255,255,0.02); border-bottom: 1px solid var(--color-border); }
	.cat-header h3 { color: var(--color-indigo); margin-bottom: 0.5rem; }
	.cat-skills { padding: 1rem; flex: 1; }
	.skill-item { display: flex; align-items: center; justify-content: space-between; padding: 1rem; border-radius: 12px; transition: all 0.2s ease; }
	.skill-item:hover { background: rgba(255,255,255,0.05); }
	.skill-name-label { display: block; font-weight: 600; text-transform: capitalize; color: var(--color-text); }
	.skill-short-desc { font-size: 0.75rem; color: var(--color-text-muted); }
	.arrow { color: var(--color-indigo); opacity: 0; transform: translateX(-10px); transition: all 0.2s ease; }
	.skill-item:hover .arrow { opacity: 1; transform: translateX(0); }

	@media (max-width: 1024px) {
		.directory-grid { grid-template-columns: 1fr; }
	}
</style>