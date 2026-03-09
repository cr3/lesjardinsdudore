"""Unit tests for the inventory module."""

import logging
from datetime import date

import pytest

from lesjardinsdudore.inventory import (
    InventoryPlant,
    parse_french_date,
)


class TestParseFrenchDate:
    """Tests for parse_french_date."""

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("9 mars 2026", date(2026, 3, 9)),
            ("1er mai 2026", date(2026, 5, 1)),
            ("15 avril 2026", date(2026, 4, 15)),
            ("1er aout 2026", date(2026, 8, 1)),
            ("5 septembre 2026", date(2026, 9, 5)),
        ],
    )
    def test_french_format(self, value, expected):
        """Standard French dates should parse correctly."""
        assert parse_french_date(value) == expected

    def test_short_year(self):
        """Two-digit years should be treated as 2000s."""
        assert parse_french_date("1er mai 26") == date(2026, 5, 1)

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("2026-04-15", date(2026, 4, 15)),
            ("2026-03-10 am", date(2026, 3, 10)),
        ],
    )
    def test_iso_format(self, value, expected):
        """ISO dates should parse, even with trailing text."""
        assert parse_french_date(value) == expected

    def test_passthrough_date(self):
        """A date object should be returned as-is."""
        d = date(2026, 1, 1)
        assert parse_french_date(d) is d

    @pytest.mark.parametrize("value", [None, "", "  "])
    def test_empty(self, value):
        """Empty or None values should return None."""
        assert parse_french_date(value) is None

    @pytest.mark.parametrize(
        "value",
        [
            "fin février",
            "hors gel",
            "juin",
            "mi-mai",
            "2025",
            "test 2024",
            "exp 2027",
            "---",
        ],
    )
    def test_unparseable_warns(self, value, caplog):
        """Unparseable values should return None and log a warning."""
        with caplog.at_level(logging.WARNING):
            result = parse_french_date(value)
        assert result is None
        assert "Unparseable date" in caplog.text


class TestInventoryPlant:
    """Tests for the InventoryPlant model."""

    @pytest.fixture
    def row(self):
        """Minimal valid CSV row as a dict."""
        return {
            "FAMILLES": "apiacées",
            "Noms": "carotte Danvers",
            "a-bis-v": "a",
            "qté": "200",
            "projet": "100",
            "origine": "écoumène",
            "date": "2025",
            "début stratif ❄️": "",
            "fin stratif": "",
            "Date semis int.": "15 mars 2026",
            "Semaines accl": "",
            "date trans": "",
            "date SD 1": "1er juin 2026",
            "SD2": "",
            "NOTES": "semer tôt",
            "Distance (cm)": "10",
            "SEMENCES à RÉCOLTER": "",
        }

    def test_valid_row(self, row):
        """A complete row should parse into an InventoryPlant."""
        plant = InventoryPlant.model_validate(row)
        assert plant.famille == "apiacées"
        assert plant.nom == "carotte Danvers"
        assert plant.date_semis_interieur == date(2026, 3, 15)
        assert plant.date_semis_direct_1 == date(2026, 6, 1)
        assert plant.notes == "semer tôt"

    def test_unparseable_date_becomes_none(self, row):
        """An unparseable date string should become None."""
        row["Date semis int."] = "fin février"
        plant = InventoryPlant.model_validate(row)
        assert plant.date_semis_interieur is None

    def test_empty_dates_become_none(self, row):
        """Empty date fields should become None."""
        plant = InventoryPlant.model_validate(row)
        assert plant.debut_stratification is None
        assert plant.fin_stratification is None
        assert plant.date_transplantation is None
        assert plant.date_semis_direct_2 is None
