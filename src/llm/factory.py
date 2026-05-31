"""
LLM 工厂模式 - 根据配置创建对应的适配器实例
"""
from typing import Optional

from .base import BaseLLM
from .openai_adapter import OpenAIAdapter
from .mock_llm import MockLLM


class LLMFactory:
    """模型抽象工厂"""
    _registry = {
        "openai": OpenAIAdapter,
        "deepseek": OpenAIAdapter,
        "mock": MockLLM
    }

    @classmethod
    def create(cls, provider: str, model_name: str, api_key: str, base_url: Optional[str] = None, **kwargs) -> BaseLLM:
        """根据 provider 创建对应的 LLM 适配器实例"""
        provider = provider.lower()
        if provider not in cls._registry:
            raise ValueError(f"当前框架暂不支持的 LLM 厂商：{provider}")
        return cls._registry[provider](
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )
