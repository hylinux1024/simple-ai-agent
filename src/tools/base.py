"""
工具系统抽象层 - 基类、参数定义和注册表
"""
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


# =====================================================================
# 工具参数定义
# =====================================================================

class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


# =====================================================================
# 工具基类
# =====================================================================

class Tool(ABC):
    """工具基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> str:
        """
        执行工具

        Args:
            parameters: 工具参数键值对

        Returns:
            工具执行结果字符串
        """
        pass

    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """
        获取工具参数定义

        Returns:
            工具参数列表
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        将工具转换为字典格式（用于 LLM Schema）

        Returns:
            工具定义的字典表示
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    p.name: {
                        "type": p.type,
                        "description": p.description
                    }
                    for p in self.get_parameters()
                },
                "required": [p.name for p in self.get_parameters() if p.required]
            }
        }


# =====================================================================
# 函数式工具适配器
# =====================================================================

class FunctionTool(Tool):
    """
    函数式工具适配器 - 将普通函数包装为 Tool

    适用于快速注册简单工具函数
    """

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[[str], str],
        parameters: Optional[List[ToolParameter]] = None
    ):
        super().__init__(name, description)
        self.func = func
        self._parameters = parameters or []

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行封装的函数"""
        # 简单适配：将参数字典转为 JSON 字符串传入
        import json
        return self.func(json.dumps(parameters, ensure_ascii=False))

    def get_parameters(self) -> List[ToolParameter]:
        """获取参数定义"""
        return self._parameters


# =====================================================================
# 工具注册表
# =====================================================================

class ToolRegistry:
    """工具注册表 - 单例模式管理所有工具"""

    _instance: Optional["ToolRegistry"] = None
    _tools: Dict[str, Tool]
    _functions: Dict[str, Dict[str, Any]]

    def __new__(cls) -> "ToolRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
            cls._instance._functions = {}
        return cls._instance

    def __init__(self):
        pass  # 单例初始化，实际初始化在 __new__

    def register_tool(self, tool: Tool):
        """
        注册 Tool 对象

        Args:
            tool: Tool 实例
        """
        if tool.name in self._tools:
            print(f"⚠️  警告：工具 '{tool.name}' 已存在，将被覆盖。")
        self._tools[tool.name] = tool
        print(f"✅ 工具 '{tool.name}' 已注册。")

    def register_function(self, name: str, description: str, func: Callable[[str], str]):
        """
        直接注册函数作为工具（简便方式）

        Args:
            name: 工具名称
            description: 工具描述
            func: 工具函数，接受字符串参数，返回字符串结果
        """
        if name in self._functions:
            print(f"⚠️  警告：工具 '{name}' 已存在，将被覆盖。")

        self._functions[name] = {
            "description": description,
            "func": func
        }
        print(f"✅ 工具 '{name}' 已注册。")

    def get_tool(self, name: str) -> Optional[Tool]:
        """
        获取已注册的工具

        Args:
            name: 工具名称

        Returns:
            Tool 实例或 None
        """
        return self._tools.get(name)

    def get_function(self, name: str) -> Optional[Callable[[str], str]]:
        """
        获取已注册的函数工具

        Args:
            name: 工具名称

        Returns:
            工具函数或 None
        """
        func_info = self._functions.get(name)
        return func_info["func"] if func_info else None

    def get_all_tools(self) -> List[Tool]:
        """获取所有已注册的工具对象"""
        return list(self._tools.values())

    def get_all_functions(self) -> Dict[str, Callable[[str], str]]:
        """获取所有已注册的函数工具"""
        return {name: info["func"] for name, info in self._functions.items()}

    def clear(self):
        """清空所有注册（用于测试）"""
        self._tools.clear()
        self._functions.clear()

    def list_tools(self) -> List[str]:
        """列出所有已注册工具名称"""
        return list(self._tools.keys()) + list(self._functions.keys())


# =====================================================================
# 全局注册表实例
# =====================================================================

registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """获取全局工具注册表实例"""
    return registry
