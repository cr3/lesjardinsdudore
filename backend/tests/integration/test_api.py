"""Integration tests for the API service."""

from hamcrest import (
    assert_that,
    contains_exactly,
    contains_inanyorder,
    has_entries,
)


def test_api_search(api_session):
    """The API should return search results for known plants."""
    response = api_session.get("/api/plants", params={"q": "symphytum"})
    data = response.json()

    assert_that(
        data,
        contains_exactly(
            has_entries(
                {"scientific name": "symphytum officinale"},
            ),
        ),
    )


def test_api_lookup(api_session):
    """The API should return characteristics for a known plant."""
    response = api_session.get("/api/plants/symphytum officinale")
    data = response.json()

    assert_that(
        data,
        has_entries(
            {
                "scientific name": "symphytum officinale",
                "common name": contains_inanyorder("comfrey"),
                "height": has_entries(max=1.2, min=0.3),
            }
        ),
    )
