"""Inventory module for downloading from a Google spreadsheet."""

import csv
import logging
import re
import types
from datetime import date
from io import StringIO
from typing import Annotated, Iterator

from attrs import define
from permaculture.google import GoogleSpreadsheet
from permaculture.storage import null_storage
from pydantic import BaseModel, BeforeValidator, Field
from yarl import URL

logger = logging.getLogger(__name__)

FRENCH_MONTHS = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "aout": 8,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12,
}


def parse_french_date(value: str | date | None) -> date | None:
    """Parse a French date string into a date object.

    Supports formats like "9 mars 2026", "1er mai 2026", "2026-04-15".
    Returns None and logs a warning for unparseable values.

    >>> parse_french_date("9 mars 2026")
    datetime.date(2026, 3, 9)
    >>> parse_french_date("1er mai 2026")
    datetime.date(2026, 5, 1)
    >>> parse_french_date("2026-04-15")
    datetime.date(2026, 4, 15)
    >>> parse_french_date("1er mai 26")
    datetime.date(2026, 5, 1)
    >>> parse_french_date("")
    >>> parse_french_date(None)
    """
    if value is None or isinstance(value, date):
        return value

    value = value.strip()
    if not value:
        return None

    # ISO format: "2026-04-15" or "2026-03-10 am"
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})\b", value)
    if m:
        return date(int(m[1]), int(m[2]), int(m[3]))

    # French format: "9 mars 2026" or "1er mai 2026" or "1er mai 26"
    m = re.match(
        r"(\d{1,2})(?:er)?\s+(\w+)\s+(\d{2,4})$",
        value,
    )
    if m:
        day, month_name, year_str = int(m[1]), m[2].lower(), m[3]
        month = FRENCH_MONTHS.get(month_name)
        if month:
            year = int(year_str)
            if year < 100:
                year += 2000
            return date(year, month, day)

    logger.warning("Unparseable date: %r", value)
    return None


FrenchDate = Annotated[date | None, BeforeValidator(parse_french_date)]


class InventoryPlant(BaseModel):
    """A plant row from the inventory spreadsheet."""

    famille: str = Field(alias="FAMILLES")
    nom: str = Field(alias="Noms")
    cycle: str = Field(alias="a-bis-v")
    quantite: str = Field(alias="qté")
    projet: str = Field(alias="projet")
    origine: str = Field(alias="origine")
    date: str = Field(alias="date")
    debut_stratification: FrenchDate = Field(
        default=None,
        alias="début stratif ❄️",
        title="Début stratification",
    )
    fin_stratification: FrenchDate = Field(
        default=None,
        alias="fin stratif",
        title="Fin stratification",
    )
    date_semis_interieur: FrenchDate = Field(
        default=None,
        alias="Date semis int.",
        title="Semis intérieur",
    )
    semaines_acclimatation: str = Field(
        default="", alias="Semaines accl"
    )
    date_transplantation: FrenchDate = Field(
        default=None,
        alias="date trans",
        title="Transplantation",
    )
    date_semis_direct_1: FrenchDate = Field(
        default=None,
        alias="date SD 1",
        title="Semis direct 1",
    )
    date_semis_direct_2: FrenchDate = Field(
        default=None,
        alias="SD2",
        title="Semis direct 2",
    )
    notes: str = Field(default="", alias="NOTES")
    distance_cm: str = Field(default="", alias="Distance (cm)")
    semences_a_recolter: str = Field(
        default="", alias="SEMENCES à RÉCOLTER"
    )

    @classmethod
    def date_fields(cls):
        """Yield (field_name, title) for each date field.

        >>> list(InventoryPlant.date_fields())[0]
        ('debut_stratification', 'Début stratification')
        """
        for name, field in cls.model_fields.items():
            ann = field.annotation
            if isinstance(ann, types.UnionType) and date in ann.__args__:
                yield name, field.title


@define(frozen=True)
class Inventory:
    """Inventory backed by a Google spreadsheet."""

    spreadsheet: GoogleSpreadsheet

    @classmethod
    def from_url(cls, url: str | URL, storage=null_storage):
        """Create an inventory from a Google spreadsheet URL."""
        spreadsheet = GoogleSpreadsheet.from_url(URL(url), storage)
        return cls(spreadsheet)

    def download(self, sheet: str):
        """Download a sheet by name as CSV."""
        sheets = self.spreadsheet.sheets()
        gid = sheets[sheet]
        return self.spreadsheet.export(gid=gid, fmt="csv")

    def get_plants(self, sheet: str) -> Iterator[InventoryPlant]:
        """Yield InventoryPlant for each row in the sheet.

        Warns about rows that cannot be parsed.
        """
        data = self.download(sheet)
        reader = csv.DictReader(StringIO(data))
        for i, row in enumerate(reader, start=2):
            try:
                yield InventoryPlant.model_validate(row)
            except Exception:
                logger.warning("Invalid row %d: %r", i, row)
