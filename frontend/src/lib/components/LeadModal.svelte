<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { saveLead } from '$lib/api';
    import { fade, scale } from 'svelte/transition';

    export let campaign: string;
    
    const dispatch = createEventDispatcher();
    
    let email = '';
    let role = '';
    let company = '';
    let loading = false;
    let error = '';

    async function handleSubmit() {
        if (!email) {
            error = 'Email is required';
            return;
        }
        
        loading = true;
        try {
            await saveLead({
                email,
                role,
                company,
                source: campaign,
                intent: 'access_terminal'
            });
            
            // Mock Login (Grant Access)
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem('agency_user_token', 'lead-' + Math.random());
                // Also set an anon ID if missing
                if (!localStorage.getItem('agency_anon_id')) {
                    localStorage.setItem('agency_anon_id', crypto.randomUUID());
                }
            }
            
            dispatch('success');
        } catch (e) {
            error = 'Failed to process request. Please try again.';
        } finally {
            loading = false;
        }
    }
</script>

<div class="modal-backdrop" on:click={() => dispatch('close')} transition:fade>
    <div class="modal-card" on:click|stopPropagation transition:scale>
        <button class="close-btn" on:click={() => dispatch('close')}>&times;</button>
        
        <div class="modal-header">
            <span class="badge-classic">ACCESS GRANTED</span>
            <h3>Initialize Terminal</h3>
            <p>Enter your credentials to unlock the full High Era suite for your {campaign} project.</p>
        </div>

        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-group">
                <label>WORK EMAIL</label>
                <input type="email" bind:value={email} placeholder="name@company.com" class="classic-input" required />
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>ROLE</label>
                    <input type="text" bind:value={role} placeholder="e.g. Director" class="classic-input" />
                </div>
                <div class="form-group">
                    <label>COMPANY</label>
                    <input type="text" bind:value={company} placeholder="Company Name" class="classic-input" />
                </div>
            </div>

            {#if error}
                <p class="error-msg">{error}</p>
            {/if}

            <button type="submit" class="btn-primary w-full" disabled={loading}>
                {#if loading}
                    INITIALIZING...
                {:else}
                    ENTER TERMINAL →
                {/if}
            </button>
        </form>
    </div>
</div>

<style>
    .modal-backdrop {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(4px);
        z-index: 1000; display: flex; align-items: center; justify-content: center;
    }
    
    .modal-card {
        background: var(--color-bg); width: 90%; max-width: 500px;
        padding: 3rem; border: 1px solid var(--color-navy);
        box-shadow: 0 20px 50px rgba(0,0,0,0.3); position: relative;
    }
    
    .close-btn {
        position: absolute; top: 1rem; right: 1rem; background: none; border: none;
        font-size: 1.5rem; color: var(--color-smoke); cursor: pointer;
    }
    
    .modal-header { text-align: center; margin-bottom: 2rem; }
    .modal-header h3 { font-family: var(--font-serif); font-size: 2rem; margin: 1rem 0 0.5rem; color: var(--color-navy); }
    .modal-header p { font-size: 0.9rem; color: var(--color-smoke); }
    
    .form-group { margin-bottom: 1.5rem; }
    .form-group label { display: block; font-family: var(--font-mono); font-size: 0.7rem; color: var(--color-navy); margin-bottom: 0.5rem; letter-spacing: 0.1em; }
    
    .classic-input {
        width: 100%; padding: 0.8rem; background: white; border: 1px solid var(--color-border);
        font-family: var(--font-sans); font-size: 1rem;
    }
    .classic-input:focus { border-color: var(--color-brass); outline: none; }
    
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    
    .error-msg { color: var(--color-error); font-size: 0.8rem; text-align: center; margin-bottom: 1rem; }
    
    .w-full { width: 100%; }
</style>
