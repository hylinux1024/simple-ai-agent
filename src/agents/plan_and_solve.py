"""
Plan-and-Solve Agent - 谋定而后动，极大提升复杂宏观任务的准度
"""
import asyncio
import json
import logging
import re
from typing import List

from ..models import BaseMessage, Role, ToolCall
from ..llm import BaseLLM
from .base import BaseAgent
from ..tools.base import Tool


def extract_json_from_response(content: str) -> dict:
    """从 LLM 响应中提取 JSON，处理 Markdown 格式等情况"""
    content = content.strip()

    # 尝试直接解析
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 尝试提取 Markdown 代码块中的 JSON
    match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 尝试提取第一个 { 到最后一个 } 之间的内容
    start = content.find('{')
    end = content.rfind('}') + 1
    if start != -1 and end > start:
        try:
            return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass

    return {}


class PlanAndSolveAgent(BaseAgent):
    """Plan-and-Solve 模式实现"""

    async def run(self, user_input: str) -> str:
        logging.info(f"=== [{self.name}] 触发 Plan-and-Solve 运作闭环 ===")

        # 1. Macro Planning Stage (宏观全局规划阶段)
        logging.info(f"[{self.name}] 阶段 1 [Planning]: 正在分解全局任务目标...")
        planner_prompt = f"{self.system_prompt}\n请深度解析用户诉求，并将其打散为结构化计划。你必须输出标准的 JSON 格式：{{\"plan\": [\"步骤 1...\", \"步骤 2...\"], \"analysis\": \"...\"}}"
        messages = [
            BaseMessage(role=Role.SYSTEM, content=planner_prompt),
            BaseMessage(role=Role.USER, content=user_input)
        ]

        # 使用 response_format="json_object" 强制 API 返回 JSON
        plan_response = await self.llm.generate(messages, response_format="json_object")
        plan_data = extract_json_from_response(plan_response.content or "{}")
        steps = plan_data.get("plan", [])
        analysis = plan_data.get("analysis", "")

        if not steps:
            logging.warning("规划器未返回有效步骤，退化为直接交付模式。")
            steps = [user_input]

        # 打印规划阶段的任务列表
        print("\n" + "-" * 50)
        print("📋 规划阶段 - 任务列表")
        print("-" * 50)
        for i, step in enumerate(steps, 1):
            print(f"  [{i}] {step}")
        if analysis:
            print(f"\n💡 分析：{analysis}")
        print("-" * 50 + "\n")

        logging.info(f"📋 Global Plan 拆解明细：{steps}")

        # 2. Sequential Solving Stage (原子子任务串行执行阶段)
        execution_results = []
        for i, step in enumerate(steps):
            logging.info(f"[{self.name}] 阶段 2 [Solving]: 推进子计划 ({i + 1}/{len(steps)}) -> {step}")
            step_messages = [
                BaseMessage(role=Role.SYSTEM, content=f"根据全局路线图，你当前的专项任务是：{step}。请直接交付执行结果。"),
                BaseMessage(role=Role.USER, content=f"执行步骤：{step}")
            ]
            step_response = await self.llm.generate(step_messages)

            # 处理工具调用（如果有）
            if step_response.tool_calls:
                for tc in step_response.tool_calls:
                    logging.info(f"🛠️ Action: 准备执行 [{tc.name}], 参数：{tc.arguments}")
                    tool = next((t for t in self.tools if t.name == tc.name), None)

                    if tool:
                        try:
                            observation = tool.run(tc.arguments)
                        except Exception as e:
                            observation = f"Execution Error: {str(e)}"
                    else:
                        observation = f"Error: 找不到注册工具 {tc.name}."

                    logging.info(f"👁️ Observation: {observation}")
                    execution_results.append(f"计划步骤：{step} | 工具调用：{tc.name} | 执行结果：{observation}")
            else:
                execution_results.append(f"计划步骤：{step} | 产出成果：{step_response.content}")

            logging.info(f"✅ 子计划 {i + 1} 阶段性执行完毕。")

        # 3. Cognitive Merging Stage (多源信息汇聚提炼阶段)
        logging.info(f"[{self.name}] 阶段 3 [Merging]: 聚合全链路控制台日志，产出最终方案...")
        final_messages = [
            BaseMessage(role=Role.SYSTEM, content="你是一个高级成果汇总分析器，请根据各维度的阶段性产出，凝练成最完美的答案回馈给客户。"),
            BaseMessage(role=Role.USER, content=f"原始核心诉求：{user_input}\n\n执行流产出完整日志如下:\n" + "\n".join(execution_results) + "\n\n请汇总所有执行结果。")
        ]
        final_response = await self.llm.generate(final_messages)
        return final_response.content or ""
