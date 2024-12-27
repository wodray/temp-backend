import sys

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_database: str
    db_user: str
    db_password: str
    db_echo: bool = False

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))


settings = Settings()  # type: ignore

# TODO 到这儿了
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        },
        {
            "sink": "logs/log_{time:YYYY-MM-DD}.log",
            "format": "{time:YYYY-MM-DDTHH:mm:ss} | {level} | {message}",
            "rotation": "10 MB",
            "retention": "10 days",
        },
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)
