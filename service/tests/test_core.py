import pytest
import asyncio
from service.core.models import ImageModels

@pytest.mark.asyncio
async def test_asset_generation_integration(asset_manager):
    """
    Integration test for FAL asset generation.
    Skipped by default unless --run-e2e is passed (implementation detail).
    For now, we just mock or verify the manager structure.
    """
    # Verify the manager has the correct storage bucket configured
    assert asset_manager.storage.bucket_name is not None
    
    # We won't actually call FAL in the unit test suite to avoid costs/latency
    # unless specifically requested.
    # But we can verify the model constants are correct
    assert ImageModels.FLUX_PRO_1_1 == "fal-ai/flux-pro/v1.1"

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
