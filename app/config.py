import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Azure AI Language (Text Analytics)
    AZURE_LANGUAGE_ENDPOINT: str = os.getenv("AZURE_LANGUAGE_ENDPOINT", "")
    AZURE_LANGUAGE_KEY: str = os.getenv("AZURE_LANGUAGE_KEY", "")

    # Limite de caracteres por análise (free tier: 5.000 por documento)
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "5000"))


settings = Settings()
