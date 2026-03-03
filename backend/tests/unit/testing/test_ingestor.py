"""Unit tests for the JSON ingestor."""

import json

from permaculture.database import DatabasePlant

from lesjardinsdudore.testing.ingestor import JSONIngestor


def test_fetch_all(tmp_path):
    """fetch_all should yield DatabasePlant for each entry."""
    plants = [
        {"scientific name": "symphytum officinale", "height/max": 1.2},
        {"scientific name": "achillea millefolium", "height/max": 0.6},
    ]
    path = tmp_path / "plants.json"
    path.write_text(json.dumps(plants))

    ingestor = JSONIngestor(path)
    result = list(ingestor.fetch_all())

    assert len(result) == 2
    assert all(isinstance(p, DatabasePlant) for p in result)
    assert result[0].scientific_name == "symphytum officinale"
    assert result[1].scientific_name == "achillea millefolium"


def test_fetch_all_empty(tmp_path):
    """fetch_all should yield nothing for an empty list."""
    path = tmp_path / "plants.json"
    path.write_text("[]")

    ingestor = JSONIngestor(path)
    result = list(ingestor.fetch_all())

    assert result == []


def test_from_config_default(monkeypatch, tmp_path):
    """from_config should read JSON_INGESTOR_PATH from env."""
    fixture = tmp_path / "test.json"
    fixture.write_text("[]")
    monkeypatch.setenv("JSON_INGESTOR_PATH", str(fixture))

    ingestor = JSONIngestor.from_config(config=None)

    assert ingestor.path == fixture


def test_from_config_unconfigured(monkeypatch):
    """from_config should return a no-op ingestor when env var is unset."""
    monkeypatch.delenv("JSON_INGESTOR_PATH", raising=False)

    ingestor = JSONIngestor.from_config(config=None)

    assert ingestor.path is None
    assert list(ingestor.fetch_all()) == []
