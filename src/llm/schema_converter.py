"""
Schema 转换器 - 抹平不同 LLM 厂商在 Tool Calling 协议上的标准差异
"""
import json
from typing import Any, Dict, Type

from pydantic import BaseModel

from ..models import UnifiedTool


class ToolSchemaConverter:
    """多态 JSON Schema 转换引擎"""

    @staticmethod
    def _base_pydantic_to_schema(pydantic_model: Type[BaseModel]) -> Dict[str, Any]:
        """提取标准的 JSON Schema"""
        return pydantic_model.model_json_schema()

    @classmethod
    def to_openai(cls, tool: UnifiedTool, strict: bool = False) -> Dict[str, Any]:
        """转换为 OpenAI/DeepSeek 兼容的高级工具规约格式"""
        schema = cls._base_pydantic_to_schema(tool.parameters)
        if strict:
            schema["additionalProperties"] = False
            if "properties" in schema:
                schema["required"] = list(schema["properties"].keys())
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": schema
            }
        }

    @classmethod
    def to_anthropic(cls, tool: UnifiedTool) -> Dict[str, Any]:
        """转换为 Anthropic Claude 厂商标准的专属架构格式"""
        schema = cls._base_pydantic_to_schema(tool.parameters)
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": schema
        }
