# SchemaForge AI Examples

This directory contains comprehensive examples demonstrating how to use SchemaForge AI for structuring data and generating Pydantic models.

*[中文文档](README_zh.md)*

## Quick Overview

The examples in this directory show three main ways to use SchemaForge AI:

1. **Using Predefined Models** - Define Pydantic models manually and use them to structure data
2. **Auto-Generating Models** - Generate Pydantic models automatically from sample data
3. **Using the SDK Wrapper** - Use a simple SDK wrapper to simplify integrating with SchemaForge AI

## File Descriptions

### `predefined_models.py`

Demonstrates using predefined Pydantic models to structure data from text inputs with several practical examples:

| Example                       | Description                                            | Model Used       |
|-------------------------------|--------------------------------------------------------|------------------|
| Person Information            | Extracts personal details from text                    | `Person`         |
| Book Information              | Structures book metadata from descriptive text         | `BookInfo`       |
| News Article                  | Parses news articles into structured data              | `NewsArticle`    |
| Model Comparison              | Compares different AI models on the same task          | Multiple models  |
| Custom Recipe Model           | Shows how to create and use a custom model             | `Recipe`         |

### `model_generation_example.py`

Shows how to automatically generate Pydantic models from different types of data samples:

| Example                        | Description                                              | Data Format |
|--------------------------------|----------------------------------------------------------|-------------|
| Product Model                  | Generates a model from JSON product data                 | JSON        |
| Customer Model with Requirements | Creates a model with specific validation requirements    | Text        |
| Book Model                     | Generates a model from CSV-like data                     | CSV         |
| Complex Nested Order Model     | Creates models with nested structures from complex JSON  | JSON        |

### `schemaforge_sdk.py` and `schemaforge_sdk_zh.py`

Provides an SDK wrapper to simplify integration with SchemaForge AI:

- **Client Abstraction** - Handles API authentication, request formatting, and response parsing
- **Type Safety** - Includes proper type hints and generic support
- **Synchronous & Asynchronous** - Both interface styles for different application needs
- **Model Loading Utility** - Helper to convert generated code into usable model classes
- **Error Handling** - Clear error messages and proper exception handling

See the [SDK Example Documentation](sdk_README.md) for detailed usage instructions.

## Setting Up

Before running these examples, make sure:

1. You have set up the SchemaForge AI service:
   ```bash
   git clone https://github.com/X-Zero-L/schemaforge-ai.git
   cd schemaforge-ai
   uv sync
   ```

2. You have an API key in the `.env` file:
   ```
   API_KEY=your_api_key_here
   ```

3. The API service is running:
   ```bash
   uvicorn app.main:app --reload
   ```

## Running the Examples

To run any example:

```bash
python examples/predefined_models.py
```

or

```bash
python examples/model_generation_example.py
```

or

```bash
python examples/schemaforge_sdk.py
```

## Creating Your Own Models

You can create custom Pydantic models following this pattern:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class YourModel(BaseModel):
    field1: str = Field(..., description="Description of field1")
    field2: int = Field(..., description="Description of field2")
    field3: Optional[List[str]] = Field(default_factory=list, description="Description of field3")
```

The `description` in each Field is important - it helps the AI understand what information to extract.

## Generating Models

If you don't want to define models manually, you can use the model generation API:

```python
result = await generate_model(
    sample_data="Your sample data (JSON, text, CSV, etc.)",
    model_name="YourModelName",
    description="Description of what the model represents",
    requirements="Optional specific requirements",
    llm_model_name="openai:gpt-4o"  # Specify AI model to use
)

# The generated model code is available in:
generated_code = result["model_code"]
```

## Best Practices

1. **Field Descriptions**: Always provide clear descriptions for each field
2. **System Prompts**: Use system prompts to improve structuring accuracy for complex tasks
3. **Model Selection**: Different models have different strengths - experiment to find the best for your use case
4. **Validation Rules**: When generating models, specify validation requirements for better data quality
5. **Error Handling**: Always check the `success` field in responses and handle errors appropriately
6. **SDK Usage**: For production integration, consider using the SDK approach to simplify your code

## Supported AI Models

The examples support various AI models including:

- **OpenAI**: gpt-3.5-turbo, gpt-4, gpt-4o
- **Anthropic**: claude-3-opus-latest, claude-3-7-sonnet-latest
- **Google**: gemini-1.5-pro, gemini-1.5-flash
- **Mistral**: mistral-large-latest, mistral-small-latest

Specify the model using the format: `provider:model_name` (e.g., `openai:gpt-4o`) 