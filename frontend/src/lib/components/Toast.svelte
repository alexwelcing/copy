<script lang="ts">
    import { fade, fly } from 'svelte/transition';
    import { flip } from 'svelte/animate';
    import { toasts, type ToastMessage } from '$lib/stores/toast';

    function getIcon(type: ToastMessage['type']): string {
        switch (type) {
            case 'success': return '✓';
            case 'error': return '✕';
            case 'warning': return '⚠';
            case 'info': return 'ℹ';
            default: return '';
        }
    }
</script>

<div class="toast-container" aria-live="polite" aria-label="Notifications">
    {#each $toasts as toast (toast.id)}
        <div
            class="toast toast-{toast.type}"
            role="alert"
            in:fly={{ y: -20, duration: 200 }}
            out:fade={{ duration: 150 }}
            animate:flip={{ duration: 200 }}
        >
            <span class="toast-icon">{getIcon(toast.type)}</span>
            <span class="toast-message">{toast.message}</span>
            <button class="toast-dismiss" on:click={() => toasts.dismiss(toast.id)} aria-label="Dismiss">
                ×
            </button>
        </div>
    {/each}
</div>

<style>
    .toast-container {
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        max-width: 400px;
    }

    .toast {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 1.25rem;
        background: var(--color-bg, white);
        border: 1px solid var(--color-border, #e2e8f0);
        border-left-width: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        font-family: var(--font-mono, monospace);
        font-size: 0.8rem;
    }

    .toast-success {
        border-left-color: #10b981;
    }

    .toast-error {
        border-left-color: #ef4444;
        background: #fef2f2;
    }

    .toast-warning {
        border-left-color: #f59e0b;
        background: #fffbeb;
    }

    .toast-info {
        border-left-color: var(--color-navy, #1e3a5f);
    }

    .toast-icon {
        font-weight: bold;
        flex-shrink: 0;
    }

    .toast-success .toast-icon { color: #10b981; }
    .toast-error .toast-icon { color: #ef4444; }
    .toast-warning .toast-icon { color: #f59e0b; }
    .toast-info .toast-icon { color: var(--color-navy, #1e3a5f); }

    .toast-message {
        flex: 1;
        color: var(--color-navy, #1e3a5f);
    }

    .toast-dismiss {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        color: var(--color-smoke, #64748b);
        padding: 0;
        line-height: 1;
    }

    .toast-dismiss:hover {
        color: var(--color-navy, #1e3a5f);
    }
</style>
