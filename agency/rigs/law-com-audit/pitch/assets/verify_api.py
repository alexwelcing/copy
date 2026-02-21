#!/usr/bin/env python3
"""
Verify Fal API connectivity and key validity.
"""

import os
import sys
import json
import urllib.request
import urllib.error


def verify():
    key = os.getenv("FAL_KEY")
    if not key:
        print("ERROR: FAL_KEY not set")
        print("Run: export FAL_KEY='your-key'")
        sys.exit(1)

    # Validate key format
    if ":" not in key:
        print("WARNING: FAL_KEY format may be incorrect")
        print("Expected format: key_id:key_secret")

    print(f"Testing API connection...")

    # Simple test request
    url = "https://fal.run/fal-ai/flux-pro/v1.1"
    headers = {
        "Authorization": f"Key {key}",
        "Content-Type": "application/json"
    }

    # Minimal test payload
    data = json.dumps({
        "prompt": "test",
        "image_size": "square",
        "num_images": 1,
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        # Don't actually wait for generation, just verify auth works
        with urllib.request.urlopen(req, timeout=30) as response:
            print("✓ API key is valid")
            print("✓ Connection successful")
            print("")
            print("Ready to generate assets.")
            return True

    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("✗ API key invalid or expired")
            print("Get a new key at: https://fal.ai/dashboard/keys")
        elif e.code == 403:
            print("✗ API access forbidden")
            print("Check your Fal account permissions")
        elif e.code == 402:
            print("✗ Insufficient credits")
            print("Add credits at: https://fal.ai/dashboard/billing")
        else:
            print(f"✗ HTTP {e.code}: {e.reason}")
        sys.exit(1)

    except urllib.error.URLError as e:
        print(f"✗ Connection failed: {e.reason}")
        print("Check your internet connection")
        sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    verify()
