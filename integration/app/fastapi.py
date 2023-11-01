from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware import Middleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from integration.app.logging import configure_logging
from integration.app.middleware import (
    RequestIdMiddleware,
    ErrorMiddleware,
    PingMiddleware,
    LoggerMiddleware,
)


status_router = APIRouter(tags=["health_check"])


def raise_exc(request, exc):
    """Raises an exception to bypass built-in Starlette and FastAPI error handlers"""
    raise exc


@status_router.get("/status")
def health_check():
    return {"status": "ok"}


def create_app():
    configure_logging()
    app = FastAPI(
        title="integration",
        middleware=[
            Middleware(LoggerMiddleware),
            Middleware(RequestIdMiddleware),
            Middleware(PingMiddleware),
            Middleware(ErrorMiddleware),
        ],
        exception_handlers={StarletteHTTPException: raise_exc, RequestValidationError: raise_exc},
    )
    app.include_router(status_router)
    return app
