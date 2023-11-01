import uvicorn

from integration.app.config import environment, Environment, settings
from integration.app.fastapi import create_app  # noqa


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=environment == Environment.local,
    )
