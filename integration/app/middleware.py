import json
import logging
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from integration.errors import ExceptionsProcessor
from integration.errors.exceptions import ErrorResponse, ErrorBase
from integration.errors.handlers import ERROR_HANDLERS
from integration.utils.request_id import X_REQUEST_ID, request_id_manager

logger = logging.getLogger(__name__)


class PingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        event = request.headers.get("X-API-Event")
        if event != "PING":
            response = await call_next(request)
        else:
            response = Response(json.dumps({"status": "ok"}))
        return response


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get(X_REQUEST_ID) or str(uuid4())
        request_id_manager.set(request_id)
        response = await call_next(request)
        response.headers[X_REQUEST_ID] = request_id
        return response


class ErrorMiddleware(BaseHTTPMiddleware):
    exc_processor = ExceptionsProcessor(*ERROR_HANDLERS)

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except Exception as ex:  # noqa
            errors = self.exc_processor.get_errors(ex)
            response = ErrorResponse(
                errors=[
                    ErrorBase(
                        type=error.type,
                        title=error.title,
                        detail=error.detail,
                        location=error.location,
                    )
                    for error in errors
                ],
            )

            return JSONResponse(
                status_code=errors[0].status,
                content=response.model_dump(exclude_none=True),
            )


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        logger.info(
            (
                f"Request from {request.client.host} to {request.url} -> "
                f"Response status code: {response.status_code}"
            )
        )
        return response
