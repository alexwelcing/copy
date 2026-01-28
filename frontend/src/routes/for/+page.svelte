<script lang="ts">
  import { audiences } from '$lib/data/audiences';
</script>

<svelte:head>
  <title>High Era - Choose Your Path</title>
  <meta name="description" content="Marketing frameworks for technical founders, freelance marketers, and startup teams." />
</svelte:head>

<main class="audience-selector">
  <section class="hero">
    <h1>Who are you?</h1>
    <p class="subheadline">
      Same 23 skills. Different entry points. Pick the path that fits.
    </p>
  </section>

  <section class="paths">
    {#each audiences as audience}
      <a href="/for/{audience.slug}" class="path-card">
        <div class="path-header">
          <span class="path-badge">{audience.audience}</span>
        </div>
        <h2>{audience.headline}</h2>
        <p class="path-description">{audience.subheadline}</p>
        <div class="path-cta">
          <span>See how this helps you</span>
          <span class="arrow">→</span>
        </div>
      </a>
    {/each}
  </section>

  <section class="all-skills">
    <p>Or just <a href="/skills">browse all 23 skills</a> and pick what you need.</p>
  </section>
</main>

<style>
  .audience-selector {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem;
  }

  .hero {
    text-align: center;
    padding: 4rem 0;
  }

  .hero h1 {
    font-family: var(--font-serif);
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 400;
    margin-bottom: 1rem;
  }

  .subheadline {
    font-size: 1.25rem;
    color: var(--color-text-secondary);
    max-width: 500px;
    margin: 0 auto;
  }

  .paths {
    display: grid;
    gap: 2rem;
    margin-bottom: 4rem;
  }

  @media (min-width: 768px) {
    .paths {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  .path-card {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    background: var(--color-cream);
    text-decoration: none;
    color: inherit;
    border: 1px solid transparent;
    transition: all 0.2s;
  }

  .path-card:hover {
    border-color: var(--color-brass);
  }

  .path-header {
    margin-bottom: 1.5rem;
  }

  .path-badge {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-brass);
    padding: 0.25rem 0.5rem;
    border: 1px solid var(--color-brass);
  }

  .path-card h2 {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 500;
    margin-bottom: 1rem;
    flex-grow: 1;
  }

  .path-description {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
    line-height: 1.5;
    margin-bottom: 1.5rem;
  }

  .path-cta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-brass);
    padding-top: 1rem;
    border-top: 1px solid var(--color-brass);
  }

  .arrow {
    transition: transform 0.2s;
  }

  .path-card:hover .arrow {
    transform: translateX(4px);
  }

  .all-skills {
    text-align: center;
    padding: 2rem;
    color: var(--color-text-secondary);
  }

  .all-skills a {
    color: var(--color-brass);
    text-decoration: underline;
  }
</style>
