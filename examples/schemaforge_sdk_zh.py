"""
SchemaForge AI SDK (中文版)

这是一个简化的SDK，封装了SchemaForge AI的API调用，使用户能够更简单地使用服务，
而无需处理底层的复杂性。
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel, Field, ConfigDict

import httpx
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 常量和配置
DEFAULT_API_BASE = "http://localhost:8000"
DEFAULT_MODEL = "openai:gpt-4o"
DEFAULT_TIMEOUT = 60  # 秒

# 泛型类型变量
T = TypeVar('T', bound=BaseModel)

class SchemaForgeClient:
    """
    SchemaForge AI客户端，简化与SchemaForge API的交互。
    
    该客户端处理认证、请求格式化和响应解析，
    让您可以专注于数据模型而不是API细节。
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        default_model: str = DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        初始化SchemaForge客户端。
        
        参数:
            api_key: 用于认证的API密钥（默认使用API_KEY环境变量）
            api_base: API的基础URL（默认使用环境变量或localhost）
            default_model: 默认使用的AI模型（例如："openai:gpt-4o"）
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key or os.getenv("API_KEY", "")
        if not self.api_key:
            raise ValueError("需要API密钥。通过构造函数或API_KEY环境变量设置。")
            
        self.api_base = api_base or os.getenv("API_BASE_URL", DEFAULT_API_BASE)
        self.default_model = default_model
        self.timeout = timeout
        
    def _get_headers(self) -> Dict[str, str]:
        """获取API请求的头信息。"""
        return {"X-API-Key": self.api_key}
    
    async def structure_data(
        self,
        content: str,
        model_class: Type[T],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> T:
        """
        使用指定的Pydantic模型结构化文本数据。
        
        参数:
            content: 要结构化的文本内容
            model_class: 用于结构化的Pydantic模型类
            model_name: 用于处理的AI模型（例如："openai:gpt-4o"）
            system_prompt: 可选的系统提示，用于指导AI
            
        返回:
            填充了结构化数据的指定模型类实例
        """
        # 从Pydantic模型获取JSON架构
        model_schema = model_class.model_json_schema()
        
        # 准备请求数据
        request_data = {
            "content": content,
            "schema_description": json.dumps(model_schema),
            "model_name": model_name or self.default_model,
        }
        
        if system_prompt:
            request_data["system_prompt"] = system_prompt
        
        # 发送请求到API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/api/v1/structure",
                json=request_data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            # 解析响应
            result = response.json()
            
            if not result.get("success", False):
                error_msg = result.get("error", "未知错误")
                raise ValueError(f"结构化数据失败: {error_msg}")
            
            # 将结构化数据转换为模型实例
            return model_class.model_validate(result["data"])
    
    async def generate_model(
        self,
        sample_data: str,
        model_name: str,
        description: str,
        requirements: Optional[str] = None,
        expected_fields: Optional[List[Dict[str, Any]]] = None,
        ai_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从样本数据生成Pydantic模型。
        
        参数:
            sample_data: 要分析的样本数据（文本、JSON、CSV等）
            model_name: 生成模型的名称
            description: 模型表示内容的描述
            requirements: 可选的特定要求或验证规则
            expected_fields: 可选的预期字段及其属性列表
            ai_model: 用于生成的AI模型
            
        返回:
            包含生成的模型代码、JSON架构和字段的字典
        """
        # 准备请求数据
        request_data = {
            "sample_data": sample_data,
            "model_name": model_name,
            "description": description,
            "llm_model_name": ai_model or self.default_model
        }
        
        if requirements:
            request_data["requirements"] = requirements
            
        if expected_fields:
            request_data["expected_fields"] = expected_fields
        
        # 发送请求到API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/api/v1/generate-model",
                json=request_data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            # 解析响应
            result = response.json()
            
            if not result.get("success", False):
                error_msg = result.get("error", "未知错误")
                raise ValueError(f"生成模型失败: {error_msg}")
            
            return {
                "model_name": result["model_name"],
                "model_code": result["model_code"],
                "json_schema": result["json_schema"],
                "fields": result["fields"],
                "model_used": result["model_used"]
            }
    
    # 异步方法的同步版本
    def structure_data_sync(
        self,
        content: str,
        model_class: Type[T],
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> T:
        """structure_data的同步版本。"""
        return asyncio.run(self.structure_data(
            content=content,
            model_class=model_class,
            model_name=model_name,
            system_prompt=system_prompt
        ))
    
    def generate_model_sync(
        self,
        sample_data: str,
        model_name: str,
        description: str,
        requirements: Optional[str] = None,
        expected_fields: Optional[List[Dict[str, Any]]] = None,
        ai_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """generate_model的同步版本。"""
        return asyncio.run(self.generate_model(
            sample_data=sample_data,
            model_name=model_name,
            description=description,
            requirements=requirements,
            expected_fields=expected_fields,
            ai_model=ai_model
        ))
    
    # 使SDK更易用的实用方法
    @staticmethod
    def load_model_from_code(model_code: str) -> Type[BaseModel]:
        """
        从生成的代码字符串加载Pydantic模型。
        
        参数:
            model_code: 包含Pydantic模型定义的Python代码字符串
            
        返回:
            Pydantic模型类
        
        警告: 
            这使用了exec()，应仅用于可信输入。
        """
        # 为模型创建命名空间
        namespace = {}
        
        # 在此命名空间中执行代码
        exec(model_code, namespace)
        
        # 在命名空间中查找模型类
        # 通常它是最后定义的类
        model_names = [name for name, obj in namespace.items() 
                      if isinstance(obj, type) and issubclass(obj, BaseModel) and obj != BaseModel]
        
        if not model_names:
            raise ValueError("在生成的代码中未找到Pydantic模型")
        
        # 返回模型类
        return namespace[model_names[0]]


# 使用示例
if __name__ == "__main__":
    # 定义一个简单的Pydantic模型
    class Person(BaseModel):
        name: str = Field(..., description="姓名")
        age: int = Field(..., description="年龄")
        height: float = Field(..., description="身高（厘米）")
        occupation: Optional[str] = Field(None, description="职业")
    
    # 创建客户端实例
    client = SchemaForgeClient()
    
    # 示例1：使用现有模型结构化数据
    try:
        # 同步版本
        person = client.structure_data_sync(
            content="张三是一名32岁的软件工程师，身高180厘米。",
            model_class=Person
        )
        print(f"结构化数据（同步）: {person.model_dump_json(indent=2)}")
        
        # 这也可以在异步代码中异步完成
        async def async_example():
            person = await client.structure_data(
                content="李四是一名28岁的教师，身高175厘米。",
                model_class=Person
            )
            print(f"结构化数据（异步）: {person.model_dump_json(indent=2)}")
        
        asyncio.run(async_example())
        
    except Exception as e:
        print(f"结构化数据错误: {e}")
    
    # 示例2：从样本数据生成新模型
    try:
        # 为产品生成模型
        product_sample = """
        {
            "product_id": "P12345",
            "name": "智能手机X",
            "price": 5999.99,
            "in_stock": true,
            "specifications": {
                "screen_size": "6.5英寸",
                "processor": "骁龙8",
                "storage": "128GB",
                "camera": "4800万像素"
            },
            "colors": ["黑色", "银色", "金色"],
            "release_date": "2024-01-15"
        }
        """
        
        result = client.generate_model_sync(
            sample_data=product_sample,
            model_name="Product",
            description="表示电子商务系统中产品信息的模型"
        )
        
        print(f"\n已生成模型 '{result['model_name']}' 使用 {result['model_used']}:")
        print(f"JSON Schema: {json.dumps(result['json_schema'], indent=2)}")
        
        # 加载并使用生成的模型
        ProductModel = client.load_model_from_code(result["model_code"])
        
        # 创建示例产品
        product_data = {
            "product_id": "P67890",
            "name": "笔记本电脑Pro",
            "price": 8999.99,
            "in_stock": True,
            "specifications": {
                "screen_size": "15.6英寸",
                "processor": "英特尔i9",
                "storage": "1TB",
                "camera": "1080p"
            },
            "colors": ["银色", "深空灰"],
            "release_date": "2024-03-01"
        }
        
        # 使用生成的模型进行验证
        product = ProductModel.model_validate(product_data)
        print(f"\n使用生成的模型验证产品: {product.model_dump_json(indent=2)}")
        
    except Exception as e:
        print(f"生成模型错误: {e}") 