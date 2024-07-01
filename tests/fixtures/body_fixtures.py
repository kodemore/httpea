import os
from io import BytesIO

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

binary_body = (
    b"GIF87a\x02\x00\x02\x00\x91\x00\x00\x00\x00\x00\xff\x8c\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\t\x00"
    b"\x00\x03\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x02\x8cS\x00;"
)

multipart_body = {
    "CONTENT_TYPE": "multipart/form-data; charset=utf-8; boundary=__TEST_BOUNDARY__",
    "REQUEST_METHOD": "POST",
    "wsgi.input": BytesIO(
        b"--__TEST_BOUNDARY__\r\n"
        b'Content-Disposition: form-data; name="id"\r\n\r\n'
        b"51b8a72aaaf909e303000034\r\n"
        b"--__TEST_BOUNDARY__\r\n"
        b'Content-Disposition: form-data; name="file_a"; filename="orange.gif"\r\n'
        b"Content-Type: image/gif\r\n\r\n"
        b"GIF87a\x02\x00\x02\x00\x91\x00\x00\x00\x00\x00\xff\x8c\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\t\x00"
        b"\x00\x03\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x02\x8cS\x00;\r\n"
        b"--__TEST_BOUNDARY__\r\n"
        b'Content-Disposition: form-data; name="file_b"; filename="yellow.gif"\r\n'
        b"Content-Type: image/gif\r\n\r\n"
        b"GIF87a\x02\x00\x02\x00\x91\x00\x00\x00\x00\x00\xff\xf6~\xff\xff\xff\x00\x00\x00!\xf9\x04\t\x00\x00"
        b"\x03\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x02\x8cS\x00;\r\n"
        b"--__TEST_BOUNDARY__\r\n"
        b'Content-Disposition: form-data; name="test_1"\r\n\r\n'
        b"only string value\r\n"
        b"--__TEST_BOUNDARY__\r\n"
        b'Content-Disposition: form-data; name="test_2"\r\n\r\n'
        b"1232\r\n"
        b"--__TEST_BOUNDARY__--\r\n"
    ),
}

form_body = {
    "CONTENT_TYPE": "application/x-www-form-urlencoded; charset=utf-8",
    "REQUEST_METHOD": "POST",
    "wsgi.input": BytesIO(b"test_1=1&test_2=Test+2&test_3=%7Btest+3%7D"),
}

json_body = {
    "CONTENT_TYPE": "application/json; charset=utf-8",
    "REQUEST_METHOD": "POST",
    "wsgi.input": BytesIO(b'{"test_1":"1","test_2":"Test 2","test_3":"{test 3}"}'),
}

cat_file = open(DIR_PATH + "/grumpy_cat_test.jpg", "rb")

cat_file_body = {
    "CONTENT_TYPE": "multipart/form-data; boundary=__CAT_BOUNDARY__",
    "REQUEST_METHOD": "POST",
    "wsgi.input": BytesIO(
        b"--__CAT_BOUNDARY__\r\n"
        b'Content-Disposition: Content-Disposition: form-data; name="image"; filename="generic-cat.jpg"\r\nContent-Type: image/jpeg"\r\n\r\n'
        + cat_file.read()
        + b"\r\n--__CAT_BOUNDARY__--\r\n"
    ),
}
