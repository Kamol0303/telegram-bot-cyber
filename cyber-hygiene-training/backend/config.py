"""
Application configuration loaded from environment variables.
Educational cybersecurity awareness platform — no real credentials collected.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for backend and bot services."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Cyber Hygiene Awareness Training"
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "dev-secret-change-in-production"
    base_url: str = "http://localhost:8000"

    database_url: str = "sqlite+aiosqlite:///./data/training.db"

    telegram_bot_token: str = ""
    telegram_webhook_url: str = ""

    admin_username: str = "admin"
    admin_password: str = "admin"

    session_token_expire_hours: int = 24
    cors_origins: str = "http://localhost:8000"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
