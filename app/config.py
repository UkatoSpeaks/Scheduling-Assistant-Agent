from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    MISTRAL_API_KEY: str = Field(...)
    MODEL_NAME: str = Field(default="mistral-large-latest")

    DATABASE_URL: str = Field(default="sqlite:///appointments.db")
    CHECKPOINT_DB: str = Field(default="memory.db")

    WEBHOOK_URL: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()