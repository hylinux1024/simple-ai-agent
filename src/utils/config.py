"""
配置加载工具 - 从环境变量加载 LLM 配置
"""
import os
from typing import Optional

from dotenv import load_dotenv


class Config:
    """LLM 配置管理器"""

    def __init__(self):
        # 加载 .env 文件
        load_dotenv()

        # LLM 基础配置
        self.provider: str = os.getenv("LLM_PROVIDER", "mock")
        self.model_name: str = os.getenv("LLM_MODEL_NAME", "mock-model")
        self.api_key: str = os.getenv("LLM_API_KEY", "")
        self.base_url: Optional[str] = os.getenv("LLM_BASE_URL")

        # 可选参数
        self.temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))

    def to_dict(self) -> dict:
        """返回配置字典"""
        return {
            "provider": self.provider,
            "model_name": self.model_name,
            "api_key": self.api_key,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

    def create_llm_kwargs(self) -> dict:
        """创建 LLM 实例所需的 kwargs"""
        kwargs = {}
        if self.temperature:
            kwargs["temperature"] = self.temperature
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens
        return kwargs


# 全局配置实例
config = Config()
