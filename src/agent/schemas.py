from __future__ import annotations

from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source: str
    page: int | None = None
    excerpt: str | None = None


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    call_id: str = Field(default_factory=lambda: str(uuid4()))


class ToolResult(BaseModel):
    call_id: str
    tool_name: str
    success: bool
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    citations: list[Citation] = Field(default_factory=list)


class AgentDecision(BaseModel):
    type: Literal["tool_call", "final_answer"]
    tool_call: ToolCall | None = None
    answer: str | None = None


class AgentStep(BaseModel):
    step: int
    decision: AgentDecision
    tool_result: ToolResult | None = None
    latency_ms: float = 0.0


class AgentRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    include_trace: bool = False


class AgentResponse(BaseModel):
    run_id: str
    session_id: str
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    steps: list[AgentStep] = Field(default_factory=list)
    latency_ms: float
    error: str | None = None


class MemoryEntry(BaseModel):
    key: str
    value: str
    session_id: str | None = None


class AgentState(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str
    user_message: str
    steps: list[AgentStep] = Field(default_factory=list)
    observations: list[ToolResult] = Field(default_factory=list)
    final_answer: str | None = None

