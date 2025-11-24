import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "个人导航网站"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "insecure_default_key"
    DATABASE_URL: str = "sqlite:///./navigator.db"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    GOOGLE_SEARCH_URL: str = "https://www.google.com/search"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
