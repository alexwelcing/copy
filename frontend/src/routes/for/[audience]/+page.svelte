<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;
  $: audience = data.audience;

  let showLeadModal = false;
</script>

<svelte:head>
  <title>High Era for {audience.audience}</title>
  <meta name="description" content={audience.subheadline} />
</svelte:head>

<main class="audience-page">
  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-badge">{audience.audience}</div>
    <h1>{audience.headline}</h1>
    <p class="subheadline">{audience.subheadline}</p>
    <div class="hero-cta">
      <a href="/skills/{audience.cta.action}" class="btn-primary">
        {audience.cta.primary}
      </a>
      <a href="/skills" class="btn-secondary">
        {audience.cta.secondary}
      </a>
    </div>
  </section>

  <!-- Pain Points Section -->
  <section class="pain-points">
    <p class="hook">{audience.painPoints.hook}</p>
    <div class="pain-grid">
      {#each audience.painPoints.points as point}
        <div class="pain-card">
          <p class="problem">{point.problem}</p>
          <p class="agitation">{point.agitation}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- Solution Section -->
  <section class="solution">
    <p class="intro">{audience.solution.intro}</p>
    <div class="solution-grid">
      {#each audience.solution.points as point}
        <div class="solution-card">
          <h3>{point.title}</h3>
          <p>{point.description}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- Proof Section -->
  <section class="proof">
    <div class="proof-card">
      {#if audience.proof.type === 'dogfood'}
        <span class="proof-badge">We eat our own cooking</span>
      {:else if audience.proof.type === 'demo'}
        <span class="proof-badge">Try it yourself</span>
      {:else}
        <span class="proof-badge">What they say</span>
      {/if}
      <p>{audience.proof.content}</p>
    </div>
  </section>

  <!-- Objections Section -->
  <section class="objections">
    <h2>You might be thinking...</h2>
    <div class="objection-grid">
      {#each audience.objections as obj}
        <div class="objection-card">
          <p class="objection">"{obj.objection}"</p>
          <p class="response">{obj.response}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- Skills Preview Section -->
  <section class="skills-preview">
    <h2>Start with these</h2>
    <p class="skills-intro">Recommended skills for {audience.audience.toLowerCase()}:</p>
    <div class="skills-grid">
      {#each audience.skills as skill}
        <a href="/skills/{skill}" class="skill-card">
          <span class="skill-name">{skill.replace(/-/g, ' ')}</span>
          <span class="skill-arrow">→</span>
        </a>
      {/each}
    </div>
  </section>

  <!-- Final CTA Section -->
  <section class="final-cta">
    <h2>Ready to ship?</h2>
    <p>Load a skill. Give it context. Ship something today.</p>
    <div class="cta-buttons">
      <a href="/skills/{audience.cta.action}" class="btn-primary btn-large">
        {audience.cta.primary}
      </a>
    </div>
  </section>
</main>

<style>
  .audience-page {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
  }

  /* Hero */
  .hero {
    text-align: center;
    padding: 4rem 0;
    border-bottom: 1px solid var(--color-brass);
  }

  .hero-badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-brass);
    padding: 0.5rem 1rem;
    border: 1px solid var(--color-brass);
    margin-bottom: 2rem;
  }

  .hero h1 {
    font-family: var(--font-serif);
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 400;
    line-height: 1.2;
    margin-bottom: 1rem;
  }

  .subheadline {
    font-size: 1.25rem;
    color: var(--color-text-secondary);
    max-width: 600px;
    margin: 0 auto 2rem;
  }

  .hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .btn-primary {
    background: var(--color-brass);
    color: var(--color-cream);
    padding: 1rem 2rem;
    text-decoration: none;
    font-family: var(--font-mono);
    font-size: 0.875rem;
    letter-spacing: 0.05em;
    transition: background 0.2s;
  }

  .btn-primary:hover {
    background: var(--color-navy);
  }

  .btn-secondary {
    color: var(--color-brass);
    padding: 1rem 2rem;
    text-decoration: none;
    font-family: var(--font-mono);
    font-size: 0.875rem;
    letter-spacing: 0.05em;
    border: 1px solid var(--color-brass);
    transition: all 0.2s;
  }

  .btn-secondary:hover {
    background: var(--color-brass);
    color: var(--color-cream);
  }

  /* Pain Points */
  .pain-points {
    padding: 4rem 0;
  }

  .hook {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-style: italic;
    text-align: center;
    margin-bottom: 3rem;
    color: var(--color-text-secondary);
  }

  .pain-grid {
    display: grid;
    gap: 2rem;
  }

  .pain-card {
    padding: 2rem;
    background: var(--color-cream);
    border-left: 3px solid var(--color-brass);
  }

  .problem {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 500;
    margin-bottom: 0.75rem;
  }

  .agitation {
    color: var(--color-text-secondary);
    line-height: 1.6;
  }

  /* Solution */
  .solution {
    padding: 4rem 0;
    background: var(--color-navy);
    color: var(--color-cream);
    margin: 0 -2rem;
    padding-left: 2rem;
    padding-right: 2rem;
  }

  .solution .intro {
    font-size: 1.25rem;
    text-align: center;
    max-width: 700px;
    margin: 0 auto 3rem;
    opacity: 0.9;
  }

  .solution-grid {
    display: grid;
    gap: 2rem;
  }

  @media (min-width: 600px) {
    .solution-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .solution-card h3 {
    font-family: var(--font-mono);
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-brass);
    margin-bottom: 0.75rem;
  }

  .solution-card p {
    opacity: 0.85;
    line-height: 1.6;
  }

  /* Proof */
  .proof {
    padding: 4rem 0;
    text-align: center;
  }

  .proof-card {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
    border: 2px solid var(--color-brass);
  }

  .proof-badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-brass);
    margin-bottom: 1rem;
  }

  .proof-card p {
    font-family: var(--font-serif);
    font-size: 1.125rem;
    font-style: italic;
    line-height: 1.6;
  }

  /* Objections */
  .objections {
    padding: 4rem 0;
  }

  .objections h2 {
    font-family: var(--font-serif);
    font-size: 1.75rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  .objection-grid {
    display: grid;
    gap: 1.5rem;
  }

  .objection-card {
    padding: 1.5rem;
    background: var(--color-cream);
  }

  .objection {
    font-family: var(--font-serif);
    font-style: italic;
    color: var(--color-text-secondary);
    margin-bottom: 0.75rem;
  }

  .response {
    line-height: 1.6;
  }

  /* Skills Preview */
  .skills-preview {
    padding: 4rem 0;
    text-align: center;
  }

  .skills-preview h2 {
    font-family: var(--font-serif);
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
  }

  .skills-intro {
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
  }

  .skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
  }

  .skill-card {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.5rem;
    background: var(--color-cream);
    text-decoration: none;
    color: inherit;
    font-family: var(--font-mono);
    font-size: 0.875rem;
    text-transform: capitalize;
    transition: all 0.2s;
    border: 1px solid transparent;
  }

  .skill-card:hover {
    border-color: var(--color-brass);
  }

  .skill-arrow {
    color: var(--color-brass);
  }

  /* Final CTA */
  .final-cta {
    padding: 4rem 0;
    text-align: center;
    border-top: 1px solid var(--color-brass);
  }

  .final-cta h2 {
    font-family: var(--font-serif);
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }

  .final-cta p {
    color: var(--color-text-secondary);
    margin-bottom: 2rem;
  }

  .btn-large {
    padding: 1.25rem 3rem;
    font-size: 1rem;
  }
</style>
