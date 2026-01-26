import asyncio
import os
import json
import time
import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import fal_client
from service.core.executor import get_executor
from service.api.schemas import SkillName, WorkRequest
from service.core.assets import get_asset_manager
from dotenv import load_dotenv

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    try:
        with open("dogfood_debug.log", "a") as f:
            f.write(line + "\n")
    except:
        pass

class DogfoodLoop:
    def __init__(self):
        load_dotenv()
        self.executor = get_executor()
        self.asset_manager = get_asset_manager()
        self.state_path = "dogfood_state.json"
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
        Evaluate this generated {asset_type} for our 'High Era' brand.
        Prompt used: {prompt}
        Asset URL: {asset_url}
        
        Criteria:
        1. NO nonsense text. If there is text, it must be legible or purely impressionistic/blurred.
        2. High realism. NO neon, NO digital-glow, NO futurism.
        3. Sophistication. Does it look like a 1960s Madison Avenue agency?
        
        Return JSON ONLY: {{'status': 'approved' | 'rejected', 'critique': '...', 'refined_prompt': '...'}}
        """
        
        request = WorkRequest(
            skill=SkillName.MARKETING_PSYCHOLOGY,
            model="claude-sonnet-4-5-20250929",
            task=eval_task
        )
        
        try:
            result = await asyncio.to_thread(self.executor.execute, request)
            text = result.output
            log(f"Evaluation raw output: {text[:100]}...")
            eval_data = json.loads(text[text.find("{"):text.rfind("}")+1])
            return eval_data
        except Exception as e:
            log(f"Evaluation error: {str(e)}")
            return {"status": "rejected", "critique": f"Evaluation failed: {str(e)}", "refined_prompt": prompt}

    async def process_target(self, target_name):
        log(f"--- Processing Target: {target_name} ---")
        
        for attempt in range(3):
            log(f"Attempt {attempt + 1} for {target_name} video...")
            
            image_prompt = "Cinematic 35mm film shot of a mid-century advertising storyboard on a corkboard, hand-drawn sketches, elegant typography, soft natural lighting, Madison Avenue office background, Kodak Portra 400."
            
            try:
                log("Generating Keyframe with Flux Pro...")
                image_asset = await self.asset_manager.generate_image(image_prompt, model="fal-ai/flux-pro/v1.1")
                log(f"Keyframe generated: {image_asset['url']}")
                
                video_prompt = "Subtle cinematic zoom into the storyboard, dust particles in sunbeams, film grain, 24fps."
                
                log("Animating Keyframe with LTX2 Distilled...")
                handler = await asyncio.to_thread(
                    fal_client.submit,
                    "fal-ai/ltx-2-19b/distilled/image-to-video",
                    arguments={
                        "image_url": image_asset['url'],
                        "prompt": video_prompt
                    }
                )
                video_result = handler.get()
                video_url = video_result['video']['url']
                log(f"Video generated: {video_url}")
                
                evaluation = await self.evaluate_asset("video", video_url, video_prompt)
                log(f"Evaluation: {evaluation['status'].upper()} - {evaluation['critique']}")
                
                if evaluation['status'] == "approved":
                    self.state["iterations"][target_name] = "complete"
                    self.save_state()
                    break
                else:
                    log(f"Iterating... Refined prompt: {evaluation.get('refined_prompt')}")
            except Exception as e:
                log(f"Error in process_target: {str(e)}")
                await asyncio.sleep(5)

    async def run(self):
        try:
            log("Loop started.")
            targets = ["homepage", "copywriting-skill", "video-skill", "seo-skill"]
            for target in targets:
                await self.process_target(target)
                log(f"Completed target: {target}")
        except Exception as e:
            log(f"CRITICAL LOOP ERROR: {str(e)}")

if __name__ == "__main__":
    loop = DogfoodLoop()
    asyncio.run(loop.run())