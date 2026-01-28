"""
Persona Loader

Loads agent personas from markdown files and converts them to system prompts.
"""

import os
import re
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Persona:
    """An agent persona loaded from markdown."""
    agent_type: str
    name: str
    system_prompt: str
    expertise: list[str]
    personality_traits: list[str]
    handoff_triggers: dict[str, str]  # condition -> target agent


class PersonaLoader:
    """Loads and parses persona markdown files."""

    # Default path relative to runtime directory
    PERSONAS_PATH = Path(__file__).parent.parent / "agents"

    @classmethod
    def load(cls, agent_type: str) -> Persona:
        """Load a persona by agent type."""
        persona_file = cls.PERSONAS_PATH / f"{agent_type}.md"

        if not persona_file.exists():
            raise FileNotFoundError(f"Persona not found: {agent_type}")

        content = persona_file.read_text()
        return cls._parse_persona(agent_type, content)

    @classmethod
    def _parse_persona(cls, agent_type: str, content: str) -> Persona:
        """Parse markdown content into a Persona."""
        # Extract the agent name from the first heading
        name_match = re.search(r'^#\s+(.+?)\s+Agent', content, re.MULTILINE)
        name = name_match.group(1) if name_match else agent_type.title()

        # Extract personality traits
        personality = cls._extract_section(content, "Your Personality")
        traits = cls._extract_list_items(personality) if personality else []

        # Extract expertise/skills
        expertise_section = cls._extract_section(content, "Your Expertise")
        expertise = cls._extract_backtick_items(expertise_section) if expertise_section else []

        # Extract handoff triggers from "Working With Other Agents" or similar
        handoff_section = cls._extract_section(content, "Working With Other Agents")
        handoffs = cls._parse_handoffs(handoff_section) if handoff_section else {}

        # Build the system prompt
        system_prompt = cls._build_system_prompt(name, agent_type, content)

        return Persona(
            agent_type=agent_type,
            name=name,
            system_prompt=system_prompt,
            expertise=expertise,
            personality_traits=traits,
            handoff_triggers=handoffs
        )

    @classmethod
    def _extract_section(cls, content: str, heading: str) -> Optional[str]:
        """Extract content under a specific heading."""
        pattern = rf'^##\s+{re.escape(heading)}.*?\n(.*?)(?=^##\s+|\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else None

    @classmethod
    def _extract_list_items(cls, text: str) -> list[str]:
        """Extract list items (lines starting with -)."""
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('- **'):
                # Bold items like "- **Skeptical.** Description"
                match = re.match(r'-\s+\*\*(.+?)\.\*\*\s*(.*)', line)
                if match:
                    items.append(match.group(1))
            elif line.startswith('-'):
                items.append(line[1:].strip())
        return items

    @classmethod
    def _extract_backtick_items(cls, text: str) -> list[str]:
        """Extract items in backticks."""
        return re.findall(r'`([^`]+)`', text)

    @classmethod
    def _parse_handoffs(cls, text: str) -> dict[str, str]:
        """Parse handoff triggers."""
        handoffs = {}

        # Look for patterns like "To Editor" or "### To Editor"
        sections = re.findall(r'###?\s+To\s+(\w+)(.*?)(?=###?\s+To|\Z)', text, re.DOTALL)

        for agent, description in sections:
            agent_lower = agent.lower()
            # Extract what triggers handoff to this agent
            if 'provide' in description.lower() or 'you provide' in description.lower():
                handoffs[agent_lower] = description.strip()[:200]

        return handoffs

    @classmethod
    def _build_system_prompt(cls, name: str, agent_type: str, content: str) -> str:
        """Build the system prompt from persona content."""
        # Start with core identity
        prompt_parts = [
            f"You are the {name}, a specialized agent in a marketing agency swarm.",
            "",
            "# Your Role",
            ""
        ]

        # Add the full persona (cleaned up)
        # Remove markdown headers that don't belong in a system prompt
        cleaned = content

        # Remove the title
        cleaned = re.sub(r'^#\s+.+?\n+', '', cleaned)

        # Convert ## headers to simpler format
        cleaned = re.sub(r'^##\s+', '\n## ', cleaned, flags=re.MULTILINE)

        prompt_parts.append(cleaned)

        # Add swarm-specific instructions
        prompt_parts.extend([
            "",
            "# Swarm Behavior",
            "",
            "You are part of a multi-agent swarm. Key behaviors:",
            "",
            "1. **Stay in role.** Only do work within your expertise.",
            "2. **Request handoffs.** When work needs another agent, request a handoff.",
            "3. **Be concise.** Other agents and humans will read your output.",
            "4. **Maintain context.** Reference the brand voice and project context.",
            "5. **Signal completion.** Clearly indicate when your part is done.",
            "",
            "When you need another agent, format your handoff request as:",
            "```handoff",
            "TO: [agent_type]",
            "CONTEXT: [what they need to know]",
            "```",
        ])

        return "\n".join(prompt_parts)


# Convenience function for testing
def preview_persona(agent_type: str):
    """Print a preview of a loaded persona."""
    persona = PersonaLoader.load(agent_type)
    print(f"=== {persona.name} ===")
    print(f"Type: {persona.agent_type}")
    print(f"Traits: {', '.join(persona.personality_traits)}")
    print(f"Expertise: {', '.join(persona.expertise)}")
    print(f"Handoffs: {persona.handoff_triggers}")
    print(f"\nSystem prompt length: {len(persona.system_prompt)} chars")
    print(f"\nFirst 500 chars of system prompt:\n{persona.system_prompt[:500]}...")


if __name__ == "__main__":
    import sys
    agent = sys.argv[1] if len(sys.argv) > 1 else "copywriter"
    preview_persona(agent)
