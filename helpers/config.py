# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_EXTENSION: list
    FILE_MAX_SIZE: 10

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
