"""
Structure-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Security
from app.core.config import settings
from app.core.auth import get_api_key
from app.schemas.structure import StructuredRequest, StructureResponse
from app.services import structure_service
from app.core.logging import get_logger
import logfire

router = APIRouter()
logger = get_logger(__name__)


@router.post("/structure", response_model=StructureResponse, description="Process and structure text data")
async def structure_data(
    request: StructuredRequest,
    api_key: str = Security(get_api_key)
):
    """
    Process and structure text data based on the provided schema.
    
    - **content**: Raw text content to be structured
    - **schema_description**: Expected structured data description
    - **system_prompt**: System prompt (optional)
    - **model_name**: Model name to use (optional)
    - **is_need_schema_description**: Whether to include schema in the system prompt
    """
    try:
        # Get model name from request or use default
        model_name = request.model_name or settings.DEFAULT_MODEL
        
        # Process the structured data
        data, used_model = await structure_service.process_structured_data(request, model_name)
        logfire.info("structure_data", data=data, used_model=used_model)
        # Return successful response
        return StructureResponse(
            success=True,
            data=data,
            model_used=used_model
        )
    except Exception as e:
        # Handle errors
        logger.error(f"Error structuring data: {e}", _exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 