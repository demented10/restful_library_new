from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://library_user:library_password@db:5432/library_db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()