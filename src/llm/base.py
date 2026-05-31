"""
LLM 硬件抽象层（HAL）核心基类
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

from ..models import BaseMessage
from ..tools.base import Tool


class BaseLLM(ABC):
    """LLM 硬件抽象层（HAL）核心基类"""

    def __init__(self, model_name: str, api_key: str, base_url: Optional[str] = None, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.kwargs = kwargs
        self.bound_tools: List[Tool] = []

    def bind_tools(self, tools: List[Tool]) -> 'BaseLLM':
        """将一组原子工具动态注入/绑定至当前大模型底座"""
        self.bound_tools = tools
        return self

    @abstractmethod
    async def generate(self, messages: List[BaseMessage], response_format: Optional[str] = None, **kwargs) -> BaseMessage:
        """异步生成核心契约接口"""
        pass
