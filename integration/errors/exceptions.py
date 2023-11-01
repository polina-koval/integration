import typing as t
from pydantic import BaseModel, Field

from integration.errors.types import ErrorType


class Location(BaseModel):
    entity: str = Field("body", description="Entity where error was raised", examples=["body"])
    variable: t.Optional[str] = Field(
        None, description="Json-pointer path to error", examples=["/users/1/name"]
    )


class ErrorBase(BaseModel):
    type: str = Field(..., description="Error type", examples=["type_error.integer"])
    title: str = Field(..., description="Title", examples=["value is not a valid integer"])
    detail: t.Optional[str] = Field(
        None,
        description="Error detail",
        examples=["Expected valid integer, got: 'peanut'"],
    )
    location: t.Optional[Location] = Field(None, description="Error location")


class ErrorResponse(BaseModel):
    errors: list[ErrorBase] = Field(..., description="Errors list")


class BaseError(Exception):
    """Base class for errors."""

    type: str = ErrorType.internal_error.name
    title: str = ErrorType.internal_error.value
    code = 500

    def __init__(
        self,
        type: str = None,
        title: str = None,
        detail: str = None,
        location: Location = None,
        code: int = None,
    ):
        self.code = code or self.code
        self.type = type or self.type
        self.title = title or self.title
        self.detail = detail
        self.location = location

    def __repr__(self):
        return f"Error({self.code=}, {self.type=}, {self.title=}, {self.detail=}, {self.location=})"


class InternalError(BaseError):
    pass


class AuthorizationError(BaseError):
    type: str = ErrorType.authorization_error.name
    title: str = ErrorType.authorization_error.value
    code = 401


class BadRequestError(BaseError):
    type: str = ErrorType.bad_request_error.name
    title: str = ErrorType.bad_request_error.value
    code = 400


class AccessDeniedError(BaseError):
    type: str = ErrorType.access_denied_error.name
    title: str = ErrorType.access_denied_error.value
    code = 403


class NotFoundError(BaseError):
    type: str = ErrorType.not_found_error.name
    title: str = ErrorType.not_found_error.value
    code = 404


class TooManyRequestsError(BaseError):
    type: str = ErrorType.too_many_requests_error.name
    title: str = ErrorType.too_many_requests_error.value
    code = 429
