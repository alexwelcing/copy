fal.ai is less “one model zoo” and more “a well-run interdimensional airport”: 600+ endpoints across image, video, audio, 3D, plus utility and routing layers. The clean way to understand “what’s available” is to think in families + tasks, because listing every endpoint one-by-one would be a phonebook (and it changes constantly). fal even provides an official Model Search API specifically so you can always pull the current catalog programmatically.

Below is a thorough breakdown by category, including what each major family is best at, and how to choose depending on quality, speed, controllability, and licensing.

1) How fal.ai organizes “models”
Endpoint IDs (the thing you actually call)

Each model is exposed as an endpoint_id like:

fal-ai/stable-diffusion-v35-large

fal-ai/veo3.1/fast

fal-ai/meshy/v6-preview/text-to-3d

You can see tons of examples directly in the public gallery list.

The official up-to-date catalog: Model Search API

fal’s Model search endpoint supports:

List mode: paginate everything

Find mode: fetch metadata for specific endpoint_ids

Search mode: filter by query, category, status
It can also expand each model with OpenAPI schema (expand=openapi-3.0).

Example (real endpoint from docs):

curl --request GET \
  --url "https://api.fal.ai/v1/models?category=image-to-video&status=active&limit=50" \
  --header "Authorization: Key $FAL_KEY"


(That https://api.fal.ai/v1/models base and the query params are straight from fal docs. )

Gallery vs API

Gallery (/explore/models) is great for browsing and discovering categories (text-to-image, image-to-video, training, etc.).

Model Search API is what you use to build product UX (dropdowns, auto-selection, internal registries).

2) Image generation (Text to Image): the main “art engines”

These are your “make me a new image from a prompt” endpoints.

A) Stable Diffusion family (fast, familiar, controllable)

Best for: proven workflows, ControlNet pipelines, “I know my SD knobs,” quick iteration.

Key endpoints:

SD 3.5 Large / Medium: improved prompt understanding, typography, complex scenes, efficiency (relative to older SD).

Fast SDXL: a speed-focused SDXL endpoint.

SDXL Lightning: “speed of light” SDXL variant.

SDXL ControlNet options (example: canny / union): for edge-guided generation and multi-control setups.

Latent Consistency (LCM): fewer steps for fast output (great when latency matters).

When to pick what:

Need speed → SDXL Lightning / LCM

Need prompt fidelity + modern SD → SD 3.5 Large

Need structure/control → SDXL ControlNet variants

B) Qwen Image (strong text rendering + editing-adjacent behavior)

Best for: text in images, sharper prompt adherence, “I need the words to actually look like words.”

Qwen Image: positioned as a foundation image model with advances in complex text rendering and precise editing.

Qwen Image 2512: explicitly calls out better text rendering, finer textures, more realistic humans vs earlier Qwen Image.

If your product repeatedly needs posters, labels, UI-like text, Qwen is often a smart first try.

C) ByteDance Seedream (unified generation + editing)

Best for: teams that want a single model family to handle both creation and modification.

Seedream 4.5 text-to-image: up to high-res (noted as up to 4MP on its page), and described as unified generation + editing architecture.

Seedream edit: natural language editing, multi-image workflows.

Pick Seedream if your workflow is “generate → tweak → regenerate” and you want fewer model switches.

D) Bria FIBO (structured controllability, enterprise-safe data story)

Best for: predictable, repeatable control, enterprise workflows, “licensed data” emphasis.

Fibo (text-to-image) exists as bria/fibo/generate and is presented as a controllable model for production use.

Fibo Lite emphasizes similar control with improved latency (distilled/two-stage).

E) LongCat (multilingual text rendering + efficient)

Best for: multilingual text overlays + photorealism with deployment efficiency emphasis.

LongCat Image highlights multilingual text rendering and a 6B parameter architecture.

3) Image editing (Image to Image): “change this picture”

This category includes inpainting, semantic edits, background removal, upscaling, and “edit by instruction.”

A) FLUX editing endpoints (Kontext + inpainting variants)

Best for: high-quality edits, reference-image guided changes, brand/style consistency via LoRA.

FLUX Kontext [pro]: designed for targeted local edits and whole-scene transformations using text + reference images.

