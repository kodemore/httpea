__all__ = [
    "HttpError",
    "HttpBadRequestError",
    "HttpUnauthorizedError",
    "HttpForbiddenError",
    "HttpNotFoundError",
    "HttpMethodNotAllowedError",
    "HttpConflictError",
    "HttpGoneError",
    "HttpPreconditionFailedError",
    "HttpPayloadTooLargeError",
    "HttpUriTooLongError",
    "HttpUnsupportedMediaTypeError",
    "HttpUnprocessableEntityError",
    "HttpLockedError",
    "HttpPreconditionRequiredError",
    "HttpTooManyRequestsError",
    "HttpServerError",
    "HttpNotImplementedError",
    "HttpBadGatewayError",
    "HttpServiceUnavailableError",
    "HttpGatewayTimeoutError",
    "HttpInsufficientStorageError",
]


class HttpError(Exception):
    status_code: int = 500
    http_message = "Internal Server Error"

    def __str__(self) -> str:
        return self.http_message

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({self.status_code}, {self.http_message})"


class HttpBadRequestError(HttpError):
    status_code: int = 400
    http_message = "Bad Request"


class HttpUnauthorizedError(HttpBadRequestError):
    status_code: int = 401
    http_message = "Unauthorized"


class HttpForbiddenError(HttpBadRequestError):
    status_code: int = 403
    http_message = "Forbidden"


class HttpNotFoundError(HttpBadRequestError):
    status_code: int = 404
    http_message = "Not Found"


class HttpMethodNotAllowedError(HttpBadRequestError):
    status_code: int = 405
    http_message = "Method Not Allowed"


class HttpConflictError(HttpBadRequestError):
    status_code: int = 409
    http_message = "Conflict"


class HttpGoneError(HttpBadRequestError):
    status_code: int = 410
    http_message = "Gone"


class HttpPreconditionFailedError(HttpBadRequestError):
    status_code: int = 412
    http_message = "Precondition Failed"


class HttpPayloadTooLargeError(HttpBadRequestError):
    status_code: int = 413
    http_message = "Payload Too Large"


class HttpUriTooLongError(HttpBadRequestError):
    status_code: int = 414
    http_message = "URI Too Long"


class HttpUnsupportedMediaTypeError(HttpBadRequestError):
    status_code: int = 415
    http_message = "Unsupported Media Type"


class HttpUnprocessableEntityError(HttpBadRequestError):
    status_code: int = 422
    http_message = "Unprocessable Entity"


class HttpLockedError(HttpBadRequestError):
    status_code: int = 423
    http_message = "Locked"


class HttpPreconditionRequiredError(HttpBadRequestError):
    status_code: int = 428
    http_message = "Precondition Required"


class HttpTooManyRequestsError(HttpBadRequestError):
    status_code: int = 429
    http_message = "Too Many Requests"


class HttpServerError(HttpError):
    status_code: int = 500
    http_message = "Internal Server Error"


class HttpNotImplementedError(HttpServerError):
    status_code: int = 501
    http_message = "Not Implemented"


class HttpBadGatewayError(HttpServerError):
    status_code: int = 502
    http_message = "Bad Gateway"


class HttpServiceUnavailableError(HttpServerError):
    status_code: int = 503
    http_message = "Service Unavailable"


class HttpGatewayTimeoutError(HttpServerError):
    status_code: int = 504
    http_message = "Gateway Timeout"


class HttpInsufficientStorageError(HttpServerError):
    status_code: int = 507
    http_message = "Insufficient Storage"
