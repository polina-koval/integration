import uvicorn

from integration.app.config import environment, Environment, settings
from integration.app.fastapi import create_app  # noqa
from cli_commands.common import RunnableCommand


class Service(RunnableCommand):
    name = "service"

    @classmethod
    def run(cls, args):
        uvicorn.run(
            "main:create_app",
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL.lower(),
            reload=environment == Environment.local,
        )
