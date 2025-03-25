"""
Main application module that initializes and configures the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging import setup_logging


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        A configured FastAPI application instance
    """
    # Set up logging first
    setup_logging()
    
    # Create FastAPI application with metadata
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    
    # Configure CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Include API routers
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app


# Create application instance
app = create_application()


@app.get("/")
async def root():
    """
    Root endpoint that redirects to API documentation.
    """
    return {"message": "Welcome to the Structured API Service. Visit /docs for API documentation."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
