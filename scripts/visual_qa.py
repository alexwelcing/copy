import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.core.executor import get_executor
from service.api.schemas import WorkRequest, SkillName

def visual_qa():
    print("Initializing Visual QA Audit...")
    executor = get_executor()
    
    # Read the file
    file_path = "frontend/src/routes/+page.svelte"
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return

    print(f"Analyzing {file_path} for layout constraints...")
    
    # Run Audit focused on the specific visual bug
    req = WorkRequest(
        skill=SkillName.PAGE_CRO,
        task="Analyze the 'Define the Objective' section CSS. The user reports that '1. DEPARTMENT & SPECIALIZATION' dropdowns are cutting off text (e.g., 'copywri...') because the columns are too narrow. Recommend a specific CSS layout change to fix this truncation.",
        content=content,
        context={
            "issue": "Text truncation in dropdowns",
            "section": "Briefing Form",
            "current_layout": "Grid with 3 columns? Or 2 columns with sidebar?",
            "goal": "Ensure full text visibility for 'Department' and 'Specialization' dropdowns"
        }
    )
    
    try:
        result = executor.execute(req)
        print("\n--- VISUAL QA RESULTS ---")
        print(result.output)
    except Exception as e:
        print(f"Audit failed: {e}")

if __name__ == "__main__":
    visual_qa()
