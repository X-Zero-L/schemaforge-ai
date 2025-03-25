# SchemaForge AI 🚀

![GitHub stars](https://img.shields.io/github/stars/X-Zero-L/schemaforge-ai?style=social)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **简化AI结构化数据处理，告别重复prompt编写**

SchemaForge AI 是一个基于FastAPI和Pydantic的服务，旨在解决开发者反复编写代码和prompt让AI将文本转换为结构化数据的问题。通过提供统一的API接口，开发者只需定义所需的数据结构，无需每次都编写专门的提示词和处理逻辑。支持多种AI提供商，包括OpenAI、Anthropic、Google等。

*[English Documentation](README.md)*

## ✨ 核心亮点

- **多模型支持** - 无缝支持OpenAI、Anthropic、Google、Mistral、Cohere和Groq的最新模型
- **动态模式定义** - 使用Pydantic模型创建自定义数据结构
- **统一接口** - 告别为每个结构化任务编写专门的prompt和处理代码
- **RESTful API** - 简单易用的API接口，支持模型选择和参数配置
- **内置安全机制** - API密钥认证和完善的错误处理
- **模型对比** - 比较不同AI模型在相同结构化任务上的表现
- **Docker支持** - 轻松部署到任何环境

## 🌟 为什么选择SchemaForge AI?

在实际开发中，我们经常需要使用AI将文本转换为结构化数据，这通常需要为每个用例手动编写prompt和处理代码。这种重复性工作既耗时又乏味。SchemaForge AI提供了一个统一的解决方案，只需定义目标数据结构，系统会自动处理prompt生成和数据验证，让开发者专注于业务逻辑而非重复编码。

**实用场景:**
- 📄 **文档解析** - 从合同、简历或表格中提取关键数据
- 🌐 **API响应转换** - 将第三方API响应统一转换为应用所需格式
- 📊 **数据规范化** - 统一不同来源的数据格式
- 💬 **AI回复结构化** - 确保AI回复符合预定义的数据模型
- 📝 **内容分析** - 从文章或社交媒体提取结构化数据

## 🚀 快速开始

### 安装

1. 克隆仓库
```bash
git clone https://github.com/X-Zero-L/schemaforge-ai.git
cd schemaforge-ai
```

2. 使用UV安装依赖
```bash
# 如果尚未安装UV，请先安装
curl -fsSL https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，添加您的API密钥
```

### 运行服务

```bash
uvicorn app.main:app --reload
```

服务将在 http://localhost:8000 运行

### 使用Docker

我们在Docker设置中使用UV进行依赖管理，以实现更快速、更可靠的构建。

```bash
docker-compose up -d
```

## 💻 使用示例

`examples` 目录包含全面的示例，展示了如何使用SchemaForge AI：

### 1. 预定义模型使用

```python
from pydantic import BaseModel, Field
import json
import httpx

# 定义你的数据模型
class Person(BaseModel):
    name: str = Field(..., description="姓名")
    age: int = Field(..., description="年龄")
    height: float = Field(..., description="身高（厘米）")
    occupation: str = Field(None, description="职业")

# 发送文本进行结构化
async def structure_data(content, model, api_key):
    schema_json = model.model_json_schema()
    
    response = await httpx.AsyncClient().post(
        "http://localhost:8000/api/v1/structure",
        json={
            "content": content,
            "schema_description": json.dumps(schema_json),
            "model_name": "openai:gpt-4o"
        },
        headers={"Authorization": "Bearer your_api_key"}
    )
    
    return response.json()

# 示例结果:
# {
#   "success": true,
#   "data": {
#     "name": "张三",
#     "age": 32,
#     "height": 175.5,
#     "occupation": "软件工程师"
#   },
#   "model_used": "openai:gpt-4o"
# }
```

### 2. 模型生成

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
        headers={"Authorization": "Bearer your_api_key"}
    )
    
    return response.json()

