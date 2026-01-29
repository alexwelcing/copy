<script lang="ts">
    import { saveUserProfile, type UserProfile } from '$lib/api';
    import { goto } from '$app/navigation';
    
    let name = '';
    let company = '';
    let productName = '';
    let targetAudience = '';
    let brandValues = '';
    let websiteUrl = '';
    
    let loading = false;
    let error = '';

    async function handleSubmit() {
        if (!company || !productName || !targetAudience) {
            error = "Please fill in the required fields.";
            return;
        }
        
        loading = true;
        error = '';
        
        try {
            const profile: UserProfile = {
                name,
                company,
                product_name: productName,
                target_audience: targetAudience,
                brand_values: brandValues,
                website_url: websiteUrl
            };
            
            await saveUserProfile(profile);
            goto('/');
        } catch (e) {
            error = "Failed to save profile. Please try again.";
            console.error(e);
        } finally {
            loading = false;
        }
    }
</script>

<svelte:head>
    <title>Agency Onboarding | HIGH ERA</title>
</svelte:head>

<div class="onboard-container fade-in">
    <div class="onboard-card paper-card">
        <div class="header">
            <div class="badge-classic-small">EST. 2026</div>
            <h1>Agency Onboarding</h1>
            <p class="sub">Establish your brand context once. We'll remember it forever.</p>
        </div>
        
        <form on:submit|preventDefault={handleSubmit} class="onboard-form">
            <div class="form-group">
                <label for="name">Your Name</label>
                <input type="text" id="name" bind:value={name} class="classic-input" placeholder="Don Draper" />
            </div>

            <div class="form-group">
                <label for="company">Company Name *</label>
                <input type="text" id="company" bind:value={company} class="classic-input" placeholder="Sterling Cooper" required />
            </div>
            
            <div class="form-group">
                <label for="website">Website URL (Optional)</label>
                <input type="url" id="website" bind:value={websiteUrl} class="classic-input" placeholder="https://..." />
            </div>

            <div class="split-group">
                <div class="form-group">
                    <label for="product">Primary Product/Service *</label>
                    <input type="text" id="product" bind:value={productName} class="classic-input" placeholder="Lucky Strike Cigarettes" required />
                </div>
                
                <div class="form-group">
                    <label for="audience">Target Audience *</label>
                    <input type="text" id="audience" bind:value={targetAudience} class="classic-input" placeholder="American Housewives" required />
                </div>
            </div>
            
            <div class="form-group">
                <label for="values">Brand Values / Tone</label>
                <textarea id="values" bind:value={brandValues} class="classic-textarea" rows="3" placeholder="Sophisticated, Nostalgic, Bold..."></textarea>
            </div>
            
            {#if error}
                <div class="error-msg">{error}</div>
            {/if}
            
            <div class="actions">
                <button type="submit" class="btn-primary" disabled={loading}>
                    {#if loading}SAVING...{:else}ESTABLISH CONTEXT →{/if}
                </button>
            </div>
        </form>
    </div>
</div>

<style>
    .onboard-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--color-bg);
        padding: 2rem;
    }
    
    .onboard-card {
        width: 100%;
        max-width: 600px;
        padding: 4rem;
        background: white;
        border: 1px solid var(--color-border);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    }
    
    .header { text-align: center; margin-bottom: 3rem; }
    .header h1 { font-family: var(--font-serif); font-size: 2.5rem; color: var(--color-navy); margin: 1rem 0 0.5rem; }
    .sub { font-family: var(--font-mono); color: var(--color-smoke); font-size: 0.9rem; }
    
    .badge-classic-small { font-family: var(--font-sans); font-weight: 800; font-size: 0.7rem; letter-spacing: 0.2em; color: var(--color-brass); }
    
    .form-group { margin-bottom: 1.5rem; }
    .split-group { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
    
    label { display: block; font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-navy); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .classic-input, .classic-textarea {
        width: 100%;
        padding: 1rem;
        border: 1px solid var(--color-border);
        background: #fcfcfc;
        font-family: var(--font-sans);
        font-size: 1rem;
        transition: all 0.2s;
    }
    .classic-input:focus, .classic-textarea:focus { border-color: var(--color-navy); outline: none; background: white; }
    
    .actions { margin-top: 2rem; display: flex; justify-content: flex-end; }
    
    .error-msg { color: #ef4444; font-family: var(--font-mono); font-size: 0.8rem; margin-top: 1rem; text-align: center; }
    
    @media (max-width: 600px) {
        .onboard-card { padding: 2rem; }
        .split-group { grid-template-columns: 1fr; }
    }
</style>