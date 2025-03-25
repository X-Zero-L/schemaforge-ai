"""
Authentication module for the structured API service.
Provides API key validation functionality.
"""

from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validate API key from request header.
    
    Args:
        api_key_header: API key from request header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not settings.REQUIRE_AUTH:
        return True  # Authentication is disabled
    
    if not settings.API_KEY:
        logger.warning("API key authentication is enabled but no API key is set in environment variables")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key authentication is enabled but no API key is set on the server",
        )
    
    if api_key_header and api_key_header.startswith("Bearer "):
        api_key = api_key_header.split(" ")[1]
    else:
        api_key = api_key_header
    
    if api_key != settings.API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return api_key 