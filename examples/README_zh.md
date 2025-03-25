# SchemaForge AI 示例

本目录包含全面的示例，展示如何使用SchemaForge AI进行数据结构化和生成Pydantic模型。

*[English Documentation](README.md)*

## 快速概览

本目录中的示例展示了使用SchemaForge AI的主要方式：

1. **使用预定义模型** - 手动定义Pydantic模型并用于结构化数据
2. **自动生成模型** - 从样本数据自动生成Pydantic模型

## 文件说明

### `predefined_models.py`

演示如何使用预定义的Pydantic模型从文本输入中结构化数据的多个实用示例：

| 示例                      | 描述                                   | 使用的模型      |
|--------------------------|----------------------------------------|----------------|
| 人物信息                  | 从文本中提取个人详细信息                 | `Person`       |
| 图书信息                  | 将描述性文本结构化为图书元数据           | `BookInfo`     |
| 新闻文章                  | 将新闻文章解析为结构化数据               | `NewsArticle`  |
| 模型比较                  | 比较不同AI模型在相同任务上的表现         | 多个模型        |
| 自定义食谱模型            | 展示如何创建和使用自定义模型             | `Recipe`       |

### `model_generation_example.py`

展示如何从不同类型的数据样本自动生成Pydantic模型：

| 示例                        | 描述                                     | 数据格式 |
|----------------------------|------------------------------------------|---------|
| 产品模型                    | 从JSON产品数据生成模型                    | JSON    |
| 带有特定要求的客户模型      | 创建具有特定验证要求的模型                | 文本     |
| 图书模型                    | 从类CSV数据生成模型                       | CSV     |
| 复杂嵌套订单模型            | 从复杂JSON创建具有嵌套结构的模型          | JSON    |


## 设置

在运行这些示例之前，确保：

1. 您已设置SchemaForge AI服务：
   ```bash
   git clone https://github.com/X-Zero-L/schemaforge-ai.git
   cd schemaforge-ai
   uv sync
   ```

2. 您在`.env`文件中有API密钥：
   ```
   API_KEY=您的API密钥
   ```

3. API服务正在运行：
   ```bash
   uvicorn app.main:app --reload
   ```

## 运行示例

要运行任何示例：

```bash
python examples/predefined_models.py
```

或

```bash
python examples/model_generation_example.py
```

或

```bash
python examples/schemaforge_sdk_zh.py
```

## 创建自己的模型

您可以按照此模式创建自定义Pydantic模型：

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class YourModel(BaseModel):
    field1: str = Field(..., description="字段1的描述")
    field2: int = Field(..., description="字段2的描述")
    field3: Optional[List[str]] = Field(default_factory=list, description="字段3的描述")
```

每个Field中的`description`很重要 - 它帮助AI理解需要提取什么信息。

## 生成模型

如果您不想手动定义模型，可以使用模型生成API：

```python
result = await generate_model(
    sample_data="您的样本数据（JSON、文本、CSV等）",
    model_name="您的模型名称",
    description="模型表示内容的描述",
    requirements="可选的特定要求",
    llm_model_name="openai:gpt-4o"  # 指定要使用的AI模型
)

# 生成的模型代码可在这里获取：
generated_code = result["model_code"]
```

## 最佳实践

1. **字段描述**：始终为每个字段提供清晰的描述
2. **系统提示词**：对于复杂任务，使用系统提示词提高结构化准确性
3. **模型选择**：不同模型有不同优势 - 实验找出最适合您用例的模型
4. **验证规则**：生成模型时，指定验证要求以提高数据质量
5. **错误处理**：始终检查响应中的`success`字段并适当处理错误
6. **使用SDK**：对于生产集成，考虑使用SDK方法简化代码

## 支持的AI模型

示例支持多种AI模型，包括：

- **OpenAI**：gpt-3.5-turbo、gpt-4、gpt-4o
- **Anthropic**：claude-3-opus-latest、claude-3-7-sonnet-latest
- **Google**：gemini-1.5-pro、gemini-1.5-flash
- **Mistral**：mistral-large-latest、mistral-small-latest

使用格式指定模型：`provider:model_name`（例如，`openai:gpt-4o`） 