# 响应包含：
# - model_code: 生成的Pydantic模型代码（适用于Python）
# - json_schema: JSON Schema表示（适用于任何编程语言）
# - fields: 结构化的字段定义
```

API同时返回Python Pydantic代码和JSON Schema表示，使您能够：
- 在Python应用中直接使用Pydantic模型
- 使用JSON Schema在任何其他语言中生成模型
- 在JavaScript、Java、C#、Go或任何支持JSON Schema的语言中构建验证

查看[examples](examples/)目录获取更详细的示例，包括：

- 结构化不同类型的内容（个人信息、图书、新闻文章）
- 在相同任务上比较不同AI模型的表现
- 从JSON、文本和CSV数据生成模型
- 处理嵌套数据结构
- 添加验证规则

## 🔍 API文档

访问 http://localhost:8000/docs 获取完整的API文档。

### 主要端点

| 端点 | 描述 |
|----------|-------------|
| `/api/v1/structure` | 使用提供的架构结构化文本数据 |
| `/api/v1/generate-model` | 从样本数据生成Pydantic模型 |

## 🧠 支持的AI模型

SchemaForge AI设计理念注重灵活性。您可以通过`提供商:模型名称`格式使用任何受支持提供商的模型：

- **OpenAI**: 支持所有OpenAI模型，包括gpt-3.5-turbo、gpt-4、gpt-4o以及未来发布的新模型
- **Anthropic**: 支持所有Claude模型，包括Claude 3系列（Opus、Sonnet、Haiku）及后续版本
- **Google**: 支持Gemini系列模型，包括gemini-1.5-pro、gemini-1.5-flash及更新版本
- **Mistral**: 支持所有Mistral AI模型，包括mistral-large、mistral-small及其最新版本
- **Cohere**: 支持Command系列模型及Cohere发布的任何新模型
- **Groq**: 支持通过Groq高速推理平台提供的LLaMA及其他模型

该服务不会将您限制在特定的模型版本 - 当提供商发布新模型时，您可以立即在请求中指定使用它们，无需等待本服务更新。

使用格式指定任何模型：`提供商:模型名称`（例如，`openai:gpt-4o`或`anthropic:claude-3-sonnet-20240229`）

## 🛠️ 高级配置

查看[配置文档](docs/configuration.md)了解更多关于自定义选项的信息。

## 🔮 未来计划

我们正在不断努力改进SchemaForge AI。以下是我们计划实现的一些功能：

- **增加AI提供商** - 扩展支持更多的LLM提供商
- **增强输入处理** - 支持更复杂的输入格式，包括表格、PDF和图像
- **性能优化** - 提高处理速度和资源利用率
- **高级验证规则** - 为生成的模型提供更复杂的验证功能
- **Web界面** - 基于浏览器的管理控制台，使配置和测试更加便捷
- **输出格式扩展** - 支持生成Python/Pydantic以外的其他编程语言模型
- **批处理API** - 在单一操作中高效处理多个结构化请求

如果您对额外功能有建议，请在我们的[讨论区](https://github.com/X-Zero-L/schemaforge-ai/discussions)分享！

## 🌍 多语言支持

虽然我们的示例主要是Python语言，但SchemaForge AI的API可以与任何能够发送HTTP请求的编程语言集成。我们欢迎社区贡献其他语言的集成示例！

如果您已经在您喜欢的编程语言中实现了SchemaForge AI的调用，请考虑分享您的代码示例。我们希望能够包含以下语言的示例：

- JavaScript/TypeScript（Node.js、浏览器）
- Java
- Go
- C#/.NET
- PHP
- Ruby
- Rust
- 以及更多！

这有助于让不同背景和生态系统的开发者更容易使用SchemaForge AI。通过拉取请求或在讨论区分享您的示例。

## 🙏 致谢

SchemaForge AI 构建在多个优秀的开源项目基础上：

- [PydanticAI](https://ai.pydantic.dev) - 强大的Agent框架，使构建生产级生成式AI应用变得更加简单
- [Logfire](https://logfire.pydantic.dev/docs/) - 全面的日志和监控解决方案，有助于调试、性能监控和行为跟踪
- FastAPI - 用于构建API的高性能Web框架
- Pydantic - 使用Python类型注解进行数据验证和设置管理
- 以及所有使本服务成为可能的AI模型提供商API

我们感谢这些项目的维护者和贡献者的出色工作。

## 🤝 贡献

欢迎贡献！如果您发现任何问题或有改进建议，请提交issue或PR。

## 📣 社区

- [讨论区](https://github.com/X-Zero-L/schemaforge-ai/discussions)

## 📄 许可证

MIT

---

<p align="center">
  <b>如果这个项目对您有帮助，请给它一个⭐️星！</b><br>
  <a href="https://github.com/X-Zero-L/schemaforge-ai">
    <img src="https://img.shields.io/github/stars/X-Zero-L/schemaforge-ai?style=social" alt="Star on GitHub">
  </a> 
</p>

## SDK 便捷集成

为了更轻松地与您的应用程序集成，我们提供了官方Python SDK:

<div align="center">
  <h3>
    <a href="https://github.com/X-Zero-L/schemaforge-sdk">
      📦 SchemaForge SDK
    </a>
  </h3>
  <p>Python应用程序的无缝集成</p>
</div>

该SDK提供了一个简洁的、Python风格的SchemaForge AI接口:

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

# 初始化客户端
client = SchemaForge(api_key="your_secure_api_key_here")

# 定义Pydantic模型
class Person(BaseModel):
    name: str
    age: int
    occupation: str
    email: str

# 使用模型结构化文本
person = client.structure(
    content="张三是一位30岁的软件工程师，邮箱是zhangsan@example.com",
    model_class=Person
)
print(person.model_dump())
# {'name': '张三', 'age': 30, 'occupation': '软件工程师', 'email': 'zhangsan@example.com'}
```

[访问SDK仓库](https://github.com/X-Zero-L/schemaforge-sdk)获取安装说明、文档和示例。

## 🛠️ 高级配置 