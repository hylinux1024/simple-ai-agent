"""
Simple AI Agent Framework - 主入口
"""
import asyncio
import logging

from src import (
    LLMFactory,
    ReActAgent,
    PlanAndSolveAgent,
    ReflectionAgent,
    config,
)
from src.tools import get_weather_tool, get_flight_tool, get_hotel_tool, get_car_rental_tool

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


async def main():
    """主函数 - 演示三种 Agent 模式"""
    # 从环境变量创建 LLM 驱动
    llm_driver = LLMFactory.create(
        provider=config.provider,
        model_name=config.model_name,
        api_key=config.api_key,
        base_url=config.base_url,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    logging.info(f"使用 LLM: {config.provider}/{config.model_name}")

    # 获取示例工具
    weather_tool = get_weather_tool()
    flight_tool = get_flight_tool()
    hotel_tool = get_hotel_tool()
    car_rental_tool = get_car_rental_tool()

    # 1. ReAct Agent 测试
    print("\n" + "=" * 70)
    print("【ReAct 范式测试】")
    print("=" * 70)
    react_agent = ReActAgent(
        name="ReAct-Core",
        system_prompt="你是一个全能生活规划师。",
        llm=llm_driver,
        tools=[weather_tool]
    )
    res_1 = await react_agent.run("帮我查询北京天气的详细情况，并告诉我出门需要注意什么。")
    print(f"\n📢 [ReAct 范式最终交付成果]:\n{res_1}")

    # 2. Plan-and-Solve Agent 测试
    print("\n" + "=" * 70)
    print("【Plan-and-Solve 范式测试】")
    print("=" * 70)
    pas_agent = PlanAndSolveAgent(
        name="Plan-Core",
        system_prompt="你是一个工业级的高级差旅大管家。",
        llm=llm_driver,
        tools=[flight_tool, hotel_tool, car_rental_tool]
    )
    res_2 = await pas_agent.run("预订一次从北京到上海的商务旅行（包括机票、酒店、租车）")
    print(f"\n📢 [Plan-and-Solve 范式最终交付成果]:\n{res_2}")

    # 3. Reflection Agent 测试
    print("\n" + "=" * 70)
    print("【Reflection 范式测试】")
    print("=" * 70)
    reflect_agent = ReflectionAgent(
        name="Reflection-Core",
        system_prompt="你是一位资深的量化金融与 AI 领域科学家。",
        llm=llm_driver,
        max_cycles=1
    )
    res_3 = await reflect_agent.run("撰写一篇关于'强化学习在量化交易中的应用'的摘要")
    print(f"\n📢 [Reflection 范式最终交付成果]:\n{res_3}")


if __name__ == "__main__":
    try:
        # 检测是否在交互式环境中运行
        loop = asyncio.get_running_loop()
        logging.info("环境审计：检测到当前脚本运行在交互式事件循环中（Notebook/Colab）。")

        try:
            import nest_asyncio
            nest_asyncio.apply()
            asyncio.run(main())
        except ImportError:
            logging.warning("环境依赖提示：未检测到 nest_asyncio，已平滑降级。")
            loop.create_task(main())
    except RuntimeError:
        # 标准控制台环境
        asyncio.run(main())
