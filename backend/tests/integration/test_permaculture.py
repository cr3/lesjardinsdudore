"""Integration tests for the permaculture service."""

from hamcrest import (
    assert_that,
    contains_exactly,
    contains_inanyorder,
    has_entries,
)


def test_permaculture_search(permaculture_session):
    """The permaculture route should return search results for known plants."""
    response = permaculture_session.get("/permaculture/plants", params={"q": "symphytum"})
    data = response.json()

    assert_that(
        data,
        contains_exactly(
            has_entries(
                {"scientific name": "symphytum officinale"},
            ),
        ),
    )


def test_permaculture_lookup(permaculture_session):
    """The permaculture route should return characteristics for a known plant."""
    response = permaculture_session.get("/permaculture/plants/symphytum officinale")
    data = response.json()

    assert_that(
        data,
        has_entries(
            {
                "scientific name": "symphytum officinale",
                "common names": contains_inanyorder("comfrey"),
                "height": has_entries(max=1.2, min=0.3),
            }
        ),
    )
