from copy import copy
from datetime import datetime

import pytest

from httpea import HttpCookie, HttpCookieJar


def test_can_instantiate() -> None:
    # given
    jar = HttpCookieJar()

    # then
    assert isinstance(jar, HttpCookieJar)


def test_set_simple_cookie() -> None:
    # given
    jar = HttpCookieJar()

    # when
    jar["test"] = "value"

    # then
    assert "test" in jar
    assert isinstance(jar["test"], HttpCookie)
    assert "value" == str(jar["test"])


def test_set_cookie() -> None:
    # given
    jar = HttpCookieJar()

    # when
    jar.append(HttpCookie("test", "value"))

    # then
    assert "test" in jar
    assert isinstance(jar["test"], HttpCookie)
    assert "value" == str(jar["test"])


def test_override_cookie() -> None:
    # given
    cookie = HttpCookie("test", "value")
    jar = HttpCookieJar()

    # when
    jar["test"] = "value"
    jar.append(cookie)

    # then
    assert jar["test"] is cookie

    # when
    jar["test"] = "123"

    # then
    assert jar["test"] is not cookie


def test_fail_to_change_cookie_name() -> None:
    jar = HttpCookieJar()
    jar["test"] = "name"
    cookie = jar["test"]

    with pytest.raises(AttributeError):
        cookie.name = "test-2"


@pytest.mark.parametrize(
    "cookie,expected",
    [
        (HttpCookie("name", "value"), "name=value"),
        (
            HttpCookie("name", "value", expires=datetime(1999, 1, 1)),
            "name=value; Expires=Fri, 01 Jan 1999 00:00:00 ",
        ),
        (HttpCookie("name", "value", http_only=True), "name=value; HttpOnly"),
        (HttpCookie("name", "value", secure=True), "name=value; Secure"),
        (
            HttpCookie("name", "value", secure=True, http_only=True),
            "name=value; Secure; HttpOnly",
        ),
        (
            HttpCookie("name", "value", secure=True, same_site=True),
            "name=value; Secure; SameSite=Strict",
        ),
        (
            HttpCookie(
                "name",
                "value",
                secure=True,
                same_site=True,
                expires=datetime(1999, 1, 1),
            ),
            "name=value; Expires=Fri, 01 Jan 1999 00:00:00 ; Secure; SameSite=Strict",
        ),
    ],
)
def test_serialise_cookie(cookie: HttpCookie, expected: str) -> None:
    assert cookie.serialise() == expected


def test_can_copy_http_jar() -> None:
    # given
    jar = HttpCookieJar()
    jar.append(HttpCookie("test", "test"))

    # when
    jar_copy = copy(jar)
    jar_copy["test"] = "test-2"

    # then
    assert jar["test"] == "test"
    assert jar_copy["test"] == "test-2"
