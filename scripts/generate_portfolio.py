import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.core.executor import get_executor
from service.api.schemas import WorkRequest, SkillName

class PortfolioGenerator:
    def __init__(self):
        self.executor = get_executor()
        self.output_dir = Path("examples")
        self.output_dir.mkdir(exist_ok=True)
        self.results = []

    def evaluate_output(self, skill: str, task: str, output: str) -> dict:
        """
        Ask the LLM to grade its own homework.
        """
        # Load the skill definition for reference
        try:
            skill_def = self.executor.load_skill(SkillName(skill))
        except:
            skill_def = "Standard Marketing Best Practices"

        prompt = f"""
        You are a Marketing Quality Assurance Director. 
        Evaluate the following marketing output against the provided Skill Definition.

        ## Skill Definition
        {skill_def[:1000]}...

        ## Task
        {task}

        ## Output to Evaluate
        {output[:2000]}...

        ## Your Evaluation
        Provide a JSON response with:
        1. "score": Integer 1-10
        2. "market_ready": Boolean (Is this client-ready?)
        3. "critique": One sentence summary of strengths/weaknesses.
        """
        
        # We use a direct client call here to act as the "Judge"
        # Using the default model configured in executor
        try:
            message = self.executor.anthropic_client.messages.create(
                model=self.executor.default_model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            eval_text = message.content[0].text
            # Naive parsing looking for JSON structure
            import re
            json_match = re.search(r"{{.*}}", eval_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return {"score": 0, "market_ready": False, "critique": "Failed to parse evaluation."}
        except Exception as e:
            print(f"Evaluation failed: {e}")
            return {"score": 0, "market_ready": False, "critique": "Evaluation error."}

    def run_skill(self, skill: SkillName, task: str, context: dict, content: str = None):
        print(f"Running {skill.value}...")
        try:
            req = WorkRequest(
                skill=skill,
                task=task,
                context=context,
                content=content
            )
            result = self.executor.execute(req)
            
            # Evaluate
            print(f"  Evaluating {skill.value}...")
            eval_result = self.evaluate_output(skill.value, task, result.output)
            
            # Save Artifact
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"{skill.value}_{timestamp}.md"
            filepath = self.output_dir / filename
            
            markdown_content = f"""# Example: {skill.value.title()}
**Date:** {timestamp}
**Status:** {"✅ Market Ready" if eval_result['market_ready'] else "⚠️ Needs Polish"}
**Score:** {eval_result['score']}/10

## The Brief
**Task:** {task}
**Context:** {json.dumps(context, indent=2)}

---

## The Output
{result.output}

---

## Quality Assurance
**Critique:** {eval_result['critique']}
"""
            filepath.write_text(markdown_content)
            
            self.results.append({
                "skill": skill.value,
                "file": filename,
                "score": eval_result['score'],
                "ready": eval_result['market_ready']
            })
            
        except Exception as e:
            print(f"Failed to run {skill.value}: {e}")

    def generate_index(self):
        index_path = self.output_dir / "README.md"
        content = "# High Era Portfolio & Capability Audit\n\n"
        content += f"Generated on {datetime.now().strftime('%Y-%m-%d')}\n\n"
        content += "| Skill | Score | Status | Example |\n"
        content += "|-------|-------|--------|---------|\n"
        
        for res in self.results:
            status_icon = "✅" if res['ready'] else "⚠️"
            link = f"[{res['file']}]({res['file']})"
            content += f"| {res['skill']} | {res['score']}/10 | {status_icon} | {link} |\n"
            
        index_path.write_text(content)
        print(f"\nPortfolio generated at {index_path}")

def main():
    gen = PortfolioGenerator()
    
    # 1. Strategy: Pricing (Restoring the work)
    gen.run_skill(
        SkillName.PRICING_STRATEGY,
        "Develop a tiered pricing strategy for 'High Era', a premium automated marketing agency.",
        {"brand": "High Era", "model": "Credits", "audience": "Mid-market B2B"}
    )
    
    # 2. Writing: Copywriting
    gen.run_skill(
        SkillName.COPYWRITING,
        "Write a high-converting landing page headline and subhead for High Era.",
        {"brand_voice": "Mid-Century Modern, Professional, Tactile", "usp": "Agency memory + Async workflow"}
    )
    
    # 3. Writing: Email Sequence
    gen.run_skill(
        SkillName.EMAIL_SEQUENCE,
        "Write a 3-email welcome sequence for new users who just signed up for the 'Studio' tier.",
        {"product": "High Era Terminal", "goal": "Activation (create first brief)"}
    )
    
    # 4. Strategy: Marketing Ideas
    gen.run_skill(
        SkillName.MARKETING_IDEAS,
        "Brainstorm 5 marketing campaigns to launch the new 'Dossier' feature.",
        {"feature": "The Dossier", "benefit": "Never repeat yourself"}
    )
    
    # 5. Video: Remotion Script (Testing the script capability)
    gen.run_skill(
        SkillName.REMOTION_SCRIPT,
        "Create a 15-second video script announcing the 'Twin-Engine' workflow.",
        {"product": "High Era", "visual_style": "Kinetic typography, split screen"}
    )
    
    # 6. CRO: Page Audit (Restoring the work)
    # We need to read the file first
    try:
        with open("frontend/src/routes/+page.svelte", "r") as f:
            page_content = f.read()
        gen.run_skill(
            SkillName.PAGE_CRO,
            "Audit the High Era landing page for conversion optimization.",
            {"goal": "Signups"},
            page_content
        )
    except FileNotFoundError:
        print("Skipping CRO audit - file not found")

    gen.generate_index()

if __name__ == "__main__":
    main()
