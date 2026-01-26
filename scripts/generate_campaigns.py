"""
Campaign Generator Script.

Generates 50 unique landing pages for hyper-specific target demographics.
"""

import sys
import os
import asyncio
import json
import random
from typing import List, Dict
from slugify import slugify

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.core.executor import get_executor
from service.api.schemas import SkillName, WorkRequest
from service.core.assets import get_asset_manager
from service.core.models import ImageModels

CAMPAIGNS_FILE = "frontend/src/lib/data/campaigns.json"

class CampaignGenerator:
    def __init__(self):
        self.executor = get_executor()
        self.asset_manager = get_asset_manager()
        self.existing_campaigns = []
        if os.path.exists(CAMPAIGNS_FILE):
            with open(CAMPAIGNS_FILE, "r") as f:
                try:
                    self.existing_campaigns = json.load(f)
                except:
                    pass

    async def generate_target_list(self) -> List[str]:
        """Ask Claude for 20 hyper-specific niche demographics."""
        print("Generating target demographics...")
        task = """
        Generate a JSON list of 20 highly specific, obscure B2B or prosumer target demographics.
        Focus on industries like Maritime, Heavy Industry, Scientific Research, or Restoration.
        Avoid generic tech roles.
        
        Examples: 
        - "Underwater Welding Contractors"
        - "Church Organ Restorers"
        - "Cryogenic Lab Technicians"
        - "Bespoke Neon Sign Benders"
        - "Rare Book Archivists"
        
        OUTPUT FORMAT: JSON List of strings only. ["Target 1", "Target 2", ...]
        """
        req = WorkRequest(skill=SkillName.MARKETING_IDEAS, task=task, model="claude-sonnet-4-5-20250929")
        result = self.executor.execute(req)
        try:
            text = result.output
            start = text.find("[")
            end = text.rfind("]") + 1
            return json.loads(text[start:end])
        except Exception as e:
            print(f"Error parsing targets: {e}")
            return []

    async def process_target(self, target: str):
        print(f"Processing: {target}")
        slug = slugify(target)
        
        # Skip if already exists
        if any(c['slug'] == slug for c in self.existing_campaigns):
            print(f"Skipping {target} (exists)")
            return

        # 1. Generate Copy & Image Prompt in one go (save latency)
        task = f"""
        Create content for a landing page targeting: {target}.
        Brand Voice: 'High Era' (Mid-Century Modern, Sophisticated, Tactile).
        
        OUTPUT JSON ONLY:
        {{
            "headline": "A clever, sophisticated headline (Mad Men style)",
            "subheadline": "A clear value prop addressing their specific pain point",
            "pain_point_copy": "1 short paragraph on why generic tools fail them",
            "solution_copy": "1 short paragraph on how our tailored craftsmanship helps",
            "image_prompt": "A detailed prompt for FLUX Pro. Subject: A mid-century {target} workspace. Elements: Period-correct tools blended with subtle holographic data. Style: Cinematic 35mm, Kodak Portra 400, Golden Hour, No CGI sheen."
        }}
        """
        
        req = WorkRequest(skill=SkillName.COPYWRITING, task=task, model="claude-sonnet-4-5-20250929")
        try:
            res = await asyncio.to_thread(self.executor.execute, req)
            text = res.output
            content = json.loads(text[text.find("{"):text.rfind("}")+1])
        except Exception as e:
            print(f"Copy gen failed for {target}: {e}")
            return

        # 2. Generate Image
        try:
            print(f"Generating Asset for {target}...")
            asset = await self.asset_manager.generate_image(
                content['image_prompt'], 
                model=ImageModels.FLUX_PRO_1_1
            )
            
            campaign = {
                "title": target,
                "slug": slug,
                "target_audience": target,
                "headline": content['headline'],
                "subheadline": content['subheadline'],
                "pain_point_copy": content['pain_point_copy'],
                "solution_copy": content['solution_copy'],
                "hero_url": asset['url'],
                "asset_prompt_summary": content['image_prompt'][:50] + "..."
            }
            
            # Atomic append
            self.existing_campaigns.append(campaign)
            with open(CAMPAIGNS_FILE, "w") as f:
                json.dump(self.existing_campaigns, f, indent=2)
            
            print(f"Saved campaign: {slug}")
            
        except Exception as e:
            print(f"Asset gen failed for {target}: {e}")

    async def run(self):
        targets = await self.generate_target_list()
        print(f"Found {len(targets)} targets.")
        
        # Batch processing (semaphores to control rate limit)
        # We'll do batches of 3 to be safe with rate limits and timeouts
        semaphore = asyncio.Semaphore(3)

        async def sem_task(tgt):
            async with semaphore:
                await self.process_target(tgt)

        # Shuffle and take 50 (or all)
        # Check against existing
        todo = [t for t in targets if not any(c['slug'] == slugify(t) for c in self.existing_campaigns)]
        
        print(f"Processing {len(todo)} new targets...")
        tasks = [sem_task(t) for t in todo]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    gen = CampaignGenerator()
    asyncio.run(gen.run())
