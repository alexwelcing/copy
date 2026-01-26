"""
FAL Model Library
Registry of curated and available FAL.ai models.
"""

from enum import Enum

class FalModel(str, Enum):
    """Base class for FAL models."""
    pass

class ImageModels(FalModel):
    """Text-to-Image Generation"""
    FLUX_PRO_1_1 = "fal-ai/flux-pro/v1.1"
    FLUX_PRO = "fal-ai/flux-pro"
    FLUX_REALISM = "fal-ai/flux-realism"
    FLUX_SCHNELL = "fal-ai/flux/schnell"
    FLUX_DEV = "fal-ai/flux/dev"
    
    SD_3_5_LARGE = "fal-ai/stable-diffusion-v35-large"
    SD_3_5_MEDIUM = "fal-ai/stable-diffusion-v35-medium"
    FAST_SDXL = "fal-ai/fast-sdxl"
    SDXL_LIGHTNING = "fal-ai/fast-lightning-sdxl"
    
    QWEN_IMAGE_2512 = "fal-ai/qwen-image-2512"  # Best for text
    LONGCAT_IMAGE = "fal-ai/longcat-image" # Multilingual text
    
    RECRAFT_V3 = "fal-ai/recraft-v3" # Vector/Design focus
    BRIA_FIBO = "bria/fibo/generate"

class EditModels(FalModel):
    """Image-to-Image / Editing"""
    NANO_BANANA_PRO_EDIT = "fal-ai/nano-banana-pro/edit" # Edit by instruction
    
    FLUX_KONTEXT_PRO = "fal-ai/flux-pro/v1.1-fill" # Context aware fill/edit
    FLUX_INPAINT = "fal-ai/flux/inpainting"
    
    SDXL_INPAINT = "fal-ai/inpaint"
    BRIA_FIBO_EDIT = "bria/fibo-edit/edit"

class VideoModels(FalModel):
    """Video Generation"""
    LUMA_DREAM_MACHINE = "fal-ai/luma-dream-machine"
    
    KLING_V1_STANDARD = "fal-ai/kling-video/v1/standard/text-to-video"
    KLING_V1_PRO = "fal-ai/kling-video/v1/pro/text-to-video"
    
    LTX_VIDEO_DISTILLED = "fal-ai/ltx-2-19b/distilled/text-to-video"
    LTX_IMAGE_TO_VIDEO = "fal-ai/ltx-2-19b/distilled/image-to-video"
    
    MINIMAX_HAILUO = "fal-ai/minimax-video"
    
    VEO_3_1 = "fal-ai/veo3.1/fast" # Google Veo
    SORA_2_PRO = "fal-ai/sora-2/pro" # (Placeholder/Availability check needed)

class AudioModels(FalModel):
    """Audio Generation"""
    STABLE_AUDIO = "fal-ai/stable-audio"
    ELEVENLABS_V3 = "fal-ai/elevenlabs/v3"
    MINIMAX_MUSIC = "fal-ai/minimax-music"
    WHISPER = "fal-ai/whisper"

class ModelRegistry:
    """Helper to find models by capability."""
    
    @staticmethod
    def get_best_for_text():
        return ImageModels.QWEN_IMAGE_2512
        
    @staticmethod
    def get_best_for_realism():
        return ImageModels.FLUX_PRO_1_1
        
    @staticmethod
    def get_best_for_editing():
        return EditModels.NANO_BANANA_PRO_EDIT
