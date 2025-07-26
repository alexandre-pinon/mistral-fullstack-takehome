from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    mistral_api_key: str
    mistral_model_name: str

    database_url: str
    allowed_origins: list[str]


@lru_cache
def get_settings() -> Settings:
    return Settings()
