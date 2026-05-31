"""
Mock LLM - 全闭环本地仿真适配器
模拟真实大模型的决策树，支持零 API-Key 本地完美调试驱动
"""
import json
import asyncio
from typing import List, Optional

from ..models import BaseMessage, Role, ToolCall
from .base import BaseLLM


class MockLLM(BaseLLM):
    """全闭环本地仿真适配器"""

    async def generate(self, messages: List[BaseMessage], response_format: Optional[str] = None, **kwargs) -> BaseMessage:
        await asyncio.sleep(0.3)  # 仿真网络网络切片耗时
        last_msg = messages[-1].content or ""

        # 1. 仿真 ReAct 状态分支切换
        if "北京天气" in last_msg:
            return BaseMessage(
                role=Role.ASSISTANT,
                content="我想先查查北京的天气。",
                tool_calls=[ToolCall(id="call_01", name="get_weather", arguments={"city": "北京"})]
            )
        elif "晴天，气温 25°C" in last_msg:
            return BaseMessage(
                role=Role.ASSISTANT,
                content="根据气象局最新回传的数据，北京今天天气晴朗，气温 25°C。非常温暖舒适，出门不需要带伞，建议做好基础防晒。"
            )

        # 2. 仿真 Plan-and-Solve 状态分支切换 - 汇总阶段（优先级高，先匹配）
        elif "汇总所有执行结果" in last_msg:
            return BaseMessage(role=Role.ASSISTANT, content="尊敬的用户，您的全套差旅方案已订妥：航班 MU5101（09:00 起飞），入驻酒店为陆家嘴香格里拉，落地后由专属专车接送。祝您旅途愉快！")

        # Plan-and-Solve 初始规划阶段
        elif "预订一次从北京到上海的商务旅行" in last_msg and "分解" not in last_msg:
            plan_payload = {
                "plan": [
                    "步骤 1: 确定北京到上海的机票 (MU5101)",
                    "步骤 2: 根据降落时间预订上海陆家嘴的酒店",
                    "步骤 3: 预订浦东机场到酒店的接机租车服务"
                ],
                "analysis": "已完成初始任务拆解，准备依次执行。"
            }
            return BaseMessage(role=Role.ASSISTANT, content=json.dumps(plan_payload, ensure_ascii=False))

        # Plan-and-Solve 工具调用仿真 - 步骤 1 机票
        elif "步骤 1: 确定北京到上海的机票" in last_msg:
            return BaseMessage(
                role=Role.ASSISTANT,
                content="正在为您预订机票...",
                tool_calls=[ToolCall(id="call_flight_01", name="book_flight", arguments={"origin": "北京", "destination": "上海", "date": "2026-06-15"})]
            )

        # Plan-and-Solve 工具调用仿真 - 步骤 2 酒店
        elif "步骤 2: 根据降落时间预订上海陆家嘴的酒店" in last_msg:
            return BaseMessage(
                role=Role.ASSISTANT,
                content="正在为您预订酒店...",
                tool_calls=[ToolCall(id="call_hotel_01", name="book_hotel", arguments={"city": "上海", "area": "陆家嘴", "date": "2026-06-15", "room_type": "高级大床房"})]
            )

        # Plan-and-Solve 工具调用仿真 - 步骤 3 租车
        elif "步骤 3: 预订浦东机场到酒店的接机租车服务" in last_msg:
            return BaseMessage(
                role=Role.ASSISTANT,
                content="正在为您安排租车...",
                tool_calls=[ToolCall(id="call_car_01", name="book_car_rental", arguments={"city": "上海", "pickup_location": "上海虹桥机场 T2 航站楼", "date": "2026-06-15"})]
            )

        # 3. 仿真 Reflection 状态分支切换
        elif "撰写一篇关于'强化学习在量化交易中的应用'的摘要" in last_msg:
            return BaseMessage(role=Role.ASSISTANT, content="摘要草稿：强化学习可以用来做量化交易。我们用 DDPG 算法训练了一个 Agent，在回测中取得了不错的收益。")
        elif "请对以下摘要进行严厉反思" in last_msg:
            return BaseMessage(role=Role.ASSISTANT, content="自我反思意见：1. 表达过于口语化，严重缺乏学术厚重感。2. 缺乏具体的量化指标。3. 未进行基线模型（Baseline）横向对比。")
        elif "结合反思意见，输出终版摘要" in last_msg:
            return BaseMessage(
                role=Role.ASSISTANT,
                content="学术版最终摘要：本文提出一种基于深度确定性策略梯度（DDPG）的端到端强化学习量化投资框架。实验表明，该模型在沪深 300 指数回测中，夏普比率达到 2.1，相比传统均值方差模型提升了 15%，具备显著的稳健性。"
            )

        return BaseMessage(role=Role.ASSISTANT, content="未能解析模拟输入，激活兜底回复。")
