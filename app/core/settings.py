from typing import List, Tuple
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
import os

APP_ENV: str = ""


class Settings(BaseSettings):
    # base
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    DEBUG: bool = True
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    TITLE: str = "fastapi clean template"
    VERSION: str = "0.0.1"

    # database
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "mongodb": "mongodb",
    }
    DB: str = "mongodb"
    DB_HOST: str = "localhost"
    DB_PORT: str = "27017"
    DB_USER: str = ""
    DB_NAME: str = ""
    DB_PASSWORD: str = ""
    DB_ENGINE: str = DB_ENGINE_MAPPER[DB]
    DATABASE_URI_FORMAT: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}"
    )
    DATABASE_URI: str = ""

    # auth
    SECRET_KEY: str = "secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    API_PREFIX: str = "/api"

    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 20

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env" if "prod" in os.getenv("APP_ENV").lower() else ".env.dev",
    )


class TestConfigs(Settings):
    APP_ENV: str = "test"


settings = Settings()

if APP_ENV == "prod":
    pass
elif APP_ENV == "stage":
    pass
elif APP_ENV == "test":
    settings = TestConfigs()
