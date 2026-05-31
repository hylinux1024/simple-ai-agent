# Simple AI Agent Framework

一个模块化、可扩展的 AI Agent 框架，支持多种 Agent 模式。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**GitHub**: [github.com/hylinux1024/simple-ai-agent](https://github.com/hylinux1024/simple-ai-agent)

## 特性

- **统一 LLM 抽象层**：支持 OpenAI、DeepSeek、Anthropic 等厂商 API
- **多种 Agent 模式**：
  - ReAct（Reasoning + Acting）
  - Plan-and-Solve（谋定而后动）
  - Reflection（自我纠偏）
- **模块化设计**：清晰的目录结构，易于扩展
- **抽象工具系统**：
  - `Tool` 基类：统一定义工具接口
  - `ToolParameter`：声明式参数定义
  - `ToolRegistry`：单例注册表，支持函数和类两种注册方式
- **环境变量配置**：敏感信息与代码分离

## 项目结构

```
simple-ai-agent/
├── src/
│   ├── models/          # 数据模型 (Role, ToolCall, BaseMessage)
│   ├── llm/             # LLM 适配器 (BaseLLM, OpenAIAdapter, MockLLM, Factory)
│   ├── agents/          # Agent 实现 (ReAct, PlanAndSolve, Reflection)
│   ├── tools/           # 工具系统 (Tool 基类，ToolParameter, ToolRegistry)
│   ├── utils/           # 工具函数 (配置加载)
│   └── __init__.py      # 模块导出
├── main.py              # 主入口
├── requirements.txt     # 依赖列表
├── .env.example         # 环境变量模板
└── README.md
```

## 快速开始

### 1. 创建虚拟环境

```bash
# 使用 uv（推荐）
uv venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 或使用 venv
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 2. 安装依赖

```bash
# 使用 uv（推荐）
uv pip install -r requirements.txt

# 或使用 pip
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置你的 LLM
```

### 3. 运行示例

```bash
# 使用 Mock LLM（无需 API Key）
python main.py
```

## 配置说明

编辑 `.env` 文件配置 LLM：

```env
# LLM Provider: openai, deepseek, anthropic, mock
LLM_PROVIDER=mock

# Model name
LLM_MODEL_NAME=mock-model

# API Key（mock 模式下可为空）
LLM_API_KEY=

# Base URL（可选，用于兼容 API）
LLM_BASE_URL=
```

## 使用示例

### 定义自定义工具

```python
from src.tools import Tool, ToolParameter
from typing import Any, Dict, List

class WeatherTool(Tool):
    """天气查询工具"""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="查询城市天气"
        )

    def run(self, parameters: Dict[str, Any]) -> str:
        city = parameters.get("city", "")
        return f"{city} 晴天，25°C"

    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="city",
                type="string",
                description="城市名称",
                required=True
            )
        ]

# 使用工具
weather = WeatherTool()
result = weather.run({"city": "北京"})
print(result)  # 北京 晴天，25°C
```

### 使用工具注册表

```python
from src.tools import registry, Tool, ToolParameter

# 方式 1: 注册函数
def hello(name: str) -> str:
    return f"Hello, {name}!"

registry.register_function(
    name="hello",
    description="打招呼",
    func=hello
)

# 方式 2: 注册 Tool 类
class GreetTool(Tool):
    def __init__(self):
        super().__init__("greet", "问候工具")
    
    def run(self, parameters): ...
    def get_parameters(self): ...

registry.register_tool(GreetTool())

# 获取所有工具
tools = registry.get_all_tools()
```

### ReAct Agent

```python
from src import ReActAgent, LLMFactory
from src.tools import get_weather_tool

llm = LLMFactory.create(
    provider="openai",
    model_name="gpt-4",
    api_key="your-api-key",
)

agent = ReActAgent(
    name="assistant",
    system_prompt="你是一个有用的助手。",
    llm=llm,
    tools=[get_weather_tool()]
)

result = await agent.run("查询北京天气")
```

### Plan-and-Solve Agent

```python
from src import PlanAndSolveAgent, LLMFactory

llm = LLMFactory.create(provider="openai", model_name="gpt-4", api_key="your-key")

agent = PlanAndSolveAgent(
    name="planner",
    system_prompt="你是一个专业的规划师。",
    llm=llm
)

result = await agent.run("计划一次商务旅行")
```

### Reflection Agent

```python
from src import ReflectionAgent, LLMFactory

llm = LLMFactory.create(provider="openai", model_name="gpt-4", api_key="your-key")

agent = ReflectionAgent(
    name="writer",
    system_prompt="你是一位专业的作家。",
    llm=llm,
    max_cycles=2
)

result = await agent.run("写一篇关于 AI 的文章")
```

## 添加新的 LLM 适配器

在 `src/llm/` 目录下创建新的适配器：

```python
from .base import BaseLLM

class MyAdapter(BaseLLM):
    async def generate(self, messages, **kwargs):
        # 实现你的适配器逻辑
        pass
```

然后在 `src/llm/factory.py` 中注册。

## 许可证

MIT
