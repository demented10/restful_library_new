from pydantic_settings import BaseSettings
from typing import Optional


#TODO можно обернуть в синглтон (?)
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/test"

    class Config:
        env_file = ".env"

settings = Settings()