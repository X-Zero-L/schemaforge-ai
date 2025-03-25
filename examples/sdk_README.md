# SchemaForge AI SDK Example

This example demonstrates how to simplify SchemaForge AI usage by creating a thin SDK wrapper. 
The SDK hides the complexity of API calls and provides an intuitive interface for both data structuring and model generation.

*[中文文档](sdk_README_zh.md)*

## Features

- **Simple Interface** - Clean, intuitive methods for data structuring and model generation
- **Type Safety** - Strong typing with Pydantic models and generics
- **Async Support** - Both asynchronous and synchronous interfaces
- **Error Handling** - Proper exception handling and user-friendly error messages
- **Environment Awareness** - Automatic loading of API keys and configuration from environment variables
- **Utility Functions** - Helpers for common tasks like converting generated code to usable models

## Usage

### Installation

The SDK example requires the following dependencies:

```bash
pip install httpx pydantic python-dotenv
```

### Configuration

The SDK uses the following environment variables (or you can provide them directly):

```
API_KEY=your_schemaforge_api_key
API_BASE_URL=http://localhost:8000  # Or your custom deployment URL
```

### Basic Examples

#### Structure Data with an Existing Model

```python
from schemaforge_sdk import SchemaForgeClient
from pydantic import BaseModel, Field
from typing import Optional

# 1. Define your model
class Person(BaseModel):
    name: str = Field(..., description="Person's full name")
    age: int = Field(..., description="Age in years")
    height: float = Field(..., description="Height in centimeters")
    occupation: Optional[str] = Field(None, description="Current occupation")

# 2. Create client
client = SchemaForgeClient()

# 3. Structure data (synchronous)
person = client.structure_data_sync(
    content="John Smith is a 32-year-old software engineer who is 182.5 cm tall.",
    model_class=Person
)

print(person.model_dump())
# Output: {'name': 'John Smith', 'age': 32, 'height': 182.5, 'occupation': 'software engineer'}
```

#### Generate a Model from Sample Data

```python
# Generate a model from JSON data
product_sample = """
{
    "product_id": "P12345",
    "name": "Smartphone X",
    "price": 799.99,
    "in_stock": true,
    "colors": ["Black", "Silver", "Gold"]
}
"""

result = client.generate_model_sync(
    sample_data=product_sample,
    model_name="Product",
    description="A model representing product information for an e-commerce system"
)

# Get the generated model class
ProductModel = client.load_model_from_code(result["model_code"])

# Use the generated model
product = ProductModel(
    product_id="P67890",
    name="Laptop Pro",
    price=1299.99,
    in_stock=True,
    colors=["Silver", "Space Gray"]
)

print(product.model_dump())
```

### Async Usage

The SDK provides async versions of all methods for use with `asyncio`:

```python
import asyncio

async def process_data():
    client = SchemaForgeClient()
    person = await client.structure_data(
        content="Emily Johnson is a 28-year-old teacher who is 165 cm tall.",
        model_class=Person
    )
    return person

# Run the async function
person = asyncio.run(process_data())
```

## Advanced Usage

### Custom System Prompts

```python
person = client.structure_data_sync(
    content="John Smith works at XYZ Corp as a software engineer. He's in his early 30s.",
    model_class=Person,
    system_prompt="You are an expert at extracting personal information. If age is approximate, use 30 for 'early 30s'."
)
```

### Specifying AI Models

```python
# Use a specific model
person = client.structure_data_sync(
    content="...",
    model_class=Person,
    model_name="anthropic:claude-3-sonnet-latest"
)

# Set a default model for the client
client = SchemaForgeClient(default_model="google-gla:gemini-1.5-pro")
```

### Model Generation with Requirements

```python
result = client.generate_model_sync(
    sample_data=product_sample,
    model_name="Product",
    description="A model representing product information",
    requirements="Price must be a positive number. Product ID must follow the format P-XXXXX."
)
```

## Benefits of Using the SDK

1. **Simplicity** - No need to understand the details of HTTP requests and JSON construction
2. **Consistency** - Standardized way to make API calls and handle responses
3. **Type Safety** - The SDK ensures that your models and data are properly typed
4. **Documentation** - Detailed docstrings and type hints provide guidance as you code
5. **Error Handling** - Clear error messages rather than raw HTTP errors

## Notes

- This is an example SDK to demonstrate how SchemaForge AI can be consumed more easily
- For production use, you might want to add more features like caching, rate limiting, etc.
- The `load_model_from_code` method uses `exec()` which should only be used with trusted inputs

## Complete Example

See the full implementation in `schemaforge_sdk.py` and its usage examples at the bottom of the file. 