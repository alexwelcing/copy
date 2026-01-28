<script lang="ts">
	import '../app.css';
    import { onMount } from 'svelte';
    import { auth, googleProvider } from '$lib/firebase';
    import { signInWithPopup, signOut, onAuthStateChanged } from 'firebase/auth';
    import Toast from '$lib/components/Toast.svelte';

    let isLoggedIn = false;
    let userName = '';

    onMount(() => {
        if (!auth) return;
        
        // Listen for auth state changes
        const unsubscribe = onAuthStateChanged(auth, async (user) => {
            if (user) {
                isLoggedIn = true;
                userName = user.displayName || user.email || 'Agent';
                const token = await user.getIdToken();
                localStorage.setItem('agency_user_token', token);
            } else {
                isLoggedIn = false;
                userName = '';
                localStorage.removeItem('agency_user_token');
            }
        });
        return unsubscribe;
    });

    async function handleLogin() {
        if (!auth || !googleProvider) {
            alert("Auth not initialized (Missing config?)");
            return;
        }
        try {
            await signInWithPopup(auth, googleProvider);
            // State update handled by onAuthStateChanged
            window.location.reload(); 
        } catch (error) {
            console.error("Login failed:", error);
            alert("Authentication failed. Please try again.");
        }
    }

    async function handleLogout() {
        if (auth) {
            await signOut(auth);
            window.location.reload();
        }
    }
</script>

<div class="app">
	<Toast />
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
                <div class="header-auth">
                    {#if isLoggedIn}
                        <div class="user-badge">
                            <span class="status-dot"></span>
                            <span class="user-name">{userName}</span>
                            <button class="auth-btn-small" on:click={handleLogout}>Exit</button>
                        </div>
                    {:else}
                        <button class="auth-btn" on:click={handleLogin}>Verify Credentials</button>
                    {/if}
                </div>
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

    /* AUTH UI */
    .header-auth { display: flex; align-items: center; }
    .auth-btn {
        background: transparent; border: 1px solid var(--color-navy); color: var(--color-navy);
        padding: 0.5rem 1rem; font-size: 0.65rem; font-weight: 800; text-transform: uppercase;
        letter-spacing: 0.1em; cursor: pointer; transition: all 0.2s ease;
    }
    .auth-btn:hover { background: var(--color-navy); color: white; }
    
    .user-badge { display: flex; align-items: center; gap: 0.75rem; background: #f1f5f9; padding: 0.4rem 0.8rem; border-radius: 4px; border: 1px solid var(--color-border); }
    .status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; }
    .user-name { font-family: var(--font-mono); font-size: 0.65rem; color: var(--color-navy); font-weight: 700; }
    .auth-btn-small { background: none; border: none; font-size: 0.6rem; text-decoration: underline; color: var(--color-smoke); cursor: pointer; }

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
