import sys
import os
import asyncio
import json
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import fal_client
from service.core.executor import get_executor
from service.api.schemas import SkillName, WorkRequest
from service.core.assets import get_asset_manager
from service.core.models import ImageModels, VideoModels

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)

class DogfoodLoop:
    def __init__(self):
        load_dotenv()
        self.executor = get_executor()
        self.asset_manager = get_asset_manager()
        self.state_path = "scripts/dogfood_state.json" 
        self.load_state()
        
        if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
            os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]

    def load_state(self):
        if os.path.exists(self.state_path):
            with open(self.state_path, "r") as f:
                self.state = json.load(f)
        else:
            self.state = {"current_target": "homepage", "completed": [], "iterations": {}}

    def save_state(self):
        with open(self.state_path, "w") as f:
            json.dump(self.state, f, indent=4)

    async def evaluate_asset(self, asset_type, asset_url, prompt):
        log(f"Evaluating {asset_type}...")
        eval_task = f"""
        Evaluate this generated {asset_type} for our 'High Era' brand identity (Vision: Madison Avenue 2026).
        Prompt used: {prompt}
        Asset URL: {asset_url}
        
        Criteria:
        1. **Tactile Realism**: Must look like 35mm film or high-end print. NO CGI sheen.
        2. **Era Fusion**: Mid-century elements (wood, brass, paper) blended with subtle futuristic data/holograms.
        3. **Composition**: Clean, uncluttered, suitable for a landing page hero (space for text).
        
        Return JSON ONLY: {{ "status": "approved" | "rejected", "critique": "...", "refined_prompt": "..." }}
        """
        
        request = WorkRequest(
            skill=SkillName.MARKETING_PSYCHOLOGY,
            model="claude-sonnet-4-5-20250929",
            task=eval_task
        )
        
        try:
            result = await asyncio.to_thread(self.executor.execute, request)
            text = result.output
            # Basic JSON extraction
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                 eval_data = json.loads(text[start:end])
                 return eval_data
            else:
                 return {"status": "rejected", "critique": "JSON parse error", "refined_prompt": prompt}
        except Exception as e:
            return {"status": "rejected", "critique": f"Eval failed: {e}", "refined_prompt": prompt}

    async def process_target(self, target_name):
        log(f"--- Processing Target: {target_name} ---")
        
        # Initial prompts based on VISION.md
        prompts = {
            "homepage": "Cinematic 35mm film shot, mid-century executive desk with a vintage typewriter connected to a glowing holographic data stream, warm golden hour lighting, dust particles, shallow depth of field, Kodak Portra 400, high texture.",
            "video": "Subtle slow pan across a mahogany desk with scattered blueprints and a glowing glass tablet, cinematic lighting, 24fps film grain."
        }

        current_prompt = prompts.get(target_name, "Abstract cinematic marketing data visualization, mid-century style.")
        
        for attempt in range(3):
            log(f"Attempt {attempt + 1} for {target_name}...")
            
            try:
                if target_name == "homepage":
                    log(f"Step 1: Generating Hero Image ({ImageModels.FLUX_PRO_1_1})...")
                    image_asset = await self.asset_manager.generate_image(
                        current_prompt, 
                        model=ImageModels.FLUX_PRO_1_1
                    )
                    log(f"Asset URL: {image_asset['url']}")
                    
                    evaluation = await self.evaluate_asset("image", image_asset['url'], current_prompt)
                
                elif target_name == "video":
                     log(f"Step 1: Generating Background Video ({VideoModels.LTX_VIDEO_DISTILLED})...")
                     # Note: Using LTX for speed in dev loop, envisioning Kling for Prod
                     video_asset = await self.asset_manager.generate_video(
                         current_prompt,
                         model=VideoModels.LTX_VIDEO_DISTILLED
                     )
                     log(f"Asset URL: {video_asset['url']}")
                     evaluation = await self.evaluate_asset("video", video_asset['url'], current_prompt)
                
                else:
                    break

                log(f"Result: {evaluation['status'].upper()} - {evaluation['critique']}")
                
                if evaluation['status'] == "approved":
                    self.state["completed"].append(target_name)
                    self.save_state()
                    log(f"Target {target_name} APPROVED and SAVED.")
                    break
                else:
                    if evaluation.get('refined_prompt'):
                        current_prompt = evaluation['refined_prompt']
                        log("Retrying with refined prompt...")
                    else:
                        log("Rejected but no refinement provided. Retrying same prompt...")

            except Exception as e:
                log(f"Error: {str(e)}")
                await asyncio.sleep(5)

    async def run(self):
        log("Dogfood Loop (High Era Edition) Started.")
        targets = ["homepage"] # Focus on Hero first
        for target in targets:
            if target not in self.state.get("completed", []):
                await self.process_target(target)
        log("All targets processed.")

if __name__ == "__main__":
    loop = DogfoodLoop()
    asyncio.run(loop.run())