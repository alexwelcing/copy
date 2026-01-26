import json
import requests
import os
from pathlib import Path

def run_audit():
    project_root = Path(__file__).parent.parent
    with open(project_root / 'frontend/src/routes/+page.svelte', 'r') as f:
        content = f.read()

    payload = {
        "skill": "page-cro",
        "model": "claude-sonnet-4-5-20250929", # Use Claude for the audit as it's better for deep analysis
        "task": "Perform a comprehensive CRO audit of our homepage to prepare for our public launch as a specialized AI Marketing Agency service.",
        "context": {
            "product": "Marketing Agency Platform",
            "goal": "Convert visitors into users who want to use our AI skills for their own business.",
            "target_audience": "Founders, Marketers, Solo-preneurs"
        },
        "content": content
    }

    try:
        response = requests.post('http://localhost:8080/work', json=payload)
        response.raise_for_status()
        result = response.json()
        
        with open('dogfood_cro_audit.md', 'w') as f:
            f.write(result['output'])
        print("Audit saved to dogfood_cro_audit.md")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_audit()