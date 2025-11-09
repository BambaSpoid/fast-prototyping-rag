from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ES_HOST: str
    ES_USERNAME: str | None = None
    ES_PASSWORD: str | None = None
    ES_INDEX: str = "metrics-cdr-alarmesu2020-bigdata"
    OPENAI_API_KEY: str | None = None
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached environment settings"""
    return Settings()
