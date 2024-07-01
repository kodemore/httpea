# httpkit

Httpkit is an abstraction library which provides a set of classes that represent different parts of the http communication process. These classes can be used to build custom http clients and servers, or to extend existing ones.

The idea behind this library is to provide an interface for manipulating http requests and responses in a way that is easy to use and understand.

## Features
- HttpRequest and HttpResponse classes for representing http requests and responses
- Multipart body parsing for handling file uploads
- Fast and efficient parsing and building of http messages from scratch
- Fast routing and router for your application
- Query string parsing
- Cookie parsing and building

## Installation

You can install httpkit using pip:
```bash
pip install httpkit
```

,or with poetry:
```bash
poetry add httpkit
```

## Usage

This is an example guide of how basic usage of the library looks like. More detailed examples can be found in tests.

### HttpRequest

HttpRequest objects can be compared, they support query string parsing, cookies, headers and body parsing, including multipart body parsing.

```python
from httpkit import HttpRequest, HttpCookie

request = HttpRequest(HttpRequest.GET, "/" ,query_string="name=John&age=30")
# set headers
request.headers["Content-Type"] = "application/json"
# set body
request.body.write(b"Hello, World!")
# set cookies
request.cookies["session"] = "1234567890"

assert isinstance(request.cookies["session"], HttpCookie)
assert request.query_string["name"] == "John"
assert request.query_string["age"] == 30
assert str(request.query_string) == "name=John&age=30"
```

### HttpResponse

Same like HttpRequest, HttpResponse objects can be compared, they support cookies, headers and body writing.

```python
from httpkit import HttpResponse, HttpCookie, HttpStatus

response = HttpResponse("Example response", HttpStatus.OK)

# write body
response.write(b"Hello, World!")

# set cookies
response.cookies.append(HttpCookie("cookie-name", "cookie-value", secure=True, http_only=True))
```

### Route and Router

```python
from httpkit import Route

route = Route("/example/{pattern}")
result = route.match("/example/test")

assert result
assert result["pattern"] == "test"
assert not route.match("/example")

# wildcard route
route = Route("/example/*")
assert route.match("/example/test")
assert route.match("/example/test/123")
assert not route.match("/invalid")
```

```python
from httpkit import Router, HttpRequest, HttpNotFoundError

router = Router()
router.append("/users/{user_id}", lambda request, response, user_id: response.write(user_id), HttpRequest.GET)

try:
    route, callback = router.match("/users/123", HttpRequest.GET)
except HttpNotFoundError:
    pass

```



