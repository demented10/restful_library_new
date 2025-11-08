from pydantic_settings import BaseSettings
from typing import Optional


#TODO можно обернуть в синглтон (?)
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://library_user:library_password@db:5432/library_db"

    class Config:
        env_file = ".env"

settings = Settings()