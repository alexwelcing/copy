import requests
import sys
import re
from typing import Dict, Optional

class DeploymentVerifier:
    def __init__(self, status_file: str = "deployment_status.txt"):
        self.urls = self._load_urls(status_file)
        self.session = requests.Session()
        # Mock a valid anonymous user to pass auth checks
        self.session.headers.update({
            "User-Agent": "Agency-Verifier/1.0",
            "Content-Type": "application/json",
            "X-Anonymous-ID": "deployment-verifier-001"
        })

    def _load_urls(self, filepath: str) -> Dict[str, str]:
        """Parse the deployment_status.txt file to get service URLs."""
        urls = {}
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Simple parsing logic
            for line in content.split('\n'):
                if "marketing-agency-api" in line:
                    urls['api'] = self._extract_url(line)
                elif "marketing-agency-frontend" in line:
                    urls['frontend'] = self._extract_url(line)
                elif "marketing-agency-worker" in line:
                    urls['worker'] = self._extract_url(line)
            
            return urls
        except FileNotFoundError:
            print(f"❌ Error: {filepath} not found. Run 'gcloud run services list' first.")
            sys.exit(1)

    def _extract_url(self, line: str) -> Optional[str]:
        """Extract https URL from a line."""
        match = re.search(r'(https://[^\s]+)', line)
        return match.group(1) if match else None

    def check_api_health(self):
        """Directly check the backend API health."""
        url = self.urls.get('api')
        if not url:
            print("⚠️  Skipping API Health: No URL found")
            return

        print(f"Testing API Health ({url})...", end=" ", flush=True)
        try:
            res = self.session.get(f"{url}/health", timeout=10)
            if res.status_code == 200:
                data = res.json()
                print(f"✅ OK (v{data.get('version')})")
            else:
                print(f"❌ FAILED ({res.status_code})")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    def check_frontend_load(self):
        """Check if the frontend loads."""
        url = self.urls.get('frontend')
        if not url:
            print("⚠️  Skipping Frontend Load: No URL found")
            return

        print(f"Testing Frontend Load ({url})...", end=" ", flush=True)
        try:
            res = self.session.get(url, timeout=10)
            if res.status_code == 200:
                print("✅ OK")
            else:
                print(f"❌ FAILED ({res.status_code})")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    def check_full_integration(self):
        """Test the full flow: Frontend Proxy -> Backend API."""
        frontend_url = self.urls.get('frontend')
        if not frontend_url:
            print("⚠️  Skipping Integration Test: No Frontend URL")
            return

        # Note: Frontend proxy is at /api/work, not /work
        proxy_url = f"{frontend_url}/api/work"
        
        print(f"Testing Integration via Proxy ({proxy_url})...", end=" ", flush=True)
        
        payload = {
            "skill": "marketing-ideas",
            "task": "Sanity check. Return the word 'CONFIRMED' and nothing else.",
            "model": "claude-sonnet-4-5-20250929" # Should be fast
        }

        try:
            # We must use POST, and we must provide X-Anonymous-ID (handled in init)
            res = self.session.post(proxy_url, json=payload, timeout=30)
            
            if res.status_code == 200:
                data = res.json()
                if data.get('output'):
                    print("✅ OK")
                else:
                    print(f"⚠️  200 OK but empty output: {data}")
            elif res.status_code == 401:
                print("❌ FAILED (401 Unauthorized) - Proxy or Backend rejected auth.")
            elif res.status_code == 504:
                print("❌ FAILED (504 Gateway Timeout) - Backend took too long.")
            else:
                print(f"❌ FAILED ({res.status_code})")
                print(f"   Response: {res.text[:200]}...")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    def run(self):
        print("=== 🚀 Deployment Verifier ===")
        print(f"Loaded {len(self.urls)} services.")
        print("-" * 30)
        
        self.check_api_health()
        self.check_frontend_load()
        self.check_full_integration()
        print("-" * 30)
        print("Done.")

if __name__ == "__main__":
    verifier = DeploymentVerifier()
    verifier.run()
