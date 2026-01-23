<script lang="ts">
	import { SKILL_CATEGORIES } from '$lib/api';
</script>

<svelte:head>
	<title>Skills | Marketing Agency</title>
</svelte:head>

<div class="container">
	<div class="page-header">
		<h1>Available Skills</h1>
		<p>23 marketing skills. Each one a complete framework.</p>
	</div>

	<div class="skills-overview">
		<div class="intro card">
			<h2>Skills vs Prompts</h2>
			<p>Unlike raw LLM prompting, each skill contains:</p>
			<ul>
				<li><strong>Context-gathering frameworks</strong> — Know what to ask before writing</li>
				<li><strong>Proven structures and formulas</strong> — Tested patterns that work</li>
				<li><strong>Psychological principles</strong> — Cialdini, cognitive biases, persuasion</li>
				<li><strong>Quality checklists</strong> — Validate output before delivery</li>
				<li><strong>Strategic rationale</strong> — Understand why, not just what</li>
			</ul>
		</div>
	</div>

	<div class="categories">
		{#each Object.entries(SKILL_CATEGORIES) as [key, category]}
			<div class="category card">
				<div class="category-header">
					<h2>{category.label}</h2>
					<p>{category.description}</p>
				</div>
				<div class="skill-list">
					{#each Object.entries(category.skills) as [skillKey, description]}
						<div class="skill-item">
							<code class="skill-name">{skillKey}</code>
							<span class="skill-description">{description}</span>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	</div>

	<div class="api-section card">
		<h2>API Access</h2>
		<p>Execute skills programmatically via the HTTP API:</p>
		<pre><code>curl -X POST http://localhost:8080/work \
  -H "Content-Type: application/json" \
  -d '&#123;
    "skill": "copywriting",
    "task": "Write a landing page headline",
    "context": &#123;
      "product": "Your product name",
      "audience": "Target audience"
    &#125;
  &#125;'</code></pre>
	</div>
</div>

<style>
	.page-header {
		margin-bottom: 2rem;
	}

	.page-header h1 {
		margin-bottom: 0.5rem;
	}

	.skills-overview {
		margin-bottom: 2rem;
	}

	.intro ul {
		margin: 1rem 0;
		padding-left: 1.5rem;
	}

	.intro li {
		margin: 0.5rem 0;
		color: var(--color-text-secondary);
	}

	.intro li strong {
		color: var(--color-text);
	}

	.categories {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
		gap: 1.5rem;
		margin-bottom: 2rem;
	}

	.category-header {
		margin-bottom: 1rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--color-border);
	}

	.category-header h2 {
		margin-bottom: 0.25rem;
	}

	.category-header p {
		font-size: 0.875rem;
	}

	.skill-list {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.skill-item {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.skill-name {
		font-size: 0.875rem;
		color: var(--color-accent);
	}

	.skill-description {
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.api-section {
		margin-top: 2rem;
	}

	.api-section h2 {
		margin-bottom: 0.5rem;
	}

	.api-section p {
		margin-bottom: 1rem;
	}

	.api-section pre {
		margin: 0;
	}
</style>
