import pytest
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from service.core.executor import get_executor
from service.core.assets import get_asset_manager
from service.core.quality import get_quality_guard
from fastapi.testclient import TestClient
from service.main import app

@pytest.fixture
def api_client():
    return TestClient(app)

@pytest.fixture
def executor():
    return get_executor()

@pytest.fixture
def asset_manager():
    return get_asset_manager()

@pytest.fixture
def quality_guard():
    return get_quality_guard()
