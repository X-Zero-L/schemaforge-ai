# SchemaForge AI 配置指南

本文档概述了SchemaForge AI的配置选项。

## 环境变量

SchemaForge AI主要通过`.env`文件中的环境变量进行配置。

```
# API认证密钥
API_KEY=your_secure_api_key_here

# 启用/禁用认证
REQUIRE_AUTH=true

# 默认使用的模型
DEFAULT_MODEL=openai:gpt-4o

# OpenAI配置
OPENAI_API_KEY=your_openai_key_here
OPENAI_BASE_URL=https://api.openai.com/v1  # 可选

# Anthropic配置
ANTHROPIC_API_KEY=your_anthropic_key_here

# Google配置
GOOGLE_API_KEY=your_google_key_here

# Mistral配置
MISTRAL_API_KEY=your_mistral_key_here

# Cohere配置
COHERE_API_KEY=your_cohere_key_here

# Groq配置
GROQ_API_KEY=your_groq_key_here

# 日志配置
LOGFIRE_ENABLED=true
LOGFIRE_TOKEN=your_logfire_token_here
```

## API端点

### 结构化数据

```
POST /api/v1/structure
```

请求示例:

```json
{
  "content": "John是一名32岁的软件工程师，身高182.5厘米。",
  "schema_description": "{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"Person's name\"},\"age\":{\"type\":\"integer\",\"description\":\"Age in years\"},\"height\":{\"type\":\"number\",\"description\":\"Height in cm\"},\"occupation\":{\"type\":\"string\",\"description\":\"Job title\"}},\"required\":[\"name\",\"age\",\"height\"]}",
  "system_prompt": "你是一位个人信息提取专家。",
  "model_name": "openai:gpt-4o",
  "is_need_schema_description": false
}
```

响应示例:

```json
{
  "success": true,
  "data": {
    "name": "John",
    "age": 32,
    "height": 182.5,
    "occupation": "软件工程师"
  },
  "error": null,
  "model_used": "openai:gpt-4o"
}
```

### 生成模型

```
POST /api/v1/generate-model
```

请求示例:

```json
{
  "sample_data": "...(样本数据)...",
  "model_name": "Product",
  "description": "表示产品信息的模型",
  "requirements": "可选的特定要求",
  "expected_fields": [
    {
      "name": "field1",
      "field_type": "string",
      "description": "field1的描述",
      "required": true
    }
  ],
  "llm_model_name": "openai:gpt-4o"
}
```

响应示例:

```json
{
  "success": true,
  "model_name": "Product",
  "model_code": "...(生成的模型代码)...",
  "fields": [...],
  "model_used": "openai:gpt-4o"
}
```

## 模型指定

API设计为对模型支持具有灵活性。您可以通过`提供商:模型名称`格式指定模型名称来使用受支持提供商的任何模型。

示例:
- `openai:gpt-4o`
- `anthropic:claude-3-opus-latest`
- `google-gla:gemini-1.5-pro`
- `mistral:mistral-large-latest`
- `cohere:command-r`
- `groq:llama-3.1-8b-instant`

## Docker部署

使用Docker时，通过`docker-compose.yml`中的环境变量配置服务：

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

## 错误处理

API响应包含`success`字段。如果`success`为`false`，`error`字段提供错误详情。

错误示例:

```json
{
  "success": false,
  "error": "模型'openai:gpt-4'返回错误：超出速率限制",
  "data": null,
  "model_used": "openai:gpt-4"
}
``` 