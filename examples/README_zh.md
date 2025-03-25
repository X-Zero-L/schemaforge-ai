# 结构化API使用示例

本目录包含了如何使用预定义的Pydantic模型来调用结构化API的示例代码，支持多种AI模型。

*[English Documentation](README.md)*

## 示例说明

`predefined_models.py` 文件展示了多个用例：

1. 人物信息结构化
   - 使用 `Person` 模型
   - 包含姓名、年龄、身高和职业信息
   - 展示了如何使用自定义系统提示词

2. 图书信息结构化
   - 使用 `BookInfo` 模型
   - 包含书名、作者、出版年份、价格和分类信息
   - 展示了如何处理列表类型的字段

3. 新闻文章结构化
   - 使用 `NewsArticle` 模型
   - 包含标题、内容、日期、来源和标签信息
   - 展示了如何处理多行文本内容

4. 模型对比
   - 演示如何使用不同AI模型结构化相同内容
   - 比较OpenAI和Anthropic模型的结果
   - 展示如何处理模型特定的API错误

## 认证

API需要使用API密钥进行认证。要使用示例：

1. 确保在项目根目录中有一个包含API密钥的`.env`文件：
```
API_KEY=你的安全API密钥
```

2. 示例代码会自动加载此密钥并将其包含在所有请求中。

3. 如果未设置API密钥，示例将显示警告并退出。

## 如何运行示例

1. 确保API服务已经启动：
```bash
uvicorn app.main:app --reload
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 确保在`.env`文件中设置了API密钥

4. 运行示例：
```bash
python examples/predefined_models.py
```

## 使用自定义模型

你可以参考示例中的模型定义方式，创建自己的Pydantic模型：

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class YourModel(BaseModel):
    field1: str = Field(..., description="字段1的描述")
    field2: int = Field(..., description="字段2的描述")
    field3: Optional[List[str]] = Field(default_factory=list, description="字段3的描述")
```

然后使用 `structure_data()` 函数来调用API，指定你偏好的模型：

```python
result = await structure_data(
    content="你的文本内容",
    model=YourModel,
    system_prompt="可选的系统提示词",
    model_name="openai:gpt-4o"  # 指定要使用的AI模型
)
```

## 可用模型

API支持来自不同提供商的各种模型，包括：

- OpenAI模型（gpt-3.5-turbo, gpt-4, gpt-4o）
- Anthropic模型（claude-3-opus-latest, claude-3-sonnet-latest）
- Google模型（gemini-1.5-pro, gemini-1.5-flash）
- Mistral模型（mistral-large-latest, mistral-small-latest）

## 动态模型创建

API服务会自动从传递的模型JSON Schema中提取字段信息，创建动态Pydantic模型。这使得你可以：

1. 使用Pydantic定义结构化数据模型
2. 传递模型的JSON Schema到API
3. API会使用`create_model`动态创建相同结构的模型
4. 系统提示词可用来指导LLM如何解析内容

## 注意事项

1. 模型定义时要善用Field的description参数，它会帮助API更好地理解字段的含义
2. 对于可选字段，使用Optional类型标注
3. 对于列表类型，建议使用default_factory=list作为默认值
4. 系统提示词可以提高结构化准确性，但不是必需的
5. 不同的AI模型可能对相同内容的结构化结果略有不同
6. 确保在.env文件中为你想使用的模型提供了适当的API密钥
7. 除非服务器禁用了认证，否则API密钥是必需的 