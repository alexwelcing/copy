"""
Skill executor - loads skills and runs them through Claude API.
"""

import os
from pathlib import Path
from typing import Optional

import anthropic

from service.api.schemas import SkillName, WorkRequest, WorkResult


class SkillExecutor:
    """Executes marketing skills using Claude API."""

    def __init__(self, skills_path: Optional[Path] = None):
        """
        Initialize the executor.

        Args:
            skills_path: Path to the skills directory. Defaults to ./skills
        """
        self.client = anthropic.Anthropic()
        self.skills_path = skills_path or Path(__file__).parent.parent.parent / "skills"
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
        self._skill_cache: dict[str, str] = {}

    def load_skill(self, skill_name: SkillName) -> str:
        """
        Load a skill's content from its markdown file.

        Args:
            skill_name: The skill to load

        Returns:
            The skill's markdown content
        """
        if skill_name.value in self._skill_cache:
            return self._skill_cache[skill_name.value]

        skill_path = self.skills_path / skill_name.value / "SKILL.md"

        if not skill_path.exists():
            raise FileNotFoundError(f"Skill not found: {skill_name.value}")

        content = skill_path.read_text()
        self._skill_cache[skill_name.value] = content
        return content

    def build_prompt(self, request: WorkRequest) -> str:
        """
        Build the full prompt for Claude, combining skill and request.

        Args:
            request: The work request

        Returns:
            The complete prompt string
        """
        skill_content = self.load_skill(request.skill)

        prompt_parts = [
            "You are operating as a marketing agency skill executor.",
            "",
            "## Skill Framework",
            "",
            skill_content,
            "",
            "---",
            "",
            "## Your Task",
            "",
            request.task,
        ]

        if request.context:
            prompt_parts.extend([
                "",
                "## Additional Context",
                "",
            ])
            for key, value in request.context.items():
                if isinstance(value, list):
                    prompt_parts.append(f"**{key}**: {', '.join(str(v) for v in value)}")
                else:
                    prompt_parts.append(f"**{key}**: {value}")

        if request.content:
            prompt_parts.extend([
                "",
                "## Content to Analyze/Improve",
                "",
                "```",
                request.content,
                "```",
            ])

        prompt_parts.extend([
            "",
            "---",
            "",
            "Execute this task using the skill framework above. ",
            "Follow the skill's methodology, apply its frameworks, and use its quality checklists.",
            "",
            "Provide structured output with clear sections. ",
            "If the skill calls for alternatives, provide them. ",
            "If it calls for recommendations, prioritize them.",
        ])

        return "\n".join(prompt_parts)

    def execute(self, request: WorkRequest) -> WorkResult:
        """
        Execute a skill with the given request.

        Args:
            request: The work request

        Returns:
            The work result
        """
        prompt = self.build_prompt(request)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        output = message.content[0].text

        # Parse structured sections from the output
        sections = self._parse_sections(output)
        alternatives = self._extract_alternatives(output)
        recommendations = self._extract_recommendations(output)

        return WorkResult(
            skill=request.skill,
            output=output,
            sections=sections if sections else None,
            alternatives=alternatives if alternatives else None,
            recommendations=recommendations if recommendations else None,
            metadata={
                "model": self.model,
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
            }
        )

    def _parse_sections(self, output: str) -> dict:
        """Extract sections from markdown output."""
        sections = {}
        current_section = None
        current_content = []

        for line in output.split("\n"):
            if line.startswith("## "):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif line.startswith("### ") and not current_section:
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line[4:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _extract_alternatives(self, output: str) -> list[str]:
        """Extract alternative options from output."""
        alternatives = []
        in_alternatives = False

        for line in output.split("\n"):
            lower = line.lower()
            if "alternative" in lower and ("headline" in lower or "cta" in lower or "option" in lower):
                in_alternatives = True
                continue
            if in_alternatives:
                if line.startswith("- ") or line.startswith("* "):
                    alternatives.append(line[2:].strip())
                elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. "):
                    alternatives.append(line[3:].strip())
                elif line.startswith("##"):
                    in_alternatives = False

        return alternatives[:10]  # Cap at 10

    def _extract_recommendations(self, output: str) -> list[str]:
        """Extract recommendations from output."""
        recommendations = []
        in_recommendations = False

        for line in output.split("\n"):
            lower = line.lower()
            if any(term in lower for term in ["recommendation", "quick win", "action item", "next step"]):
                in_recommendations = True
                continue
            if in_recommendations:
                if line.startswith("- ") or line.startswith("* "):
                    recommendations.append(line[2:].strip())
                elif line.startswith(("1. ", "2. ", "3. ", "4. ", "5. ")):
                    recommendations.append(line[3:].strip())
                elif line.startswith("##"):
                    in_recommendations = False

        return recommendations[:20]  # Cap at 20


# Singleton instance
_executor: Optional[SkillExecutor] = None


def get_executor() -> SkillExecutor:
    """Get or create the skill executor singleton."""
    global _executor
    if _executor is None:
        _executor = SkillExecutor()
    return _executor
