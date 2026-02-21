"""
Cloud Function: Generate Image via Fal API

Handles image generation requests, calls Fal API, stores results in GCS.
Triggered via HTTP or Pub/Sub.

HTTP Request:
    POST /generate-image
    {
        "prompt": "A beautiful sunset",
        "model": "flux-pro-1.1",  // optional, defaults to flux-pro-1.1
        "size": "landscape_16_9", // optional
        "output_path": "pitch/cover.png",  // GCS path
        "tenant_id": "tenant123"  // for billing/organization
    }

Pub/Sub Message:
    Same JSON payload as HTTP request
"""

import os
import json
import base64
import urllib.request
import urllib.error
import functions_framework
from google.cloud import storage
from google.cloud import secretmanager


# Configuration
PROJECT_ID = os.environ.get("GCP_PROJECT", os.environ.get("GOOGLE_CLOUD_PROJECT"))
BUCKET_NAME = os.environ.get("GCS_BUCKET", "marketing-copy-assets")

# Model aliases
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
    "square": {"width": 1024, "height": 1024},
    "square_hd": {"width": 1408, "height": 1408},
    "landscape_4_3": {"width": 1408, "height": 1024},
    "landscape_16_9": {"width": 1920, "height": 1080},
    "portrait_3_4": {"width": 1024, "height": 1408},
    "portrait_9_16": {"width": 1080, "height": 1920},
}


def get_secret(secret_id: str) -> str:
    """Retrieve secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def get_fal_key() -> str:
    """Get Fal API key from Secret Manager or environment."""
    # Try environment first (for local testing)
    key = os.environ.get("FAL_KEY")
    if key:
        return key

    # Try Secret Manager
    try:
        return get_secret("fal-api-key")
    except Exception as e:
        raise ValueError(f"FAL_KEY not found in environment or Secret Manager: {e}")


def call_fal_api(prompt: str, model: str, size: dict, fal_key: str) -> dict:
    """Call Fal API to generate image."""

    # Resolve model alias
    model_id = MODELS.get(model, model)
    if not model_id.startswith("fal-ai/"):
        model_id = f"fal-ai/{model_id}"

    url = f"https://fal.run/{model_id}"

    headers = {
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "image_size": size,
        "num_images": 1,
        "enable_safety_checker": True,
    }

    # Add model-specific params
    if "flux-pro" in model_id:
        payload["safety_tolerance"] = "2"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"Fal API error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Fal API connection error: {e.reason}")


def download_image(url: str) -> bytes:
    """Download image from URL."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def upload_to_gcs(image_data: bytes, output_path: str, content_type: str = "image/png") -> str:
    """Upload image to GCS and return public URL."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(output_path)

    blob.upload_from_string(image_data, content_type=content_type)

    # Make public
    blob.make_public()

    return blob.public_url


def generate_image(request_data: dict) -> dict:
    """Main generation logic."""

    # Validate required fields
    prompt = request_data.get("prompt")
    if not prompt:
        raise ValueError("'prompt' is required")

    output_path = request_data.get("output_path")
    if not output_path:
        raise ValueError("'output_path' is required")

    # Get optional params
    model = request_data.get("model", "flux-pro-1.1")
    size_name = request_data.get("size", "landscape_16_9")
    size = SIZES.get(size_name, SIZES["landscape_16_9"])
    tenant_id = request_data.get("tenant_id", "default")

    # Prefix with tenant for organization
    full_path = f"{tenant_id}/{output_path}"

    # Get API key
    fal_key = get_fal_key()

    # Call Fal API
    result = call_fal_api(prompt, model, size, fal_key)

    # Extract image URL from result
    images = result.get("images", [])
    if not images:
        raise RuntimeError("No images returned from Fal API")

    image_url = images[0].get("url")
    if not image_url:
        raise RuntimeError("No image URL in Fal response")

    # Download and upload to GCS
    image_data = download_image(image_url)

    # Determine content type
    content_type = "image/png"
    if output_path.endswith(".jpg") or output_path.endswith(".jpeg"):
        content_type = "image/jpeg"
    elif output_path.endswith(".webp"):
        content_type = "image/webp"

    gcs_url = upload_to_gcs(image_data, full_path, content_type)

    return {
        "success": True,
        "gcs_url": gcs_url,
        "gcs_path": f"gs://{BUCKET_NAME}/{full_path}",
        "model": model,
        "size": size,
        "seed": result.get("seed"),
    }


@functions_framework.http
def generate_image_http(request):
    """HTTP endpoint for image generation."""

    # CORS headers
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*"}

    try:
        request_data = request.get_json(silent=True) or {}
        result = generate_image(request_data)
        return (json.dumps(result), 200, headers)

    except ValueError as e:
        return (json.dumps({"error": str(e), "type": "validation"}), 400, headers)

    except RuntimeError as e:
        return (json.dumps({"error": str(e), "type": "api_error"}), 502, headers)

    except Exception as e:
        return (json.dumps({"error": str(e), "type": "internal"}), 500, headers)


@functions_framework.cloud_event
def generate_image_pubsub(cloud_event):
    """Pub/Sub trigger for image generation."""

    # Decode Pub/Sub message
    data = cloud_event.data
    message_data = base64.b64decode(data["message"]["data"]).decode("utf-8")
    request_data = json.loads(message_data)

    try:
        result = generate_image(request_data)
        print(f"Generated image: {result['gcs_url']}")
        return result

    except Exception as e:
        print(f"Error generating image: {e}")
        raise
