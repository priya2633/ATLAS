from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import dotenv_values
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

print(dotenv_values(BASE_DIR / ".env"))

from pathlib import Path



BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):

    app_name: str = Field(default="Atlas")
    app_version: str = Field(default="1.0.0")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    database_url: str

    redis_url: str

    openai_api_key: str = ""

    debug: bool = False

    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """
    Returns a singleton Settings instance.
    Configuration is loaded once and cached for the
    lifetime of the application.
    """
    return Settings()


settings = get_settings()