import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path so we can import service
sys.path.append(str(Path(__file__).parent))

from service.core.executor import get_executor
from service.api.schemas import WorkRequest, SkillName

async def dogfood():
    print("🐶 Dogfooding: Running Agency Skills on Itself...")
    executor = get_executor()
    
    # 1. Audit the Frontend Interface using page-cro
    print("\n[1/2] Auditing Frontend Interface (page-cro)...")
    fe_path = Path("frontend/src/routes/+page.svelte")
    if fe_path.exists():
        fe_content = fe_path.read_text()
        req = WorkRequest(
            skill=SkillName.PAGE_CRO,
            task="Audit this Svelte application interface. Focus on UX/UI improvements, accessibility, and conversion (usage) optimization. Suggest specific code changes.",
            context={
                "project": "Marketing Agency AI Platform",
                "audience": "Marketers and Copywriters",
                "goal": "Increase skill usage and ease of use"
            },
            content=fe_content
        )
        try:
            result = executor.execute(req)
            print("\n--- CRO Audit Results ---")
            print(result.output[:1000] + "...") # Print first 1000 chars
            
            # Save full output for review
            Path("dogfood_cro_audit.md").write_text(result.output)
            print(">> Saved full audit to dogfood_cro_audit.md")
        except Exception as e:
            print(f"Error executing page-cro: {e}")
    else:
        print("Could not find frontend file.")

    # 2. Generate Feature Ideas using marketing-ideas
    print("\n[2/2] Brainstorming New Features (marketing-ideas)...")
    req = WorkRequest(
        skill=SkillName.MARKETING_IDEAS,
        task="Brainstorm 5 innovative features for this AI Marketing Agency platform that would differentiate it from generic AI writers. Focus on 'Agency' workflows.",
        context={
            "current_features": "23 expert skills, multi-agent orchestration, structured output, fork & run deployment",
            "positioning": "Expertise encoded into skills, not just prompting"
        }
    )
    try:
        result = executor.execute(req)
        print("\n--- Feature Ideas ---")
        print(result.output[:1000] + "...")
        
        # Save full output
        Path("dogfood_ideas.md").write_text(result.output)
        print(">> Saved ideas to dogfood_ideas.md")
    except Exception as e:
        print(f"Error executing marketing-ideas: {e}")

if __name__ == "__main__":
    # Ensure event loop
    asyncio.run(dogfood())
