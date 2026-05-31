"""
Tools 模块 - 工具定义和 Schema 转换
"""
from .base import (
    Tool,
    ToolParameter,
    FunctionTool,
    ToolRegistry,
    registry,
    get_registry,
)
from .example_tools import (
    get_weather_tool,
    get_flight_tool,
    get_hotel_tool,
    get_car_rental_tool,
    get_all_tools,
    WeatherTool,
    FlightTool,
    HotelTool,
    CarRentalTool,
)

__all__ = [
    # 核心抽象
    "Tool",
    "ToolParameter",
    "FunctionTool",
    "ToolRegistry",
    "registry",
    "get_registry",
    # 示例工具
    "get_weather_tool",
    "get_flight_tool",
    "get_hotel_tool",
    "get_car_rental_tool",
    "get_all_tools",
    "WeatherTool",
    "FlightTool",
    "HotelTool",
    "CarRentalTool",
]
