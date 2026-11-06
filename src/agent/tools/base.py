from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from agent.schemas import ToolCall, ToolResult


class Tool(ABC):
    name: str
    description: str
    input_model: type[BaseModel]

    def schema(self) -> dict[str, Any]:
        return self.input_model.model_json_schema()

    @abstractmethod
    def execute(self, call: ToolCall) -> ToolResult: ...

