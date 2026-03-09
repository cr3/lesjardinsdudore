"""Unit tests for the FastAPI app module."""

from datetime import date, timedelta
from unittest.mock import Mock

import pytest
from icalendar import Calendar

from lesjardinsdudore.api import (
    group_characteristics,
    plant_events,
    translate_keys,
)
from lesjardinsdudore.inventory import InventoryPlant
from lesjardinsdudore.locales import Locales
from lesjardinsdudore.testing.database import FakeDatabase

PLANTS = [
    {
        "scientific name": "symphytum officinale",
        "common name/comfrey": True,
        "height/max": 1.2,
    },
    {
        "scientific name": "achillea millefolium",
        "common name/yarrow": True,
        "height/max": 0.6,
    },
]


@pytest.fixture
def database():
    """Override the default database fixture with test plants."""
    return FakeDatabase(PLANTS)


def test_suggest_by_scientific_name(api_client):
    """Suggest should match scientific names."""
    response = api_client.get("/api/plants", params={"q": "symphytum"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["scientific_name"] == "symphytum officinale"


def test_suggest_by_common_name(api_client):
    """Suggest should match common names."""
    response = api_client.get("/api/plants", params={"q": "yarrow"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["scientific_name"] == "achillea millefolium"
    assert "yarrow" in results[0]["common_names"]


def test_suggest_empty_query(api_client):
    """Suggest should reject an empty query."""
    response = api_client.get("/api/plants", params={"q": ""})
    assert response.status_code == 422


def test_suggest_no_match(api_client):
    """Suggest should return empty for unknown names."""
    response = api_client.get("/api/plants", params={"q": "zzzzz"})
    assert response.status_code == 200
    assert response.json() == []


def test_suggest_limit(api_client):
    """Suggest should respect the limit parameter."""
    response = api_client.get("/api/plants", params={"q": "a", "limit": 1})
    assert response.status_code == 200
    assert len(response.json()) <= 1


def test_lookup_found(api_client):
    """Lookup should return full characteristics for a known plant."""
    response = api_client.get("/api/plants/symphytum officinale")
    assert response.status_code == 200
    data = response.json()
    assert data["scientific name"] == "symphytum officinale"
    assert data["common name"] == ["comfrey"]
    assert data["height"] == {"max": 1.2}


def test_lookup_not_found(api_client):
    """Lookup should return empty for an unknown plant."""
    response = api_client.get("/api/plants/nonexistent plant")
    assert response.status_code == 200
    assert response.json() == {}


def test_translate_keys_flat():
    """Translate keys should translate top-level keys."""
    locales = Locales.from_domain("display", language="fr")
    data = {"scientific name": "test", "height": 1.2}
    result = translate_keys(data, locales)
    assert result == {"nom scientifique": "test", "hauteur": 1.2}


def test_translate_keys_nested():
    """Translate keys should recurse into nested dicts."""
    locales = Locales.from_domain("display", language="fr")
    data = {"height": {"max": 1.2}}
    result = translate_keys(data, locales)
    assert result == {"hauteur": {"max": 1.2}}


def test_translate_keys_passthrough():
    """Untranslated keys should pass through unchanged."""
    locales = Locales.from_domain("display", language="fr")
    data = {"unknown key": 42}
    result = translate_keys(data, locales)
    assert result == {"unknown key": 42}


def test_lookup_french(api_client):
    """Lookup with French Accept-Language should translate keys."""
    response = api_client.get(
        "/api/plants/symphytum officinale",
        headers={"Accept-Language": "fr-CA,fr;q=0.9,en;q=0.8"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom scientifique"] == "symphytum officinale"
    assert data["nom commun"] == ["comfrey"]
    assert data["hauteur"] == {"max": 1.2}


def test_group_characteristics_bool_subkeys():
    """Boolean sub-keys should be grouped into a sorted list."""
    data = {"sun/partial": True, "sun/full": True}
    result = group_characteristics(data)
    assert result == {"sun": ["full", "partial"]}


def test_group_characteristics_mixed_subkeys():
    """Non-boolean sub-keys should remain as dicts."""
    data = {"height/max": 1.2, "height/min": 0.5}
    result = group_characteristics(data)
    assert result == {"height": {"max": 1.2, "min": 0.5}}


def make_plant(**overrides):
    """Create an InventoryPlant with sensible defaults."""
    defaults = {
        "FAMILLES": "apiacées",
        "Noms": "carotte Danvers",
        "a-bis-v": "a",
        "qté": "200",
        "projet": "100",
        "origine": "écoumène",
        "date": "2025",
        "début stratif ❄️": "",
        "fin stratif": "",
        "Date semis int.": "",
        "Semaines accl": "",
        "date trans": "",
        "date SD 1": "",
        "SD2": "",
        "NOTES": "",
        "Distance (cm)": "",
        "SEMENCES à RÉCOLTER": "",
    }
    defaults.update(overrides)
    return InventoryPlant.model_validate(defaults)


class TestPlantEvents:
    """Tests for the plant_events helper."""

    def test_event_per_date(self):
        """Each date field should produce one event."""
        plant = make_plant(
            **{
                "Date semis int.": "15 mars 2026",
                "date SD 1": "1er juin 2026",
            }
        )
        events = list(plant_events(plant))
        assert len(events) == 2

    def test_event_summary(self):
        """Event summary should include label, name, and famille."""
        plant = make_plant(**{"date SD 1": "1er juin 2026"})
        event = list(plant_events(plant))[0]
        summary = str(event["summary"])
        assert "Semis direct 1" in summary
        assert "carotte Danvers" in summary
        assert "apiacées" in summary

    def test_event_dates(self):
        """Event should span one day."""
        plant = make_plant(**{"date SD 1": "1er juin 2026"})
        event = list(plant_events(plant))[0]
        assert event["dtstart"].dt == date(2026, 6, 1)
        assert event["dtend"].dt == date(2026, 6, 2)

    def test_event_description_from_notes(self):
        """Notes should become the event description."""
        plant = make_plant(
            **{"date SD 1": "1er juin 2026", "NOTES": "semer tôt"}
        )
        event = list(plant_events(plant))[0]
        assert str(event["description"]) == "semer tôt"

    def test_no_description_without_notes(self):
        """No description when notes are empty."""
        plant = make_plant(**{"date SD 1": "1er juin 2026"})
        event = list(plant_events(plant))[0]
        assert "description" not in event

    def test_no_events_without_dates(self):
        """A plant with no dates should produce no events."""
        plant = make_plant()
        assert list(plant_events(plant)) == []


class TestPlantsIcs:
    """Tests for the /plants.ics endpoint."""

    @pytest.fixture
    def inventory(self):
        """Fake inventory returning canned CSV."""
        inv = Mock()
        inv.get_plants.return_value = iter(
            [
                make_plant(
                    **{
                        "Noms": "tomate",
                        "Date semis int.": "15 mars 2026",
                        "date SD 1": "1er juin 2026",
                    }
                ),
                make_plant(
                    **{
                        "Noms": "basilic",
                        "date SD 1": "20 mai 2026",
                    }
                ),
            ]
        )
        return inv

    def test_content_type(self, api_client):
        """Response should have text/calendar content type."""
        resp = api_client.get("/plants.ics")
        assert resp.headers["content-type"] == "text/calendar; charset=utf-8"

    def test_valid_icalendar(self, api_client):
        """Response should be parseable as iCalendar."""
        resp = api_client.get("/plants.ics")
        cal = Calendar.from_ical(resp.content)
        assert cal["prodid"] == "-//Les Jardins du Doré//Plantes//FR"

    def test_event_count(self, api_client):
        """Should contain one event per plant date."""
        resp = api_client.get("/plants.ics")
        cal = Calendar.from_ical(resp.content)
        events = [c for c in cal.walk() if c.name == "VEVENT"]
        assert len(events) == 3

    def test_sheet_parameter(self, api_client, inventory):
        """Sheet parameter should be forwarded to get_plants."""
        api_client.get("/plants.ics?sheet=2025")
        inventory.get_plants.assert_called_once_with("2025")
