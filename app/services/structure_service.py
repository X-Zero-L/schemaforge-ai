"""
Service module for handling structured data processing.
"""

import json
from typing import Dict, Any, Tuple, List, Optional, Literal, Type
from pydantic import BaseModel, Field, create_model
from pydantic_ai import Agent
from enum import Enum

from app.core.logging import get_logger
from app.core.config import settings
from app.schemas.structure import StructuredRequest
import logfire

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
        agent = Agent(model_name, result_type=dynamic_model, retries=settings.RETRIES)

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
    根据 JSON Schema 递归生成 Pydantic 模型，支持：
    - object/array 递归建模
    - required 可选性
    - enum → Literal
    - additionalProperties → Dict[str, T]
    - default 映射到 Field(default=...)
    """
    logfire.info("create_dynamic_model", schema_description=schema_description)
    def json_schema_to_base_model(schema: dict[str, Any]) -> Type[BaseModel]:
        type_mapping: dict[str, type] = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])
        model_fields = {}

        def process_field(field_name: str, field_props: dict[str, Any]) -> tuple:
            """Recursively processes a field and returns its type and Field instance."""
            json_type = field_props.get("type", "string")
            enum_values = field_props.get("enum")

            # Handle Enums
            if enum_values:
                enum_name: str = f"{field_name.capitalize()}Enum"
                field_type = Enum(enum_name, {v: v for v in enum_values})
            # Handle Nested Objects
            elif json_type == "object" and "properties" in field_props:
                field_type = json_schema_to_base_model(
                    field_props
                )  # Recursively create submodel
            # Handle Arrays with Nested Objects
            elif json_type == "array" and "items" in field_props:
                item_props = field_props["items"]
                if item_props.get("type") == "object":
                    item_type: type[BaseModel] = json_schema_to_base_model(item_props)
                else:
                    item_type: type = type_mapping.get(item_props.get("type"), Any)
                field_type = list[item_type]
            else:
                field_type = type_mapping.get(json_type, Any)

            # Handle default values and optionality
            default_value = field_props.get("default", ...)
            nullable = field_props.get("nullable", False)
            description = field_props.get("title", "")

            if nullable:
                field_type = Optional[field_type]

            if field_name not in required_fields:
                default_value = field_props.get("default", None)

            return field_type, Field(default_value, description=description)

        # Process each field
        for field_name, field_props in properties.items():
            model_fields[field_name] = process_field(field_name, field_props)

        return create_model(schema.get("title", "DynamicModel"), **model_fields)
    return json_schema_to_base_model(json.loads(schema_description))