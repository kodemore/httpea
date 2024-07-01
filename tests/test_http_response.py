from io import BytesIO

import pytest

from http_kit import (HttpCookie, HttpHeaders, HttpResponse, HttpStatus,
                     JsonHttpMessage)


def test_can_instantiate() -> None:
    # when
    instance = HttpResponse(status=200)

    # then
    assert isinstance(instance, HttpResponse)
    assert instance


def test_can_write_and_read_body() -> None:
    # given
    instance = HttpResponse(status=200)

    # when
    instance.write("Example text")

    # then
    assert str(instance) == "Example text"
    instance.body.seek(0)
    assert instance.body.read() == b"Example text"


def test_can_write_bytesio_body() -> None:
    # given
    body = BytesIO()

    # when
    body.write(b"example text")
    instance = HttpResponse(status=200)
    instance.write(body)

    # then
    assert str(instance) == "example text"
    instance.body.seek(0)
    assert instance.body.read() == b"example text"

    # when
    instance.write(" and string")

    # then
    assert str(instance) == "example text and string"


def test_can_close_body() -> None:
    # given
    instance = HttpResponse(status=HttpStatus.OK)

    # when
    instance.write("Test")

    # then
    assert instance.writable
    instance.close()
    assert not instance.writable


def test_headers() -> None:
    # given
    instance = HttpResponse()

    # when
    with pytest.raises(AttributeError):
        instance.headers = None

    # then
    assert isinstance(instance.headers, HttpHeaders)


def test_set_cookie() -> None:
    # given
    instance = HttpResponse()

    # when
    instance.cookies.append(HttpCookie("name", "value"))

    # then
    assert "name" in instance.cookies


@pytest.mark.parametrize(
    "instance, instance_copy",
    [
        [HttpResponse(), HttpResponse()],
        [HttpResponse(status=HttpStatus.OK), HttpResponse(status=HttpStatus.OK)],
        [HttpResponse(headers={"test": "1"}), HttpResponse(headers={"test": "1"})],
        [HttpResponse(encoding="iso-8859-1"), HttpResponse(encoding="iso-8859-1")],
        [
            HttpResponse(body="test 1"),
            HttpResponse(body="test 2"),
        ],  # HttpResponse only compares size of bodies not the exact values
        [
            HttpResponse(
                status=HttpStatus.OK, headers={"test": "1"}, encoding="iso-8859-1"
            ),
            HttpResponse(
                status=HttpStatus.OK, headers={"test": "1"}, encoding="iso-8859-1"
            ),
        ],
    ],
)
def test_two_response_instances_are_equal(
    instance: HttpResponse, instance_copy: HttpResponse
) -> None:

    assert instance == instance_copy


@pytest.mark.parametrize(
    "instance, instance_copy",
    [
        [HttpResponse(), HttpResponse(status=HttpStatus.CREATED)],
        [
            HttpResponse(status=HttpStatus.OK),
            HttpResponse(status=HttpStatus.OK, headers={"test": "1"}),
        ],
        [HttpResponse(), HttpResponse(encoding="iso-8859-2")],
        [HttpResponse(), HttpResponse(body="iso-8859-2")],
    ],
)
def test_two_response_instances_are_different(
    instance: HttpResponse, instance_copy: HttpResponse
) -> None:

    assert not instance == instance_copy


def test_http_response_as_str() -> None:
    # given
    body = '{"a": 1}'

    # when
    response = HttpResponse(body)

    # then
    assert response.as_str() == body
    assert response.as_str() == body


def test_http_response_as_dict() -> None:

    # given
    body = '{"a": 1}'

    # when
    response = HttpResponse(body)

    # then
    assert response.as_str() == body
    assert response.as_dict() == {"a": 1}


def test_http_response_parsed_body_as_json_message() -> None:
    # given
    body = '{"a": 1}'

    # when
    response = HttpResponse(body=body, headers={"content-type": "application/json"})

    # then
    assert isinstance(response.parsed_body, JsonHttpMessage)
