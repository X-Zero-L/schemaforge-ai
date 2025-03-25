# Structured API Usage Examples

This directory contains example code showing how to use predefined Pydantic models to call the structuring API, with support for multiple AI models.

*[中文文档](README_zh.md)*

## Example Description

The `predefined_models.py` file demonstrates several use cases:

1. Person Information Structuring
   - Uses the `Person` model
   - Includes name, age, height, and occupation information
   - Demonstrates how to use custom system prompts

2. Book Information Structuring
   - Uses the `BookInfo` model
   - Includes title, author, publication year, price, and category information
   - Shows how to handle list-type fields

3. News Article Structuring
   - Uses the `NewsArticle` model
   - Includes headline, content, date, source, and tag information
   - Shows how to handle multi-line text content

4. Model Comparison
   - Demonstrates how to structure the same content using different AI models
   - Compares results between OpenAI and Anthropic models
   - Shows how to handle model-specific API errors

## Authentication

The API requires authentication using an API key. To use the examples:

1. Make sure you have an `.env` file in the project root with your API key:
```
API_KEY=your_secure_api_key
```

2. The example code automatically loads this key and includes it in all requests.

3. If the API key is not set, the example will display a warning and exit.

## How to Run Examples

1. Make sure the API service is running:
```bash
uvicorn app.main:app --reload
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure your API key is set in the `.env` file

4. Run the example:
```bash
python examples/predefined_models.py
```

## Using Custom Models

You can refer to the model definition method in the examples to create your own Pydantic models:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class YourModel(BaseModel):
    field1: str = Field(..., description="Description of field1")
    field2: int = Field(..., description="Description of field2")
    field3: Optional[List[str]] = Field(default_factory=list, description="Description of field3")
```

Then use the `structure_data()` function to call the API with your preferred model:

```python
result = await structure_data(
    content="Your text content",
    model=YourModel,
    system_prompt="Optional system prompt",
    model_name="openai:gpt-4o"  # Specify the AI model to use
)
```

## Available Models

The API supports various models from different providers, including:

- OpenAI models (gpt-3.5-turbo, gpt-4, gpt-4o)
- Anthropic models (claude-3-opus-latest, claude-3-sonnet-latest)
- Google models (gemini-1.5-pro, gemini-1.5-flash)
- Mistral models (mistral-large-latest, mistral-small-latest)

## Dynamic Model Creation

The API service automatically extracts field information from the model's JSON Schema to create a dynamic Pydantic model. This allows you to:

1. Define structured data models using Pydantic
2. Pass the model's JSON Schema to the API
3. The API uses `create_model` to dynamically create a model with the same structure
4. System prompts can guide the LLM in how to parse content

## Notes

1. Make good use of the Field description parameter when defining models, as it helps the API better understand the meaning of fields
2. Use Optional type annotations for optional fields
3. For list types, it's recommended to use default_factory=list as the default value
4. System prompts can improve structuring accuracy, but are not required
5. Different AI models may structure the same content slightly differently
6. Make sure you have the appropriate API keys in your .env file for the models you want to use
7. The API key is required for authentication unless the server has disabled authentication 