from io import BytesIO

from fixtures.body_fixtures import (binary_body, cat_file, cat_file_body,
                                    form_body, json_body, multipart_body)

from httpea import (BinaryHttpMessage, FormHttpMessage, HttpMethod,
                    HttpRequest, JsonHttpMessage, MultipartHttpMessage,
                    SimpleHttpMessage, UploadedFile, YamlHttpMessage)


def test_parse_multipart_body() -> None:
    # given
    request = HttpRequest(
        multipart_body["REQUEST_METHOD"],
        body=multipart_body["wsgi.input"],
        headers={"content-type": multipart_body["CONTENT_TYPE"]},
    )

    # when
    body = request.parsed_body

    # then
    assert isinstance(body, MultipartHttpMessage)
    assert str(body["id"]) == "51b8a72aaaf909e303000034"
    assert str(body["test_1"]) == "only string value"
    assert str(body["test_2"]) == "1232"
    assert isinstance(body["file_a"], UploadedFile)
    assert isinstance(body["file_b"], UploadedFile)
    assert body["file_a"].filename == "orange.gif"
    assert body["file_b"].filename == "yellow.gif"
    assert body.get("test2", "default") == "default"
    assert len(body["file_a"]) == 49


def test_parse_files() -> None:
    # given
    request = HttpRequest(
        cat_file_body["REQUEST_METHOD"],
        body=cat_file_body["wsgi.input"],
        headers={"content-type": cat_file_body["CONTENT_TYPE"]},
    )

    # when
    body = request.parsed_body
    body["image"].seek(0)
    cat_file.seek(0)

    # then
    assert body["image"].read() == cat_file.read()


def test_parse_form_body() -> None:
    # given
    request = HttpRequest(
        form_body["REQUEST_METHOD"],
        body=form_body["wsgi.input"],
        headers={"content-type": form_body["CONTENT_TYPE"]},
    )

    # when
    body = request.parsed_body

    # then
    assert isinstance(body, FormHttpMessage)
    assert str(body["test_1"]) == "1"
    assert body.get("test2", "default") == "default"


def test_parse_json_body() -> None:
    # given
    request = HttpRequest(
        json_body["REQUEST_METHOD"],
        body=json_body["wsgi.input"],
        headers={"content-type": json_body["CONTENT_TYPE"]},
    )

    # when
    body = request.parsed_body

    # then
    assert isinstance(body, JsonHttpMessage)
    assert "test_1" in body
    assert body["test_1"] == "1"
    assert body.get("test2", "default") == "default"


def test_parse_yaml_body() -> None:
    # given
    yaml_body = b"""
    test_1: 1
    test2: default
    """
    request = HttpRequest(
        HttpMethod.POST,
        body=yaml_body,
        headers={"content-type": "text/vnd.yaml"},
    )

    # when
    body = request.parsed_body

    # then
    assert isinstance(body, YamlHttpMessage)
    assert "test_1" in body
    assert body["test_1"] == 1
    assert body.get("test2", "default") == "default"


def test_simple_http_message() -> None:
    # given
    http_message = SimpleHttpMessage("Hello World!")

    # then
    assert http_message[0:5] == "Hello"
    assert http_message == "Hello World!"
    assert http_message.upper() == "HELLO WORLD!"
    assert isinstance(http_message, SimpleHttpMessage)


def test_can_convert_uploaded_file_to_bytes() -> None:
    # given
    request = HttpRequest(
        multipart_body["REQUEST_METHOD"],
        body=multipart_body["wsgi.input"],
        headers={"content-type": multipart_body["CONTENT_TYPE"]},
    )

    # when
    body = request.parsed_body
    file_bytes = bytes(body["file_a"])

    # then
    assert (
        file_bytes
        == b"GIF87a\x02\x00\x02\x00\x91\x00\x00\x00\x00\x00\xff\x8c\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\t\x00\x00\x03\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x02\x8cS\x00;"
    )


def test_can_create_binary_message() -> None:
    # given
    request = HttpRequest(HttpMethod.POST, "/test", body=binary_body)

    # when
    parsed_body = request.parsed_body
    binary_data = request.parsed_body.read()

    # then
    assert isinstance(parsed_body, BytesIO)
    assert isinstance(parsed_body, BinaryHttpMessage)
    assert binary_data == binary_body
