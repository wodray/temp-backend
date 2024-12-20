from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_database: str
    db_user: str
    db_password: str
    db_echo: bool = False

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))


settings = Settings()
