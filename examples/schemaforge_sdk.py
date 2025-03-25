"""
SchemaForge AI SDK

A simple SDK that wraps SchemaForge AI API calls, making it easier to use
the service without dealing with the underlying complexity.
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel, Field, ConfigDict

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants and configuration
DEFAULT_API_BASE = "http://localhost:8000"
DEFAULT_MODEL = "openai:gpt-4o"
DEFAULT_TIMEOUT = 60  # seconds

# Type variables for generic type hints
T = TypeVar('T', bound=BaseModel)

class SchemaForgeClient:
    """
    SchemaForge AI client that simplifies interacting with the SchemaForge API.
    
    This client handles authentication, request formatting, and response parsing,
    allowing you to focus on your data models rather than API details.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        default_model: str = DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize the SchemaForge client.
        
        Args:
            api_key: API key for authentication (defaults to API_KEY environment variable)
            api_base: Base URL for the API (defaults to environment variable or localhost)
            default_model: Default AI model to use (e.g., "openai:gpt-4o")
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.getenv("API_KEY", "")
        if not self.api_key:
            raise ValueError("API key is required. Set it via constructor or API_KEY environment variable.")
            
        self.api_base = api_base or os.getenv("API_BASE_URL", DEFAULT_API_BASE)
        self.default_model = default_model
        self.timeout = timeout
        
    def _get_headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        return {"X-API-Key": self.api_key}
    
    async def structure_data(
        self,
        content: str,
        model_class: Type[T],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> T:
        """
        Structure text data using the specified Pydantic model.
        
        Args:
            content: Text content to structure
            model_class: Pydantic model class to use for structuring
            model_name: AI model to use for processing (e.g., "openai:gpt-4o")
            system_prompt: Optional system prompt to guide the AI
            
        Returns:
            An instance of the specified model class populated with structured data
        """
        # Get the JSON schema from the Pydantic model
        model_schema = model_class.model_json_schema()
        
        # Prepare the request data
        request_data = {
            "content": content,
            "schema_description": json.dumps(model_schema),
            "model_name": model_name or self.default_model,
        }
        
        if system_prompt:
            request_data["system_prompt"] = system_prompt
        
        # Send the request to the API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/api/v1/structure",
                json=request_data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            # Parse the response
            result = response.json()
            
            if not result.get("success", False):
                error_msg = result.get("error", "Unknown error")
                raise ValueError(f"Failed to structure data: {error_msg}")
            
            # Convert the structured data into the model instance
            return model_class.model_validate(result["data"])
    
    async def generate_model(
        self,
        sample_data: str,
        model_name: str,
        description: str,
        requirements: Optional[str] = None,
        expected_fields: Optional[List[Dict[str, Any]]] = None,
        ai_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a Pydantic model from sample data.
        
        Args:
            sample_data: Sample data to analyze (text, JSON, CSV, etc.)
            model_name: Name for the generated model
            description: Description of what the model represents
            requirements: Optional specific requirements or validation rules
            expected_fields: Optional list of expected fields and their properties
            ai_model: AI model to use for generation
            
        Returns:
            Dictionary containing generated model code, JSON schema and fields
        """
        # Prepare the request data
        request_data = {
            "sample_data": sample_data,
            "model_name": model_name,
            "description": description,
            "llm_model_name": ai_model or self.default_model
        }
        
        if requirements:
            request_data["requirements"] = requirements
            
        if expected_fields:
            request_data["expected_fields"] = expected_fields
        
        # Send the request to the API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/api/v1/generate-model",
                json=request_data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            # Parse the response
            result = response.json()
            
            if not result.get("success", False):
                error_msg = result.get("error", "Unknown error")
                raise ValueError(f"Failed to generate model: {error_msg}")
            
            return {
                "model_name": result["model_name"],
                "model_code": result["model_code"],
                "json_schema": result["json_schema"],
                "fields": result["fields"],
                "model_used": result["model_used"]
            }
    
    # Synchronous versions of the async methods
    def structure_data_sync(
        self,
        content: str,
        model_class: Type[T],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> T:
        """Synchronous version of structure_data."""
        return asyncio.run(self.structure_data(
            content=content,
            model_class=model_class,
            model_name=model_name,
            system_prompt=system_prompt
        ))
    
    def generate_model_sync(
        self,
        sample_data: str,
        model_name: str,
        description: str,
        requirements: Optional[str] = None,
        expected_fields: Optional[List[Dict[str, Any]]] = None,
        ai_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synchronous version of generate_model."""
        return asyncio.run(self.generate_model(
            sample_data=sample_data,
            model_name=model_name,
            description=description,
            requirements=requirements,
            expected_fields=expected_fields,
            ai_model=ai_model
        ))
    
    # Utility methods to make working with the SDK easier
    @staticmethod
    def load_model_from_code(model_code: str) -> Type[BaseModel]:
        """
        Load a Pydantic model from generated code string.
        
        Args:
            model_code: Python code string containing a Pydantic model definition
            
        Returns:
            The Pydantic model class
        
        Warning: 
            This uses exec() which should only be used with trusted inputs.
        """
        # Create a namespace for the model
        namespace = {}
        
        # Execute the code in this namespace
        exec(model_code, namespace)
        
        # Find the model class in the namespace
        # Usually it will be the last class defined
        model_names = [name for name, obj in namespace.items() 
                      if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel]
        
        if not model_names:
            raise ValueError("No Pydantic model found in the generated code")
        
        # Return the model class
        return namespace[model_names[0]]


# Example usage
if __name__ == "__main__":
    # Define a simple Pydantic model
    class Person(BaseModel):
        name: str = Field(..., description="Person's full name")
        age: int = Field(..., description="Age in years")
        height: float = Field(..., description="Height in centimeters")
        occupation: Optional[str] = Field(None, description="Current occupation")
    
    # Create a client instance
    client = SchemaForgeClient()
    
    # Example 1: Structure data using an existing model
    try:
        # Synchronous version
        person = client.structure_data_sync(
            content="John Smith is a 32-year-old software engineer who is 182.5 cm tall.",
            model_class=Person
        )
        print(f"Structured data (sync): {person.model_dump_json(indent=2)}")
        
        # This can also be done asynchronously in your async code
        async def async_example():
            person = await client.structure_data(
                content="Emily Johnson is a 28-year-old teacher who is 165 cm tall.",
                model_class=Person
            )
            print(f"Structured data (async): {person.model_dump_json(indent=2)}")
        
        asyncio.run(async_example())
        
    except Exception as e:
        print(f"Error structuring data: {e}")
    
    # Example 2: Generate a new model from sample data
    try:
        # Generate a model for a product
        product_sample = """
        {
            "product_id": "P12345",
            "name": "Smartphone X",
            "price": 799.99,
            "in_stock": true,
            "specifications": {
                "screen_size": "6.5 inches",
                "processor": "SnapDragon 8",
                "storage": "128GB",
                "camera": "48MP"
            },
            "colors": ["Black", "Silver", "Gold"],
            "release_date": "2024-01-15"
        }
        """
        
        result = client.generate_model_sync(
            sample_data=product_sample,
            model_name="Product",
            description="A model representing product information for an e-commerce system"
        )
        
        print(f"\nGenerated model '{result['model_name']}' using {result['model_used']}:")
        print(f"JSON Schema: {json.dumps(result['json_schema'], indent=2)}")
        
        # Load and use the generated model
        ProductModel = client.load_model_from_code(result["model_code"])
        
        # Create a sample product
        product_data = {
            "product_id": "P67890",
            "name": "Laptop Pro",
            "price": 1299.99,
            "in_stock": True,
            "specifications": {
                "screen_size": "15.6 inches",
                "processor": "Intel i9",
                "storage": "1TB",
                "camera": "1080p"
            },
            "colors": ["Silver", "Space Gray"],
            "release_date": "2024-03-01"
        }
        
        # Validate using the generated model
        product = ProductModel.model_validate(product_data)
        print(f"\nValidated product using generated model: {product.model_dump_json(indent=2)}")
        
    except Exception as e:
        print(f"Error generating model: {e}") 