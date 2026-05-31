"""
智能体基类
"""
from abc import ABC, abstractmethod
from typing import List

from ..models import BaseMessage, Role
from ..llm import BaseLLM
from ..tools.base import Tool


class BaseAgent(ABC):
    """统一标准的智能体核心高度抽象基类"""

    def __init__(self, name: str, system_prompt: str, llm: BaseLLM, tools: List[Tool] = None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        self.tools = tools or []
        if self.tools:
            self.llm.bind_tools(self.tools)

    @abstractmethod
    async def run(self, user_input: str) -> str:
        """核心交互控制流单次执行入口契约"""
        pass
