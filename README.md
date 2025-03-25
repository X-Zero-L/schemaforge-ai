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

### Basic Structuring Request

```python
import requests
import json

api_url = "http://localhost:8000/api/structure"
api_key = "your_api_key_here"

content = "John is a 32-year-old software engineer, with a height of 182.5 centimeters."

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Person's name"},
        "age": {"type": "integer", "description": "Age in years"},
        "height": {"type": "number", "description": "Height in cm"},
        "occupation": {"type": "string", "description": "Job title"}
    },
    "required": ["name", "age", "height"]
}

response = requests.post(
    api_url,
    json={
        "content": content,
        "schema_description": json.dumps(schema),
        "model_name": "openai:gpt-4o"
    },
    headers={"X-API-Key": api_key}
)

print(response.json())
```

**Response:**

```json
{
  "success": true,
  "data": {
    "name": "John",
    "age": 32,
    "height": 182.5,
    "occupation": "software engineer"
  },
  "error": null,
  "model_used": "openai:gpt-4o"
}
```

Check the [examples](examples/) directory for more detailed examples.

## 🔍 API Documentation

Visit http://localhost:8000/docs to view the complete API documentation.

## 🛠️ Advanced Configuration

See the [configuration documentation](docs/configuration.md) for more information about customization and configuration.

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
