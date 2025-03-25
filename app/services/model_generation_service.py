"""
Service module for handling model generation.
"""

import json
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field, create_model
from pydantic_ai import Agent

from app.core.logging import get_logger
from app.schemas.structure import ModelGenerationRequest, ModelFieldDefinition

logger = get_logger(__name__)


async def generate_model(
    request: ModelGenerationRequest, llm_model_name: str
) -> Tuple[str, List[ModelFieldDefinition], str]:
    """
    Generate a Pydantic model based on the request.

    Args:
        request: The model generation request
        llm_model_name: The name of the LLM model to use

    Returns:
        A tuple containing the generated model code, list of fields, and the model used

    Raises:
        Exception: If there's an error processing the request
    """
    try:
        # Define the ModelGenerator dynamic model
        class ModelGeneratorOutput(BaseModel):
            model_code: str = Field(..., description="The generated model code in Python using Pydantic")
            fields: List[ModelFieldDefinition] = Field(..., description="List of fields defined in the model")
            rationale: str = Field(..., description="Explanation of why these fields were chosen and how they relate to the sample data")

        # Initialize agent with specified model
        agent = Agent(llm_model_name, result_type=ModelGeneratorOutput)

        # Set system prompt
        @agent.system_prompt
        async def system_prompt():
            base_prompt = """You are an expert at creating Pydantic models based on sample data.
Your task is to analyze the provided sample data and generate a Pydantic model that accurately represents this data structure.
The model should follow best practices for Pydantic models, including:
1. Proper typing of fields using Python type hints
2. Using Field() with detailed descriptions for each field
3. Handling optional fields appropriately with Optional[] type hints
4. Using appropriate default values and factories where needed
5. Following Pydantic conventions for model creation

The output model should be production-ready and follow PEP 8 standards.
Ensure imports are specified correctly at the top of the file.
"""
            
            if request.requirements:
                base_prompt += f"\nThe model should adhere to these specific requirements: {request.requirements}"
                
            if request.expected_fields:
                base_prompt += "\nThe model should include these expected fields, but you can add more if needed based on the sample data:"
                for field in request.expected_fields:
                    default_info = f", default={field.default}" if field.default is not None else ""
                    required_info = "required" if field.required else "optional"
                    base_prompt += f"\n- {field.name} ({field.field_type}, {required_info}): {field.description}{default_info}"
                    
            return base_prompt

        # Create a structured input object
        structured_input = {
            "sample_data": request.sample_data,
            "model_name": request.model_name,
            "description": request.description
        }
        
        # Run the agent to get the model generation result
        result = await agent.run(json.dumps(structured_input))
        
        # Return the generated model code, fields, and model used
        return result.data.model_code, result.data.fields, llm_model_name

    except Exception as e:
        logger.error(f"Error generating model: {e}", _exc_info=True)
        raise e 