from enum import Enum


class ErrorType(str, Enum):
    access_denied_error = "Access Denied Error"
    authorization_error = "Authorization Error"
    bad_request_error = "Bad Request Error"
    internal_error = "Internal Server Error"
    not_found_error = "Not Found"
    too_many_requests_error = "Too Many Requests Error"
