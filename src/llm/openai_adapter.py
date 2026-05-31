"""
OpenAI 及兼容生态适配器
支持：OpenAI, DeepSeek, 通义千问，Moonshot 等
"""
import json
import asyncio
from typing import List, Optional, Any

from ..models import BaseMessage, Role, ToolCall, UnifiedTool
from .base import BaseLLM
from .schema_converter import ToolSchemaConverter


class OpenAIAdapter(BaseLLM):
    """支持高并发异步请求的 OpenAI 及完全兼容生态"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("生产环境下请安装官方 SDK: pip install openai")
        # 实例化异步 Client
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def generate(self, messages: List[BaseMessage], response_format: Optional[str] = None, **kwargs) -> BaseMessage:
        # 1. 协议转换：将内部标准流转格式翻译成 OpenAI 字典规范
        oai_messages = []
        for m in messages:
            msg_dict: dict[str, Any] = {"role": m.role.value}
            if m.content:
                msg_dict["content"] = m.content
            if m.name:
                msg_dict["name"] = m.name
            if m.tool_call_id:
                msg_dict["tool_call_id"] = m.tool_call_id
            if m.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.name, "arguments": json.dumps(tc.arguments, ensure_ascii=False)}
                    } for tc in m.tool_calls
                ]
            oai_messages.append(msg_dict)

        # 2. 调用多态转换引擎翻译绑定的工具
        oai_tools = [ToolSchemaConverter.to_openai(t) for t in self.bound_tools] if self.bound_tools else []

        # 3. 设置响应格式（用于强制 JSON 输出）
        extra_kwargs = {**self.kwargs, **kwargs}
        if response_format == "json_object":
            extra_kwargs["response_format"] = {"type": "json_object"}

        # 4. 异步非阻塞通信
        request_kwargs = {
            "model": self.model_name,
            "messages": oai_messages,
            **extra_kwargs,
        }
        if oai_tools:
            request_kwargs["tools"] = oai_tools

        response = await self.client.chat.completions.create(**request_kwargs)

        choice = response.choices[0].message

        # 5. 反向翻译：将外部实体转换回内部标准 BaseMessage
        parsed_tool_calls = None
        if choice.tool_calls:
            parsed_tool_calls = [
                ToolCall(id=tc.id, name=tc.function.name, arguments=json.loads(tc.function.arguments))
                for tc in choice.tool_calls
            ]

        return BaseMessage(role=Role.ASSISTANT, content=choice.content, tool_calls=parsed_tool_calls)
