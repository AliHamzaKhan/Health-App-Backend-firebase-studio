
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
from pydantic import model_validator
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME: str = "MediConnect"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    GEMINI_API_KEY: str

    @model_validator(mode='after')
    def set_test_database_url(self) -> 'Settings':
        if self.TEST_DATABASE_URL is None:
            self.TEST_DATABASE_URL = self.DATABASE_URL.replace(
                self.POSTGRES_DB, f"{self.POSTGRES_DB}_test"
            )
        return self

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
