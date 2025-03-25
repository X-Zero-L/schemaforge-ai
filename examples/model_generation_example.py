"""
Model Generation API Usage Example

This script demonstrates how to use the model generation API to automatically create Pydantic models
from different types of data. Supports generating from JSON, text, CSV, and other formats.
"""

import httpx
import asyncio
import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("API_KEY", "")
# Default API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class ModelFieldDefinition(BaseModel):
    """Definition of a single field for a model"""
    
    name: str = Field(..., description="Field name")
    field_type: str = Field(..., description="Field type (string, integer, number, boolean, array, etc.)")
    description: str = Field(..., description="Field description")
    required: bool = Field(True, description="Whether the field is required")
    default: Optional[Any] = Field(None, description="Default value for the field")


async def generate_model(
    sample_data: str,
    model_name: str,
    description: str,
    requirements: str = None,
    expected_fields: List[Dict[str, Any]] = None,
    llm_model_name: str = None
) -> Dict[str, Any]:
    """
    Send a model generation request to the API

    Args:
        sample_data: Sample data text to analyze for model creation
        model_name: Name to use for the generated model
        description: Description of what the model represents
        requirements: Specific requirements or expectations (optional)
        expected_fields: Optional list of expected fields
        llm_model_name: Model name to use for generation (optional, e.g., "openai:gpt-4o")

    Returns:
        Dictionary containing the generated model code and other information
    """
    request_data = {
        "sample_data": sample_data,
        "model_name": model_name,
        "description": description
    }

    if requirements:
        request_data["requirements"] = requirements
        
    if expected_fields:
        request_data["expected_fields"] = expected_fields
        
    if llm_model_name:
        request_data["llm_model_name"] = llm_model_name

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/api/v1/generate-model",
            json=request_data,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=60
        )
        return response.json()


async def json_model_example():
    """Example 1: Generate a model from JSON data"""
    json_sample = '''
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
    '''
    
    print("\n=== Example 1: Generate Product Model ===")
    result = await generate_model(
        sample_data=json_sample,
        model_name="Product",
        description="A model representing product information for an e-commerce system",
        llm_model_name="openai:gpt-4o"
    )
    
    print(f"Success: {result.get('success', False)}")
    print(f"Model Name: {result.get('model_name')}")
    print("\nGenerated Model Code:")
    print(result.get('model_code'))
    print(f"\nModel Used: {result.get('model_used')}")


async def text_model_example_with_requirements():
    """Example 2: Generate a model with specific requirements"""
    text_sample = '''
    Customer: John Smith
    Email: john.smith@example.com
    Phone: (555) 123-4567
    Membership Level: Gold
    Points: 1250
    Sign-up Date: 2023-03-15
    Last Purchase: 2024-02-20
    Preferred Categories: Electronics, Books, Home Appliances
    Address: 123 Main St, Apt 4B, New York, NY 10001
    '''
    
    # Define expected fields
    expected_fields = [
        {
            "name": "customer_id",
            "field_type": "string",
            "description": "Unique identifier for the customer",
            "required": True
        },
        {
            "name": "email",
            "field_type": "string",
            "description": "Customer's email address",
            "required": True
        },
        {
            "name": "phone",
            "field_type": "string",
            "description": "Customer's phone number",
            "required": False
        }
    ]
    
    print("\n=== Example 2: Generate Customer Model with Requirements ===")
    result = await generate_model(
        sample_data=text_sample,
        model_name="Customer",
        description="A model representing customer information for a CRM system",
        requirements="Email must be validated. Phone should be optional. Include address parsing into components.",
        expected_fields=expected_fields,
        llm_model_name="openai:gpt-4o"
    )
    
    print(f"Success: {result.get('success', False)}")
    print(f"Model Name: {result.get('model_name')}")
    print("\nGenerated Model Code:")
    print(result.get('model_code'))
    print(f"\nModel Used: {result.get('model_used')}")


async def csv_model_example():
    """Example 3: Generate a model from CSV-like sample"""
    csv_sample = '''
    id,title,author,year,pages,genre,rating,is_bestseller
    1,"The Great Novel","Jane Smith",2022,320,"Fiction",4.8,true
    2,"Science Explained","John Doe",2021,250,"Non-fiction",4.5,true
    3,"History of Everything","Alice Johnson",2023,420,"History",4.2,false
    '''
    
    print("\n=== Example 3: Generate Book Model from CSV-like Data ===")
    result = await generate_model(
        sample_data=csv_sample,
        model_name="Book",
        description="A model representing book information for a library system",
        requirements="Year should be validated to be between 1900 and current year. Rating should be a float between 0 and 5."
    )
    
    print(f"Success: {result.get('success', False)}")
    print(f"Model Name: {result.get('model_name')}")
    print("\nGenerated Model Code:")
    print(result.get('model_code'))
    print(f"\nModel Used: {result.get('model_used')}")


async def complex_nested_model_example():
    """Example 4: Generate a complex nested model"""
    nested_json_sample = '''
    {
        "order_id": "ORD-2024-12345",
        "customer": {
            "id": "CUST-789",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "vip_level": 3
        },
        "items": [
            {
                "product_id": "P-001",
                "name": "Smart Watch",
                "quantity": 1,
                "unit_price": 1299.99,
                "discount": 0.15
            },
            {
                "product_id": "P-002",
                "name": "Bluetooth Earphones",
                "quantity": 2,
                "unit_price": 299.50,
                "discount": 0
            }
        ],
        "payment": {
            "method": "Credit Card",
            "status": "Completed",
            "transaction_id": "TXN-887766",
            "amount": 1618.99
        },
        "shipping": {
            "address": "88 Market Street, San Francisco, CA 94103",
            "method": "Express",
            "fee": 20.00,
            "estimated_delivery": "2024-04-15"
        },
        "order_date": "2024-04-01",
        "status": "Confirmed"
    }
    '''
    
    print("\n=== Example 4: Generate Complex Nested Order Model ===")
    result = await generate_model(
        sample_data=nested_json_sample,
        model_name="Order",
        description="A model representing order information for an e-commerce system, including customer details, line items, payment, and shipping information",
        requirements="All price fields should be non-negative. Item quantities must be positive integers. Create appropriate sub-models for nested structures.",
        llm_model_name="openai:gpt-4o"
    )
    
    print(f"Success: {result.get('success', False)}")
    print(f"Model Name: {result.get('model_name')}")
    print("\nGenerated Model Code:")
    print(result.get('model_code'))
    print(f"\nModel Used: {result.get('model_used')}")


async def main():
    # Check if API_KEY is set
    if not API_KEY:
        print(
            "WARNING: API_KEY environment variable is not set. API requests may fail."
        )
        print("Please set the API_KEY in your .env file and try again.")
        return

    try:
        # Example 1: Generate model from JSON data
        await json_model_example()
        
        # Example 2: Generate model with specific requirements
        await text_model_example_with_requirements()
        
        # Example 3: Generate model from CSV data
        await csv_model_example()
        
        # Example 4: Generate complex nested model
        await complex_nested_model_example()
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Please ensure the API service is running and your API key is valid.")


if __name__ == "__main__":
    asyncio.run(main()) 