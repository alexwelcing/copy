#!/bin/bash
# Run the full test suite
# Usage: ./scripts/test_suite.sh [--e2e]

if [[ "$1" == "--e2e" ]]; then
    echo "Running Full End-to-End Test Suite (WARNING: Costs API Credits)..."
    python -m pytest service/tests/ -v -m "e2e or not e2e"
else
    echo "Running Fast Unit/Integration Tests (No API Cost)..."
    python -m pytest service/tests/ -v -m "not e2e"
fi
