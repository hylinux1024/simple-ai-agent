"""
ReAct Agent - 经典 ReAct 模式实现（Reasoning + Acting 协同动态闭环）
"""
import asyncio
import logging
from typing import List

from ..models import BaseMessage, Role, UnifiedTool
from ..llm import BaseLLM
from .base import BaseAgent


class ReActAgent(BaseAgent):
    """经典 ReAct 模式实现"""

    def __init__(self, name: str, system_prompt: str, llm: BaseLLM, tools: List[UnifiedTool] = None, max_steps: int = 5):
        super().__init__(name, system_prompt, llm, tools)
        self.max_steps = max_steps

    async def run(self, user_input: str) -> str:
        logging.info(f"=== [{self.name}] 触发 ReAct 运作闭环 ===")
        messages = [
            BaseMessage(role=Role.SYSTEM, content=self.system_prompt),
            BaseMessage(role=Role.USER, content=user_input)
        ]

        for step in range(self.max_steps):
            logging.info(f"[{self.name}] 循环第 {step + 1} 步 -> 发起思考推理...")
            response = await self.llm.generate(messages)
            messages.append(response)

            if response.content:
                logging.info(f"💭 Thought: {response.content}")

            if response.tool_calls:
                for tc in response.tool_calls:
                    logging.info(f"🛠️ Action (发起工具检索): 准备执行 [{tc.name}], 核心参数：{tc.arguments}")
                    tool = next((t for t in self.tools if t.name == tc.name), None)

                    if tool and tool.executable:
                        try:
                            # 深度兼容异步执行与同步阻塞函数
                            if asyncio.iscoroutinefunction(tool.executable):
                                observation = await tool.executable(**tc.arguments)
                            else:
                                observation = tool.executable(**tc.arguments)
                        except Exception as e:
                            observation = f"Execution Error: {str(e)}"
                    else:
                        observation = f"Error: 找不到注册工具 {tc.name}."

                    logging.info(f"👁️ Observation (观察结果): {observation}")

                    messages.append(BaseMessage(
                        role=Role.TOOL, content=observation, name=tc.name, tool_call_id=tc.id
                    ))
            else:
                logging.info(f"🏆 ReAct 决策链收敛完成。")
                return response.content or ""

        return "达到最大步数上限，ReAct 执行强行断开。"
