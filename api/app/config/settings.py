import os
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"))

    mistral_api_key: str
    mistral_model_name: str

    database_url: str
    allowed_origins: list[str]
    api_version: str

    @computed_field
    @property
    def api_prefix(self) -> str:
        return f"/api/{self.api_version}"


@lru_cache
def settings() -> Settings:
    return Settings()
