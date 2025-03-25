"""
API v1 routes for the application.
"""

from fastapi import APIRouter
from .endpoints import structure

# Create API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(structure.router, tags=["structure"])