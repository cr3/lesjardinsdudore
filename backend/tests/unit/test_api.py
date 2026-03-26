"""Unit tests for the api module."""

from datetime import date
from unittest.mock import Mock

import pytest
from icalendar import Calendar

from lesjardinsdudore.api import plant_events
from lesjardinsdudore.inventory import InventoryPlant


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
        "SI": "",
        "Semaines accl": "",
        "date trans": "",
        "SD1": "",
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
                "SI": "15 mars 2026",
                "SD1": "1er juin 2026",
            }
        )
        events = list(plant_events(plant))
        assert len(events) == 2

    def test_event_summary(self):
        """Event summary should include label, name, and famille."""
        plant = make_plant(**{"SD1": "1er juin 2026"})
        event = next(iter(plant_events(plant)))
        summary = str(event["summary"])
        assert "SD1" in summary
        assert "carotte Danvers" in summary
        assert "apiacées" in summary

    def test_event_dates(self):
        """Event should span one day."""
        plant = make_plant(**{"SD1": "1er juin 2026"})
        event = next(iter(plant_events(plant)))
        assert event["dtstart"].dt == date(2026, 6, 1)
        assert event["dtend"].dt == date(2026, 6, 2)

    def test_event_description_from_notes(self):
        """Notes should become the event description."""
        plant = make_plant(
            **{"SD1": "1er juin 2026", "NOTES": "semer tôt"}
        )
        event = next(iter(plant_events(plant)))
        assert str(event["description"]) == "semer tôt"

    def test_no_description_without_notes(self):
        """No description when notes are empty."""
        plant = make_plant(**{"SD1": "1er juin 2026"})
        event = next(iter(plant_events(plant)))
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
                        "SI": "15 mars 2026",
                        "SD1": "1er juin 2026",
                    }
                ),
                make_plant(
                    **{
                        "Noms": "basilic",
                        "SI": "20 mai 2026",
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
