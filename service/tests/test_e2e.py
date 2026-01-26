import pytest
import asyncio
from service.api.schemas import SkillName, WorkRequest

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_full_copy_audit_flow(executor, quality_guard):
    """
    E2E Test: Generate copy -> Evaluate copy -> Verify quality.
    WARNING: Consumes API credits.
    """
    # 1. Generate Copy
    task = "Write a high-converting H1 and Subheadline for a luxury coffee subscription."
    req = WorkRequest(skill=SkillName.COPYWRITING, task=task)
    
    print("\n--- Generating Copy ---")
    result = executor.execute(req)
    copy_text = result.output
    assert copy_text is not None
    print(f"Generated: {copy_text[:100]}...")
    
    # 2. Evaluate Copy
    print("\n--- Evaluating Copy ---")
    eval_result = await quality_guard.evaluate_copy(copy_text, context="Luxury Coffee Brand")
    
    print(f"Score: {eval_result.get('score')}")
    print(f"Status: {eval_result.get('status')}")
    
    assert eval_result.get("score") > 0
    assert "status" in eval_result

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_asset_creation_flow(asset_manager, quality_guard):
    """
    E2E Test: Generate Asset -> Evaluate Asset.
    WARNING: Consumes API credits (FAL + Claude).
    """
    prompt = "A minimalist, geometric logo for a coffee brand, vector style, dark brown and gold."
    
    print("\n--- Generating Asset ---")
    asset = await asset_manager.generate_image(prompt, model="fal-ai/recraft-v3")
    assert asset["url"] is not None
    print(f"Asset URL: {asset['url']}")
    
    print("\n--- Evaluating Asset ---")
    eval_result = await quality_guard.evaluate_asset("image", asset['url'], prompt)
    
    print(f"Status: {eval_result.get('status')}")
    print(f"Critique: {eval_result.get('critique')}")
    
    assert "status" in eval_result
