import re
from copy import copy

import pytest

from httpkit import HttpNotFoundError, Route, Router


def test_route_parsing() -> None:
    # when
    route = Route("/example/{pattern}")

    # then
    assert route.match("/example/test")


def test_route_parsing_with_wildcards() -> None:
    # when
    route = Route("/example/{a}*")

    # then
    assert route.pattern == re.compile(r"^/example/([^/]+).*?$", re.I | re.M)
    assert route.match("/example/test/1/2/3")
    assert route.match("/example/11")


def test_route_is_wildcard() -> None:
    # when
    route = Route("*")

    # then
    assert route.is_wildcard
    assert route.pattern == re.compile(r"^.*?$", re.I | re.M)


def test_route_match() -> None:
    # when
    route = Route("/pets/{pet_id}")
    route = route.match("/pets/11a22")

    # then
    assert route["pet_id"] == "11a22"

    # then
    route = Route("/pets/{pet_id}")
    route = route.match("/pets/22")

    # then
    assert route._parameters == {"pet_id": 22}


def test_route_match_with_wildcard() -> None:
    # given
    route = Route("/pets/{pet_id}/*")

    # when
    route = route.match("/pets/22/1/2/3")

    # then
    assert route
    assert route["pet_id"] == 22


def test_router() -> None:
    # given
    def test_controller() -> None:
        pass

    router = Router()

    # when
    router.append("/pets/{pet_id}", test_controller)
    router.append("/pets", test_controller)
    match = router.match("/pets/12")

    # then
    assert match[0]["pet_id"] == 12
    assert router.match("/pets")


def test_router_fail_matching() -> None:
    # given
    def test_controller():
        pass

    router = Router()

    # when
    router.append(Route("/pets/{pet_id}"), test_controller)

    # then
    with pytest.raises(HttpNotFoundError):
        router.match("/pet/12")


def test_route_match_multiple_parameters() -> None:
    # given
    route = Route("/pets/{pet_id}/{category}")

    # when
    route = route.match("/pets/11a22/test")

    # then
    assert route["pet_id"] == "11a22"
    assert route["category"] == "test"


def test_router_prioritise_routes_with_no_wildcards() -> None:
    # given
    def test_controller():
        pass

    router = Router()
    router.append(Route("/pets/*"), test_controller)
    router.append(Route("/pets/{pet_id}"), test_controller)
    router.append(Route("*"), test_controller)

    # when
    route, controller = router.match("/pets/11a22")

    # then
    assert route.route == "/pets/{pet_id}"


def test_can_copy_route() -> None:
    # given
    base_route = Route("/test/{parameter}")

    # when
    match_route = base_route.match("/test/test-1")
    route_copy = copy(match_route)

    # then
    assert match_route
    assert route_copy.route == match_route.route
    assert route_copy.parameters == match_route.parameters
