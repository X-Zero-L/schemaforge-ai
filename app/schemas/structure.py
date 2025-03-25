"""
Schema definitions for structure-related endpoints.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class StructuredRequest(BaseModel):
    """Request schema for structuring data."""

    content: str = Field(..., description="Raw text content to be structured")
    schema_description: str = Field(
        ..., description="Expected structured data description"
    )
    system_prompt: Optional[str] = Field(None, description="System prompt (optional)")
    model_name: Optional[str] = Field(
        None,
        description="Model name to use (e.g., 'openai:gpt-4o', 'anthropic:claude-3-opus-latest')",
    )
    is_need_schema_description: bool = Field(
        False,
        description="Whether schema description should be included in system prompt. Default is False as advanced models usually don't need it",
    )
    struct_model_name: Optional[str] = Field(
        "DynamicModel", description="Model name to use for structuring"
    )


class StructureResponse(BaseModel):
    """Response schema for structured data."""

    success: bool = Field(..., description="Whether processing was successful")
    data: Dict[str, Any] = Field(..., description="Structured data")
    error: Optional[str] = Field(None, description="Error message")
    model_used: str = Field(..., description="The model used for processing")
