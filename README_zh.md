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

### 基本结构化请求

```python
import requests
import json

api_url = "http://localhost:8000/api/structure"
api_key = "your_api_key_here"

content = "小明今年18岁，身高175cm，是一名学生。"

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "姓名"},
        "age": {"type": "integer", "description": "年龄"},
        "height": {"type": "number", "description": "身高（厘米）"},
        "occupation": {"type": "string", "description": "职业"}
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

**响应:**
```json
{
    "success": true,
    "data": {
        "name": "小明",
        "age": 18,
        "height": 175,
        "occupation": "学生"
    },
    "error": null,
    "model_used": "openai:gpt-4o"
}
```

更多示例请查看[examples](examples/)目录。

## 🔍 API文档

访问 http://localhost:8000/docs 获取完整的API文档。

## 🛠️ 高级配置

查看[配置文档](docs/configuration.md)了解更多关于自定义和配置的信息。

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