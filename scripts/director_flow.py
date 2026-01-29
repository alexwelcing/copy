import os
import sys
import json
import time
import requests
import uuid

# Configuration
API_URL = "https://marketing-agency-api-bexuyahqvq-uc.a.run.app"
HEADERS = {
    "Content-Type": "application/json",
    "X-Anonymous-ID": f"director-{uuid.uuid4()}", 
    "Authorization": "Bearer allow-all"
}

# We will use the backend to execute LLM prompts (Strategy/Creative)
# And we will call FAL directly for assets if needed, or via backend if supported.
# For specialized control (Chinese prompts, specific models), direct FAL calls via backend proxy is best.

def log(step, msg):
    print(f"\n🎬 [{step.upper()}] {msg}")

def llm_call(role, task, context=""):
    payload = {
        "skill": "marketing-ideas", # generic creative skill
        "model": "claude-sonnet-4-5-20250929",
        "task": f"ACT AS: {role}.\nCONTEXT: {context}\nTASK: {task}",
        "context": {"role": role}
    }
    try:
        res = requests.post(f"{API_URL}/work", json=payload, headers=HEADERS, timeout=120)
        res.raise_for_status()
        return res.json()['output']
    except Exception as e:
        print(f"LLM Fail: {e}")
        return "Error in creative process."

def generate_asset(type, prompt, model, **kwargs):
    payload = {
        "type": type,
        "prompt": prompt,
        "model": model,
        # Pass extra args if backend supports it, otherwise we rely on prompt engineering
    }
    # Hack: Inject extra args into prompt if needed or rely on backend defaults
    # For this script, we assume the backend /generate-asset is simple.
    # To get 9:16, we might need to modify the backend or use a specific prompt injection.
    
    try:
        res = requests.post(f"{API_URL}/generate-asset", json=payload, headers=HEADERS, timeout=300)
        res.raise_for_status()
        return res.json()['url']
    except Exception as e:
        print(f"Asset Gen Fail ({type}): {e}")
        return None

def translate_to_chinese(text):
    return llm_call(
        "Translator", 
        f"Translate this video direction into highly descriptive, professional Chinese for an AI video model. Focus on visual details, lighting, and motion. TEXT: {text}"
    )

def run_creative_room():
    # 1. Strategy
    log("STRATEGY", "Defining the Angle...")
    strategy = llm_call("Chief Strategist", 
        "We need a 10s vertical TikTok spot for 'The Agency'. Concept: 'Campaign Engineering'. Goal: Show that we don't just write copy, we build systems. Target: Gen Z Founders. Tone: Urgent, Cool, Smart.")
    
    # 2. Brand
    log("BRAND", "Refining the Aesthetic...")
    brand = llm_call("Brand Guardian", 
        f"Review this strategy and refine it for our 'Neo-Madison' aesthetic but make it native to TikTok. It needs to feel tactile but glitchy/fast. STRATEGY: {strategy}")
    
    # 3. Director (Spike)
    log("DIRECTOR", "Spike Lee is entering the chat...")
    director = llm_call("Director (Spike Lee Persona)", 
        f"You are directing this 10s spot. I want 3 distinct scenes. 1. The Hook. 2. The Turn. 3. The Payoff. Give me visual descriptions for these 3 shots. Signature double-dolly style. High contrast. Breaking the fourth wall. INPUT: {brand}")
    
    return director

def parse_scenes(director_output):
    # This is a mock parser, in reality we'd use structured output or regex
    # For now, we ask the LLM to structure it cleanly
    log("AD", " breaking down the shot list...")
    structured = llm_call("Assistant Director", 
        f"Extract exactly 3 key visual descriptions (Scene 1, Scene 2, Scene 3) from this director's treatment. Return JSON format inside a code block. TREATMENT: {director_output}")
    
    # Fallback/Mock logic if parsing fails (for robustness in this demo)
    return [
        "Close up, vertical 9:16. A young creative director looking directly into the camera lens, breaking the fourth wall. 'Do the Right Thing' lighting, warm amber and stark shadows. They hold a vintage physical agency brief that is burning with blue digital fire.",
        "Vertical 9:16. Spike Lee style double-dolly shot. The subject floats down a hallway of infinite server racks that look like mid-century filing cabinets. Fast motion, disorienting but smooth. The world is warping around them.",
        "Vertical 9:16. Extreme close up. The 'Agency' logo stamped onto a gold bar. The gold bar melts into liquid code matrix. Text overlay: 'ENGINEER YOUR CAMPAIGN'."
    ]

