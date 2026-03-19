"""Unit tests for the http module."""

import pytest
import responses
from requests.exceptions import HTTPError

from lesjardinsdudore.http import HTTPSession


@responses.activate
@pytest.mark.parametrize("method", [
    "GET",
    "HEAD",
    "OPTIONS",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "PATCH",
])
def test_http_session_request(method):
    """The HTTP session request should append the path to the base URL."""
    responses.add(
        method,
        "http://localhost/a",
        status=200,
    )

    session = HTTPSession("http://localhost/")
    result = session.request(method, "a")
    assert result.status_code == 200


@responses.activate
def test_http_session_get():
    """The HTTP session should map methods to request."""
    responses.add(
        responses.GET,
        "http://localhost/a",
        status=200,
    )

    session = HTTPSession("http://localhost/")
    result = session.get("a")
    assert result.status_code == 200


@responses.activate
@pytest.mark.parametrize("origin", [
    "http://localhost/",
    "http://localhost",
])
@pytest.mark.parametrize("path", [
    "a",
    "/a",
])
def test_http_session_origin(origin, path):
    """The HTTP session origin should handle slashes."""
    responses.add(
        responses.GET,
        "http://localhost/a",
        status=200,
    )

    session = HTTPSession(origin)
    result = session.request("GET", path)
    assert result.status_code == 200


def test_http_session_repr():
    """The HTTPSession repr should include origin and timeout."""
    session = HTTPSession("http://localhost/", timeout=30)
    assert repr(session) == "HTTPSession(origin=URL('http://localhost/'), timeout=30)"


@responses.activate
def test_http_session_raises_on_error():
    """The HTTP session should raise and log on a non-2xx response."""
    responses.add(responses.GET, "http://localhost/bad", status=404)

    session = HTTPSession("http://localhost/")
    with pytest.raises(HTTPError):
        session.request("GET", "bad")