FLUX Kontext [max]: positioned for improved prompt adherence and typography consistency.

Flux General Inpainting: inpainting with support for LoRA, ControlNet, IP-Adapter (i.e., lots of control surfaces).

B) “Edit-with-language” premium style (Nano Banana Pro)

Best for: semantic edits without fiddly masks, character consistency, text rendering.

Nano Banana Pro edit (fal-ai/nano-banana-pro/edit) is described as Google’s state-of-the-art image generation/editing model and calls out semantic editing + higher-end capability set.

C) Bria Fibo Edit (structured, controllable editing)

Best for: production editing where you want structured instructions + masks.

Fibo Edit: “maximum controllability and transparency” by combining JSON + Mask + Image.

Includes task-specific variants like erase-by-text, add-object-by-text, rewrite text, colorize, restyle in the Bria family.

D) Classic SD/SDXL editing utilities

Best for: familiar inpainting/outpainting workflows.

Inpaint (SD + SDXL): fal-ai/inpaint is explicitly “inpaint images with SD and SDXL.”

4) Video generation: text-to-video, image-to-video, and video editing

Video is where the catalog gets spicy fast. The big split:

Text → Video (pure generation)

Image → Video (animate a still / keep identity)

Video → Video (restyle, remix, background removal, motion transfer)

A) Top-tier “cinematic + audio” generators

Best for: marketing clips, cinematic shots, dialogue + sound, higher budgets.

Veo 3.1 (Fast and standard variants): fal offers Veo 3.1 endpoints including fast text-to-video and extend-video; pricing guidance is shown on the model pages.

Sora 2 / Sora 2 Pro: text-to-video and image-to-video endpoints, with audio noted on the pages.

Seedance 1.5 Pro: explicitly positioned as generating video with synchronized audio from a single prompt (text-to-video and image-to-video).

Kling Video: multiple versions and modes including text-to-video, image-to-video, lipsync, and motion control variants.

When to choose what

Need best “film-like” and have budget → Sora 2 Pro / Veo 3.1

Need audio + tight sync in a single pass → Seedance 1.5 Pro

Need variety of creative controls and strong ecosystem of modes → Kling

B) Practical “creator workhorses” (quality + cost balance)

Best for: social clips, quick iterations, image-anchored animation.

PixVerse v5 / v5.5: image-to-video endpoints; v5.5 page highlights resolution options and pricing ranges.

MiniMax Hailuo-02 (standard/pro): image-to-video with multiple resolutions; pro explicitly notes 1080p.

Kandinsky 5 / 5 Pro / distilled: text-to-video and image-to-video; distilled emphasizes lightweight speed.

Wan video family: multiple endpoints including text-to-video (and also image-to-image/text-to-image in Wan v2.6 listings).

C) Video-to-video and “editing the motion”

Best for: remixing existing video, style transfer, background removal, relighting.

Sora 2 remix (video-to-video): transform existing videos with text/image prompts while preserving motion/structure.

LTX Video 13B distilled (multiconditioning): blends prompts + images + video inputs for transformations.

VEED video background removal: production-friendly subject extraction from video.

BiRefNet video background removal: a video variant is listed as well.

Kling motion control: transfer movements from a reference video to a character image (standard vs pro).

5) Audio: speech, transcription, music, and dialogue
A) Text-to-speech and dialogue generation

Best for: voice agents, narration, multi-speaker dialogue.

ElevenLabs Eleven v3 (text-to-dialogue): positioned for realistic dialogues, streaming supported.

MiniMax Speech models appear in the gallery list (e.g., speech-02-hd).

B) Speech-to-text (ASR)

Best for: transcription pipelines, captioning, indexing audio/video.

Whisper (fal-ai/whisper): transcription and translation.

Wizper: Whisper v3 Large optimized by fal for faster performance (same WER claim).

ElevenLabs Speech-to-Text (Scribe v1): separate ASR option.

There’s also a generic speech-to-text/turbo endpoint.

C) Music generation

Best for: instant background tracks, jingle drafts, lyric-to-song experiments.

CassetteAI music generator: 30s sample quickly, full tracks in seconds (per page).

YuE (lyrics-to-song): explicitly “lyrics into full songs.”

