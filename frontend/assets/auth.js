/**
 * Firebase Auth for Agency Studio
 *
 * Provides sign-in/sign-up/sign-out, token management,
 * and authenticated fetch wrapper for /api/* calls.
 */

const firebaseConfig = {
  apiKey: window.__FIREBASE_CONFIG__?.apiKey || "AIzaSyDEFAULT",
  authDomain: window.__FIREBASE_CONFIG__?.authDomain || "agency-studio.firebaseapp.com",
  projectId: window.__FIREBASE_CONFIG__?.projectId || "agency-studio",
};

firebase.initializeApp(firebaseConfig);

const AgencyAuth = {
  _user: null,
  _token: null,
  _listeners: [],

  /** Get current Firebase user */
  getUser() {
    return this._user;
  },

  /** Get cached ID token, refreshing if needed */
  async getIdToken() {
    if (!this._user) return null;
    try {
      this._token = await this._user.getIdToken();
      return this._token;
    } catch (e) {
      console.error("Failed to get ID token:", e);
      return null;
    }
  },

  /** Get anonymous ID from localStorage */
  getAnonymousId() {
    let id = localStorage.getItem("agency_anon_id");
    if (!id) {
      id = "anon_" + crypto.randomUUID();
      localStorage.setItem("agency_anon_id", id);
    }
    return id;
  },

  /** Sign in with email and password */
  async signIn(email, password) {
    const cred = await firebase.auth().signInWithEmailAndPassword(email, password);
    return cred.user;
  },

  /** Create account with email and password */
  async signUp(email, password) {
    const cred = await firebase.auth().createUserWithEmailAndPassword(email, password);
    return cred.user;
  },

  /** Sign in with Google */
  async signInWithGoogle() {
    const provider = new firebase.auth.GoogleAuthProvider();
    const cred = await firebase.auth().signInWithPopup(provider);
    return cred.user;
  },

  /** Sign out */
  async signOut() {
    await firebase.auth().signOut();
    this._user = null;
    this._token = null;
  },

  /** Register a callback for auth state changes */
  onAuthStateChanged(callback) {
    this._listeners.push(callback);
  },

  /**
   * Authenticated fetch wrapper.
   * Attaches Bearer token for signed-in users or X-Anonymous-ID for anon.
   */
  async fetch(url, options = {}) {
    const headers = { ...(options.headers || {}) };

    if (this._user) {
      const token = await this.getIdToken();
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    } else {
      headers["X-Anonymous-ID"] = this.getAnonymousId();
    }

    return fetch(url, { ...options, headers });
  },

  /** Redirect to Stripe Checkout for a plan */
  async checkout(plan) {
    const token = await this.getIdToken();
    if (!token) {
      window.location.href = "/login?redirect=/pricing";
      return;
    }

    const res = await fetch("/api/checkout", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ plan }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Checkout failed");
    }

    const { url } = await res.json();
    window.location.href = url;
  },

  /** Open Stripe Customer Portal */
  async openBillingPortal() {
    const token = await this.getIdToken();
    if (!token) return;

    const res = await fetch("/api/billing/portal", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Could not open billing portal");
    }

    const { url } = await res.json();
    window.location.href = url;
  },
};

// Listen for auth state changes and update nav
firebase.auth().onAuthStateChanged((user) => {
  AgencyAuth._user = user;

  // Update nav
  const navAuth = document.getElementById("nav-auth");
  if (navAuth) {
    if (user) {
      navAuth.innerHTML =
        '<a href="/dashboard">Dashboard</a>' +
        '<span style="color: var(--muted); font-size: 0.8rem; margin-left: 2rem;">' +
        user.email +
        "</span>" +
        '<a href="#" onclick="AgencyAuth.signOut().then(() => window.location.href = \'/\'); return false;">Sign Out</a>';
    } else {
      navAuth.innerHTML = '<a href="/login">Sign In</a>';
    }
  }

  // Notify listeners
  AgencyAuth._listeners.forEach((cb) => {
    try {
      cb(user);
    } catch (e) {
      console.error("Auth listener error:", e);
    }
  });
});

// Expose globally
window.AgencyAuth = AgencyAuth;
