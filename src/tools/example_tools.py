"""
示例工具定义 - Mock 接口
用于演示和测试 Agent 框架的工具调用功能
"""
from typing import Any, Dict, List

from .base import Tool, ToolParameter


# =====================================================================
# 天气查询工具
# =====================================================================

def local_weather_api(city: str) -> str:
    """模拟天气查询 API"""
    if "北京" in city:
        return "晴天，气温 25°C, 东南风 2 级"
    return "目标行政区气象数据缺损"


class WeatherTool(Tool):
    """天气查询工具"""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="实时检索中国气象局底层数据库获取最新城市天气状况"
        )

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行天气查询"""
        city = parameters.get("city", "")
        return local_weather_api(city)

    def get_parameters(self) -> List[ToolParameter]:
        """获取参数定义"""
        return [
            ToolParameter(
                name="city",
                type="string",
                description="目标查询城市中文名称",
                required=True
            )
        ]


def get_weather_tool() -> WeatherTool:
    """获取天气查询工具"""
    return WeatherTool()


# =====================================================================
# 机票预订工具
# =====================================================================

def book_flight(origin: str, destination: str, date: str) -> str:
    """模拟机票预订 API"""
    if "北京" in origin and "上海" in destination:
        return "【机票已预订】MU5101 航班，北京首都 T3 -> 上海虹桥 T2, 2026-06-15 09:00 起飞，商务舱 ¥2,580"
    return "【预订失败】航线暂未支持"


class FlightTool(Tool):
    """机票预订工具"""

    def __init__(self):
        super().__init__(
            name="book_flight",
            description="预订国内航班机票"
        )

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行机票预订"""
        origin = parameters.get("origin", "")
        destination = parameters.get("destination", "")
        date = parameters.get("date", "")
        return book_flight(origin, destination, date)

    def get_parameters(self) -> List[ToolParameter]:
        """获取参数定义"""
        return [
            ToolParameter(name="origin", type="string", description="出发城市", required=True),
            ToolParameter(name="destination", type="string", description="目的城市", required=True),
            ToolParameter(name="date", type="string", description="出发日期，格式 YYYY-MM-DD", required=True),
        ]


def get_flight_tool() -> FlightTool:
    """获取机票预订工具"""
    return FlightTool()


# =====================================================================
# 酒店预订工具
# =====================================================================

def book_hotel(city: str, area: str, date: str, room_type: str = "高级大床房") -> str:
    """模拟酒店预订 API"""
    if "上海" in city and "陆家嘴" in area:
        return "【酒店已预订】上海陆家嘴香格里拉大酒店，高级大床房一晚，2026-06-15 入住，含双早 ¥1,280"
    return "【预订失败】目标区域酒店暂未支持"


class HotelTool(Tool):
    """酒店预订工具"""

    def __init__(self):
        super().__init__(
            name="book_hotel",
            description="预订酒店客房"
        )

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行酒店预订"""
        city = parameters.get("city", "")
        area = parameters.get("area", "")
        date = parameters.get("date", "")
        room_type = parameters.get("room_type", "高级大床房")
        return book_hotel(city, area, date, room_type)

    def get_parameters(self) -> List[ToolParameter]:
        """获取参数定义"""
        return [
            ToolParameter(name="city", type="string", description="入住城市", required=True),
            ToolParameter(name="area", type="string", description="区域/商圈", required=True),
            ToolParameter(name="date", type="string", description="入住日期，格式 YYYY-MM-DD", required=True),
            ToolParameter(name="room_type", type="string", description="房型", required=False, default="高级大床房"),
        ]


def get_hotel_tool() -> HotelTool:
    """获取酒店预订工具"""
    return HotelTool()


# =====================================================================
# 租车服务工具
# =====================================================================

def book_car_rental(city: str, pickup_location: str, date: str) -> str:
    """模拟租车服务 API"""
    if "上海" in city:
        return "【租车已安排】神州专车 - 别克 GL8 商务车，2026-06-15 于上海虹桥机场 T2 航站楼接车，含司机服务 ¥800/天"
    return "【预订失败】目标城市租车服务暂未支持"


class CarRentalTool(Tool):
    """租车服务工具"""

    def __init__(self):
        super().__init__(
            name="book_car_rental",
            description="预订租车服务（含司机可选）"
        )

    def run(self, parameters: Dict[str, Any]) -> str:
        """执行租车预订"""
        city = parameters.get("city", "")
        pickup_location = parameters.get("pickup_location", "")
        date = parameters.get("date", "")
        return book_car_rental(city, pickup_location, date)

    def get_parameters(self) -> List[ToolParameter]:
        """获取参数定义"""
        return [
            ToolParameter(name="city", type="string", description="取车城市", required=True),
            ToolParameter(name="pickup_location", type="string", description="具体取车地点", required=True),
            ToolParameter(name="date", type="string", description="取车日期，格式 YYYY-MM-DD", required=True),
        ]


def get_car_rental_tool() -> CarRentalTool:
    """获取租车服务工具"""
    return CarRentalTool()


# =====================================================================
# 工具集合
# =====================================================================

def get_all_tools() -> list[Tool]:
    """获取所有示例工具"""
    return [
        get_weather_tool(),
        get_flight_tool(),
        get_hotel_tool(),
        get_car_rental_tool(),
    ]
