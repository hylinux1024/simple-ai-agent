"""
Schema 转换器 - 抹平不同 LLM 厂商在 Tool Calling 协议上的标准差异
"""
import json
from typing import Any, Dict

from ..tools.base import Tool, ToolParameter


class ToolSchemaConverter:
    """多态 JSON Schema 转换引擎"""

    @staticmethod
    def _tool_parameters_to_schema(parameters: list[ToolParameter]) -> Dict[str, Any]:
        """从 ToolParameter 列表生成 JSON Schema"""
        properties = {}
        required = []

        for p in parameters:
            properties[p.name] = {
                "type": p.type,
                "description": p.description
            }
            if p.default is not None:
                properties[p.name]["default"] = p.default
            if p.required:
                required.append(p.name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    @classmethod
    def to_openai(cls, tool: Tool, strict: bool = False) -> Dict[str, Any]:
        """转换为 OpenAI/DeepSeek 兼容的高级工具规约格式"""
        schema = cls._tool_parameters_to_schema(tool.get_parameters())
        if strict:
            schema["additionalProperties"] = False
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
    def to_anthropic(cls, tool: Tool) -> Dict[str, Any]:
        """转换为 Anthropic Claude 厂商标准的专属架构格式"""
        schema = cls._tool_parameters_to_schema(tool.get_parameters())
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": schema
        }
