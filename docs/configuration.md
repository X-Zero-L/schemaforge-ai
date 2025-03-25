# SchemaForge AI Configuration Guide

This document outlines the configuration options available in SchemaForge AI.

## Environment Variables

SchemaForge AI is primarily configured through environment variables in the `.env` file.

```
# API key for authentication
API_KEY=your_secure_api_key_here

# Enable/disable authentication
REQUIRE_AUTH=true

# Default model to use when none specified
DEFAULT_MODEL=openai:gpt-4o

# OpenAI configuration
OPENAI_API_KEY=your_openai_key_here
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional

# Anthropic configuration
ANTHROPIC_API_KEY=your_anthropic_key_here

# Google configuration
GOOGLE_API_KEY=your_google_key_here

# Mistral configuration
MISTRAL_API_KEY=your_mistral_key_here

# Cohere configuration
COHERE_API_KEY=your_cohere_key_here

# Groq configuration
GROQ_API_KEY=your_groq_key_here

# Logging configuration
LOGFIRE_ENABLED=true
LOGFIRE_TOKEN=your_logfire_token_here
```

## API Endpoints

### Structure Data

```
POST /api/v1/structure
```

Request example:

```json
{
  "content": "John is a 32-year-old software engineer, with a height of 182.5 centimeters.",
  "schema_description": "{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"Person's name\"},\"age\":{\"type\":\"integer\",\"description\":\"Age in years\"},\"height\":{\"type\":\"number\",\"description\":\"Height in cm\"},\"occupation\":{\"type\":\"string\",\"description\":\"Job title\"}},\"required\":[\"name\",\"age\",\"height\"]}",
  "system_prompt": "You are a personal information extraction expert.",
  "model_name": "openai:gpt-4o",
  "is_need_schema_description": false
}
```

Response example:

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

### Generate Model

```
POST /api/v1/generate-model
```

Request example:

```json
{
  "sample_data": "...(Sample data)...",
  "model_name": "Product",
  "description": "A model representing product information",
  "requirements": "Optional specific requirements",
  "expected_fields": [
    {
      "name": "field1",
      "field_type": "string",
      "description": "Description of field1",
      "required": true
    }
  ],
  "llm_model_name": "openai:gpt-4o"
}
```

Response example:

```json
{
  "success": true,
  "model_name": "Product",
  "model_code": "...(Generated model code)...",
  "fields": [...],
  "model_used": "openai:gpt-4o"
}
```

## Model Specification

The API is designed to be flexible with model support. You can use any model from supported providers by specifying the model name in the format `provider:model_name`.

Examples:
- `openai:gpt-4o`
- `anthropic:claude-3-opus-latest`
- `google-gla:gemini-1.5-pro`
- `mistral:mistral-large-latest`
- `cohere:command-r`
- `groq:llama-3.1-8b-instant`

## Docker Deployment

When using Docker, configure the service with environment variables in `docker-compose.yml`:

```yaml
services:
  schemaforge-ai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=your_secure_api_key
      - REQUIRE_AUTH=true
      - OPENAI_API_KEY=your_openai_api_key
      - ANTHROPIC_API_KEY=your_anthropic_api_key
      - DEFAULT_MODEL=openai:gpt-4o
      - LOGFIRE_ENABLED=true
```

## Error Handling

API responses include a `success` field. If `success` is `false`, the `error` field provides details about what went wrong.

Error example:

```json
{
  "success": false,
  "error": "Model 'openai:gpt-4' returned an error: Rate limit exceeded",
  "data": null,
  "model_used": "openai:gpt-4"
}
``` 