<script lang="ts">
	import '../app.css';
</script>

<div class="app">
	<header>
		<div class="container">
			<div class="header-content">
				<a href="/" class="logo">
					<span class="logo-text">Marketing Agency</span>
				</a>
				<nav>
					<a href="/">Execute</a>
					<a href="/skills">Skills</a>
					<a href="https://github.com" target="_blank" rel="noopener">GitHub</a>
				</nav>
			</div>
		</div>
	</header>

	<main>
		<slot />
	</main>

	<footer>
		<div class="container">
			<p class="text-muted">
				23 marketing skills. Each one a complete framework.
			</p>
		</div>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	header {
		border-bottom: 1px solid var(--color-border);
		padding: 1rem 0;
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
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--color-text);
	}

	nav {
		display: flex;
		gap: 1.5rem;
	}

	nav a {
		color: var(--color-text-secondary);
		font-size: 0.9375rem;
		transition: color 0.15s ease;
	}

	nav a:hover {
		color: var(--color-text);
		text-decoration: none;
	}

	main {
		flex: 1;
		padding: 2rem 0;
	}

	footer {
		border-top: 1px solid var(--color-border);
		padding: 1.5rem 0;
		text-align: center;
	}
</style>
