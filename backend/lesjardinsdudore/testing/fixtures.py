"""Testing fixtures."""

import pytest
from fastapi.testclient import TestClient

from lesjardinsdudore.api import (
    app,
    get_database,
)
from lesjardinsdudore.testing.database import FakeDatabase


@pytest.fixture
def database():
    """Fake database with no plants."""
    return FakeDatabase([])


@pytest.fixture
def api_client(database):
    """API testing client backed by a fake database."""
    app.dependency_overrides[get_database] = lambda: database

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
