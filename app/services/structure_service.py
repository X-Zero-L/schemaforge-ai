"""
Service module for handling structured data processing.
"""

import json
from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field, create_model
from pydantic_ai import Agent

from app.core.logging import get_logger
from app.schemas.structure import StructuredRequest

logger = get_logger(__name__)


async def process_structured_data(
    request: StructuredRequest, model_name: str
) -> Tuple[Dict[str, Any], str]:
    """
    Process structured data based on the request.

    Args:
        request: The structured request containing content and schema
        model_name: The name of the model to use

    Returns:
        A tuple containing the structured data and the model used

    Raises:
        Exception: If there's an error processing the request
    """
    try:
        # Create dynamic model based on schema
        dynamic_model = create_dynamic_model(
            request.schema_description, request.struct_model_name
        )

        # Initialize agent with specified model
        agent = Agent(model_name, result_type=dynamic_model)

        # Set system prompt
        @agent.system_prompt
        async def system_prompt():
            default_prompt = "You are a data structuring expert. Please extract structured information from the provided content."
            prompt = request.system_prompt or default_prompt
            schema = (
                request.schema_description if request.is_need_schema_description else ""
            )
            return f"{prompt}\n{schema}"

        # Run the agent to get structured data
        result = await agent.run(request.content)

        # Return the structured data and model used
        return result.data.model_dump(), model_name

    except Exception as e:
        logger.error(f"Error processing structured data: {e}", _exc_info=True)
        raise e


def create_dynamic_model(
    schema_description: str, struct_model_name: str = "DynamicModel"
) -> BaseModel:
    """
    Create a dynamic Pydantic model from schema description.

    Args:
        schema_description: JSON schema or description string

    Returns:
        A dynamically created Pydantic model
    """
    try:
        # Try to parse schema_description as JSON
        schema_dict = json.loads(schema_description)
        # Extract field information from schema
        properties = schema_dict.get("properties", {})

        # Build field dictionary for create_model
        fields = {}
        for field_name, field_info in properties.items():
            field_type = str  # Default type
            description = field_info.get("description", "")

            # Set field type based on schema type
            type_str = field_info.get("type", "string")
            if type_str == "integer":
                field_type = int
            elif type_str == "number":
                field_type = float
            elif type_str == "boolean":
                field_type = bool
            elif type_str == "array":
                field_type = list

            # Create Field
            fields[field_name] = (field_type, Field(..., description=description))

        # Create dynamic model using create_model
        dynamic_model = create_model(struct_model_name, **fields)
        dynamic_model.__doc__ = schema_dict.get("description", schema_description)

    except (json.JSONDecodeError, Exception):
        # If JSON parsing fails, use a simple model
        logger.warning("Failed to parse schema_description as JSON, using simple model")
        dynamic_model = create_model(struct_model_name, __doc__=schema_description)

    return dynamic_model
