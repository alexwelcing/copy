# Contributing to High Era

We welcome contributions to High Era! This project is designed to be the open-source standard for automated marketing agencies. Whether you're fixing a bug, adding a new skill, or improving the documentation, your help is appreciated.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Cloud SDK (for deployment)
- Firebase Project (for auth/database)

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/high-era.git
    cd high-era
    ```

2.  **Backend Setup:**
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    
    # Set up environment variables
    cp .env.example .env
    # Edit .env with your API keys (Anthropic, FAL, etc.)
    
    # Run the server locally
    python3 -m uvicorn service.main:app --reload --port 8080
    ```

3.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

4.  **Access the app:**
    Open http://localhost:3000 in your browser.

## Architecture Overview

High Era follows a "Twin-Engine" architecture:
-   **Frontend (SvelteKit):** Handles the "Briefing Terminal" UI, Dossier management, and real-time feedback.
-   **Backend (FastAPI):** Exposes the skill execution engine.
    -   **Synchronous API:** For fast tasks (copywriting, strategy).
    -   **Asynchronous Workers (Pub/Sub):** For heavy tasks (video, deep research).
-   **State (Firestore):** Stores briefs, leads, and user history.

## Adding a New Skill

1.  **Create the Skill Definition:**
    Add a new directory in `skills/<category>/<skill-name>/`.
    Create `SKILL.md` following the standard template (Overview, Frameworks, Checklist).

2.  **Register the Skill:**
    Update `service/api/schemas.py` to include your new `SkillName` enum.
    Update `frontend/src/lib/api.ts` to include it in `SKILL_CATEGORIES`.

3.  **Test It:**
    Use `scripts/generate_portfolio.py` to run a test case against your new skill.

## Pull Request Process

1.  Fork the repo and create your branch from `main`.
2.  Run `scripts/test_suite.sh` (if available) or ensure your changes don't break existing flows.
3.  Update documentation if you changed API endpoints or configuration.
4.  Submit a PR with a clear description of the "Why" and "How".

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.