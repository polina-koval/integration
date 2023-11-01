from dataclasses import dataclass

import logging
import typing as t
from abc import ABC, abstractmethod
from fastapi.exceptions import RequestValidationError
from httpx import HTTPError
from inflection import parameterize, underscore
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any, Type

from integration.errors import BaseError
from integration.errors.exceptions import Location
from integration.errors.types import ErrorType


@dataclass(frozen=True)
class Error:
    status: int = None
    type: str = None
    title: str = None
    location: Any = None
    detail: str = None


class AbstractErrorHandler(ABC):
    handle_exception: t.Union[Exception, tuple[Exception]] = None

    def __init__(self):
        if not self.handle_exception:
            raise NotImplemented

    @abstractmethod
    def get_errors(self, exc: Exception) -> list[Error]:
        pass


class BaseErrorHandler(AbstractErrorHandler):
    handle_exception = BaseError

    def get_errors(self, exc: BaseError) -> list[Error]:
        return [
            Error(
                status=exc.code,
                type=exc.type,
                title=exc.title,
                detail=exc.detail,
                location=exc.location,
            )
        ]


class FastAPIErrorHandler(BaseErrorHandler):
    handle_exception = HTTPException

    def get_errors(self, exception: HTTPException) -> list[Error]:
        return [
            Error(
                status=exception.status_code,
                type=underscore(parameterize(exception.detail)).lower(),
                title=exception.detail,
            )
        ]


class ValidationErrorHandler(BaseErrorHandler):
    handle_exception = RequestValidationError, ValidationError

    def get_variable(self, path: tuple):
        if not path:
            return None
        return "/" + "/".join(str(elem) for elem in path)

    def get_location(self, pydantic_location: tuple = None) -> t.Optional[Location]:
        if pydantic_location is None:
            return None

        entity, *path = pydantic_location
        return Location(entity=entity, variable=self.get_variable(path))

    def get_errors(self, exception: RequestValidationError) -> list[Error]:
        return [
            Error(
                status=HTTP_400_BAD_REQUEST,
                type=error.get("type"),
                title=error.get("msg"),
                location=self.get_location(error.get("loc")),
            )
            for error in exception.errors()
        ]


class HttpxErrorHandler(BaseErrorHandler):
    handle_exception = HTTPError

    def get_errors(self, exception: HTTPError) -> list[Error]:
        return [
            Error(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                type=ErrorType.internal_error.name,
                title=str(exception) or exception.__class__.__name__,
            )
        ]


ERROR_HANDLERS = [
    FastAPIErrorHandler,
    ValidationErrorHandler,
    BaseErrorHandler,
    HttpxErrorHandler,
]


class ExceptionsProcessor:
    def __init__(self, *args: Type[AbstractErrorHandler]):
        self.handlers = []
        self.add_handlers(*args)

    def add_handlers(self, *args: Type[AbstractErrorHandler]):
        self.handlers.extend(
            [
                handler if isinstance(handler, AbstractErrorHandler) else handler()
                for handler in args
            ]
        )

    def get_errors(self, exc: Exception) -> list[Error]:
        for handler in self.handlers:
            if isinstance(exc, handler.handle_exception):
                return handler.get_errors(exc)

        logging.exception("An unknown exception was raised")

        return [
            Error(
                status=500,
                type=ErrorType.internal_error.name,
                title=str(exc).capitalize(),
            )
        ]
