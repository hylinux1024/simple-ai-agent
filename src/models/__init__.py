"""
统一数据模型协议层 (Unified Data Models)
框架内所有模块流通的标准数据载体
"""
from enum import Enum
from typing import List, Optional, Any, Dict, Type, Callable

from pydantic import BaseModel, Field


class Role(Enum):
    """消息角色枚举"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ToolCall(BaseModel):
    """大模型发起的结构化工具调用请求"""
    id: str
    name: str
    arguments: Dict[str, Any]


class BaseMessage(BaseModel):
    """框架内标准流通的元消息体（屏蔽各厂商底层 Message 协议差异）"""
    role: Role
    content: Optional[str] = None
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class UnifiedTool(BaseModel):
    """跨模型标准工具抽象定义"""
    name: str
    description: str
    parameters: Type[BaseModel]
    executable: Optional[Callable] = None

    class Config:
        arbitrary_types_allowed = True
