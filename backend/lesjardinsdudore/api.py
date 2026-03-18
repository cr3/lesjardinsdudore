"""FastAPI application for plant lookup."""

import os
from datetime import date, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import Response
from icalendar import Calendar, Event

from lesjardinsdudore.inventory import Inventory, InventoryPlant


def get_inventory() -> Inventory:
    """Return the inventory."""
    url = os.environ.get("INVENTORY_URL")
    return Inventory.from_url(url)


InventoryDep = Annotated[Inventory, Depends(get_inventory)]

app = FastAPI(title="Les Jardins du Doré", docs_url="/api/docs")


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
