import os
import fal_client
import httpx
from typing import Optional, Dict, Any
from service.core.storage import get_storage
from service.core.models import ImageModels, VideoModels, AudioModels
from pathlib import Path

class AssetManager:
    """Manages AI asset generation via FAL and storage in GCS."""
    
    def __init__(self):
        self.storage = get_storage()
        # Ensure FAL_KEY is set correctly for the client
        if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
            os.environ["FAL_KEY"] = os.environ["FAL_API_KEY"]

    async def generate_image(self, prompt: str, model: str = ImageModels.FLUX_PRO_1_1, sync: bool = True) -> Dict[str, Any]:
        """Generates an image and saves it to GCS."""
        print(f"Generating image with model: {model}")
        
        handler = fal_client.submit(
            model,
            arguments={
                "prompt": prompt,
                "image_size": "landscape_16_9"
            }
        )
        
        result = handler.get()
        image_url = result['images'][0]['url']
        
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            if response.status_code == 200:
                filename = f"generated_{handler.request_id}.png"
                local_path = f"/tmp/{filename}"
                with open(local_path, "wb") as f:
                    f.write(response.content)
                
                # Upload to GCS
                self.storage.upload_file(local_path, f"images/{filename}")
                public_url = f"https://storage.googleapis.com/{self.storage.bucket_name}/images/{filename}"
                os.remove(local_path)
                
                return {
                    "id": handler.request_id,
                    "url": public_url,
                    "gcs_path": f"images/{filename}",
                    "prompt": prompt,
                    "model": model
                }
        
        raise Exception("Failed to download generated image")

    async def generate_video(self, prompt: str, model: str = VideoModels.KLING_V1_STANDARD) -> Dict[str, Any]:
        """Generates a video and saves it to GCS."""
        print(f"Generating video with model: {model}")
        
        handler = fal_client.submit(
            model,
            arguments={
                "prompt": prompt,
                "aspect_ratio": "16:9"
            }
        )
        
        result = handler.get()
        video_url = result['video']['url']
        
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url)
            if response.status_code == 200:
                filename = f"generated_{handler.request_id}.mp4"
                local_path = f"/tmp/{filename}"
                with open(local_path, "wb") as f:
                    f.write(response.content)
                
                # Upload to GCS
                self.storage.upload_file(local_path, f"videos/{filename}")
                public_url = f"https://storage.googleapis.com/{self.storage.bucket_name}/videos/{filename}"
                os.remove(local_path)
                
                return {
                    "id": handler.request_id,
                    "url": public_url,
                    "gcs_path": f"videos/{filename}",
                    "prompt": prompt,
                    "model": model
                }

    async def generate_audio(self, prompt: str, model: str = AudioModels.STABLE_AUDIO) -> Dict[str, Any]:
        """Generates audio and saves it to GCS."""
        print(f"Generating audio with model: {model}")
        
        handler = fal_client.submit(
            model,
            arguments={
                "prompt": prompt,
                "seconds_total": 30
            }
        )
        
        result = handler.get()
        audio_url = result['audio']['url']
        
        async with httpx.AsyncClient() as client:
            response = await client.get(audio_url)
            if response.status_code == 200:
                filename = f"generated_{handler.request_id}.mp3"
                local_path = f"/tmp/{filename}"
                with open(local_path, "wb") as f:
                    f.write(response.content)
                
                # Upload to GCS
                self.storage.upload_file(local_path, f"audio/{filename}")
                public_url = f"https://storage.googleapis.com/{self.storage.bucket_name}/audio/{filename}"
                os.remove(local_path)
                
                return {
                    "id": handler.request_id,
                    "url": public_url,
                    "gcs_path": f"audio/{filename}",
                    "prompt": prompt,
                    "model": model
                }
        
        raise Exception("Failed to download generated audio")

# Singleton
_asset_manager: Optional[AssetManager] = None

def get_asset_manager() -> AssetManager:
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager