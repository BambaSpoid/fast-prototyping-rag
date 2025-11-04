from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ES_HOST: str
    ES_USERNAME: str
    ES_PASSWORD: str
    ES_INDEX: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached environment settings"""
    return Settings()
