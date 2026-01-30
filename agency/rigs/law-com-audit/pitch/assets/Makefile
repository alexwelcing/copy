# HIGH ERA AGENCY - PITCH ASSET GENERATION
# Law.com Strategic Transformation
#
# Usage:
#   make setup      - Verify environment and dependencies
#   make generate   - Generate all premium assets
#   make preview    - Generate single test asset
#   make clean      - Remove generated assets

.PHONY: setup generate preview clean verify help

# Default target
help:
	@echo "============================================================"
	@echo "HIGH ERA AGENCY - PITCH ASSET TOOLKIT"
	@echo "============================================================"
	@echo ""
	@echo "Commands:"
	@echo "  make setup      Check environment and install dependencies"
	@echo "  make verify     Verify FAL_KEY is valid"
	@echo "  make preview    Generate one test asset (fast check)"
	@echo "  make generate   Generate all premium pitch assets"
	@echo "  make clean      Remove generated assets"
	@echo ""
	@echo "Quick Start:"
	@echo "  export FAL_KEY='your-key-here'"
	@echo "  make setup"
	@echo "  make generate"
	@echo ""

# Check environment
setup:
	@echo "Checking environment..."
	@command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 required"; exit 1; }
	@echo "✓ Python3 found"
	@python3 -c "import urllib.request" 2>/dev/null && echo "✓ urllib available" || echo "✗ urllib missing"
	@python3 -c "import json" 2>/dev/null && echo "✓ json available" || echo "✗ json missing"
	@if [ -z "$$FAL_KEY" ]; then \
		echo ""; \
		echo "WARNING: FAL_KEY not set"; \
		echo "Run: export FAL_KEY='your-fal-api-key'"; \
		echo "Get one at: https://fal.ai/dashboard/keys"; \
	else \
		echo "✓ FAL_KEY is set"; \
	fi
	@echo ""
	@echo "Setup complete. Run 'make generate' to create assets."

# Verify API key works
verify:
	@if [ -z "$$FAL_KEY" ]; then \
		echo "ERROR: FAL_KEY not set"; \
		echo "Run: export FAL_KEY='your-key'"; \
		exit 1; \
	fi
	@echo "Verifying FAL_KEY..."
	@python3 verify_api.py

# Generate single preview asset
preview:
	@if [ -z "$$FAL_KEY" ]; then \
		echo "ERROR: FAL_KEY not set"; \
		exit 1; \
	fi
	@echo "Generating preview asset..."
	@python3 generate_premium.py --preview

# Generate all assets
generate:
	@if [ -z "$$FAL_KEY" ]; then \
		echo "ERROR: FAL_KEY not set"; \
		echo "Run: export FAL_KEY='your-key'"; \
		exit 1; \
	fi
	@echo "Starting premium asset generation..."
	@python3 generate_premium.py

# Clean generated assets
clean:
	@echo "Cleaning generated assets..."
	@rm -rf ./generated_assets
	@echo "Done."
