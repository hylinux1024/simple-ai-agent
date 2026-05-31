"""
示例工具定义 - Mock 接口
用于演示和测试 Agent 框架的工具调用功能
"""
from pydantic import BaseModel, Field

from ..models import UnifiedTool


# =====================================================================
# 天气查询工具
# =====================================================================

def local_weather_api(city: str) -> str:
    """模拟天气查询 API"""
    if "北京" in city:
        return "晴天，气温 25°C, 东南风 2 级"
    return "目标行政区气象数据缺损"


class WeatherSchema(BaseModel):
    city: str = Field(..., description="目标查询城市中文名称")


def get_weather_tool() -> UnifiedTool:
    """获取天气查询工具"""
    return UnifiedTool(
        name="get_weather",
        description="实时检索中国气象局底层数据库获取最新城市天气状况",
        parameters=WeatherSchema,
        executable=local_weather_api,
    )


# =====================================================================
# 机票预订工具
# =====================================================================

def book_flight(origin: str, destination: str, date: str) -> str:
    """模拟机票预订 API"""
    if "北京" in origin and "上海" in destination:
        return "【机票已预订】MU5101 航班，北京首都 T3 -> 上海虹桥 T2, 2026-06-15 09:00 起飞，商务舱 ¥2,580"
    return "【预订失败】航线暂未支持"


class FlightSchema(BaseModel):
    origin: str = Field(..., description="出发城市")
    destination: str = Field(..., description="目的城市")
    date: str = Field(..., description="出发日期，格式 YYYY-MM-DD")


def get_flight_tool() -> UnifiedTool:
    """获取机票预订工具"""
    return UnifiedTool(
        name="book_flight",
        description="预订国内航班机票",
        parameters=FlightSchema,
        executable=book_flight,
    )


# =====================================================================
# 酒店预订工具
# =====================================================================

def book_hotel(city: str, area: str, date: str, room_type: str = "高级大床房") -> str:
    """模拟酒店预订 API"""
    if "上海" in city and "陆家嘴" in area:
        return "【酒店已预订】上海陆家嘴香格里拉大酒店，高级大床房一晚，2026-06-15 入住，含双早 ¥1,280"
    return "【预订失败】目标区域酒店暂未支持"


class HotelSchema(BaseModel):
    city: str = Field(..., description="入住城市")
    area: str = Field(..., description="区域/商圈")
    date: str = Field(..., description="入住日期，格式 YYYY-MM-DD")
    room_type: str = Field(default="高级大床房", description="房型")


def get_hotel_tool() -> UnifiedTool:
    """获取酒店预订工具"""
    return UnifiedTool(
        name="book_hotel",
        description="预订酒店客房",
        parameters=HotelSchema,
        executable=book_hotel,
    )


# =====================================================================
# 租车服务工具
# =====================================================================

def book_car_rental(city: str, pickup_location: str, date: str) -> str:
    """模拟租车服务 API"""
    if "上海" in city:
        return "【租车已安排】神州专车 - 别克 GL8 商务车，2026-06-15 于上海虹桥机场 T2 航站楼接车，含司机服务 ¥800/天"
    return "【预订失败】目标城市租车服务暂未支持"


class CarRentalSchema(BaseModel):
    city: str = Field(..., description="取车城市")
    pickup_location: str = Field(..., description="具体取车地点")
    date: str = Field(..., description="取车日期，格式 YYYY-MM-DD")


def get_car_rental_tool() -> UnifiedTool:
    """获取租车服务工具"""
    return UnifiedTool(
        name="book_car_rental",
        description="预订租车服务（含司机可选）",
        parameters=CarRentalSchema,
        executable=book_car_rental,
    )


# =====================================================================
# 工具集合
# =====================================================================

def get_all_tools() -> list[UnifiedTool]:
    """获取所有示例工具"""
    return [
        get_weather_tool(),
        get_flight_tool(),
        get_hotel_tool(),
        get_car_rental_tool(),
    ]
