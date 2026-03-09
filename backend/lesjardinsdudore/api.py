"""FastAPI application for plant lookup."""

import os
from datetime import date, timedelta
from itertools import islice
from typing import Annotated

from fastapi import Depends, FastAPI, Header, Query
from fastapi.responses import Response
from icalendar import Calendar, Event
from permaculture.data import unflatten
from permaculture.database import Database
from permaculture.storage import Storage

from lesjardinsdudore.inventory import Inventory, InventoryPlant
from lesjardinsdudore.locales import Locales


def group_characteristics(data):
    """Group flat characteristics into a presentation-friendly structure.

    Sub-keys where all values are True are collected into a list:
    ``{"sun/partial": True, "sun/full": True}`` becomes ``{"sun": ["partial", "full"]}``.
    """
    nested = unflatten(data)
    if not isinstance(nested, dict):
        return nested

    return {
        key: (
            sorted(value)
            if isinstance(value, dict) and all(v is True for v in value.values())
            else value
        )
        for key, value in nested.items()
    }


def translate_keys(data, locales):
    """Recursively translate dictionary keys using locales."""
    if not isinstance(data, dict):
        return data

    return {
        locales.translate(key): (
            translate_keys(value, locales) if isinstance(value, dict) else value
        )
        for key, value in data.items()
    }


def get_database() -> Database:
    """Return the database."""
    storage = Storage.load(os.environ.get("PERMACULTURE_STORAGE"))
    return Database.from_storage(storage)


DatabaseDep = Annotated[Database, Depends(get_database)]

def get_inventory() -> Inventory:
    """Return the inventory."""
    url = os.environ.get("INVENTORY_URL")
    return Inventory.from_url(url)


InventoryDep = Annotated[Inventory, Depends(get_inventory)]

app = FastAPI(title="Les Jardins du Doré", docs_url="/api/docs")


@app.get("/api/plants")
def get_plants(
    database: DatabaseDep,
    q: str = Query(min_length=1, description="Search prefix"),
    limit: int = Query(default=10, ge=1, le=100),
):
    """Return typeahead suggestions for the given prefix."""
    return list(islice(database.search(q, score=0.6), limit))


@app.get("/api/plants/{scientific_name}")
def get_plant(
    database: DatabaseDep,
    scientific_name: str,
    accept_language: str = Header(default="en"),
):
    """Return full characteristics for a scientific name."""
    plants = list(database.lookup([scientific_name], score=1.0))
    if not plants:
        return {}

    lang = accept_language.split(",")[0].split("-")[0].strip()
    locales = Locales.from_domain("display", language=lang)
    data = group_characteristics(dict(plants[0].items()))
    return translate_keys(data, locales)


def plant_events(plant: InventoryPlant):
    """Yield calendar events for each date on a plant."""
    for attr, label in InventoryPlant.date_fields():
        d = getattr(plant, attr)
        if not isinstance(d, date):
            continue
        event = Event()
        event.add("summary", f"{label}: {plant.nom} ({plant.famille})")
        event.add("dtstart", d)
        event.add("dtend", d + timedelta(days=1))
        if plant.notes:
            event.add("description", plant.notes)
        yield event


@app.get("/plants.ics")
def get_plants_ics(inventory: InventoryDep, sheet: str = "2026"):
    """Return an iCalendar with planting dates."""
    cal = Calendar()
    cal.add("prodid", "-//Les Jardins du Doré//Plantes//FR")
    cal.add("version", "2.0")
    for plant in inventory.get_plants(sheet):
        for event in plant_events(plant):
            cal.add_component(event)
    return Response(
        content=cal.to_ical(),
        media_type="text/calendar",
    )
