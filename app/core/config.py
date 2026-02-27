# app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

    def get_async_db_url(self) -> str:
        """Convert DATABASE_URL to async format, removing SSL query params."""
        url = self.DATABASE_URL
        if "?" in url:
            base_url = url.split("?")[0]
        else:
            base_url = url

        # Ensure it has asyncpg driver
        if "postgresql://" in base_url:
            base_url = base_url.replace("postgresql://", "postgresql+asyncpg://")

        return base_url

    def get_sync_db_url(self) -> str:

        url = self.DATABASE_URL
        if "postgresql+asyncpg://" in url:
            url = url.replace("postgresql+asyncpg://", "postgresql://")

        if "?" in url:
            base_url = url.split("?")[0]
        else:
            base_url = url

        return base_url


settings = Settings()
