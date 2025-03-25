"""
Model generation API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Security
from app.core.config import settings
from app.core.auth import get_api_key
from app.schemas.structure import ModelGenerationRequest, ModelGenerationResponse, ModelFieldDefinition
from app.services import model_generation_service
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/generate-model", response_model=ModelGenerationResponse, description="Generate a Pydantic model from sample data")
async def generate_model(
    request: ModelGenerationRequest,
    api_key: str = Security(get_api_key)
):
    """
    Generate a Pydantic model based on sample data and requirements.
    
    - **sample_data**: Sample data in text format to analyze for model creation
    - **model_name**: Name to use for the generated model
    - **description**: Description of what the model represents
    - **requirements**: Specific requirements or expectations for the model (optional)
    - **expected_fields**: Optional list of expected fields
    - **llm_model_name**: Model name to use for generation (optional)
    """
    try:
        # Get model name from request or use default
        llm_model_name = request.llm_model_name or settings.DEFAULT_MODEL
        
        # Generate the model
        model_code, fields, used_model = await model_generation_service.generate_model(request, llm_model_name)
        
        # Return successful response
        data = ModelGenerationResponse(
            success=True,
            model_name=request.model_name,
            model_code=model_code,
            fields=fields,
            model_used=used_model
        )
        logger.info("generate_result", data=data)
        return data
    except Exception as e:
        # Handle errors
        logger.error(f"Error generating model: {e}", _exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 