"""Testing fixtures."""

import pytest
from fastapi.testclient import TestClient

from lesjardinsdudore.api import (
    app,
    get_inventory,
)


@pytest.fixture
def inventory():
    """No inventory by default."""
    return None


@pytest.fixture
def api_client(inventory):
    """API testing client backed by a testing inventory."""
    app.dependency_overrides[get_inventory] = lambda: inventory

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
