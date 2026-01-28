<script lang="ts">
    export let lines: number = 3;
    export let variant: 'text' | 'card' | 'form' = 'text';
</script>

<div class="skeleton skeleton-{variant}" role="status" aria-label="Loading content">
    {#if variant === 'text'}
        {#each Array(lines) as _, i}
            <div 
                class="skeleton-line" 
                style="width: {i === lines - 1 ? '60%' : '100%'}"
            ></div>
        {/each}
    {:else if variant === 'card'}
        <div class="skeleton-card">
            <div class="skeleton-header"></div>
            <div class="skeleton-body">
                <div class="skeleton-line" style="width: 80%"></div>
                <div class="skeleton-line" style="width: 60%"></div>
            </div>
        </div>
    {:else if variant === 'form'}
        <div class="skeleton-form">
            <div class="skeleton-label"></div>
            <div class="skeleton-input"></div>
            <div class="skeleton-label" style="margin-top: 1rem"></div>
            <div class="skeleton-textarea"></div>
        </div>
    {/if}
    <span class="sr-only">Loading...</span>
</div>

<style>
    .skeleton {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .skeleton-line {
        height: 1rem;
        background: linear-gradient(90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        border-radius: 4px;
        margin-bottom: 0.75rem;
    }

    @keyframes shimmer {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }

    .skeleton-card {
        border: 1px solid var(--color-border, #e2e8f0);
        padding: 1.5rem;
    }

    .skeleton-header {
        height: 1.5rem;
        width: 40%;
        background: linear-gradient(90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        margin-bottom: 1rem;
        border-radius: 4px;
    }

    .skeleton-body {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .skeleton-form {
        display: flex;
        flex-direction: column;
    }

    .skeleton-label {
        height: 0.75rem;
        width: 30%;
        background: linear-gradient(90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        margin-bottom: 0.5rem;
        border-radius: 2px;
    }

    .skeleton-input {
        height: 2.5rem;
        background: linear-gradient(90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        border-radius: 4px;
    }

    .skeleton-textarea {
        height: 6rem;
        background: linear-gradient(90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        border-radius: 4px;
    }

    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
</style>
