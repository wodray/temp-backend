import sys

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_password: str
    db_echo: bool = False

    redis_host: str
    redis_port: int
    redis_password: str

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))


settings = Settings()  # type: ignore


log_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "{time:[YYYY-MM-DD HH:mm:ss]}[{level}] - {message}",
        },
        {
            "sink": "logs/log_{time:YYYY-MM-DD}.log",
            "format": "{time:[YYYY-MM-DDTHH:mm:ss.SSS]}[{level}] - {message}",
            "rotation": "10 MB",
            "retention": "10 days",
        },
    ],
    "extra": None,
}
logger.configure(**log_config)
