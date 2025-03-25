# SchemaForge AI 🚀

![GitHub stars](https://img.shields.io/github/stars/X-Zero-L/schemaforge-ai?style=social)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **Simplify AI structured data processing, eliminate repetitive prompt engineering**

SchemaForge AI is a service based on FastAPI and Pydantic designed to solve the problem of developers repeatedly writing code and prompts to have AI convert text into structured data. By providing a unified API interface, developers only need to define the desired data structure without writing specialized prompts and processing logic each time. Supports multiple AI providers including OpenAI, Anthropic, Google, and more.

_[中文文档](README_zh.md)_

## ✨ Core Features

- **Multi-model Support** - Seamlessly integrate with the latest models from OpenAI, Anthropic, Google, Mistral, Cohere, and Groq
- **Dynamic Schema Definition** - Create custom data structures using Pydantic models
- **Unified Interface** - Eliminate the need to write specialized prompts and processing code for each structuring task
- **RESTful API** - Easy-to-use API interface with model selection and parameter configuration
- **Built-in Security** - API key authentication and comprehensive error handling
- **Model Comparison** - Compare different AI models' performance on the same structuring tasks
- **Docker Support** - Easy deployment to any environment

## 🌟 Why Choose SchemaForge AI?

In real-world development, we often need to use AI to convert text into structured data, which typically requires manually writing prompts and processing code for each use case. This repetitive work is both time-consuming and tedious. SchemaForge AI provides a unified solution where you only need to define the target data structure, and the system automatically handles prompt generation and data validation, allowing developers to focus on business logic rather than repetitive coding.

**Practical Use Cases:**

- 📄 **Document Parsing** - Extract key data from contracts, resumes, or forms
- 🌐 **API Response Conversion** - Standardize third-party API responses to your application's required format
- 📊 **Data Normalization** - Unify data formats from different sources
- 💬 **AI Response Structuring** - Ensure AI responses conform to predefined data models
- 📝 **Content Analysis** - Extract structured data from articles or social media

## 🚀 Quick Start

### Installation

1. Clone the repository

```bash
git clone https://github.com/X-Zero-L/schemaforge-ai.git
cd schemaforge-ai
```

2. Install dependencies with UV

```bash
# Install UV if you haven't already
curl -fsSL https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

3. Configure environment variables

```bash
cp .env.example .env
# Edit the .env file to add your API keys
```

### Running the Service

```bash
uvicorn app.main:app --reload
```

The service will run at http://localhost:8000

### Using Docker

We use UV for dependency management in our Docker setup for faster and more reliable builds.

```bash
docker-compose up -d
```

## 💻 Usage Examples

The `examples` directory contains comprehensive examples showing how to use SchemaForge AI:

### 1. Predefined Model Usage

```python
from pydantic import BaseModel, Field
import json
import httpx

# Define your data model
class Person(BaseModel):
    name: str = Field(..., description="Person's full name")
    age: int = Field(..., description="Age in years")
    height: float = Field(..., description="Height in centimeters")
    occupation: str = Field(None, description="Current occupation")

# Send text for structuring
async def structure_data(content, model, api_key):
    schema_json = model.model_json_schema()
    
    response = await httpx.AsyncClient().post(
        "http://localhost:8000/api/v1/structure",
        json={
            "content": content,
            "schema_description": json.dumps(schema_json),
            "model_name": "openai:gpt-4o"
        },
        headers={"X-API-Key": api_key}
    )
    
    return response.json()

# Example result:
# {
#   "success": true,
#   "data": {
#     "name": "John Smith",
#     "age": 32,
#     "height": 182.5,
#     "occupation": "software engineer"
#   },
#   "model_used": "openai:gpt-4o"
# }
```

### 2. Model Generation

```python
async def generate_model(sample_data, model_name, description, api_key):
    response = await httpx.AsyncClient().post(
        "http://localhost:8000/api/v1/generate-model",
        json={
            "sample_data": sample_data,
            "model_name": model_name,
            "description": description,
            "llm_model_name": "openai:gpt-4o"
        },
        headers={"X-API-Key": api_key}
    )
    
    return response.json()

# Response includes:
# - model_code: Generated Pydantic model code (for Python)
# - json_schema: JSON Schema representation (for any programming language)
# - fields: Structured field definitions
```

The API returns both Python Pydantic code and a JSON Schema representation, allowing you to:
- Use the Pydantic model directly in Python applications
- Use the JSON Schema to generate models in any other language
- Build validations in JavaScript, Java, C#, Go, or any other language that supports JSON Schema

Check out the [examples](examples/) directory for more detailed examples including:

- Structuring different types of content (person info, books, news articles)
- Comparing different AI models on the same task
- Generating models from JSON, text, and CSV data
- Working with nested data structures
- Adding validation rules

## 🔍 API Documentation

Visit http://localhost:8000/docs to view the complete API documentation.

### Main Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/structure` | Structure text data using a provided schema |
| `/api/v1/generate-model` | Generate a Pydantic model from sample data |

## 🧠 Supported AI Models

SchemaForge AI is designed with flexibility in mind. You can use models from any supported provider by specifying them in the format `provider:model_name`:

- **OpenAI**: Any model from their lineup including gpt-3.5-turbo, gpt-4, gpt-4o, and future models as they become available
- **Anthropic**: Any Claude model including the Claude 3 family (Opus, Sonnet, Haiku) and future releases
- **Google**: Gemini models including gemini-1.5-pro, gemini-1.5-flash, and newer versions
- **Mistral**: Any Mistral AI models including mistral-large, mistral-small, and their latest versions
- **Cohere**: Command models and any new Cohere releases
- **Groq**: LLaMA and other models available through Groq's fast inference platform

The service doesn't restrict you to specific model versions - as providers release new models, you can immediately use them by specifying them in your requests without waiting for updates to this service.

Specify any model using the format: `provider:model_name` (e.g., `openai:gpt-4o` or `anthropic:claude-3-sonnet-20240229`)

## 🛠️ Advanced Configuration

See the [configuration documentation](docs/configuration.md) for more information about customization options:

- Custom system prompts
- Retry behavior
- Timeout settings
- Model-specific parameters
- Caching options

## 🔮 Future Plans

We're continuously working to improve SchemaForge AI. Here are some of the features we plan to implement:

- **Additional AI Providers** - Expand support to include more LLM providers as they become available
- **Enhanced Input Processing** - Support for more complex input formats including tables, PDFs, and images
- **Performance Optimization** - Improvements to processing speed and resource utilization
- **Advanced Validation Rules** - More sophisticated validation capabilities for generated models
- **Web Interface** - A browser-based management console for easier configuration and testing
- **Output Format Extensions** - Support for generating models in additional programming languages beyond Python/Pydantic
- **Batch Processing API** - Efficiently process multiple structuring requests in a single operation

If you have suggestions for additional features, please share them in our [Discussion Forum](https://github.com/X-Zero-L/schemaforge-ai/discussions)!

## 🌍 Multi-language Support

While our examples are primarily in Python, the SchemaForge AI API can be integrated with any programming language capable of making HTTP requests. We welcome community contributions of integration examples in other languages!

If you've implemented SchemaForge AI in your favorite language, please consider sharing your code samples. We'd love to include examples for:

- JavaScript/TypeScript (Node.js, browser)
- Java
- Go
- C#/.NET
- PHP
- Ruby
- Rust
- And more!

This helps make SchemaForge AI more accessible to developers from different backgrounds and ecosystems. Submit your examples through a pull request or share them in the discussions.

## 🤝 Contributing

Contributions welcome! If you find any issues or have suggestions for improvements, please submit an issue or PR.

## 📣 Community

- [Discussion Forum](https://github.com/X-Zero-L/schemaforge-ai/discussions)

## 📄 License

MIT

---

<p align="center">
  <b>If this project has been helpful to you, please give it a ⭐️ star!</b><br>
  <a href="https://github.com/X-Zero-L/schemaforge-ai">
    <img src="https://img.shields.io/github/stars/X-Zero-L/schemaforge-ai?style=social" alt="Star on GitHub">
  </a>
</p>
