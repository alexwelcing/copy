<script lang="ts">
    import { page } from '$app/stores';
    import campaigns from '$lib/data/campaigns.json';
    import LeadModal from '$lib/components/LeadModal.svelte';
    import { goto } from '$app/navigation';

    $: slug = $page.params.slug;
    $: campaign = campaigns.find(c => c.slug === slug);
    
    let showModal = false;

    function handleSuccess() {
        showModal = false;
        goto('/');
    }
</script>

<svelte:head>
    <title>{campaign ? campaign.headline : 'Page Not Found'} | HIGH ERA</title>
</svelte:head>

{#if campaign}
    <div class="campaign-page fade-in">
        {#if showModal}
            <LeadModal campaign={campaign.title} on:close={() => showModal = false} on:success={handleSuccess} />
        {/if}

        <section class="hero">
            <div class="container" style="position: relative;">
                <nav class="manual-nav mb-4" style="position: absolute; top: -3rem;">
                    <a href="/" style="text-decoration: none; color: var(--color-brass); font-family: var(--font-mono); font-size: 0.8rem; font-weight: bold;">← TERMINAL</a>
                </nav>
                <div class="hero-grid">
                    <div class="hero-content">
                        <div class="badge-classic">USE CASE: {campaign.target_audience.toUpperCase()}</div>
                        <h1>{campaign.headline}</h1>
                        <p class="hero-sub">{campaign.subheadline}</p>
                        <div class="hero-actions">
                            <button class="btn-primary" on:click={() => showModal = true}>Start {campaign.target_audience} Project</button>
                        </div>
                    </div>
                    <div class="hero-visual">
                        <div class="frame-classic">
                            <img src={campaign.hero_url} alt={campaign.title} class="hero-image-styled" />
                        </div>
                        <div class="caption-classic">
                            GENERATED ASSET: {campaign.asset_prompt_summary}
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="content-body">
            <div class="container">
                <div class="copy-block typewriter">
                    <h2>Why generic marketing fails <span class="text-italic">{campaign.target_audience}</span></h2>
                    <p>{campaign.pain_point_copy}</p>
                </div>
                <div class="copy-block typewriter">
                    <h2>The High Era Solution</h2>
                    <p>{campaign.solution_copy}</p>
                </div>
            </div>
        </section>
    </div>
{:else}
    <div class="container" style="padding: 10rem; text-align: center;">
        <h1 style="font-size: 8rem; opacity: 0.1;">404</h1>
        <p>Campaign not found in current records.</p>
        <a href="/" class="btn-secondary mt-4">Return to Terminal</a>
    </div>
{/if}

<style>
    .campaign-page { padding-bottom: 8rem; background: var(--color-bg); min-height: 100vh; }
    .hero { padding: 6rem 0; }
    .hero-grid { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 5rem; align-items: center; }
    
    h1 { font-size: 4rem; margin-bottom: 2rem; color: var(--color-navy); line-height: 1.1; }
    .hero-sub { font-size: 1.25rem; margin-bottom: 3rem; line-height: 1.8; color: var(--color-smoke); }
    .hero-image-styled { width: 100%; display: block; filter: sepia(0.1) contrast(1.1); }
    
    .content-body { background: white; padding: 6rem 0; border-top: 1px solid var(--color-border); }
    .copy-block { max-width: 750px; margin: 0 auto 6rem; }
    .copy-block h2 { font-family: var(--font-serif); font-size: 2.5rem; margin-bottom: 2rem; color: var(--color-navy); }
    .copy-block p { font-size: 1.2rem; line-height: 1.8; color: var(--color-ink); }

    @media (max-width: 1024px) {
        .hero-grid { grid-template-columns: 1fr; gap: 3rem; }
        h1 { font-size: 3rem; }
    }
</style>