"""
Image Generation Service

Client for generating images via Cloud Function or direct Fal API.
Integrates with the agency system for asset generation.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class GeneratedImage:
    """Result of image generation."""
    success: bool
    gcs_url: Optional[str] = None
    gcs_path: Optional[str] = None
    error: Optional[str] = None
    model: Optional[str] = None
    seed: Optional[int] = None


@dataclass
class ImageRequest:
    """Image generation request."""
    prompt: str
    output_path: str
    model: str = "flux-pro-1.1"
    size: str = "landscape_16_9"
    tenant_id: str = "default"


class ImageGenerationService:
    """
    Service for generating images.

    Uses Cloud Function by default, falls back to direct Fal API if configured.
    """

    # Available models
    MODELS = {
        "flux-pro-1.1": "fal-ai/flux-pro/v1.1",
        "flux-pro": "fal-ai/flux-pro",
        "flux-dev": "fal-ai/flux/dev",
        "flux-schnell": "fal-ai/flux/schnell",
        "recraft-v3": "fal-ai/recraft-v3",
        "ideogram-v2": "fal-ai/ideogram/v2",
    }

    # Size presets
    SIZES = {
        "square": "1024x1024",
        "square_hd": "1408x1408",
        "landscape_4_3": "1408x1024",
        "landscape_16_9": "1920x1080",
        "portrait_3_4": "1024x1408",
        "portrait_9_16": "1080x1920",
    }

    def __init__(
        self,
        function_url: Optional[str] = None,
        fal_key: Optional[str] = None,
        default_tenant: str = "default"
    ):
        """
        Initialize the service.

        Args:
            function_url: URL of the generate-image Cloud Function
            fal_key: Direct Fal API key (fallback if function not available)
            default_tenant: Default tenant ID for asset organization
        """
        self.function_url = function_url or os.environ.get("IMAGE_FUNCTION_URL")
        self.fal_key = fal_key or os.environ.get("FAL_KEY")
        self.default_tenant = default_tenant

        if not self.function_url and not self.fal_key:
            raise ValueError(
                "Either IMAGE_FUNCTION_URL or FAL_KEY must be set. "
                "Deploy the Cloud Function or provide a direct Fal API key."
            )

    def generate(self, request: ImageRequest) -> GeneratedImage:
        """
        Generate a single image.

        Args:
            request: Image generation request

        Returns:
            GeneratedImage with result or error
        """
        if self.function_url:
            return self._generate_via_function(request)
        else:
            return self._generate_direct(request)

    def generate_batch(
        self,
        requests: List[ImageRequest],
        max_workers: int = 3
    ) -> List[GeneratedImage]:
        """
        Generate multiple images in parallel.

        Args:
            requests: List of image generation requests
            max_workers: Maximum concurrent generations

        Returns:
            List of GeneratedImage results (same order as requests)
        """
        results = [None] * len(requests)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(self.generate, req): idx
                for idx, req in enumerate(requests)
            }

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = GeneratedImage(
                        success=False,
                        error=str(e)
                    )

        return results

    def _generate_via_function(self, request: ImageRequest) -> GeneratedImage:
        """Generate via Cloud Function."""
        payload = {
            "prompt": request.prompt,
            "model": request.model,
            "size": request.size,
            "output_path": request.output_path,
            "tenant_id": request.tenant_id or self.default_tenant,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.function_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=600) as response:
                result = json.loads(response.read().decode("utf-8"))

                if result.get("success"):
                    return GeneratedImage(
                        success=True,
                        gcs_url=result.get("gcs_url"),
                        gcs_path=result.get("gcs_path"),
                        model=result.get("model"),
                        seed=result.get("seed"),
                    )
                else:
                    return GeneratedImage(
                        success=False,
                        error=result.get("error", "Unknown error")
                    )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            try:
                error_data = json.loads(error_body)
                error_msg = error_data.get("error", f"HTTP {e.code}")
            except:
                error_msg = f"HTTP {e.code}: {error_body[:200]}"
            return GeneratedImage(success=False, error=error_msg)

        except Exception as e:
            return GeneratedImage(success=False, error=str(e))

    def _generate_direct(self, request: ImageRequest) -> GeneratedImage:
        """Generate directly via Fal API (fallback)."""
        model_id = self.MODELS.get(request.model, f"fal-ai/{request.model}")
        url = f"https://fal.run/{model_id}"

        # Parse size
        size_map = {
            "square": {"width": 1024, "height": 1024},
            "square_hd": {"width": 1408, "height": 1408},
            "landscape_4_3": {"width": 1408, "height": 1024},
            "landscape_16_9": {"width": 1920, "height": 1080},
            "portrait_3_4": {"width": 1024, "height": 1408},
            "portrait_9_16": {"width": 1080, "height": 1920},
        }
        size = size_map.get(request.size, size_map["landscape_16_9"])

        payload = {
            "prompt": request.prompt,
            "image_size": size,
            "num_images": 1,
        }

        headers = {
            "Authorization": f"Key {self.fal_key}",
            "Content-Type": "application/json"
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))

                images = result.get("images", [])
                if not images:
                    return GeneratedImage(success=False, error="No images returned")

                image_url = images[0].get("url")

                # Note: Direct mode returns Fal URL, not GCS
                # Would need to download and upload to GCS separately
                return GeneratedImage(
                    success=True,
                    gcs_url=image_url,  # Actually Fal URL
                    model=request.model,
                    seed=result.get("seed"),
                )

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            return GeneratedImage(success=False, error=f"Fal API error {e.code}: {error_body[:200]}")

        except Exception as e:
            return GeneratedImage(success=False, error=str(e))


# Convenience function
def generate_image(
    prompt: str,
    output_path: str,
    model: str = "flux-pro-1.1",
    size: str = "landscape_16_9",
    tenant_id: str = "default",
    function_url: Optional[str] = None
) -> GeneratedImage:
    """
    Generate a single image.

    Quick helper function for one-off generation.

    Args:
        prompt: Image description
        output_path: Where to save in GCS (e.g., "pitch/cover.png")
        model: Model to use (flux-pro-1.1, flux-schnell, etc.)
        size: Size preset (landscape_16_9, square, etc.)
        tenant_id: Tenant ID for organization
        function_url: Optional Cloud Function URL override

    Returns:
        GeneratedImage with result
    """
    service = ImageGenerationService(function_url=function_url)
    request = ImageRequest(
        prompt=prompt,
        output_path=output_path,
        model=model,
        size=size,
        tenant_id=tenant_id
    )
    return service.generate(request)
