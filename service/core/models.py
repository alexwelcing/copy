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
    # Premium quality
    FLUX_PRO_1_1 = "fal-ai/flux-pro/v1.1"
    FLUX_PRO = "fal-ai/flux-pro"
    FLUX_REALISM = "fal-ai/flux-realism"
    FLUX_DEV = "fal-ai/flux/dev"

    # Turbo/Fast models - prioritize for campaign generation
    FLUX_SCHNELL = "fal-ai/flux/schnell"              # Fast + high quality
    FAST_SDXL = "fal-ai/fast-sdxl"                    # Balanced speed/quality
    SDXL_LIGHTNING = "fal-ai/fast-lightning-sdxl"    # Ultra fast
    LCM = "fal-ai/lcm"                                # Latency optimized

    # Stable Diffusion 3.5
    SD_3_5_LARGE = "fal-ai/stable-diffusion-v35-large"
    SD_3_5_MEDIUM = "fal-ai/stable-diffusion-v35-medium"

    # Text rendering specialists
    QWEN_IMAGE_2512 = "fal-ai/qwen-image-2512"        # Best for text in images
    LONGCAT_IMAGE = "fal-ai/longcat-image"            # Multilingual text

    # Design/Vector focus
    RECRAFT_V3 = "fal-ai/recraft-v3"
    IDEOGRAM_2 = "fal-ai/ideogram-v2"                 # Design + typography

    # Enterprise/Production
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
        """Best for rendering text within images."""
        return ImageModels.QWEN_IMAGE_2512

    @staticmethod
    def get_best_for_realism():
        """Best for photorealistic output."""
        return ImageModels.FLUX_PRO_1_1

    @staticmethod
    def get_best_for_editing():
        """Best for natural language image editing."""
        return EditModels.NANO_BANANA_PRO_EDIT

    @staticmethod
    def get_turbo():
        """Fastest generation with good quality - use for campaigns."""
        return ImageModels.FLUX_SCHNELL

    @staticmethod
    def get_lightning():
        """Ultra-fast generation - use for rapid iteration."""
        return ImageModels.SDXL_LIGHTNING

    @staticmethod
    def get_best_for_design():
        """Best for design/vector/typography work."""
        return ImageModels.RECRAFT_V3

    @staticmethod
    def get_turbo_models():
        """Returns all fast/turbo models for campaign generation."""
        return [
            ImageModels.FLUX_SCHNELL,
            ImageModels.FAST_SDXL,
            ImageModels.SDXL_LIGHTNING,
            ImageModels.LCM
        ]
