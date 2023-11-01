import os
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    prod = "prod"
    docker = "docker"
    local = "local"
    test = "test"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    APP_NAME: str = "integration"
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    LOG_LEVEL: str = "INFO"
    LOG_FILENAME: str = ""
    ENVIRONMENT: str = "prod"


environment: str = os.getenv("ENVIRONMENT", Environment.local).lower()
settings = Settings(_env_file=f"config/{environment}.env")
