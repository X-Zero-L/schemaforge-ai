"""
API v1 routes for the application.
"""

from fastapi import APIRouter
from .endpoints import structure, model_generation

# Create API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(structure.router, tags=["structure"])
api_router.include_router(model_generation.router, tags=["model_generation"])