<script lang="ts">
    export let product = "";
    export let audience = "";
    export let value = "";
</script>

<div class="mad-lib">
    I am building a 
    <span class="input-wrapper">
        <input 
            type="text" 
            bind:value={product} 
            placeholder="[Product/Service]" 
            class="mad-input"
            style:width="{Math.max(product.length || 15, 10)}ch"
        />
        <span class="underline"></span>
    </span>
    for 
    <span class="input-wrapper">
        <input 
            type="text" 
            bind:value={audience} 
            placeholder="[Target Audience]" 
            class="mad-input"
            style:width="{Math.max(audience.length || 15, 10)}ch"
        />
        <span class="underline"></span>
    </span>
    that focuses on 
    <span class="input-wrapper">
        <input 
            type="text" 
            bind:value={value} 
            placeholder="[Core Value/USP]" 
            class="mad-input"
            style:width="{Math.max(value.length || 15, 10)}ch"
        />
        <span class="underline"></span>
    </span>.
</div>

<style>
    .mad-lib {
        font-family: var(--font-serif);
        font-size: 1.25rem;
        line-height: 2;
        color: var(--color-navy);
    }

    .input-wrapper {
        position: relative;
        display: inline-block;
        margin: 0 0.25rem;
    }

    .mad-input {
        background: transparent;
        border: none;
        font-family: var(--font-mono);
        font-size: 1rem;
        color: var(--color-brass);
        padding: 0 0.5rem;
        outline: none;
        transition: color 0.3s ease;
        min-width: 120px;
    }

    .mad-input::placeholder {
        color: var(--color-text-muted);
        opacity: 0.5;
        font-family: var(--font-serif);
        font-style: italic;
    }

    .underline {
        position: absolute;
        bottom: 4px;
        left: 0;
        width: 100%;
        height: 1px;
        background: var(--color-border);
        transition: background 0.3s ease, height 0.3s ease;
    }

    .mad-input:focus + .underline {
        background: var(--color-brass);
        height: 2px;
    }
</style>
