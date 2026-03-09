"""Testing fixtures."""

import pytest
from fastapi.testclient import TestClient

from lesjardinsdudore.api import (
    app,
    get_database,
    get_inventory,
)
from lesjardinsdudore.testing.database import FakeDatabase


@pytest.fixture
def database():
    """Fake database with no plants."""
    return FakeDatabase([])


@pytest.fixture
def inventory():
    """No inventory by default."""
    return None


@pytest.fixture
def api_client(database, inventory):
    """API testing client backed by a fake database."""
    app.dependency_overrides[get_database] = lambda: database
    if inventory is not None:
        app.dependency_overrides[get_inventory] = lambda: inventory

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
