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
    API_KEY_NAME: str = "X-API-Key"
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

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


# Dictionary of supported model categories for API reference
SUPPORTED_MODEL_CATEGORIES: Dict[str, List[str]] = {
    "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini"],
    "anthropic": [
        "claude-3-5-sonnet-latest",
        "claude-3-opus-latest",
        "claude-3-7-sonnet-latest",
    ],
    "google": ["google-gla:gemini-1.5-pro", "google-gla:gemini-1.5-flash"],
    "mistral": ["mistral:mistral-large-latest", "mistral:mistral-small-latest"],
    "cohere": ["cohere:command-r", "cohere:command-r-plus"],
    "groq": ["groq:llama-3.1-8b-instant", "groq:llama-3.2-90b-vision-preview"],
}
