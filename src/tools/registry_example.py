"""
工具注册表示例 - 演示如何使用 registry 快速注册工具
"""
from .base import registry, Tool, ToolParameter


# =====================================================================
# 示例：使用全局 registry 注册工具
# =====================================================================

def demo_tool_function(param_str: str) -> str:
    """示例工具函数"""
    import json
    params = json.loads(param_str)
    name = params.get("name", "访客")
    return f"你好，{name}！这是一个示例工具的响应。"


def register_demo_tools():
    """注册演示工具"""
    # 方式 1: 直接注册函数
    registry.register_function(
        name="demo_function",
        description="示例函数工具 - 展示直接注册函数的方式",
        func=demo_tool_function
    )

    # 方式 2: 注册 Tool 类实例
    class DemoTool(Tool):
        """演示工具类"""

        def __init__(self):
            super().__init__(
                name="demo_class",
                description="示例类工具 - 展示继承 Tool 类的方式"
            )

        def run(self, parameters):
            message = parameters.get("message", "无消息")
            return f"收到消息：{message}"

        def get_parameters(self):
            return [
                ToolParameter(
                    name="message",
                    type="string",
                    description="发送给工具的消息内容",
                    required=False,
                    default="无消息"
                )
            ]

    registry.register_tool(DemoTool())

    print(f"✅ 当前已注册工具：{registry.list_tools()}")
    return registry


def get_demo_tools():
    """获取所有演示工具"""
    register_demo_tools()
    return registry.get_all_tools()
