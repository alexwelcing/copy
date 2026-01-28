import pytest
import asyncio
import os
from service.core.models import ImageModels

# Skip tests that require GCP credentials if not available
requires_gcp = pytest.mark.skipif(
    not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not os.path.exists("service.json"),
    reason="GCP credentials not available"
)

@requires_gcp
@pytest.mark.asyncio
async def test_asset_generation_integration(asset_manager):
    """
    Integration test for FAL asset generation.
    Skipped by default unless GCP credentials are available.
    """
    # Verify the manager has the correct storage bucket configured
    assert asset_manager.storage.bucket_name is not None
    
    # We won't actually call FAL in the unit test suite to avoid costs/latency
    # unless specifically requested.
    # But we can verify the model constants are correct
    assert ImageModels.FLUX_PRO_1_1 == "fal-ai/flux-pro/v1.1"

def test_image_models_structure():
    """
    Unit test to verify model constants without GCP credentials.
    """
    assert ImageModels.FLUX_PRO_1_1 == "fal-ai/flux-pro/v1.1"
    assert ImageModels.FLUX_SCHNELL == "fal-ai/flux/schnell"
    assert hasattr(ImageModels, 'SDXL_LIGHTNING')

@pytest.mark.asyncio
async def test_evaluator_structure(quality_guard):
    """
    Test the QualityGuard structure.
    """
    # Mocking the executor response for the unit test
    class MockResult:
        output = '{"score": 95, "status": "approved", "critique": "Great work", "issues": [], "refined_prompt": null}'
    
    # Monkeypatch the executor.execute method temporarily
    original_execute = quality_guard.executor.execute
    quality_guard.executor.execute = lambda req: MockResult()
    
    result = await quality_guard.evaluate_asset(
        "image", 
        "http://fake.url/img.png", 
        "A prompt"
    )
    
    assert result["status"] == "approved"
    assert result["score"] == 95
    
    # Restore
    quality_guard.executor.execute = original_execute
