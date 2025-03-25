"""
Logging setup for the application.
Uses logfire for structured logging.
"""

import logfire
from .config import settings


def setup_logging():
    """Configure the logging system for the application."""
    if settings.LOGFIRE_ENABLED:
        logfire.configure(send_to_logfire="if-token-present")
        logfire.instrument_pydantic_ai()
        logfire.info("Logging initialized with logfire")


def get_logger(name: str):
    """Get a logger instance for a specific module.

    Args:
        name: The name of the module or component

    Returns:
        A configured logger instance
    """
    return logfire