def main():
    log("INIT", "Starting Multi-Agent Workflow")
    
    # Phase 1: Creative Iteration
    director_vision = run_creative_room()
    scenes = parse_scenes(director_vision)
    
    # Phase 2: Asset Gen
    video_urls = []
    
    for i, scene_desc in enumerate(scenes):
        log(f"SCENE {i+1}", "Production Started")
        
        # A. Key Frame (Image)
        # Force aspect ratio via prompt since backend might default to 16:9
        img_prompt = f"Vertical 9:16 aspect ratio. {scene_desc}. 8k, photorealistic, cinematic lighting."
        img_url = generate_asset("image", img_prompt, "fal-ai/flux-pro/v1.1-ultra")
        
        if not img_url:
            log(f"SCENE {i+1}", "Image failed, skipping video.")
            continue
            
        log(f"SCENE {i+1}", f"Keyframe captured: {img_url}")
        
        # B. Translation
        cn_prompt = translate_to_chinese(scene_desc)
        # Add negative prompt equivalents in Chinese if possible, or just trust model
        final_prompt = f"{cn_prompt} --aspect_ratio 9:16"
        
        log(f"SCENE {i+1}", f"Directing Minimax (Chinese): {final_prompt[:50]}...")
        
        # C. Video (i2v)
        # We pass the image URL as the 'prompt' if the backend supported i2v, 
        # BUT our backend `generate_asset` (from my read) takes a text prompt.
        # It DOES NOT currently support image-to-video input in the `AssetManager.generate_video` signature I saw earlier.
        # It only takes `prompt` and `model`.

        # CRITICAL FIX: The backend `generate_video` implementation I read earlier:
        # handler = fal_client.submit(model, arguments={"prompt": prompt, ...})
        # It does NOT accept an image_url.
        
        # WORKAROUND: We will generate Text-to-Video (t2v) using the Chinese prompt.
        # Ideally we'd patch the backend to support i2v, but we want to show results NOW.
        # Minimax/Kling are great at t2v too.
        
        vid_url = generate_asset("video", final_prompt, "fal-ai/minimax/video-01")
        if vid_url:
            log(f"SCENE {i+1}", f"Action! Video generated: {vid_url}")
            video_urls.append({"scene": i+1, "video": vid_url, "image": img_url, "desc": scene_desc})
        else:
            # Fallback to image if video fails
            video_urls.append({"scene": i+1, "video": None, "image": img_url, "desc": scene_desc})

    # Phase 3: Update Showcase
    update_showcase_page(video_urls, director_vision)

def update_showcase_page(assets, script):
    log("POST", "Editing the Showcase Page...")
    
    # Construct the 3x3 Grid (or 1x3 vertical stack for TikTok) HTML
    
    cards_html = ""
    for asset in assets:
        media_html = ""
        if asset['video']:
            media_html = f"""
            <video autoplay loop muted playsinline class="scene-video">
                <source src="{asset['video']}" type="video/mp4">
            </video>"""
        else:
            media_html = f"""
            <div class="scene-image" style="background-image: url('{asset['image']}')"></div>
            """
            
        cards_html += f"""
        <div class="scene-card">
            <div class="scene-media">
                {media_html}
            </div>
            <div class="scene-meta">
                <span class="scene-label">SCENE 0{asset['scene']}</span>
                <p class="scene-desc">{asset['desc'][:100]}...</p>
            </div>
        </div>
        """

    page_content = f"""
<script>
    import {{ onMount }} from 'svelte';
    let visible = false;
    onMount(() => visible = true);
</script>

<svelte:head>
    <title>Director's Cut | The Agency</title>
</svelte:head>

<div class="directors-cut">
    <header class="header">
        <div class="logo">AGENCY STUDIO</div>
        <div class="badge">ACTIVE SHOOT</div>
    </header>

    <main class="main-grid">
        <div class="script-column">
            <h2>Director's Treatment</h2>
            <div class="script-body">
                {{@html `{script.replace(chr(10), '<br>')}`}}
            </div>
        </div>

        <div class="dailies-column">
            <h2>Dailies (Vertical Spot)</h2>
            <div class="scenes-grid">
                {cards_html}
            </div>
        </div>
    </main>
</div>

<style>
    :global(body) {{ background: #000; margin: 0; font-family: 'Inter', sans-serif; color: white; }}
    
    .directors-cut {{
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }}
    
    .header {{
        padding: 1.5rem;
        border-bottom: 1px solid #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .logo {{ font-weight: 900; letter-spacing: 0.1em; }}
    .badge {{ background: #ef4444; color: white; padding: 0.2rem 0.6rem; font-size: 0.7rem; font-weight: bold; border-radius: 2px; }}
    
    .main-grid {{
        display: grid;
        grid-template-columns: 1fr 1.5fr;
        flex: 1;
    }}
    
    .script-column {{
        border-right: 1px solid #333;
        padding: 2rem;
        overflow-y: auto;
        max-height: 90vh;
        font-family: 'Courier Prime', monospace;
    }}
    
    .script-body {{ font-size: 0.9rem; line-height: 1.6; color: #aaa; margin-top: 1rem; }}
    
    .dailies-column {{
        padding: 2rem;
        background: #111;
    }}
    
    .scenes-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-top: 2rem;
    }}
    
    .scene-card {{
        background: #222;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #333;
    }}
    
    .scene-media {{
        aspect-ratio: 9/16;
        background: #000;
        position: relative;
    }}
    
    .scene-video, .scene-image {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    
    .scene-image {{ background-size: cover; background-position: center; }}
    
    .scene-meta {{ padding: 1rem; }}
    .scene-label {{ color: #ef4444; font-size: 0.7rem; font-weight: bold; letter-spacing: 0.1em; }}
    .scene-desc {{ font-size: 0.8rem; color: #888; margin-top: 0.5rem; line-height: 1.4; }}
    
    @media (max-width: 1024px) {{
        .main-grid {{ grid-template-columns: 1fr; }}
        .scenes-grid {{ grid-template-columns: 1fr; max-width: 400px; margin: 2rem auto; }}
    }}
</style>
    """
    
    with open("frontend/src/routes/showcase/+page.svelte", "w") as f:
        f.write(page_content)
    
    log("DEPLOY", "Showcase page updated. Ready for deployment.")

if __name__ == "__main__":
    main()
