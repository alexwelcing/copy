"""
Claude Executor

Handles Claude API calls with output parsing for handoffs and reviews.
"""

import re
import anthropic
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class ExecutionResult:
    """Result from Claude execution."""
    output: str
    tokens_used: int
    model: str

    # Handoff detection
    handoff_requested: bool = False
    handoff_to: Optional[str] = None
    handoff_context: Optional[Dict] = None

    # Review detection
    review_requested: bool = False
    review_questions: List[str] = field(default_factory=list)


class ClaudeExecutor:
    """Executes prompts against Claude API."""

    DEFAULT_MODEL = "claude-sonnet-4-20250514"
    MAX_TOKENS = 4096

    def __init__(self, api_key: str, system_prompt: str, model: str = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model or self.DEFAULT_MODEL

    def execute(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        max_tokens: int = None
    ) -> ExecutionResult:
        """Execute a prompt and return structured result."""

        # Call Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens or self.MAX_TOKENS,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract output
        output = response.content[0].text

        # Calculate tokens
        tokens_used = response.usage.input_tokens + response.usage.output_tokens

        # Parse for handoffs and reviews
        handoff_requested, handoff_to, handoff_context = self._parse_handoff(output)
        review_requested, review_questions = self._parse_review(output)

        # Clean output (remove handoff/review blocks)
        clean_output = self._clean_output(output)

        return ExecutionResult(
            output=clean_output,
            tokens_used=tokens_used,
            model=self.model,
            handoff_requested=handoff_requested,
            handoff_to=handoff_to,
            handoff_context=handoff_context,
            review_requested=review_requested,
            review_questions=review_questions
        )

    def _parse_handoff(self, output: str) -> tuple[bool, Optional[str], Optional[Dict]]:
        """Parse handoff request from output."""
        # Look for handoff block
        pattern = r'```handoff\s*\n(.*?)```'
        match = re.search(pattern, output, re.DOTALL | re.IGNORECASE)

        if not match:
            return False, None, None

        block = match.group(1)

        # Parse TO: and CONTEXT:
        to_match = re.search(r'TO:\s*(\w+)', block, re.IGNORECASE)
        context_match = re.search(r'CONTEXT:\s*(.*?)(?=\n[A-Z]+:|\Z)', block, re.DOTALL | re.IGNORECASE)

        if not to_match:
            return False, None, None

        to_agent = to_match.group(1).lower()
        context = {"notes": context_match.group(1).strip()} if context_match else {}

        return True, to_agent, context

    def _parse_review(self, output: str) -> tuple[bool, List[str]]:
        """Parse review request from output."""
        # Look for review block
        pattern = r'```review\s*\n(.*?)```'
        match = re.search(pattern, output, re.DOTALL | re.IGNORECASE)

        if not match:
            return False, []

        block = match.group(1)

        # Extract questions
        questions = []
        for line in block.split('\n'):
            line = line.strip()
            if line.startswith('-'):
                questions.append(line[1:].strip())
            elif line.startswith('*'):
                questions.append(line[1:].strip())

        return len(questions) > 0, questions

    def _clean_output(self, output: str) -> str:
        """Remove handoff and review blocks from output."""
        # Remove handoff blocks
        output = re.sub(r'```handoff\s*\n.*?```', '', output, flags=re.DOTALL | re.IGNORECASE)

        # Remove review blocks
        output = re.sub(r'```review\s*\n.*?```', '', output, flags=re.DOTALL | re.IGNORECASE)

        # Clean up extra whitespace
        output = re.sub(r'\n{3,}', '\n\n', output)

        return output.strip()


class MockExecutor:
    """Mock executor for testing without API calls."""

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def execute(self, prompt: str, context: Optional[Dict] = None, max_tokens: int = None) -> ExecutionResult:
        """Return a mock result."""
        return ExecutionResult(
            output=f"[Mock response to: {prompt[:100]}...]",
            tokens_used=100,
            model="mock",
            handoff_requested=False,
            review_requested=False
        )
