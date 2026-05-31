"""
Reflection Agent - 基于对抗性自我纠偏的自愈博弈
"""
import logging

from ..models import BaseMessage, Role
from ..llm import BaseLLM
from .base import BaseAgent


class ReflectionAgent(BaseAgent):
    """Reflection 模式实现（基于对抗性自我纠偏的自愈博弈）"""

    def __init__(self, name: str, system_prompt: str, llm: BaseLLM, max_cycles: int = 1):
        super().__init__(name, system_prompt, llm)
        self.max_cycles = max_cycles

    async def run(self, user_input: str) -> str:
        logging.info(f"=== [{self.name}] 触发 Reflection 运作闭环 ===")

        # 1. Draft Generation (初稿生成)
        logging.info(f"[{self.name}] 阶段 1: 驱动生成初始雏形草稿...")
        messages = [
            BaseMessage(role=Role.SYSTEM, content=self.system_prompt),
            BaseMessage(role=Role.USER, content=user_input)
        ]
        draft_response = await self.llm.generate(messages)
        current_draft = draft_response.content or ""
        logging.info(f"📄 Initial Draft (原始初稿):\n{current_draft}\n")

        for cycle in range(self.max_cycles):
            logging.info(f"[{self.name}] 循环轮次 {cycle + 1} -> 唤醒自我批判审计专家...")

            # 2. Adversarial Critique (批判性质疑反思)
            critic_messages = [
                BaseMessage(role=Role.SYSTEM, content="你是一位吹毛求疵的终审学术评委与行业专家。请对下述段落发起无情的深度剖析，无保留地指出其中的常识错误、逻辑软肋与润色改写空间。"),
                BaseMessage(role=Role.USER, content=f"请对以下摘要进行严厉反思:\n\n{current_draft}")
            ]
            critic_response = await self.llm.generate(critic_messages)
            critique = critic_response.content or ""
            logging.info(f"🔍 Critique Comments (深层审计意见):\n{critique}\n")

            # 3. Targeted Refinement (针对性重构自愈)
            logging.info(f"[{self.name}] 循环轮次 {cycle + 1} -> 正在吸收缺陷审查报告，进行架构进化...")
            refine_messages = [
                BaseMessage(role=Role.SYSTEM, content=self.system_prompt),
                BaseMessage(role=Role.USER, content=f"原始缺陷版本:\n{current_draft}\n\n审稿人优化意见如下:\n{critique}\n\n请结合反思意见，输出终版摘要。")
            ]
            refine_response = await self.llm.generate(refine_messages)
            current_draft = refine_response.content or ""
            logging.info(f"✨ Refined Output (第 {cycle + 1} 轮自愈重组完毕):\n{current_draft}\n")

        return current_draft
