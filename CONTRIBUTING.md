# Contributing to Copy Agency

## Project Structure

This project follows a strict directory structure to maintain organization. Please adhere to these guidelines when adding new files.

### 📂 `scripts/`
**All development, testing, and utility scripts go here.**
- **Do not** create `dogfood_vX.py` or `generate_X.py` files in the root directory.
- Use `scripts/dogfood.py` to run the main end-to-end testing loop.
- Use `scripts/tools/` for asset generation utilities.
- If you need a new one-off script, place it in `scripts/` or `scripts/sandbox/`.

### 📂 `skills/`
**The single source of truth for agent skills.**
- Contains markdown definitions (`SKILL.md`) and supporting resources (templates, references) for AI skills.
- The backend service loads skills from here.
- Agentic tools read context from here.

### 📂 `service/`
**The Python backend API.**
- `service/api`: FastAPI routes and schemas.
- `service/core`: Core logic, executors, and asset managers.

### 📂 `frontend/`
**The SvelteKit frontend application.**

## Development Workflow

### Running Scripts
Scripts in `scripts/` are configured to find the `service` module automatically.
```bash
python scripts/dogfood.py
```

### Adding New Skills
1. Create a new directory in `skills/<skill-name>`.
2. Add a `SKILL.md` file defining the skill.
3. Add any necessary templates or reference docs in subdirectories.

### Version Control
- Avoid checking in `_v2`, `_v3` file versions. Use Git branches or commits for version history.
- Remove temporary test files before committing.
