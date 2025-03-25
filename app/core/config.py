"""
Core configuration module for the structured API service.
Handles environment variables and application settings.
"""

import os
from typing import Dict, List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings configured via environment variables."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Structured API Service"
    PROJECT_DESCRIPTION: str = "Structured data processing API based on Pydantic-AI"

    # Auth settings
    API_KEY: str = os.getenv("API_KEY", "")
    API_KEY_NAME: str = "Authorization"
    REQUIRE_AUTH: bool = os.getenv("REQUIRE_AUTH", "true").lower() == "true"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Default model configuration
    DEFAULT_MODEL: str = "openai:gpt-4o"

    # Logging
    LOGFIRE_ENABLED: bool = True
    LOGFIRE_TOKEN: Optional[str] = os.getenv("LOGFIRE_TOKEN")

    # Model provider configurations
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL")

    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")

    MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")

    COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")

    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")

    RETRIES: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()