MiniMax Music: text-to-music with “production-ready” framing and pay-per-generation note.

Gallery also lists ElevenLabs Music.

6) 3D: text-to-3D, image-to-3D, retexture, remesh
A) Meshy (high quality, production-ready)

Best for: high-quality creative assets, textured models, 3D workflows.

Meshy v6 Preview text-to-3D: supports preview vs full (untextured vs textured) and positions itself as “latest model with best quality.”

Meshy retexture (v5): apply new textures with text or reference images, supports PBR.

Meshy remesh (v5): remesh/export utility.

Meshy multi-image-to-3D: better geometry via multiple views (but slower).

B) Tripo / TripoSR (speed and prototyping)

Best for: fast 3D from a single image, iteration velocity.

Tripo3D v2.5 image-to-3D: single-image to 3D, production-ready GLB/OBJ claims on page.

Tripo multiview-to-3D: multiple images for better reconstruction.

TripoSR: explicitly emphasizes very fast reconstruction from single images.

7) Utility “glue models”: segmentation, upscaling, captioning, etc.

These don’t generate “new worlds,” they make your pipeline usable.

Background removal (image)

Bria RMBG 2.0: foreground extraction, licensed-data emphasis.

BiRefNet: high-resolution segmentation; includes multiple modes on API page.

Upscaling

ESRGAN: classic super-resolution baseline.

Clarity Upscaler: “high fidelity” upscaling positioning.

Recraft Crisp Upscale: focus on refining small details and faces.

Ideogram Upscale: 2x upscale plus optional prompt refinement.

Flux Vision Upscaler: fidelity + creativity framing.

Vision understanding helpers

Florence-2 tasks (captioning, region-to-category): prompt-based vision foundation model approach.

8) LLMs and routing on fal: “bring your own brain, keep fal’s infra”

fal supports “LLM endpoints” that are essentially routers to many providers/models.

A) Any LLM / Any VLM (powered by OpenRouter)

fal-ai/any-llm: use models from a selected catalog via OpenRouter, with a fal tutorial showing usage and an example model name like anthropic/claude-3.5-sonnet.

openrouter/router: direct OpenRouter LLM routing endpoint; fal notes token-based billing and streaming.

OpenAI-compatible shapes: OpenRouter endpoints that mimic OpenAI APIs (chat completions, responses, embeddings).

Vision and audio router endpoints exist too (openrouter/router/vision, /audio).

Best for: products that want one integration surface but the flexibility to swap underlying LLMs without rewriting your app.

9) A practical “what should I use?” cheat sheet

Here’s a blunt-but-useful chooser:

If you’re building an image product

Fast iteration / SD ecosystem → fal-ai/fast-sdxl, fal-ai/fast-lightning-sdxl, fal-ai/lcm

Modern SD quality → fal-ai/stable-diffusion-v35-large

Text inside images matters → fal-ai/qwen-image-2512 or fal-ai/longcat-image

Editing with high control → bria/fibo-edit/edit or FLUX inpainting/general inpainting

Natural-language “just do it” editing → fal-ai/nano-banana-pro/edit

If you’re building a video product

Premium cinematic + audio → Veo 3.1, Sora 2 Pro, Seedance 1.5 Pro

Image animation / creator clips → PixVerse v5.5, Hailuo-02, Kling

Edit existing video → Sora remix, LTX multiconditioning, VEED background removal

If you’re building audio features

Voice/dialogue → Eleven v3 (dialogue)

Transcription → Whisper / Wizper / ElevenLabs STT

Music → CassetteAI, YuE, MiniMax Music

If you’re building 3D

Highest quality assets → Meshy v6 preview (text-to-3D / image-to-3D), plus retexture/remesh tools

Fast prototyping → TripoSR / Tripo3D

10) The “be thorough” closer: how to get the full list you can trust

Because fal’s catalog is living and constantly expanding, the most thorough workflow is:

Use the Model Search API to pull the authoritative list (filter by category and status=active).

For each endpoint you care about, fetch OpenAPI schema via expand=openapi-3.0 so your codegen/types stay correct.

Use the gallery (/explore/models) to discover new “best-of” groupings and newly added endpoints.