"""
Pytest test suite for ACEest Fitness & Gym Flask application.
"""

import os
import pytest

from app import app as flask_app
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
        "DATABASE": "test_aceest.db"
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
