"""
Quality Assurance and Evaluation Engine.

This module provides the 'QualityGuard' class, which acts as an automated critic
for generated content (text and assets). It is used by the test framework
and can be integrated into the main service pipeline.
"""

import json
import asyncio
from typing import Dict, Any, Optional
from service.core.executor import get_executor
from service.api.schemas import SkillName, WorkRequest

class QualityGuard:
    """
    Evaluates content against specific brand and quality standards.
    """
    
    def __init__(self):
        self.executor = get_executor()

    async def evaluate_asset(self, asset_type: str, asset_url: str, prompt: str, criteria: list[str] = None) -> Dict[str, Any]:
        """
        Evaluate a visual/audio asset against brand standards.
        """
        if not criteria:
            criteria = [
                "Technical quality (resolution, artifacts)",
                "Prompt adherence",
                "Brand alignment (High Era / Mid-Century Modern)"
            ]

        eval_task = f"""
        ACT AS: A Senior Creative Director at a high-end agency.
        
        TASK: Evaluate this generated {asset_type}.
        
        CONTEXT:
        - Asset URL: {asset_url}
        - Original Prompt: {prompt}
        - Brand Vision: 'High Era' (Tactile, Cinematic, Mid-Century Modern + Hard Sci-Fi).
        
        CRITERIA TO CHECK:
        {chr(10).join([f"{i+1}. {c}" for i, c in enumerate(criteria)])} 
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "score": <0-100 integer>,
            "status": "approved" | "rejected" | "needs_revision",
            "critique": "<concise actionable feedback>",
            "issues": ["<list>", "<of>", "<specific>", "<flaws>"],
            "refined_prompt": "<an improved version of the prompt if rejected>"
        }}
        """

        request = WorkRequest(
            skill=SkillName.MARKETING_PSYCHOLOGY,
            model="claude-sonnet-4-5-20250929", # Use strongest model for eval
            task=eval_task
        )

        try:
            result = await asyncio.to_thread(self.executor.execute, request)
            text = result.output
            
            # Robust JSON extraction
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
            else:
                return {"status": "error", "critique": "Failed to parse evaluation JSON", "score": 0}
        except Exception as e:
            return {"status": "error", "critique": f"Evaluation exception: {str(e)}", "score": 0}

    async def evaluate_copy(self, text_content: str, context: str = "") -> Dict[str, Any]:
        """
        Evaluate text copy against copywriting best practices.
        """
        eval_task = f"""
        ACT AS: A Senior Copy Chief.
        
        TASK: critique the following marketing copy.
        
        COPY TO REVIEW:
        ```
        {text_content}
        ```
        
        CONTEXT: {context}
        
        CRITERIA:
        1. Clarity & Concision (No fluff)
        2. Persuasion (PAS or AIDA framework used?)
        3. Tone (Sophisticated, confident, human)
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "score": <0-100 integer>,
            "status": "approved" | "rejected",
            "critique": "<feedback>",
            "suggestions": ["<list of improvements>"]
        }}
        """
        
        request = WorkRequest(
            skill=SkillName.COPY_EDITING,
            model="claude-sonnet-4-5-20250929",
            task=eval_task
        )
        
        try:
            result = await asyncio.to_thread(self.executor.execute, request)
            # JSON extraction logic (same as above)
            text = result.output
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
            return {"status": "error", "critique": "JSON parse error", "score": 0}
        except Exception as e:
             return {"status": "error", "critique": f"Error: {e}", "score": 0}

# Singleton
_guard: Optional[QualityGuard] = None

def get_quality_guard() -> QualityGuard:
    global _guard
    if _guard is None:
        _guard = QualityGuard()
    return _guard
