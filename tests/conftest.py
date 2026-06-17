"""Pytest configuration and fixtures for the FastAPI backend tests."""

import importlib
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture(autouse=True)
def reset_app_state():
    """Reload the app module before each test to reset in-memory state."""
    importlib.reload(app_module)
    yield


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app_module.app)
