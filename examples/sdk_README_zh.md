# SchemaForge AI SDK 示例

本示例演示如何通过创建简单的SDK封装来简化SchemaForge AI的使用。
SDK隐藏了API调用的复杂性，并为数据结构化和模型生成提供了直观的接口。

*[English Documentation](sdk_README.md)*

## 特点

- **简单接口** - 简洁直观的数据结构化和模型生成方法
- **类型安全** - 使用Pydantic模型和泛型进行强类型定义
- **异步支持** - 同时提供异步和同步接口
- **错误处理** - 适当的异常处理和用户友好的错误消息
- **环境感知** - 自动从环境变量加载API密钥和配置
- **实用函数** - 为常见任务提供帮助，如将生成的代码转换为可用模型

## 使用方法

### 安装

SDK示例需要以下依赖：

```bash
pip install httpx pydantic python-dotenv
```

### 配置

SDK使用以下环境变量（或者您可以直接提供）：

```
API_KEY=您的schemaforge_api_密钥
API_BASE_URL=http://localhost:8000  # 或您的自定义部署URL
```

### 基本示例

#### 使用现有模型结构化数据

```python
from schemaforge_sdk_zh import SchemaForgeClient
from pydantic import BaseModel, Field
from typing import Optional

# 1. 定义您的模型
class Person(BaseModel):
    name: str = Field(..., description="姓名")
    age: int = Field(..., description="年龄")
    height: float = Field(..., description="身高（厘米）")
    occupation: Optional[str] = Field(None, description="职业")

# 2. 创建客户端
client = SchemaForgeClient()

# 3. 结构化数据（同步）
person = client.structure_data_sync(
    content="张三是一名32岁的软件工程师，身高180厘米。",
    model_class=Person
)

print(person.model_dump())
# 输出: {'name': '张三', 'age': 32, 'height': 180, 'occupation': '软件工程师'}
```

#### 从样本数据生成模型

```python
# 从JSON数据生成模型
product_sample = """
{
    "product_id": "P12345",
    "name": "智能手机X",
    "price": 5999.99,
    "in_stock": true,
    "colors": ["黑色", "银色", "金色"]
}
"""

result = client.generate_model_sync(
    sample_data=product_sample,
    model_name="Product",
    description="表示电子商务系统中产品信息的模型"
)

# 获取生成的模型类
ProductModel = client.load_model_from_code(result["model_code"])

# 使用生成的模型
product = ProductModel(
    product_id="P67890",
    name="笔记本电脑Pro",
    price=8999.99,
    in_stock=True,
    colors=["银色", "深空灰"]
)

print(product.model_dump())
```

### 异步使用

SDK为所有方法提供了异步版本，可与`asyncio`一起使用：

```python
import asyncio

async def process_data():
    client = SchemaForgeClient()
    person = await client.structure_data(
        content="李四是一名28岁的教师，身高175厘米。",
        model_class=Person
    )
    return person

# 运行异步函数
person = asyncio.run(process_data())
```

## 高级用法

### 自定义系统提示

```python
person = client.structure_data_sync(
    content="张三在XYZ公司工作，是一名软件工程师。他30岁出头。",
    model_class=Person,
    system_prompt="你是提取个人信息的专家。如果年龄是近似值，对'30岁出头'使用32。"
)
```

### 指定AI模型

```python
# 使用特定模型
person = client.structure_data_sync(
    content="...",
    model_class=Person,
    model_name="anthropic:claude-3-sonnet-latest"
)

# 为客户端设置默认模型
client = SchemaForgeClient(default_model="google-gla:gemini-1.5-pro")
```

### 带需求的模型生成

```python
result = client.generate_model_sync(
    sample_data=product_sample,
    model_name="Product",
    description="表示产品信息的模型",
    requirements="价格必须是正数。产品ID必须遵循P-XXXXX格式。"
)
```

## 使用SDK的好处

1. **简单性** - 无需了解HTTP请求和JSON构造的细节
2. **一致性** - 标准化的API调用和响应处理方式
3. **类型安全** - SDK确保您的模型和数据正确类型化
4. **文档** - 详细的文档字符串和类型提示在编码时提供指导
5. **错误处理** - 清晰的错误消息而不是原始HTTP错误

## 注意事项

- 这是一个示例SDK，用于演示如何更轻松地使用SchemaForge AI
- 对于生产使用，您可能需要添加更多功能，如缓存、速率限制等
- `load_model_from_code`方法使用`exec()`，应仅用于可信输入

## 完整示例

请参阅`schemaforge_sdk_zh.py`中的完整实现及其底部的使用示例。 