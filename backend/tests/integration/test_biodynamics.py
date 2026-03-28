"""Integration tests for the biodynamics service."""

from hamcrest import (
    all_of,
    assert_that,
    contains_string,
)


def test_biodynamics_calendar(biodynamics_session):
    """The calendar.ics route should return a calendar."""
    response = biodynamics_session.get("/biodynamics/calendar.ics")
    assert_that(response.text, all_of(
        contains_string("BEGIN:VCALENDAR"),
        contains_string("END:VCALENDAR"),
    ))
