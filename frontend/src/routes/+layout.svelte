<script lang="ts">
	import '../app.css';
</script>

<div class="app">
	<header class="main-header">
		<div class="container">
			<div class="header-content">
				<a href="/" class="logo">
					<span class="logo-text">HIGH<span class="text-italic">ERA</span></span>
				</a>
				<nav class="main-nav">
					<a href="/">Terminal</a>
					<a href="/skills">Index</a>
					<a href="/assess">Lab</a>
				</nav>
			</div>
		</div>
	</header>

	<main>
		<slot />
	</main>

	<footer class="main-footer">
		<div class="container">
			<div class="footer-grid">
				<div class="footer-brand">
					<span class="logo-text">HIGH<span class="text-italic">ERA</span></span>
					<p>Established 2026. Automated Creative Infrastructure.</p>
				</div>
				<div class="footer-meta">
					<span class="meta-label">SYSTEM: ONLINE</span>
					<span class="meta-label">VERSION: 1.0.0</span>
				</div>
			</div>
		</div>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	.main-header {
		border-bottom: 2px solid var(--color-navy);
		padding: 1.5rem 0;
		background: var(--color-bg);
		position: sticky;
		top: 0;
		z-index: 100;
	}

	.header-content {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.logo {
		text-decoration: none;
	}

	.logo-text {
		font-family: var(--font-serif);
		font-size: 1.5rem;
		font-weight: 900;
		color: var(--color-navy);
		letter-spacing: -0.02em;
	}

    .logo-text .text-italic {
        font-weight: 400;
        margin-left: 2px;
    }

	.main-nav {
		display: flex;
		gap: 2rem;
	}

	.main-nav a {
		color: var(--color-navy);
		font-size: 0.75rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		transition: all 0.2s ease;
        text-decoration: none;
        border-bottom: 1px solid transparent;
        padding-bottom: 2px;
	}

	.main-nav a:hover {
		color: var(--color-brass);
        border-bottom-color: var(--color-brass);
	}

    .nav-dim {
        opacity: 0.5;
    }

	main {
		flex: 1;
	}

	.main-footer {
		border-top: 1px solid var(--color-border);
		padding: 4rem 0;
        background: white;
	}

    .footer-grid {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .footer-brand p {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        color: var(--color-smoke);
    }

    .footer-meta {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        text-align: right;
    }

    .meta-label {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        color: var(--color-smoke);
        letter-spacing: 0.1em;
    }
</style>
