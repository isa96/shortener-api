from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    """ Settings for the application """

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener_app.db"

    class Config:
        """ Config for the settings """

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """ Get settings for the application """

    settings = Settings()
    print(f"Load settings for {settings.env_name}")

    return settings
