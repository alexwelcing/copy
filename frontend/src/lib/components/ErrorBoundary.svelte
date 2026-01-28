<script lang="ts">
    export let title: string = "Something went wrong";
    export let message: string = "An unexpected error occurred. Please try again.";
    export let onRetry: (() => void) | null = null;
    export let onDismiss: (() => void) | null = null;
</script>

<div class="error-boundary paper-card" role="alert">
    <div class="error-icon">⚠</div>
    <div class="error-content">
        <h4 class="error-title">{title}</h4>
        <p class="error-message">{message}</p>
    </div>
    <div class="error-actions">
        {#if onRetry}
            <button class="btn-primary btn-sm" on:click={onRetry}>
                Try Again
            </button>
        {/if}
        {#if onDismiss}
            <button class="btn-secondary btn-sm" on:click={onDismiss}>
                Dismiss
            </button>
        {/if}
    </div>
</div>

<style>
    .error-boundary {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 2rem;
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
    }

    .error-icon {
        font-size: 2rem;
        color: #ef4444;
        margin-bottom: 1rem;
    }

    .error-content {
        margin-bottom: 1.5rem;
    }

    .error-title {
        font-family: var(--font-serif, Georgia, serif);
        font-size: 1.1rem;
        color: #991b1b;
        margin: 0 0 0.5rem 0;
    }

    .error-message {
        font-family: var(--font-mono, monospace);
        font-size: 0.8rem;
        color: #7f1d1d;
        margin: 0;
        max-width: 400px;
    }

    .error-actions {
        display: flex;
        gap: 0.75rem;
    }

    /* Button styles - matching existing design system */
    .btn-sm {
        padding: 0.5rem 1rem;
        font-size: 0.7rem;
    }
</style>
